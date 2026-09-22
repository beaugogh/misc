#!/usr/bin/env python3
"""Validate speaker-labeled transcripts and write a corpus manifest."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import json
import statistics


LABELS = {"LAOGAO", "XIAOMO"}


def video_id(path: Path) -> str:
    return path.parent.name.rsplit("__", 1)[-1]


def parse_args():
    skill = Path(__file__).resolve().parent.parent
    output = skill / "output"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=output / "whisper-large-v3")
    parser.add_argument("--labeled-dir", type=Path, default=output / "speaker-labeled")
    parser.add_argument("--manifest", type=Path, default=output / "speaker-labeled" / "manifest.json")
    return parser.parse_args()


def main():
    args = parse_args()
    sources = sorted(args.source_dir.glob("*/*.json"))
    labeled = sorted(args.labeled_dir.glob("*/*.speaker-labeled.json"))
    by_id = {video_id(path): path for path in labeled}
    problems = []
    episodes = []
    corpus_labels = {label: 0 for label in LABELS}
    corpus_seconds = {label: 0.0 for label in LABELS}
    all_confidence = []

    for source_path in sources:
        vid = video_id(source_path)
        labeled_path = by_id.get(vid)
        if labeled_path is None:
            problems.append(f"missing labeled JSON: {vid}")
            continue
        source = json.loads(source_path.read_text(encoding="utf-8"))
        result = json.loads(labeled_path.read_text(encoding="utf-8"))
        source_rows = source.get("segments", [])
        rows = result.get("segments", [])
        if len(source_rows) != len(rows):
            problems.append(f"segment count mismatch: {vid}")
            continue

        counts = {label: 0 for label in LABELS}
        seconds = {label: 0.0 for label in LABELS}
        confidences = []
        low_confidence = 0
        for index, (original, row) in enumerate(zip(source_rows, rows)):
            original_core = (original.get("start"), original.get("end"), original.get("text"))
            result_core = (row.get("start"), row.get("end"), row.get("text"))
            if original_core != result_core:
                problems.append(f"source content changed: {vid}, segment {index}")
            label = row.get("speaker")
            if label not in LABELS:
                problems.append(f"invalid speaker: {vid}, segment {index}")
                continue
            try:
                confidence = float(row["speaker_confidence"])
            except (KeyError, TypeError, ValueError):
                problems.append(f"invalid confidence: {vid}, segment {index}")
                continue
            if not 0 <= confidence <= 1:
                problems.append(f"out-of-range confidence: {vid}, segment {index}")
            duration = max(0.0, float(row["end"]) - float(row["start"]))
            counts[label] += 1
            seconds[label] += duration
            corpus_labels[label] += 1
            corpus_seconds[label] += duration
            confidences.append(confidence)
            all_confidence.append(confidence)
            low_confidence += confidence < 0.75

        total = sum(counts.values())
        duration = sum(seconds.values())
        episodes.append({
            "video_id": vid,
            "episode_directory": source_path.parent.name,
            "source_json": str(source_path),
            "labeled_json": str(labeled_path),
            "segments": total,
            "segment_counts": counts,
            "xiaomo_segment_share": round(counts["XIAOMO"] / total, 6) if total else 0,
            "spoken_seconds": round(duration, 3),
            "speaker_seconds": {key: round(value, 3) for key, value in seconds.items()},
            "xiaomo_duration_share": round(seconds["XIAOMO"] / duration, 6) if duration else 0,
            "median_confidence": round(statistics.median(confidences), 6) if confidences else 0,
            "segments_below_0_75_confidence": low_confidence,
        })

    for extension in ("txt", "srt"):
        found = len(list(args.labeled_dir.glob(f"*/*.speaker-labeled.{extension}")))
        if found != len(sources):
            problems.append(f"expected {len(sources)} labeled {extension} files; found {found}")

    total_segments = sum(corpus_labels.values())
    total_seconds = sum(corpus_seconds.values())
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_episode_count": len(sources),
        "labeled_episode_count": len(labeled),
        "integrity_errors": problems,
        "corpus": {
            "segments": total_segments,
            "segment_counts": corpus_labels,
            "xiaomo_segment_share": round(corpus_labels["XIAOMO"] / total_segments, 6),
            "spoken_hours": round(total_seconds / 3600, 6),
            "speaker_hours": {key: round(value / 3600, 6) for key, value in corpus_seconds.items()},
            "xiaomo_duration_share": round(corpus_seconds["XIAOMO"] / total_seconds, 6),
            "median_confidence": round(statistics.median(all_confidence), 6),
            "segments_below_0_75_confidence": sum(value < 0.75 for value in all_confidence),
        },
        "episodes": episodes,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Audited {len(episodes)} episodes and {total_segments} segments; "
        f"{len(problems)} integrity errors. Manifest: {args.manifest}"
    )
    if problems:
        for problem in problems[:25]:
            print(f"ERROR: {problem}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
