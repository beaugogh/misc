#!/usr/bin/env python3
"""Batch-transcribe 老高與小茉 channel videos (they have NO captions on YouTube).

Pipeline, replicating the existing corpus conventions:
  select top-N by view count (not already done)
  → yt-dlp audio download (.webm, kept in output/audio/)
  → Whisper ASR, language zh, condition_on_previous_text off
  → OpenCC t2s → simplified Chinese
  → output/<engine-dir>/<YYYY-MM-DD>__<simplified-title>__<id>/{.txt,.json,.srt}

Two engines (the legacy 'base' corpus lives in output/whisper/, kept untouched):
  --engine whisper (default)   OpenAI Whisper via the repo .venv, model 'base'
  --engine faster              faster-whisper (ctranslate2, GPU float16),
                               --model large-v3, staged into output/whisper-large-v3/

JSON schema per video:
  {"language": "zh", "segments": [{"start", "end", "text"}],
   "text": <rebuilt from segments>, "script": "zh-Hans",
   "normalization": "OpenCC t2s",
   "engine"/"model"/"model_size"/"device"/"compute_type"/"params"/"transcribed_at"/"duration_s": ...}

Resume-safe: existing <out-dir>/<base>.json and existing .webm files are
skipped/reused. `--count N` means "process the next N not-yet-done videos"
(NOT "grow the corpus to N total"). Run with the repo .venv python:

  .venv/bin/python3 skills/youtube-transcript/scripts/whisper_batch.py --list
  .venv/bin/python3 skills/youtube-transcript/scripts/whisper_batch.py --count 10
  .venv/bin/python3 skills/youtube-transcript/scripts/whisper_batch.py --engine faster --model large-v3 --count 100
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import time

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(SKILL_DIR, 'output')
AUDIO_DIR = os.path.join(OUT_DIR, 'audio')
WHISPER_DIR = os.path.join(OUT_DIR, 'whisper')
LARGE_DIR = os.path.join(OUT_DIR, 'whisper-large-v3')
CATALOG = os.path.join(OUT_DIR, 'laogao-channel-catalog.json')
PROXY = os.environ.get('BATCH_PROXY') or 'http://127.0.0.1:15236'  # this network requires it
VENV_BIN = os.path.normpath(os.path.join(SKILL_DIR, '..', '..', '.venv', 'bin'))
YTDLP = os.path.join(VENV_BIN, 'yt-dlp')

# Channel fixed phrases for the ASR initial prompt (todo.md item 3):
# host names, the standard opener, and recurring topic vocabulary.
CHANNEL_PROMPT = '以下是老高与小茉的节目。大家好我是老高，这是小茉。老高，小茉，远古生物，大灭绝，三星堆，南极，北极，宇宙，外星人，人类起源。'


def eprint(*a):
    print(*a, file=sys.stderr, flush=True)


def load_catalog():
    d = json.load(open(CATALOG))
    return d['entries']


YT_ID_RE = re.compile(r'([A-Za-z0-9_-]{11})$')
AUDIO_EXTS = ('.webm', '.m4a', '.opus', '.mp3')


def video_id_from(name):
    """The 11-char YouTube video ID at the end of a dir or audio file name.

    A plain rsplit('__', 1) eats the leading '_' of IDs like '_IMww7gwIus'
    (separator + ID merge into '___'), so a completed video looks not-done
    and gets re-processed. Match a strict 11-char [A-Za-z0-9_-] ID at the
    end instead. Returns None for names that don't end in a valid ID
    (README.md, todo.md, partial files...)."""
    stem = name
    for ext in AUDIO_EXTS:
        if stem.endswith(ext):
            stem = stem[: -len(ext)]
            break
    m = YT_ID_RE.search(stem)
    return m.group(1) if m else None


def audio_path_for(vid):
    """Existing downloaded audio file for vid, if any."""
    if not os.path.isdir(AUDIO_DIR):
        return None
    for name in os.listdir(AUDIO_DIR):
        if video_id_from(name) == vid:
            return os.path.join(AUDIO_DIR, name)
    return None


def fetch_upload_date(vid):
    """YYYY-MM-DD via one yt-dlp metadata call (catalog lacks upload dates)."""
    proc = subprocess.run(
        [YTDLP, '--skip-download', '--print', '%(upload_date)s',
         '--socket-timeout', '15', '--proxy', PROXY,
         f'https://www.youtube.com/watch?v={vid}'],
        capture_output=True, text=True, timeout=180)
    raw = (proc.stdout or '').strip().splitlines()[-1].strip() if proc.stdout.strip() else ''
    if re.match(r'^\d{8}$', raw):
        return f'{raw[:4]}-{raw[4:6]}-{raw[6:]}'
    return 'unknown-date'


def download_audio(vid, dest_path):
    if os.path.exists(dest_path):
        return dest_path  # resume-safe
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # title comes from catalog; upload date fetched separately
    proc = subprocess.run(
        [YTDLP, '-f', 'bestaudio', '--socket-timeout', '15', '--proxy', PROXY,
         '-o', dest_path,
         f'https://www.youtube.com/watch?v={vid}'],
        capture_output=True, text=True, timeout=900)
    # yt-dlp may append the real ext; find what landed
    if proc.returncode == 0:
        for cand in (dest_path, dest_path + '.webm', dest_path + '.m4a', dest_path + '.opus'):
            if os.path.exists(cand):
                return cand
    raise RuntimeError(f'audio download failed for {vid}: {(proc.stderr or "")[-300:]}')


def transcribe_and_write(audio_path, out_dir, base_name, cc, model_cache={}):
    """OpenAI Whisper `base` (legacy engine) → corpus format. Kept for
    compatibility with the existing output/whisper/ corpus."""
    import whisper
    if 'm' not in model_cache:
        model_cache['m'] = whisper.load_model('base')
    model = model_cache['m']
    result = model.transcribe(audio_path, language='zh', condition_on_previous_text=False,
                              verbose=False)
    meta = {
        'engine': 'openai-whisper',
        'model': 'base',
        'device': 'cuda' if model.device.type == 'cuda' else 'cpu',
        'params': {'language': 'zh', 'condition_on_previous_text': False},
    }
    _write_corpus(segments_from_openai(result, cc), meta, out_dir, base_name)


def segments_from_openai(result, cc):
    return [{'start': s['start'], 'end': s['end'], 'text': cc.convert(s['text'].strip())}
            for s in result.get('segments', []) if s.get('text', '').strip()]


def transcribe_faster_and_write(audio_path, out_dir, base_name, cc, title,
                                 model='large-v3', device='cuda', compute_type='float16',
                                 model_cache={}):
    """faster-whisper engine → corpus format, staged into output/whisper-large-v3/.

    Differences from the legacy base run (todo.md item 3):
      - initial_prompt = channel fixed phrases + this episode's title (boosts
        recurring proper nouns: 老高/小茉/远古生物/大灭绝/三星堆/南极...)
      - full run metadata recorded in the JSON (engine/model/device/params/time)
      - `text` is rebuilt from the corrected segments so TXT/SRT/JSON agree
    """
    from faster_whisper import WhisperModel
    key = ('fw', model, device, compute_type)
    if key not in model_cache:
        model_cache[key] = WhisperModel(model, device=device, compute_type=compute_type)
    fw = model_cache[key]

    t0 = time.time()
    gen, info = fw.transcribe(
        audio_path, language='zh', condition_on_previous_text=False,
        initial_prompt=f'{CHANNEL_PROMPT}{title}。', beam_size=5, vad_filter=True)
    segments = [{'start': s.start, 'end': s.end, 'text': cc.convert(s.text.strip())}
                for s in gen if s.text.strip()]
    elapsed = time.time() - t0
    meta = {
        'engine': 'faster-whisper',
        'model': model,
        'device': device,
        'compute_type': compute_type,
        'params': {
            'language': 'zh',
            'condition_on_previous_text': False,
            'initial_prompt': f'{CHANNEL_PROMPT}{title}。',
            'beam_size': 5,
            'vad_filter': True,
        },
        'transcribed_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
        'transcription_seconds': round(elapsed, 1),
        'audio_duration_seconds': round(getattr(info, 'duration', 0) or 0, 1),
    }
    _write_corpus(segments, meta, out_dir, base_name)
    return len(segments)


def _write_corpus(segments, meta, out_dir, base_name):
    """Common corpus writer: JSON + TXT + SRT, `text` rebuilt from segments."""
    payload = {
        'language': 'zh',
        'segments': segments,
        'text': '\n'.join(seg['text'] for seg in segments),
        'script': 'zh-Hans',
        'normalization': 'OpenCC t2s',
    }
    payload.update(meta)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, base_name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    def ts(sec):
        h, rem = divmod(int(sec), 3600)
        m, s = divmod(rem, 60)
        return f'{h:02d}:{m:02d}:{s:02d}'

    def srt_ts(sec):
        ms = int(round(sec * 1000))
        h, rem = divmod(ms, 3600000)
        m, rem = divmod(rem, 60000)
        s, ms = divmod(rem, 1000)
        return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

    with open(os.path.join(out_dir, base_name + '.txt'), 'w', encoding='utf-8') as f:
        for seg in segments:
            f.write(f"[{ts(seg['start'])}] {seg['text']}\n")

    with open(os.path.join(out_dir, base_name + '.srt'), 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            f.write(f'{i}\n{srt_ts(seg["start"])} --> {srt_ts(seg["end"])}\n{seg["text"]}\n\n')
    return len(segments)


def done_ids(out_dir=WHISPER_DIR):
    """Video IDs already transcribed under out_dir (names end with __<id>)."""
    ids = set()
    if os.path.isdir(out_dir):
        for name in os.listdir(out_dir):
            vid = video_id_from(name)
            if vid:
                ids.add(vid)
    return ids


def select(count, out_dir=WHISPER_DIR):
    """Top-`count` eligible not-done videos by view count (>=5min, <=1h, not live)."""
    done = done_ids(out_dir)
    eligible = [e for e in load_catalog()
                if 300 <= (e.get('duration') or 0) <= 3600
                and (not e.get('live_status') or e.get('live_status') == 'not_live')
                and e['id'] not in done]
    eligible.sort(key=lambda e: -(e.get('view_count') or 0))
    return eligible[:count]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--count', type=int, default=75,
                    help='process the next N not-yet-done videos this run (NOT "grow the corpus to N total" — '
                         'completed videos are never re-counted; top-N by view count among the not-done)')
    ap.add_argument('--start', type=int, default=0, help='skip the first N of the selection (for staged runs)')
    ap.add_argument('--list', action='store_true', help='only print the selection, do nothing')
    ap.add_argument('--engine', choices=('whisper', 'faster'), default='whisper',
                    help="ASR engine: 'whisper' = legacy OpenAI Whisper base (output/whisper/), "
                         "'faster' = faster-whisper GPU (output/whisper-large-v3/ unless --out-dir)")
    ap.add_argument('--model', default=None,
                    help="model for the engine (faster engine default: large-v3; whisper engine: base)")
    ap.add_argument('--device', default='cuda', help="faster engine device (default cuda)")
    ap.add_argument('--out-dir', default=None,
                    help='transcript output dir (default depends on engine: whisper/ or whisper-large-v3/)')
    ap.add_argument('--no-download', action='store_true',
                    help='never fetch audio; transcribe only what is already in output/audio/ '
                         '(use when a separate process owns downloads, to avoid two yt-dlp '
                         'processes writing the same file)')
    args = ap.parse_args()

    if args.engine == 'faster':
        out_root = args.out_dir or LARGE_DIR
        model_name = args.model or 'large-v3'
    else:
        out_root = args.out_dir or WHISPER_DIR
        model_name = args.model or 'base'

    from opencc import OpenCC
    cc = OpenCC('t2s')

    picked = select(args.count + args.start, out_dir=out_root)[args.start:]
    if args.list:
        for i, e in enumerate(picked):
            m, s = divmod(e['duration'], 60)
            print(f"{args.start + i + 1:3d}  {(e.get('view_count') or 0)/1e6:5.1f}M  {m:3d}:{s:02d}  {e['id']}  {e['title'][:50]}")
        print(f'--- {len(picked)} videos selected (of {args.count} requested, start={args.start}, engine={args.engine}, out={os.path.basename(out_root)})')
        return

    eprint(f'engine={args.engine} model={model_name} out={out_root}')
    eprint(f'processing {len(picked)} videos; done so far: {len(done_ids(out_root))}')
    failures = []
    for i, e in enumerate(picked):
        vid = e['id']
        title = e['title'].split('|')[0].strip()  # drop " | 老高與小茉 Mr & Mrs Gao"
        try:
            date = fetch_upload_date(vid)
            sim_title = cc.convert(title)
            base_name = f'{date}__{sim_title}__{vid}'

            out_dir = os.path.join(out_root, base_name)
            if os.path.isdir(out_dir) and os.path.exists(os.path.join(out_dir, base_name + '.json')):
                eprint(f'[{i+1}/{len(picked)}] {vid} already done, skipping')
                continue

            existing_audio = audio_path_for(vid)
            if existing_audio:
                audio_file = existing_audio
            elif args.no_download:
                eprint(f'[{i+1}/{len(picked)}] {vid} no local audio (--no-download), skipping')
                continue
            else:
                audio_dest = os.path.join(AUDIO_DIR, f'{base_name}.webm')
                eprint(f'[{i+1}/{len(picked)}] {vid} downloading audio...')
                audio_file = download_audio(vid, audio_dest)

            eprint(f'[{i+1}/{len(picked)}] {vid} transcribing ({os.path.basename(audio_file)})...')
            t0 = time.time()
            if args.engine == 'faster':
                nseg = transcribe_faster_and_write(
                    audio_file, out_dir, base_name, cc, sim_title,
                    model=model_name, device=args.device,
                    model_cache=main._mc)
            else:
                nseg = transcribe_and_write(audio_file, out_dir, base_name, cc,
                                            model_cache=main._mc)
            el = time.time() - t0
            eprint(f'[{i+1}/{len(picked)}] {vid} OK: {nseg} segments in {el/60:.1f} min')
        except Exception as err:
            failures.append((vid, str(err)))
            eprint(f'[{i+1}/{len(picked)}] {vid} FAILED: {err}')

    eprint(f'--- batch complete: {len(picked) - len(failures)} ok, {len(failures)} failed')
    for vid, err in failures:
        eprint(f'    {vid}: {err[:120]}')


main._mc = {}  # model cache shared across videos in one run


if __name__ == '__main__':
    main()
