---
name: youtube-transcript
description: Extracts the full transcript of a YouTube video into a timestamped Markdown file plus a machine-readable JSON sidecar. Uses YouTube's existing caption tracks (manual or auto-generated) — no transcription needed, so it's free and fast. Two backends opencli (default, drives your logged-in Chrome, no rate limits) and yt-dlp (headless, no browser). Use when asked to get/fetch/extract the transcript, subtitles, captions, or full text of a YouTube video, or when a task needs to read what was said in a video. Caption-less videos and live streams fail with a clear error — audio transcription (whisper) is out of scope.
---

# YouTube transcript

Extract the **full transcript of a YouTube video** into a timestamped
Markdown file + JSON sidecar, using captions YouTube has already generated.

## Quick start

```bash
python3 skills/youtube-transcript/scripts/youtube_transcript.py "<youtube-url-or-video-id>"
```

Writes `<title-slug>__<videoId>.md` + `.json` into
`skills/youtube-transcript/output/` (configurable via `config.yaml`).

```bash
# options
python3 skills/youtube-transcript/scripts/youtube_transcript.py "<url>" --lang zh-CN   # pick language
python3 skills/youtube-transcript/scripts/youtube_transcript.py "<url>" --mode raw     # every segment w/ precise start/end
python3 skills/youtube-transcript/scripts/youtube_transcript.py "<url>" --backend yt-dlp  # headless, no Chrome
python3 skills/youtube-transcript/scripts/youtube_transcript.py "<url>" --output-dir <dir> --md <path> --json-out <path>
```

## Backends

| | `--backend opencli` (default) | `--backend yt-dlp` |
|---|---|---|
| Requires | opencli + Browser Bridge + running Chrome | `yt-dlp` on PATH only |
| Rate limits | none (YouTube sees your normal browser) | yes — YouTube's timedtext endpoint 429s aggressively; the script paces (`--sleep-subtitles 5`) and retries with backoff (90s/180s/270s) |
| Output quality | best — `--mode grouped` gives paragraphs, chapter markers, speaker detection | plain segments only |
| Proxy handling | handled by the browser | auto-detected from env `HTTPS_PROXY` / `git config http.proxy` — **direct connections to youtube.com time out on proxied networks**, so this matters |

Decision rule: use **opencli** whenever Chrome is up (default). Reach for
**yt-dlp** only when there's no browser (headless box, CI) or opencli is
broken. For batches of videos, prefer opencli — yt-dlp will hit 429s after a
few videos and spend minutes in backoff sleeps.

## Prerequisites

- **opencli backend** (default): `opencli doctor` green — opencli installed,
  Browser Bridge extension connected, Chrome running. No YouTube login
  needed for public videos.
- **yt-dlp backend**: `yt-dlp` on PATH (`brew install yt-dlp` /
  `pip install yt-dlp` / standalone binary from
  https://github.com/yt-dlp/yt-dlp/releases — on macOS `~/bin` works).
- Python 3.9+ stdlib only — nothing to install.

## What you get

Markdown (`<slug>__<id>.md`): YAML frontmatter (title, channel, url,
duration, language, backend, segment count, **coverage %**, date), then the
transcript. Grouped mode renders `[Chapter]` markers as `##` headings and
timestamps as inline code; raw mode lists every caption segment.

JSON (`<slug>__<id>.json`): the frontmatter fields plus the full `segments`
array — grouped rows are `{timestamp, speaker, text, is_chapter}`, raw rows
are `{start, end, text}` (seconds, float).

The script prints a **coverage warning on stderr** when the transcript covers
<50% of the video duration — usually means captions are truncated or the
wrong language track was selected.

## Reading the output downstream

- "What did they say at 12:30?" → open the JSON, binary-search `segments` by
  `start`/timestamp.
- Summary / Q&A tasks → feed the Markdown to the model directly; it's clean
  prose in grouped mode.
- Chapters: filter `is_chapter: true` rows for a table of contents.

## Limitations & failure modes

- **Videos with no caption tracks at all** (rare, e.g. some music videos,
  freshly uploaded, or caption-disabled) → both backends fail. This skill
  does **not** transcribe audio (no whisper) — that's a deliberate scope
  decision; extend with faster-whisper if ever needed.
- **Live streams** → detected via metadata (`isLive`), clear error.
- **Auto-captions have no punctuation/speakers** — grouped mode's speaker
  detection and chapters only work where manual captions exist. The text is
  still complete and timestamped.
- **opencli `-f json` stdout carries trailing update notices** — the script
  parses around this (finds the JSON array boundaries); don't naively pipe
  opencli output to `json.load` in your own code.
- **yt-dlp without a JS runtime warns** "No supported JavaScript runtime" —
  extraction still works for captions; some format listings degrade. Install
  deno to silence it.
- **Language codes**: use `zh-CN` not `zh-Hans` for auto-translated Chinese
  tracks (opencli's available-list uses YouTube's codes); `--lang en` works
  everywhere English captions exist.

## Troubleshooting

- *opencli: extension not connected* → `opencli doctor`, make sure Chrome is
  running with the Browser Bridge extension enabled.
- *yt-dlp: connection timed out* → you're on a proxied network; the script
  reads the proxy from env or `git config http.proxy`. Set `HTTPS_PROXY` if
  neither is configured.
- *yt-dlp: HTTP 429 persists after retries* → wait ~10 min; YouTube's
  timedtext rate limit is IP-wide. Or switch to the opencli backend.
- *Transcript looks like the wrong video* → upstream opencli already scopes
  timedtext captures per-video (SPA navigation), but if you see this, re-run
  with `--mode raw`.
