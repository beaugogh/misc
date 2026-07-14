#!/usr/bin/env python3
"""Transcribe a meeting recording's audio to a timestamped transcript.

Uses faster-whisper (CPU, ONNX runtime). Reads audio.wav produced by
extract.py, or extracts audio on the fly from a video file / recording dir.

Outputs (into --out, default <source>/_analysis/):
  transcript.json   segments: [{start, end, text}], full text
  transcript.txt    plain text with [HH:MM:SS] timestamps per segment
  transcript.srt    SubRip subtitles

Model choice:
  tiny    ~75 MB   fastest, rough            — quick skim / very long meetings
  base    ~145 MB  good balance (default)    — general use
  small   ~480 MB  high accuracy             — when you need detail / jargon
  medium  ~1.5 GB  very accurate             — heavy; long CPU runs
  large-v3 ~3 GB   best                      — only when accuracy is critical

First run downloads the model from HuggingFace (through the proxy). On CPU,
expect roughly realtime-to-2x realtime for tiny/base, slower for larger.

Language: auto-detected by default. Pass --language (e.g. zh, en) to pin it
and speed things up.
"""
import argparse
import json
import os
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="recording dir, video file, or audio.wav")
    ap.add_argument("--out", help="output dir (default: <source>/_analysis)")
    ap.add_argument("--model", default="base",
                    help="whisper model: tiny/base/small/medium/large-v3 (default base)")
    ap.add_argument("--language", help="language code e.g. zh, en (default: auto-detect)")
    ap.add_argument("--device", default="cpu", help="cpu (default) or cuda")
    ap.add_argument("--compute-type", default="int8",
                    help="int8 (default, CPU-friendly) / float16 (GPU) / float32")
    args = ap.parse_args()

    # Resolve the audio input
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

    print(f"loading faster-whisper model '{args.model}' (first run downloads it)...")
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper not installed. See the pip-corporate-proxy skill.")
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)

    print(f"transcribing: {audio}")
    segments_iter, info = model.transcribe(
        audio, language=args.language, vad_filter=True,
        beam_size=5, vad_parameters={"min_silence_duration_ms": 500})
    print(f"  detected language: {info.language} (p={info.language_probability:.2f})")
    print(f"  duration: {info.duration:.0f}s ({info.duration/60:.1f} min)")

    segments = []
    print("\nsegments:")
    for seg in segments_iter:
        line = f"[{fmt_ts(seg.start)} -> {fmt_ts(seg.end)}] {seg.text.strip()}"
        print(line)
        segments.append({"start": round(seg.start, 2), "end": round(seg.end, 2),
                         "text": seg.text.strip()})

    # transcript.json
    with open(os.path.join(out_dir, "transcript.json"), "w", encoding="utf-8") as f:
        json.dump({"language": info.language, "duration": info.duration,
                   "segments": segments,
                   "text": " ".join(s["text"] for s in segments)}, f, indent=2, ensure_ascii=False)

    # transcript.txt (timestamped)
    with open(os.path.join(out_dir, "transcript.txt"), "w", encoding="utf-8") as f:
        for s in segments:
            f.write(f"[{fmt_ts(s['start'])}] {s['text']}\n")

    # transcript.srt
    with open(os.path.join(out_dir, "transcript.srt"), "w", encoding="utf-8") as f:
        for i, s in enumerate(segments, 1):
            f.write(f"{i}\n{srt_ts(s['start'])} --> {srt_ts(s['end'])}\n{s['text']}\n\n")

    print(f"\n{len(segments)} segments written to {out_dir}/transcript.{{json,txt,srt}}")


if __name__ == "__main__":
    main()
