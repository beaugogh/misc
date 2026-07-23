#!/usr/bin/env python3
"""Extract key frames + a whisper-ready WAV from a meeting recording.

Handles WeLink recordings (a directory containing meeting_1.mp4) or any video
file. Uses the ffmpeg binary bundled by imageio-ffmpeg, so no system ffmpeg
install is needed.

Outputs (into --out, default <recording>/_analysis/):
  frames/frame_HHMMSS.png   key frames, timestamped by their position in the video
  audio.wav                 16 kHz mono PCM — exactly what faster-whisper wants
  manifest.json             source, duration, frame list (path + timestamp), audio path

Sampling: scene-change detection by default (captures slide/screen changes
without thousands of frames). Fallback to uniform interval sampling for
talking-head sections or when scene detection yields too little.
"""
import argparse
import json
import os
import re
import subprocess
import sys

import imageio_ffmpeg


def ffmpeg():
    return imageio_ffmpeg.get_ffmpeg_exe()


def probe_duration(src):
    """Get duration in seconds via ffmpeg stderr parsing.

    Capture as BYTES and decode defensively: ffmpeg's stderr includes
    non-UTF8 bytes (e.g. the box-drawing 0xab on a zh-CN locale), and
    subprocess's default text mode decodes as the system ANSI codepage
    (GBK here), which raises UnicodeDecodeError on those bytes — leaving
    r.stderr as None. bytes + errors='replace' never throws.
    """
    r = subprocess.run([ffmpeg(), "-i", src], capture_output=True)
    stderr = r.stderr.decode("utf-8", errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", stderr)
    if not m:
        return None
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def find_source(path):
    """Accept a dir (WeLink recording) or a video file. Return the video path."""
    if os.path.isdir(path):
        for name in ("meeting_1.mp4", "meeting.mp4"):
            cand = os.path.join(path, name)
            if os.path.isfile(cand):
                return cand
        # fall back to any .mp4 in the dir
        for name in os.listdir(path):
            if name.lower().endswith(".mp4"):
                return os.path.join(path, name)
        sys.exit(f"No .mp4 found in directory: {path}")
    if os.path.isfile(path):
        return path
    sys.exit(f"Not found: {path}")


def fmt_ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    return f"{h:02d}{m:02d}{s:02d}"


def extract_audio(src, out_wav):
    """16 kHz mono PCM WAV — whisper's expected input."""
    if os.path.exists(out_wav):
        print(f"  audio.wav exists, skipping ({os.path.getsize(out_wav)//1024} KB)")
        return
    print("  extracting audio.wav (16 kHz mono)...")
    subprocess.run(
        [ffmpeg(), "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
         "-c:a", "pcm_s16le", out_wav],
        check=True, stderr=subprocess.DEVNULL)


def extract_frames_scene(src, frames_dir, threshold, max_frames):
    """Scene-change detection. Returns [(path, timestamp_seconds), ...].

    showinfo logs one pts_time line per selected frame, in output order, so we
    zip the parsed timestamps with the image2 filenames (frame_0001.png ...).
    """
    # First pass: select + showinfo, discard frames, just to count/time? No —
    # do it in one pass: output frames AND capture showinfo stderr.
    # Capture as bytes + decode with errors='replace' (see probe_duration):
    # ffmpeg's showinfo stderr isn't clean UTF8 on a zh-CN locale.
    proc = subprocess.run(
        [ffmpeg(), "-y", "-i", src,
         "-vf", f"select='gt(scene,{threshold})',showinfo",
         "-vsync", "vfr", "-frame_pts", "0",
         os.path.join(frames_dir, "frame_%04d.png")],
        capture_output=True)
    stderr = proc.stderr.decode("utf-8", errors="replace")
    times = [float(x) for x in re.findall(r"pts_time:(\d+(?:\.\d+)?)", stderr)]
    files = sorted(f for f in os.listdir(frames_dir) if re.match(r"frame_\d+\.png", f))
    # zip; if counts mismatch (rare), trim to the shorter
    pairs = list(zip(files, times))
    if len(files) != len(times):
        print(f"  warn: {len(files)} frames vs {len(times)} showinfo lines; using {len(pairs)}")

    # Rename to timestamped names + subsample if over the cap
    result = []
    step = max(1, (len(pairs) + max_frames - 1) // max_frames) if len(pairs) > max_frames else 1
    if step > 1:
        print(f"  {len(pairs)} frames > cap {max_frames}; subsampling every {step}th")
    for i, (fname, t) in enumerate(pairs):
        if i % step != 0:
            os.remove(os.path.join(frames_dir, fname))
            continue
        new_name = f"frame_{fmt_ts(t)}.png"
        new_path = os.path.join(frames_dir, new_name)
        # Disambiguate when two scene-changes land in the same whole second:
        # os.rename raises WinError 183 if the target exists. The manifest still
        # stores the precise float timestamp, so alignment is preserved.
        if os.path.exists(new_path):
            stem, ext = os.path.splitext(new_name)
            k = 2
            while os.path.exists(new_path):
                new_path = os.path.join(frames_dir, f"{stem}_{k}{ext}")
                k += 1
            new_name = os.path.basename(new_path)
        os.rename(os.path.join(frames_dir, fname), new_path)
        result.append((new_name, t))
    return result


def extract_frames_interval(src, frames_dir, interval, max_frames):
    """Uniform sampling: one frame every `interval` seconds."""
    dur = probe_duration(src) or 0
    times = []
    t = 0.0
    while t < dur and len(times) < max_frames:
        times.append(t)
        t += interval
    for t in times:
        subprocess.run(
            [ffmpeg(), "-y", "-ss", str(t), "-i", src, "-frames:v", "1",
             os.path.join(frames_dir, f"frame_{fmt_ts(t)}.png")],
            check=True, stderr=subprocess.DEVNULL)
    return [(f"frame_{fmt_ts(t)}.png", t) for t in times]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="recording directory or video file")
    ap.add_argument("--out", help="output dir (default: <source>/_analysis)")
    ap.add_argument("--mode", choices=["scene", "interval"], default="scene")
    ap.add_argument("--threshold", type=float, default=0.30,
                    help="scene-change threshold (lower=more frames). default 0.30")
    ap.add_argument("--interval", type=float, default=60,
                    help="seconds between frames in interval mode. default 60")
    ap.add_argument("--max-frames", type=int, default=80,
                    help="cap on frame count (subsampled if exceeded). default 80")
    args = ap.parse_args()

    src = find_source(args.source)
    base = src if os.path.isfile(args.source) else args.source
    out_dir = args.out or os.path.join(base, "_analysis")
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    dur = probe_duration(src)
    print(f"source: {src}")
    print(f"duration: {dur:.0f}s ({dur/60:.1f} min)" if dur else "duration: unknown")

    extract_audio(src, os.path.join(out_dir, "audio.wav"))

    print(f"extracting frames (mode={args.mode})...")
    if args.mode == "scene":
        frames = extract_frames_scene(src, frames_dir, args.threshold, args.max_frames)
    else:
        frames = extract_frames_interval(src, frames_dir, args.interval, args.max_frames)
    print(f"  {len(frames)} frames -> {frames_dir}")

    manifest = {
        "source": src,
        "duration_seconds": dur,
        "audio": "audio.wav",
        "frames": [{"file": f, "timestamp": round(t, 1)} for f, t in frames],
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"manifest -> {os.path.join(out_dir, 'manifest.json')}")
    print("\nNext: transcribe.py to get the transcript, then analyze.")


if __name__ == "__main__":
    main()
