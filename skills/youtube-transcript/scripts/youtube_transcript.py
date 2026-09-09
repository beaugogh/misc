#!/usr/bin/env python3
"""Extract the full transcript of a YouTube video into Markdown + JSON.

Two backends, same output:

  yt-dlp (default) — headless, no Chrome required. Downloads caption tracks
      only (`--skip-download`). YouTube's timedtext endpoint rate-limits
      (HTTP 429) aggressively, so the script paces requests and retries with
      backoff. Auto-detects a proxy from env / git config — direct
      connections to youtube.com time out on some networks.

  opencli (backup) — `opencli youtube transcript` drives your logged-in
      Chrome via the OpenCLI Browser Bridge. No rate limits (YouTube sees a
      normal browser), handles PO tokens, offers grouped mode (paragraphs,
      chapters, speaker detection).

Python 3.9+ stdlib only.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse

# --------------------------------------------------------------------------
# URL / ID parsing

VIDEO_ID_RE = re.compile(r'^[A-Za-z0-9_-]{11}$')

def parse_video_id(arg):
    """Accept a watch URL, youtu.be URL, shorts URL, embed URL, or bare ID."""
    arg = arg.strip()
    if VIDEO_ID_RE.match(arg):
        return arg
    try:
        parsed = urllib.parse.urlparse(arg if '://' in arg else 'https://' + arg)
    except ValueError:
        raise SystemExit(f"error: cannot parse input as URL or video ID: {arg!r}")
    host = parsed.netloc.lower().removeprefix('www.')
    if host not in ('youtube.com', 'm.youtube.com', 'music.youtube.com', 'youtu.be'):
        raise SystemExit(f"error: not a YouTube URL: {arg!r}")
    if host == 'youtu.be':
        vid = parsed.path.lstrip('/')
    else:
        vid = urllib.parse.parse_qs(parsed.query).get('v', [None])[0]
        if not vid:
            m = re.match(r'^/(shorts|embed|live|v)/([A-Za-z0-9_-]{11})', parsed.path)
            if not m:
                raise SystemExit(f"error: no video ID found in URL: {arg!r}")
            vid = m.group(2)
    vid = vid.split('/')[0].split('?')[0]
    if not VIDEO_ID_RE.match(vid):
        raise SystemExit(f"error: malformed video ID extracted from {arg!r}: {vid!r}")
    return vid


# --------------------------------------------------------------------------
# shared helpers

def slugify(text, max_chars=60):
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    text = re.sub(r'[\s_]+', '-', text.strip())
    return (text[:max_chars].rstrip('-') or 'video').lower()


def fmt_ts(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


def run(cmd, timeout=300):
    """Run a subprocess; a hang becomes a clean SystemExit, not a traceback."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise SystemExit(f'error: command timed out after {timeout}s: {" ".join(cmd[:6])} …')
    except FileNotFoundError:
        raise SystemExit(f'error: command not found: {cmd[0]}')


# --------------------------------------------------------------------------
# backend: yt-dlp

# yt-dlp metadata fields can't contain \x1f (unit separator), so it's a safe
# --print delimiter. Named (not inline) so editors can see it.
YT_SEP = '\x1f'
YT_PRINT_TMPL = YT_SEP.join(('%(title)s', '%(channel)s', '%(duration)s',
                             '%(id)s', '%(is_live)s'))


def detect_ytdlp():
    """Locate yt-dlp, or exit with install instructions."""
    path = shutil.which('yt-dlp')
    if path:
        return [path]
    raise SystemExit(
        'error: yt-dlp not found on PATH.\n'
        'Install it first, e.g.:\n'
        '  brew install yt-dlp        (macOS)\n'
        '  pip install yt-dlp\n'
        '  or download the standalone binary from https://github.com/yt-dlp/yt-dlp/releases\n'
        'Then rerun, or use --backend opencli to extract through your browser instead.'
    )


def detect_proxy():
    """Direct youtube.com connections time out on some networks (this is
    common behind corporate proxies). Resolution order mirrors git's own:
    env vars, then git config http.proxy."""
    for var in ('https_proxy', 'HTTPS_PROXY', 'http_proxy', 'HTTP_PROXY'):
        val = os.environ.get(var)
        if val:
            return val
    try:
        proc = run(['git', 'config', '--get', 'http.proxy'], timeout=10)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except SystemExit:
        pass
    return None


def ytdlp_detect_language(base_cmd, url):
    """Detect the video's language for auto caption selection. %(language)s
    is populated when YouTube declares it (reliably for music, patchily for
    talks); returns None when 'NA'. Note --list-subs can NOT be used for
    this: its language list is alphabetical, not original-first."""
    proc = run(base_cmd + ['--skip-download', '--print', '%(language)s',
                           '--socket-timeout', '15', url])
    if proc.returncode != 0:
        return None
    lang = proc.stdout.strip().splitlines()[-1].strip() if proc.stdout.strip() else 'NA'
    return lang if lang and lang != 'NA' else None


def ytdlp_backend(video_id, lang, mode):
    """Returns (metadata dict, segments list).
    Raw mode: segments are [{start, end, text}] (seconds, float).
    Grouped mode: [{timestamp, speaker, text, is_chapter}]."""
    ytdlp = detect_ytdlp()
    url = f'https://www.youtube.com/watch?v={video_id}'
    proxy = detect_proxy()

    import tempfile
    workdir = tempfile.mkdtemp(prefix='yt-transcript-')

    def base_cmd():
        cmd = list(ytdlp)
        if proxy:
            cmd += ['--proxy', proxy]
        return cmd

    # Language selection: --lang flag wins; otherwise %(language)s when
    # YouTube declares it (one cheap pre-pass, no subtitle requests);
    # final fallback English.
    if lang:
        sub_langs = lang
    else:
        sub_langs = ytdlp_detect_language(base_cmd(), url) or 'en'

    # Single extraction call: metadata printed AND captions downloaded in one
    # pass (separate calls would multiply request volume — and 429s).
    # NB: --print implies --simulate, which ALSO swallows subtitle download
    # errors (exit 0, no files) — --no-simulate is required for real writes.
    out_tmpl = os.path.join(workdir, '%(id)s.%(ext)s')
    attempts = 0
    while True:
        attempts += 1
        dl = run(base_cmd() + [
            '--skip-download', '--write-auto-subs', '--write-subs',
            '--sub-langs', sub_langs, '--sub-format', 'json3/vtt',
            '--sleep-subtitles', '5',   # pace timedtext requests: 429s are the #1 failure mode
            '--socket-timeout', '15',
            '--print', YT_PRINT_TMPL, '--no-simulate',
            '-o', out_tmpl, url,
        ])
        combined = (dl.stdout or '') + (dl.stderr or '')
        files = [f for f in os.listdir(workdir) if f.endswith(('.json3', '.vtt', '.srt'))]
        if files:
            break
        if '429' in (dl.stderr or '') and attempts <= 3:
            wait = 90 * attempts  # 429s on the timedtext endpoint outlast short cooldowns
            print(f'rate-limited (HTTP 429); waiting {wait}s before retry...', file=sys.stderr)
            time.sleep(wait)
            continue
        if 'no subtitles' in combined.lower() or 'There is no subtitle' in combined:
            raise SystemExit(
                f'error: yt-dlp found no caption track for language {sub_langs!r}.\n'
                'Run yt-dlp --list-subs on the video to see what exists.'
            )
        if '429' in combined:
            raise SystemExit(
                f'error: YouTube rate-limited (HTTP 429) caption downloads for '
                f'language {sub_langs!r} and retries are exhausted.\n'
                'The timedtext limit is per-language and lasts ~10+ minutes. '
                'Try again later, pick another --lang, or use --backend opencli '
                '(extracts through your browser, no rate limit).'
            )
        shutil.rmtree(workdir, ignore_errors=True)
        raise SystemExit('error: yt-dlp caption download failed:\n' + (dl.stderr or dl.stdout)[-500:])

    # metadata line: first stdout line carrying the separator
    meta_line = next((ln for ln in dl.stdout.splitlines() if YT_SEP in ln), None)
    if not meta_line:
        shutil.rmtree(workdir, ignore_errors=True)
        raise SystemExit('error: yt-dlp metadata output missing:\n' + (dl.stderr or dl.stdout)[-500:])
    title, channel, duration, vid, is_live = (meta_line.split(YT_SEP) + [''] * 5)[:5]
    if is_live.lower() == 'true':
        shutil.rmtree(workdir, ignore_errors=True)
        raise SystemExit('error: this is a live stream — transcripts only exist for finished videos')
    metadata = {
        'title': title,
        'channel': channel,
        # duration is 'NA' for unknown/upcoming — don't write 'NAs' garbage
        'duration': f'{duration}s' if re.match(r'^[\d.]+$', duration) else 'unknown',
        'videoId': vid,
    }

    sub_path = os.path.join(workdir, files[0])
    try:
        segments = parse_json3(sub_path) if sub_path.endswith('.json3') else parse_vtt(sub_path)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    if mode == 'raw':
        return metadata, segments
    grouped = []
    for seg in segments:
        grouped.append({
            'timestamp': fmt_ts(seg['start']),
            'speaker': '',
            'text': seg['text'],
            'is_chapter': False,
        })
    return metadata, grouped


def parse_json3(path):
    data = json.load(open(path, encoding='utf-8'))
    rows = []
    for event in data.get('events', []):
        segs = event.get('segs') or []
        # YouTube's json3 line breaks appear either as real newlines (from
        # \n escapes) or literal backslash-n sequences — flatten both to spaces
        text = ''.join(s.get('utf8', '') for s in segs)
        text = text.replace('\\n', ' ').replace('\n', ' ').strip()
        if not text:
            continue
        start = int(event.get('tStartMs', 0)) / 1000
        dur = int(event.get('dDurationMs', 0)) / 1000
        rows.append({'start': start, 'end': start + dur, 'text': text})
    return rows


def parse_vtt(path):
    """Minimal WebVTT parser: cue timestamps + text.
    Handles auto-caption rolling duplicates (each cue repeats the previous
    cue's line) by dropping leading lines already emitted."""
    content = open(path, encoding='utf-8').read()  # noqa: SIM115 — small temp file
    rows = []
    seen_cues = set()
    prev_lines = []
    for m in re.finditer(
            r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.(\d{3})[^\n]*\n'
            r'((?:[^\n]+\n)*[^\n]*)(?:\n|$)',
            content):
        h1, m1, s1, ms1, h2, m2, s2, ms2 = (int(g) for g in m.groups()[:8])
        start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000
        end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000
        cue_lines = [re.sub(r'<[^>]+>', '', ln).strip() for ln in m.group(9).splitlines()]
        cue_lines = [ln for ln in cue_lines if ln]
        while cue_lines and cue_lines[0] in prev_lines:
            cue_lines.pop(0)
        prev_lines = cue_lines
        if not cue_lines:
            continue
        # flatten wrapped cue lines into one text line (json3 does the same)
        text = ' '.join(cue_lines)
        key = text.lower()
        if key in seen_cues:
            continue
        seen_cues.add(key)
        rows.append({'start': start, 'end': end, 'text': text})
    return rows


# --------------------------------------------------------------------------
# backend: opencli

def extract_json_array(stdout):
    """opencli -f json stdout can carry non-JSON junk (update notices).
    Find a JSON array anywhere in the text and parse exactly that."""
    origin = 0
    while True:
        start = stdout.find('[', origin)
        if start == -1:
            return None
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(stdout)):
            c = stdout[i]
            if in_str:
                if esc:
                    esc = False
                elif c == '\\':
                    esc = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(stdout[start:i + 1])
                    except json.JSONDecodeError:
                        break  # malformed candidate — re-seek from the next '['
        origin = start + 1


def opencli_backend(video_id, lang, mode):
    """Returns (metadata dict, segments list).
    Raw mode: segments are [{start, end, text}] (seconds, float).
    Grouped mode: [{timestamp, speaker, text, is_chapter}]."""
    meta_proc = run(['opencli', 'youtube', 'video', video_id, '-f', 'json'])
    if meta_proc.returncode != 0:
        raise SystemExit('error: opencli youtube video failed:\n' + (meta_proc.stderr or meta_proc.stdout)[-500:])
    meta_rows = extract_json_array(meta_proc.stdout)
    if not meta_rows:
        raise SystemExit('error: could not parse opencli youtube video output as JSON')
    metadata = {row.get('field'): row.get('value') for row in meta_rows if isinstance(row, dict)}

    if str(metadata.get('isLive', '')).lower() == 'true':
        raise SystemExit('error: this is a live stream — transcripts only exist for finished videos')

    cmd = ['opencli', 'youtube', 'transcript', video_id, '-f', 'json', '--mode', mode]
    if lang:
        cmd += ['--lang', lang]
    # one retry: the browser bridge occasionally hiccups on first tab lease
    last_err = ''
    for attempt in range(2):
        proc = run(cmd)
        combined = (proc.stdout or '') + (proc.stderr or '')
        last_err = combined[-500:]
        rows = extract_json_array(proc.stdout or '')
        if rows:
            break
        # language fallback hint from opencli is informational, not fatal —
        # the retry picks up whatever fallback opencli selected
        if 'not found. Using' in combined and rows is None:
            continue
        time.sleep(3)
    else:
        raise SystemExit('error: opencli youtube transcript failed:\n' + last_err)

    segments = []
    if mode == 'raw':
        for r in rows:
            if not isinstance(r, dict) or 'text' not in r:
                continue
            segments.append({
                'start': parse_opencli_seconds(r.get('start', '0s')),
                'end': parse_opencli_seconds(r.get('end', '0s')),
                'text': str(r.get('text', '')),
            })
    else:  # grouped
        for r in rows:
            if not isinstance(r, dict) or not r.get('text'):
                continue
            segments.append({
                'timestamp': str(r.get('timestamp', '0:00')),
                'speaker': str(r.get('speaker', '')),
                'text': str(r.get('text', '')),
                # keep [Chapter] markers distinguishable for rendering
                'is_chapter': str(r.get('text', '')).startswith('[Chapter]'),
            })
    return metadata, segments


def parse_opencli_seconds(val):
    m = re.match(r'^([\d.]+)s?$', str(val))
    return float(m.group(1)) if m else 0.0


# --------------------------------------------------------------------------
# output rendering

def render_markdown(metadata, segments, mode, backend, lang, video_id, coverage_pct):
    lines = []
    def fm(key, val):
        # JSON string = valid YAML double-quoted scalar; titles often contain ': '
        lines.append(f'{key}: {json.dumps(str(val), ensure_ascii=False)}')
    lines.append('---')
    fm('title', metadata.get('title', 'unknown'))
    fm('channel', metadata.get('channel', ''))
    fm('video_id', video_id)
    fm('url', f'https://www.youtube.com/watch?v={video_id}')
    fm('duration', metadata.get('duration', ''))
    if lang:
        fm('language', lang)
    fm('mode', mode)
    fm('backend', f'youtube captions via {backend}')
    fm('segments', len(segments))
    if coverage_pct is not None:
        fm('coverage', f'{coverage_pct:.0f}% of duration')
    fm('date_extracted', datetime.date.today().isoformat())
    lines.append('---')
    lines.append('')
    desc_lines = (metadata.get('description') or '').strip().splitlines()
    if desc_lines:
        lines.append(f'> {desc_lines[0][:300]}')
        lines.append('')
    for seg in segments:
        if seg.get('is_chapter'):
            lines.append('')
            lines.append(f"## {seg['text'].removeprefix('[Chapter] ').strip()}")
        else:
            ts = seg.get('timestamp', '')
            speaker = seg.get('speaker', '')
            prefix = f'`{ts}` ' if ts else ''
            if speaker:
                prefix += f'**{speaker}:** '
            lines.append(f"{prefix}{seg['text']}")
    lines.append('')
    return '\n'.join(lines)


# --------------------------------------------------------------------------
# main

def main():
    ap = argparse.ArgumentParser(description='Extract a YouTube video transcript to Markdown + JSON')
    ap.add_argument('video', help='YouTube URL or 11-char video ID')
    ap.add_argument('--backend', choices=['yt-dlp', 'opencli'], default='yt-dlp',
                    help='extraction backend (default: yt-dlp; opencli extracts through your browser)')
    ap.add_argument('--lang', default='', help='language code, e.g. en, zh-CN (default: auto — original caption track)')
    ap.add_argument('--mode', choices=['grouped', 'raw'], default='grouped',
                    help='grouped: readable paragraphs + chapters; raw: every caption segment')
    ap.add_argument('--output-dir', default=None, help='output directory (default: skill output/ or config)')
    ap.add_argument('--md', default=None, help='explicit path for the Markdown output')
    ap.add_argument('--json-out', default=None, help='explicit path for the JSON output')
    args = ap.parse_args()

    video_id = parse_video_id(args.video)

    if args.backend == 'opencli':
        metadata, segments = opencli_backend(video_id, args.lang, args.mode)
    else:
        metadata, segments = ytdlp_backend(video_id, args.lang, args.mode)

    if not segments:
        raise SystemExit('error: extraction returned an empty transcript — the video likely has no caption tracks')

    # coverage sanity check: last segment vs video duration
    coverage_pct = None
    dur_m = re.match(r'^([\d.]+)s?$', str(metadata.get('duration', '')))
    if dur_m:
        duration = float(dur_m.group(1))
        if args.mode == 'raw' and duration > 0:
            last_end = max((s.get('end', 0) for s in segments), default=0)
            coverage_pct = min(last_end / duration * 100, 100)
        elif duration > 0:
            # grouped rows carry m:ss / h:mm:ss timestamps
            last_ts = segments[-1].get('timestamp', '0:00')
            parts = [float(p) for p in last_ts.split(':')]
            last_secs = sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
            coverage_pct = min(last_secs / duration * 100, 100)
        if coverage_pct is not None and coverage_pct < 50:
            print(f'warning: transcript covers only {coverage_pct:.0f}% of the video duration — '
                  'it may be truncated', file=sys.stderr)

    # resolve output dir: explicit flag > config.yaml > default
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = args.output_dir
    if not output_dir:
        cfg = os.path.join(script_dir, 'config.yaml')
        if os.path.isfile(cfg):
            m = re.search(r'^output_dir:\s*(\S+)', open(cfg).read(), re.M)
            if m:
                candidate = m.group(1).strip('\'"')
                output_dir = candidate if os.path.isabs(candidate) else os.path.join(script_dir, candidate)
    if not output_dir:
        output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    slug = slugify(metadata.get('title', 'video'))
    # tag the language so the same video in two languages doesn't overwrite
    lang_tag = f'.{args.lang}' if args.lang else ''
    md_path = args.md or os.path.join(output_dir, f'{slug}__{video_id}{lang_tag}.md')
    json_path = args.json_out or os.path.join(output_dir, f'{slug}__{video_id}{lang_tag}.json')

    md = render_markdown(metadata, segments, args.mode, args.backend, args.lang, video_id, coverage_pct)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    payload = {
        'video_id': video_id,
        'url': f'https://www.youtube.com/watch?v={video_id}',
        'title': metadata.get('title'),
        'channel': metadata.get('channel'),
        'duration': metadata.get('duration'),
        'language': args.lang or 'auto',
        'mode': args.mode,
        'backend': args.backend,
        'segments_count': len(segments),
        'coverage_pct': round(coverage_pct, 1) if coverage_pct is not None else None,
        'date_extracted': datetime.date.today().isoformat(),
        'segments': segments,
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    cov = f', coverage {coverage_pct:.0f}%' if coverage_pct is not None else ''
    print(f'{md_path}')
    print(f'{json_path}')
    print(f'{len(segments)} segments, mode={args.mode}, backend={args.backend}{cov}')


if __name__ == '__main__':
    main()
