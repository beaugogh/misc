---
name: huawei-meeting-analysis
description: Works with meeting recordings — can extract/download the recording video from a Huawei eMeeting (w3.huawei.com/emeeting) URL, transcribe speech to a timestamped transcript, extract key frames from screen-share video, then summarize / pull action items / answer questions about the meeting. Built for WeLink recordings (a directory with meeting_1.mp4 + meeting_1.m4a + audio.pcm) but works on any video file. Optional multi-modal mode sends every frame to a vision model (glm-5.3-flash) and writes per-frame text descriptions; the agent itself reads frame PNGs directly as images (primary evidence path). Use when the user wants to download an eMeeting recording, know what happened in a recorded meeting, get a summary or action items, extract something shown on the shared screen (slides, code, a diagram), or search what was said by timestamp. Video extraction needs an opencli browser session; transcription needs the Python venv with openai-whisper + imageio-ffmpeg (see Setup).
---

# Meeting recording analysis (video + audio)

## What this skill does
Turn a meeting recording into something you can read and reason about:
0. **Extract the video** — download a Huawei eMeeting recording from its
   `w3.huawei.com/emeeting/#/aiSummary/...` URL (highest quality available).
   Standalone: no whisper/venv needed, just an opencli browser session.
1. **Transcribe** the audio → timestamped transcript (`.txt` / `.json` / `.srt`).
2. **Extract key frames** from the video → PNGs at slide/screen changes.
3. **Analyze** — summarize, pull action items, find decisions, answer
   "what was said about X", or read a specific shared screen (slide/code).

The agent reads the transcript as text and **the frame PNGs directly as
images** (the model is multimodal — that is the primary evidence path), using
the per-frame text descriptions (Step 2b, if generated) only to locate frames
cheaply. Both caches are produced once, so follow-up questions are cheap.

## Step 0 — extract (download) an eMeeting recording video
For a meeting whose recording lives on **w3.huawei.com/emeeting** (the
AI-summary page link). Validated 2026-10-28 on a 3-hour SPEAKER_SHARE_VIDEO
recording (Extreme tier, AES-128 HLS).

```bash
# 1. open a browser session on the meeting page (cookies required)
opencli browser emeeting open "<emeeting-url>" --window background

# 2. run the extractor (downloads + decrypts + merges to mp4)
python <path-to>/huawei-meeting-analysis/extract_video.py emeeting "<url>" "<out-dir>"
```

How it works: `getCloudRecord/<32-hex-id>` API (record id = the aiSummary URL
segment) → quality tiers (`Extreme > High > Medium > Low > Audio`, m3u8 each)
→ AES-128 encrypted HLS segments fetched as base64 through `opencli eval`
(session cookies; **measured ~10 s/segment — a 3 h meeting ≈ 3.5-4 h at best
tier; run it in the background and report ETA, or `--quality High` for ~2-3×
faster download when 1080p isn't needed**)
→ key fetch → openssl `-aes-128-cbc -d -nopad` (IV from the playlist tag;
TS sync 0x47 verified) → ffmpeg concat/remux to mp4, verified by ffprobe
duration vs the record metadata.

- Resumable: encrypted segments are kept in `<out-dir>/segs/`; re-run fetches
  only the missing ones (transient network failures just need a re-run).
- `--quality High` etc. to take a lower tier; default is the best available.
- Multi-part meetings: `--record-index N` picks among `record_meta.json`
  entries (a meeting can have several recordings, e.g. speaker view + share view).
- After it lands, the mp4 feeds the normal pipeline below (frames/transcript).
- Grep `record_meta.json` for duration/fileSize/recordType before downloading
  if you want to confirm you have the right recording.

## WeLink recording layout (the common case here)
A WeLink local recording is a **directory** named like
`20260709 14.10.40 高博 00563677的呼叫 73090114893` containing:

| File | What |
|---|---|
| `meeting_1.mp4` | the video (H.264, with AAC audio) — **primary source** |
| `meeting_1.m4a` | audio-only copy (same track as the mp4's audio) |
| `YYYYMMDDHHMMSS/audio.pcm` | raw PCM before conversion |
| `录制失败请查阅.txt` | "if mp4/m4a missing, run the .bat to convert" |

**Always use `meeting_1.mp4`** — it has both audio and video. The `.m4a` is
redundant (same audio), the `.pcm` is raw, and the `.txt` is just a help note.
If only `.pcm` exists, the recording wasn't converted — run the
`meeting_1_double_click_to_convert_video.bat` in that folder (WeLink's own
converter) before using this skill.

These recordings live under:
`%APPDATA%\WeLink_Desktop\appdata\imCloudInstantmeetingPc\HwmSdk\localRecordFiles\`

## Setup — one-time environment (CRITICAL: read the Meteor Lake note)

### The Meteor Lake problem (Intel Core Ultra CPUs)
On machines with **Intel Core Ultra (Meteor Lake)** CPUs (Family 6 Model 170):
- **`faster-whisper` / `ctranslate2`** — segfaults (exit 139) at model load
  on every compute type (`int8`, `float32`, `int8_float32`). The `ctranslate2`
  native library's OpenMP runtime crashes when probing the CPU's 3-tier hybrid
  topology (P-cores, E-cores, LP E-cores). **Do not use faster-whisper on
  Meteor Lake.**
- **`torch >= 2.12`** — `c10.dll`'s `DllMain` fails (WinError 1114) for the
  same topology-probing reason. **Use `torch==2.5.1+cpu`** (predates the
  aggressive native CPU detection).
- **`openai-whisper`** works once torch 2.5.1 is installed and the ffmpeg
  path is patched (see below).

### Install steps
```bash
# 1. Install CPU-only torch 2.5.1 (NOT 2.12+ — crashes on Meteor Lake)
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu

# 2. Install openai-whisper (uses PyTorch, not ctranslate2)
pip install openai-whisper

# 3. imageio-ffmpeg + pillow + numpy (for frame extraction + image reading)
pip install imageio-ffmpeg pillow numpy
```

If pip stalls on large wheels (corporate proxy), use the
[[pip-corporate-proxy]] skill's `fetch_wheels.py` to download wheels with
curl's `--speed-limit` stall-kill, then `pip install` from local files.

### ffmpeg path patch (required on Windows)
`openai-whisper` shells out to `ffmpeg` via `subprocess.run(["ffmpeg", ...])`,
but Windows needs the full path. The bundled `imageio-ffmpeg` binary is named
`ffmpeg-win-x86_64-v7.1.exe`, not `ffmpeg.exe`, so subprocess can't find it.
`transcribe_openai.py` handles this automatically by monkeypatching
`whisper.audio.load_audio` to use the `imageio-ffmpeg` path directly.

## Required inputs — confirm with the user
1. **Path** to the recording (the directory, or a video file).
2. **What they want**: full transcript? summary? action items? a specific
   slide/screenshot? This decides whether you need transcription or just frames.
3. **Language** if known (speeds up transcription): `zh`, `en`, etc.
4. **Model size** — the script defaults to `large-v3` (best quality, ~1.5 GB
   download on first run, multi-hour CPU transcription for long meetings).
   Only downgrade if the user explicitly wants speed over accuracy:
   - `tiny` (~75 MB) — fast (~5 min for 87 min audio on CPU), rough quality
   - `base` (~145 MB) — good balance, ~30-40 min for 87 min on CPU
   - `small` / `medium` / `large` — higher accuracy, much longer CPU runs

## The pipeline — run these in order

### Step 1 — extract frames + audio
(Skip Step 0 if the mp4 already exists — e.g. from Step 0 or a WeLink dir.
Step 1 itself still runs on that mp4 to produce audio.wav + frames.)
```bash
python skills/huawei-meeting-analysis/extract.py "<recording-dir-or-file>"
```
Default: scene-change detection → key frames. Outputs to `<recording>/_analysis/`:
- `frames/frame_HHMMSS.png` — key frames, named by their time in the video
- `audio.wav` — 16 kHz mono, exactly what Whisper wants
- `manifest.json` — source, duration, frame list (file + timestamp)

Options: `--mode interval --interval 60`, `--threshold 0.30`, `--max-frames 80`.

### Step 2 — transcribe (use transcribe_openai.py, NOT transcribe.py)
```bash
# Set PYTHONIOENCODING to avoid GBK console crash on zh-CN Windows
PYTHONIOENCODING=utf-8 python skills/huawei-meeting-analysis/transcribe_openai.py \
  "<recording-dir-or-file>" --language zh
```
Outputs `<recording>/_analysis/transcript.{txt,json,srt}`.
Default model is `large-v3` (best quality). Add `--model base` (or tiny)
only for a quick skim.

**Why `transcribe_openai.py` and not `transcribe.py`?** The original
`transcribe.py` uses `faster-whisper`, which segfaults on Meteor Lake.
`transcribe_openai.py` uses `openai-whisper` (PyTorch backend) and includes
the ffmpeg monkeypatch. Use `transcribe_openai.py` on this machine.

**Critical flags:**
- `--model large-v3` is the default (best accuracy, slow on CPU);
  `--model tiny`/`base` only for quick skims (~5 min / ~30 min per 87 min audio)
- `--language zh` to pin the language (faster than auto-detect)
- `PYTHONIOENCODING=utf-8` env var — without it, `whisper.transcribe(verbose=True)`
  crashes with `UnicodeEncodeError: 'gbk' codec can't encode` on a zh-CN
  Windows console. The script uses `verbose=False` to avoid this, but set the
  env var too as a belt-and-suspenders fix.

### Step 2b — frame descriptions (optional multi-modal mode)
```bash
# Vision model writes a text description of every frame (resumable, cached)
PYTHONIOENCODING=utf-8 python skills/huawei-meeting-analysis/analyze_frames.py \
  "<recording-dir-or-file>"
```
Outputs `<recording>/_analysis/frames_analysis.{json,md}` — one description
per frame (layout, title, verbatim bullet text, chart/table/code content).

Uses the rnd gateway's **glm-5.3-flash** by default (proven vision-capable;
verified 2026-10-27). Pure stdlib urllib, proxy handlers stripped for the
intranet gateway, 4 parallel workers, retried 4×, resumable cache (re-run
retries only failed/missing frames; `--force` redoes all). Do NOT add
thinking/reasoning params — the gateway rejects them for GLM models.

When to use: many frames and tight agent context, or when you want frame
content greppable as text. **It is an auxiliary cache, not the primary
evidence** — the underlying model (e.g. glm-5.3-flash) is multimodal and can
read the PNGs directly, which is higher-fidelity than any text description.
Use the descriptions to locate relevant frames cheaply, then read those PNGs
as images for the actual content.

### Step 3 — analyze (the agent does this; no script)
The underlying model is **multimodal — read the frame PNGs directly as
images**. That is the primary evidence path; text caches are for locating
frames cheaply.

Once you have the transcript + frames:
- **Read** `_analysis/transcript.txt` for the full text.
- **Read** `_analysis/manifest.json` to get the frame list + timestamps.
- **Locate** the frames that matter:
  - if `_analysis/frames_analysis.md` exists (Step 2b), grep/skim it to pick
    the frames worth reading — descriptions are cheaper to scan than images;
  - otherwise pick by timestamp gaps from `manifest.json`.
- **Read the selected PNGs (`_analysis/frames/frame_HHMMSS.png`) as images.**
  Don't write analysis.md from the descriptions alone — verify every load-
  bearing claim (UI text, numbers, tables, error codes) against the actual
  image. The vision model's per-frame text is OCR-prone, especially dense
  tables, small log text, and CJK glyphs.
- **Budget the reads**: for an 80-frame meeting, spot-checking 5-10 key
  frames is usually enough; read exhaustively only when the user asks for
  screen-level detail.
- **Synthesize**: summary, action items, decisions, topic search, or answer
  the specific question. Cite timestamps from the transcript.
- **Write** the analysis to `_analysis/analysis.md` (in the user's language,
  e.g. Chinese for a Chinese meeting) with: meeting summary, key topics with
  timestamps, action items, key concepts glossary, and conclusions. See the
  existing `_analysis/analysis.md` from the 2026-07-09 meeting as a template.
- **State the evidence basis** in analysis.md (e.g. "frame content verified
  by direct image reads on N frames; transcript covers mm:ss–mm:ss"). This
  lets the user judge how much was seen firsthand vs mediated.

## Verify (quick smoke test)
```bash
# Test that torch imports (will fail if wrong version on Meteor Lake)
python -c "import torch; print(torch.__version__)"

# Test that openai-whisper can load a model
python -c "import whisper; m = whisper.load_model('tiny'); print('OK')"

# Probe the recording
python skills/huawei-meeting-analysis/extract.py "<recording-dir>" --max-frames 5
```

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| `faster-whisper` segfaults (exit 139) at model load | `ctranslate2` crashes on Meteor Lake CPU topology probing | Use `transcribe_openai.py` (openai-whisper/PyTorch) instead of `transcribe.py` |
| `torch` import: `WinError 1114` on `c10.dll` | torch 2.12+ native libs crash on Meteor Lake LP E-cores | `pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu` |
| `UnicodeEncodeError: 'gbk' codec` during transcription | zh-CN Windows console defaults to GBK; whisper's verbose print can't encode Unicode | `PYTHONIOENCODING=utf-8` + script uses `verbose=False` |
| `FileNotFoundError: [WinError 2]` in `load_audio` | `openai-whisper` shells out to `ffmpeg` which isn't on PATH | `transcribe_openai.py` monkeypatches `load_audio` to use `imageio-ffmpeg`'s bundled binary |
| ffmpeg subprocess can't find `ffmpeg` even with dir on PATH | bundled exe is `ffmpeg-win-x86_64-v7.1.exe`, not `ffmpeg.exe` | The monkeypatch in `transcribe_openai.py` passes the full path — don't rely on PATH |
| `OSError: [WinError 1114]` on `c10.dll` after swapping `libiomp5md.dll` | OpenMP swap alone doesn't fix it; `c10.dll` itself has the topology code | Downgrade to torch 2.5.1 (the real fix) |
| Model download hangs / 407 | Same corporate-proxy stall | Set `HTTPS_PROXY` env var; see [[pip-corporate-proxy]] |
| Frame extraction: `UnicodeDecodeError: 'gbk'` | zh-CN locale; ffmpeg stderr has non-UTF8 bytes | `extract.py` captures as bytes + `errors='replace'` (already fixed) |
| `_analysis/` writes into WeLink's folder | Expected — WeLink ignores subfolders it didn't create | Pass `--out <path>` to write elsewhere |

## Notes
- Outputs go in `<recording>/_analysis/`. WeLink ignores subfolders it didn't
  create. If you'd rather not write there, pass `--out <path>`.
- `_analysis/` and its contents are **not** committed (user data, not repo).
  The full `_analysis/` output is: `frames/`, `audio.wav`, `manifest.json`,
  `transcript.{txt,json,srt}`, `frames_analysis.{json,md}` (Step 2b), and
  `analysis.md`.
- The `.m4a` and `audio.pcm` are redundant once `meeting_1.mp4` exists.
- Timestamps in frame filenames align with transcript segment times, so "the
  slide shown at 00:14:30" maps directly to both.
- `transcribe.py` (faster-whisper) is kept for non-Meteor-Lake machines where
  ctranslate2 works. On this machine, always use `transcribe_openai.py`.
- For Meteor Lake + IPEX (Intel Extension for PyTorch): no Windows wheels
  exist on PyPI (all `manylinux`), so IPEX is not a viable path on Windows.
  torch 2.5.1 is the fix.
