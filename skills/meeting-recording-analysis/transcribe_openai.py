#!/usr/bin/env python3
"""Transcribe a meeting recording's audio to a timestamped transcript.

Uses openai-whisper (PyTorch backend). Reads audio.wav produced by extract.py,
or extracts audio on the fly from a video file / recording dir.

IMPORTANT (Windows + Intel Core Ultra / Meteor Lake):
  - torch >= 2.12 crashes on Meteor Lake (c10.dll DllMain fails during CPU
    topology probing of LP E-cores). Use torch 2.5.1+cpu.
  - faster-whisper / ctranslate2 segfaults at model load on the same CPU.
  - openai-whisper shells out to `ffmpeg` which isn't on PATH; this script
    monkeypatches load_audio to use the imageio-ffmpeg bundled binary.

Outputs (into --out, default <source>/_analysis/):
  transcript.json   segments: [{start, end, text}], full text
  transcript.txt    plain text with [HH:MM:SS] timestamps per segment
  transcript.srt    SubRip subtitles
"""
import argparse
import json
import os
import subprocess
import sys


def fmt_ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def srt_ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def find_source(path):
    """Accept a dir (WeLink recording) or a video file. Return the video path."""
    if os.path.isdir(path):
        for name in ("meeting_1.mp4", "meeting.mp4"):
            cand = os.path.join(path, name)
            if os.path.isfile(cand):
                return cand
        for name in os.listdir(path):
            if name.lower().endswith(".mp4"):
                return os.path.join(path, name)
        sys.exit(f"No .mp4 found in directory: {path}")
    if os.path.isfile(path):
        return path
    sys.exit(f"Not found: {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="recording dir, video file, or audio.wav")
    ap.add_argument("--out", help="output dir (default: <source>/_analysis)")
    ap.add_argument("--model", default="tiny",
                    help="whisper model: tiny/base/small/medium/large (default tiny)")
    ap.add_argument("--language", default=None, help="language code e.g. zh, en (default: auto-detect)")
    args = ap.parse_args()

    # Resolve audio input
    src = args.source
    audio = None
    if os.path.isdir(src):
        cand = os.path.join(src, "_analysis", "audio.wav")
        audio = cand if os.path.isfile(cand) else None
        if not audio:
            for name in ("meeting_1.mp4", "meeting.mp4"):
                p = os.path.join(src, name)
                if os.path.isfile(p):
                    audio = p
                    break
    elif src.lower().endswith(".wav"):
        audio = src
    elif os.path.isfile(src):
        audio = src
    if not audio:
        sys.exit(f"No audio/video found for: {src}\nRun extract.py first, or pass the recording dir.")
    out_dir = args.out or (os.path.join(src, "_analysis") if os.path.isdir(src)
                           else os.path.dirname(audio) or ".")
    os.makedirs(out_dir, exist_ok=True)

    # --- Meteor Lake / Windows workarounds ---
    # openai-whisper shells out to `ffmpeg` which isn't on PATH on this box.
    # Monkeypatch load_audio to use the imageio-ffmpeg bundled binary directly.
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
    import numpy as np
    import whisper.audio as wa
    def patched_load_audio(audio_file):
        cmd = [FF, "-i", str(audio_file), "-ar", str(wa.SAMPLE_RATE),
               "-ac", "1", "-f", "f32le", "-"]
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
        return np.frombuffer(out, np.float32)
    wa.load_audio = patched_load_audio
    print(f"ffmpeg patched: {FF}", flush=True)

    print(f"loading openai-whisper model '{args.model}'...", flush=True)
    import whisper
    import torch
    print(f"  torch {torch.__version__}", flush=True)
    model = whisper.load_model(args.model)

    print(f"transcribing: {audio}", flush=True)
    # fp16=False required for CPU
    # verbose=False: verbose=True calls print() which crashes on zh-CN Windows
    # consoles (GBK codec can't encode Unicode replacement chars in the transcript).
    result = model.transcribe(audio, language=args.language, fp16=False, verbose=False)
    segments = result["segments"]
    print(f"\n{len(segments)} segments, language={result['language']}", flush=True)

    # transcript.json
    with open(os.path.join(out_dir, "transcript.json"), "w", encoding="utf-8") as f:
        json.dump({"language": result["language"], "segments": [
            {"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()}
            for s in segments],
            "text": result["text"]}, f, indent=2, ensure_ascii=False)

    # transcript.txt (timestamped)
    with open(os.path.join(out_dir, "transcript.txt"), "w", encoding="utf-8") as f:
        for s in segments:
            f.write(f"[{fmt_ts(s['start'])}] {s['text'].strip()}\n")

    # transcript.srt
    with open(os.path.join(out_dir, "transcript.srt"), "w", encoding="utf-8") as f:
        for i, s in enumerate(segments, 1):
            f.write(f"{i}\n{srt_ts(s['start'])} --> {srt_ts(s['end'])}\n{s['text'].strip()}\n\n")

    print(f"\n{len(segments)} segments written to {out_dir}/transcript.{{json,txt,srt}}", flush=True)


if __name__ == "__main__":
    main()
