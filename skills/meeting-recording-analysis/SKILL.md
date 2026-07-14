---
name: meeting-recording-analysis
description: Analyzes meeting recordings (video + audio) — transcribes speech to a timestamped transcript and extracts key frames from screen-share video, then summarizes / pulls action items / answers questions about the meeting. Built for WeLink recordings (a directory with meeting_1.mp4 + meeting_1.m4a + audio.pcm) but works on any video file. Use when the user wants to know what happened in a recorded meeting, get a summary or action items, extract something shown on the shared screen (slides, code, a diagram), or search what was said by timestamp. Requires the Python venv with openai-whisper + imageio-ffmpeg (see Setup).
---

# Meeting recording analysis (video + audio)

## What this skill does
Turn a meeting recording into something you can read and reason about:
1. **Transcribe** the audio → timestamped transcript (`.txt` / `.json` / `.srt`).
2. **Extract key frames** from the video → PNGs at slide/screen changes.
3. **Analyze** — summarize, pull action items, find decisions, answer
   "what was said about X", or read a specific shared screen (slide/code).

The agent reads the transcript as text and the frames as images, then
synthesizes the answer. Both are produced once and cached, so follow-up
questions are cheap.

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
4. **Model size** if they care about speed vs accuracy:
   - `tiny` (~75 MB) — fast (~5 min for 87 min audio on CPU), rough quality
   - `base` (~145 MB) — good balance, ~30-40 min for 87 min on CPU
   - `small` / `medium` / `large` — higher accuracy, much longer CPU runs

## The pipeline — run these in order

### Step 1 — extract frames + audio
```bash
python skills/meeting-recording-analysis/extract.py "<recording-dir-or-file>"
```
Default: scene-change detection → key frames. Outputs to `<recording>/_analysis/`:
- `frames/frame_HHMMSS.png` — key frames, named by their time in the video
- `audio.wav` — 16 kHz mono, exactly what Whisper wants
- `manifest.json` — source, duration, frame list (file + timestamp)

Options: `--mode interval --interval 60`, `--threshold 0.20`, `--max-frames 80`.

### Step 2 — transcribe (use transcribe_openai.py, NOT transcribe.py)
```bash
# Set PYTHONIOENCODING to avoid GBK console crash on zh-CN Windows
PYTHONIOENCODING=utf-8 python skills/meeting-recording-analysis/transcribe_openai.py \
  "<recording-dir-or-file>" --model base --language zh
```
Outputs `<recording>/_analysis/transcript.{txt,json,srt}`.

**Why `transcribe_openai.py` and not `transcribe.py`?** The original
`transcribe.py` uses `faster-whisper`, which segfaults on Meteor Lake.
`transcribe_openai.py` uses `openai-whisper` (PyTorch backend) and includes
the ffmpeg monkeypatch. Use `transcribe_openai.py` on this machine.

**Critical flags:**
- `--model tiny` for a quick skim (~5 min), `--model base` for accuracy (~30 min)
- `--language zh` to pin the language (faster than auto-detect)
- `PYTHONIOENCODING=utf-8` env var — without it, `whisper.transcribe(verbose=True)`
  crashes with `UnicodeEncodeError: 'gbk' codec can't encode` on a zh-CN
  Windows console. The script uses `verbose=False` to avoid this, but set the
  env var too as a belt-and-suspenders fix.

### Step 3 — analyze (the agent does this; no script)
Once you have the transcript + frames:
- **Read** `_analysis/transcript.txt` for the full text.
- **Read** `_analysis/manifest.json` to get the frame list + timestamps.
- **Read** the frames (`_analysis/frames/frame_HHMMSS.png`) as images when
  the user asks about something visual, or to enrich the summary.
- **Synthesize**: summary, action items, decisions, topic search, or answer
  the specific question. Cite timestamps from the transcript.
- **Write** the analysis to `_analysis/analysis.md` (in the user's language,
  e.g. Chinese for a Chinese meeting) with: meeting summary, key topics with
  timestamps, action items, key concepts glossary, and conclusions. See the
  existing `_analysis/analysis.md` from the 2026-07-09 meeting as a template.

## Verify (quick smoke test)
```bash
# Test that torch imports (will fail if wrong version on Meteor Lake)
python -c "import torch; print(torch.__version__)"

# Test that openai-whisper can load a model
python -c "import whisper; m = whisper.load_model('tiny'); print('OK')"

# Probe the recording
python skills/meeting-recording-analysis/extract.py "<recording-dir>" --max-frames 5
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
  `transcript.{txt,json,srt}`, and `analysis.md`.
- The `.m4a` and `audio.pcm` are redundant once `meeting_1.mp4` exists.
- Timestamps in frame filenames align with transcript segment times, so "the
  slide shown at 00:14:30" maps directly to both.
- `transcribe.py` (faster-whisper) is kept for non-Meteor-Lake machines where
  ctranslate2 works. On this machine, always use `transcribe_openai.py`.
- For Meteor Lake + IPEX (Intel Extension for PyTorch): no Windows wheels
  exist on PyPI (all `manylinux`), so IPEX is not a viable path on Windows.
  torch 2.5.1 is the fix.
