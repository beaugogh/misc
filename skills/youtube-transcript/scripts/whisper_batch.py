#!/usr/bin/env python3
"""Batch-transcribe 老高與小茉 channel videos (they have NO captions on YouTube).

Pipeline, replicating the existing 25-video corpus exactly:
  select top-N by view count (not already done)
  → yt-dlp audio download (.webm, kept in output/audio/)
  → OpenAI Whisper `base` model, language zh, condition_on_previous_text off
  → OpenCC t2s → simplified Chinese
  → output/whisper/<YYYY-MM-DD>__<simplified-title>__<id>/{.txt,.json,.srt}

JSON schema per video (matches the existing corpus):
  {"language": "zh", "segments": [{"start", "end", "text"}],
   "text": <joined>, "script": "zh-Hans", "normalization": "OpenCC t2s"}

Resume-safe: existing whisper/<...>__<id>/ dirs and existing .webm files are
skipped/reused. Run with the repo .venv python (openai-whisper, yt-dlp, opencc):

  .venv/bin/python3 skills/youtube-transcript/scripts/whisper_batch.py --list
  .venv/bin/python3 skills/youtube-transcript/scripts/whisper_batch.py --count 75
  .venv/bin/python3 skills/youtube-transcript/scripts/whisper_batch.py --count 75 --start 10
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
CATALOG = os.path.join(OUT_DIR, 'laogao-channel-catalog.json')
PROXY = os.environ.get('BATCH_PROXY') or 'http://127.0.0.1:15236'  # this network requires it
VENV_BIN = os.path.normpath(os.path.join(SKILL_DIR, '..', '..', '.venv', 'bin'))
YTDLP = os.path.join(VENV_BIN, 'yt-dlp')
WHISPER = os.path.join(VENV_BIN, 'whisper')


def eprint(*a):
    print(*a, file=sys.stderr, flush=True)


def load_catalog():
    d = json.load(open(CATALOG))
    return d['entries']


def done_ids():
    """Video IDs already transcribed (whisper dir names end with __<id>)."""
    ids = set()
    if os.path.isdir(WHISPER_DIR):
        for name in os.listdir(WHISPER_DIR):
            if '__' in name:
                ids.add(name.rsplit('__', 1)[1])
    return ids


def audio_path_for(vid):
    """Existing downloaded audio file for vid, if any."""
    if not os.path.isdir(AUDIO_DIR):
        return None
    for name in os.listdir(AUDIO_DIR):
        if name.rsplit('__', 1)[1].rsplit('.', 1)[0] == vid:
            return os.path.join(AUDIO_DIR, name)
    return None


def select(count):
    """Top-`count` eligible not-done videos by view count (>=5min, <=1h, not live)."""
    done = done_ids()
    eligible = [e for e in load_catalog()
                if 300 <= (e.get('duration') or 0) <= 3600
                and (not e.get('live_status') or e.get('live_status') == 'not_live')
                and e['id'] not in done]
    eligible.sort(key=lambda e: -(e.get('view_count') or 0))
    return eligible[:count]


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
    """Whisper base, zh (Python API), converted straight to corpus format.
    The CLI's output_format=json proved flaky under subprocess capture; the
    API returns the result dict directly — no intermediate files at all."""
    import whisper
    if 'm' not in model_cache:
        model_cache['m'] = whisper.load_model('base')
    model = model_cache['m']
    result = model.transcribe(audio_path, language='zh', condition_on_previous_text=False,
                              verbose=False)

    segments = [{'start': s['start'], 'end': s['end'], 'text': cc.convert(s['text'].strip())}
                for s in result.get('segments', []) if s.get('text', '').strip()]
    payload = {
        'language': 'zh',
        'segments': segments,
        'text': cc.convert(result.get('text', '').strip()),
        'script': 'zh-Hans',
        'normalization': 'OpenCC t2s',
    }
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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--count', type=int, default=75, help='how many videos to process in this run (top-N by views)')
    ap.add_argument('--start', type=int, default=0, help='skip the first N of the selection (for staged runs)')
    ap.add_argument('--list', action='store_true', help='only print the selection, do nothing')
    args = ap.parse_args()

    from opencc import OpenCC
    cc = OpenCC('t2s')

    picked = select(args.count + args.start)[args.start:]
    if args.list:
        for i, e in enumerate(picked):
            m, s = divmod(e['duration'], 60)
            print(f"{args.start + i + 1:3d}  {(e.get('view_count') or 0)/1e6:5.1f}M  {m:3d}:{s:02d}  {e['id']}  {e['title'][:50]}")
        print(f'--- {len(picked)} videos selected (of {args.count} requested, start={args.start})')
        return

    eprint(f'processing {len(picked)} videos; done so far: {len(done_ids())}')
    failures = []
    for i, e in enumerate(picked):
        vid = e['id']
        title = e['title'].split('|')[0].strip()  # drop " | 老高與小茉 Mr & Mrs Gao"
        try:
            date = fetch_upload_date(vid)
            sim_title = cc.convert(title)
            base_name = f'{date}__{sim_title}__{vid}'

            out_dir = os.path.join(WHISPER_DIR, base_name)
            if os.path.isdir(out_dir) and os.path.exists(os.path.join(out_dir, base_name + '.json')):
                eprint(f'[{i+1}/{len(picked)}] {vid} already done, skipping')
                continue

            existing_audio = audio_path_for(vid)
            if existing_audio:
                audio_file = existing_audio
            else:
                audio_dest = os.path.join(AUDIO_DIR, f'{base_name}.webm')
                eprint(f'[{i+1}/{len(picked)}] {vid} downloading audio...')
                audio_file = download_audio(vid, audio_dest)

            eprint(f'[{i+1}/{len(picked)}] {vid} transcribing ({os.path.basename(audio_file)})...')
            t0 = time.time()
            nseg = transcribe_and_write(audio_file, out_dir, base_name, cc)
            el = time.time() - t0
            eprint(f'[{i+1}/{len(picked)}] {vid} OK: {nseg} segments in {el/60:.1f} min')
        except Exception as err:
            failures.append((vid, str(err)))
            eprint(f'[{i+1}/{len(picked)}] {vid} FAILED: {err}')

    eprint(f'--- batch complete: {len(picked) - len(failures)} ok, {len(failures)} failed')
    for vid, err in failures:
        eprint(f'    {vid}: {err[:120]}')


if __name__ == '__main__':
    main()
