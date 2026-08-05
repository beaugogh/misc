"""Segmentation evaluation metrics (Phase 9.8.2).

Pure-stdlib implementation of two standard text-segmentation metrics, adapted for
temporal task-boundary evaluation:

  - **WindowDiff** (Pevzner & Hearst, 2002): slides a window of size k over two
    binary boundary sequences and counts positions where the number of boundaries
    in the window differs between reference and hypothesis. Lower = better.
    0 means perfect agreement.

  - **Collar-Based F1**: standard precision/recall/F1 over boundary positions,
    where a predicted boundary is a true positive if it falls within +/- collar
    seconds of a reference boundary. This handles the temporal nature of task
    boundaries — being off by 30 seconds is not the same as being off by 30 minutes.

These metrics let us tune PELT penalty beta and GMM thresholds against a labeled
benchmark instead of by eyeballing. See research-findings.md
section 7.1 for the research grounding.

No external dependencies (no `segeval` needed). The `segeval` library implements
these for text segmentation; our adaptation works on temporal event timelines.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone


def _build_binary_sequence(boundaries: list[float], timeline: list[float]) -> list[int]:
    """Build a binary sequence over the event timeline.

    Each position in the timeline gets a 1 if a boundary falls at or very near
    (within 1 second) that event's timestamp, 0 otherwise. The first event
    position is always 0 (a boundary at the very start is a session start, not
    a task boundary within the timeline).

    Args:
        boundaries: boundary timestamps (epoch seconds).
        timeline: sorted event timestamps (epoch seconds).

    Returns:
        Binary list of same length as timeline.
    """
    if not timeline:
        return []
    bs = sorted(boundaries)
    result = [0] * len(timeline)
    for b in bs:
        # Find the closest timeline position
        best_idx = -1
        best_dist = float("inf")
        for i, t in enumerate(timeline):
            dist = abs(t - b)
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        # Only mark if within 1 second of an event
        if best_idx >= 0 and best_dist <= 1.0:
            result[best_idx] = 1
        elif best_idx >= 0:
            # If no event is within 1s, mark the nearest event position
            # (the boundary is between events, but for WindowDiff we need
            # it on the event grid)
            result[best_idx] = 1
    # First position is session start, not a task boundary
    if result:
        result[0] = 0
    return result


def windowdiff(ref: list[int], hyp: list[int], k: int) -> float:
    """Compute the WindowDiff metric (Pevzner & Hearst, 2002).

    Slides a window of size k over two binary boundary sequences. At each
    position i (0 to len-k), counts a disagreement if the number of boundaries
    in ref[i:i+k] differs from hyp[i:i+k]. Returns the normalized count
    (total disagreements / number of windows).

    The window size k is typically half the average reference segment length.
    A perfect hypothesis (hyp == ref) yields 0.0.

    Args:
        ref: reference binary boundary sequence.
        hyp: hypothesis binary boundary sequence.
        k: window size (must be >= 2).

    Returns:
        Normalized WindowDiff score in [0, 1]. Lower is better.
    """
    if len(ref) != len(hyp):
        raise ValueError(f"ref and hyp must have the same length: {len(ref)} vs {len(hyp)}")
    n = len(ref)
    if n < k:
        # Not enough data for even one window
        return 0.0
    if k < 2:
        raise ValueError("window size k must be >= 2")

    total_disagreements = 0
    num_windows = n - k + 1
    for i in range(num_windows):
        ref_count = sum(ref[i:i + k])
        hyp_count = sum(hyp[i:i + k])
        if ref_count != hyp_count:
            total_disagreements += 1

    return total_disagreements / num_windows if num_windows > 0 else 0.0


def collar_f1(predicted: list[float], reference: list[float], collar: float) -> dict:
    """Compute collar-based precision, recall, and F1 for boundary positions.

    A predicted boundary is a true positive (TP) if it falls within +/- collar
    seconds of a reference boundary. Each reference boundary can match at most
    one predicted boundary (one-to-one matching).

    Args:
        predicted: predicted boundary timestamps (epoch seconds).
        reference: reference boundary timestamps (epoch seconds).
        collar: tolerance in seconds (e.g., 300 for 5 minutes).

    Returns:
        Dict with keys: precision, recall, f1, tp, fp, fn.
    """
    if not predicted and not reference:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0, "tp": 0, "fp": 0, "fn": 0}
    if not predicted:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "tp": 0, "fp": 0, "fn": len(reference)}
    if not reference:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "tp": 0, "fp": len(predicted), "fn": 0}

    pred_sorted = sorted(predicted)
    ref_sorted = sorted(reference)

    # Greedy one-to-one matching: for each reference boundary, find the closest
    # unmatched predicted boundary within the collar.
    matched_pred = set()  # indices of predicted boundaries already matched
    tp = 0
    for ref_ts in ref_sorted:
        best_idx = -1
        best_dist = float("inf")
        for j, pred_ts in enumerate(pred_sorted):
            if j in matched_pred:
                continue
            dist = abs(pred_ts - ref_ts)
            if dist <= collar and dist < best_dist:
                best_dist = dist
                best_idx = j
        if best_idx >= 0:
            matched_pred.add(best_idx)
            tp += 1

    fp = len(pred_sorted) - tp
    fn = len(ref_sorted) - tp

    precision = tp / len(pred_sorted) if pred_sorted else 0.0
    recall = tp / len(ref_sorted) if ref_sorted else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def _average_segment_length(boundaries: list[float], timeline: list[float]) -> float:
    """Compute the average segment length (in event positions) from boundaries.

    Given boundary positions on the timeline, segments are the spans between
    consecutive boundaries (including the implicit boundaries at start and end).
    Returns the average segment length in number of events.
    """
    if not timeline:
        return 1.0
    # Map boundaries to timeline indices
    binary = _build_binary_sequence(boundaries, timeline)
    # Find segment boundaries (including implicit 0 and n-1)
    segment_starts = [0]
    for i in range(1, len(binary)):
        if binary[i] == 1:
            segment_starts.append(i)
    segment_starts.append(len(timeline))  # implicit end

    segment_lengths = []
    for i in range(len(segment_starts) - 1):
        length = segment_starts[i + 1] - segment_starts[i]
        if length > 0:
            segment_lengths.append(length)

    if not segment_lengths:
        return float(len(timeline))

    return sum(segment_lengths) / len(segment_lengths)


def evaluate_segmentation(
    predicted_boundaries: list[float],
    reference_boundaries: list[float],
    event_timeline: list[float],
    collar_seconds: float = 300,
) -> dict:
    """Evaluate predicted task boundaries against reference boundaries.

    Computes both WindowDiff (sequence-level) and Collar-Based F1 (position-level)
    metrics. The event timeline is used to build binary boundary sequences for
    WindowDiff and to determine the window size k.

    Args:
        predicted_boundaries: predicted boundary timestamps (epoch seconds).
            These are the start timestamps of tasks (excluding the very first task).
        reference_boundaries: reference (ground-truth) boundary timestamps.
        event_timeline: sorted list of all event timestamps for the day.
        collar_seconds: tolerance for collar-based F1 (default 300 = 5 minutes).

    Returns:
        Dict with keys: windowdiff, precision, recall, f1, collar_seconds,
        n_ref_boundaries, n_pred_boundaries.
    """
    timeline = sorted(event_timeline)

    # Build binary sequences for WindowDiff
    ref_binary = _build_binary_sequence(reference_boundaries, timeline)
    hyp_binary = _build_binary_sequence(predicted_boundaries, timeline)

    # Window size k: half the average reference segment length (rounded, min 2)
    avg_seg = _average_segment_length(reference_boundaries, timeline)
    k = max(2, int(round(avg_seg / 2)))

    # Compute WindowDiff
    if len(ref_binary) == len(hyp_binary) and len(ref_binary) >= k:
        wd = windowdiff(ref_binary, hyp_binary, k)
    else:
        wd = 0.0

    # Compute Collar-Based F1
    f1_result = collar_f1(predicted_boundaries, reference_boundaries, collar_seconds)

    return {
        "windowdiff": wd,
        "window_k": k,
        "precision": f1_result["precision"],
        "recall": f1_result["recall"],
        "f1": f1_result["f1"],
        "tp": f1_result["tp"],
        "fp": f1_result["fp"],
        "fn": f1_result["fn"],
        "collar_seconds": collar_seconds,
        "n_ref_boundaries": len(reference_boundaries),
        "n_pred_boundaries": len(predicted_boundaries),
    }


def load_benchmark(fixture_path: str | None = None) -> dict:
    """Load the hand-labeled benchmark fixture.

    Args:
        fixture_path: path to the benchmark JSON. If None, uses the default
            path at tests/fixtures/eval_benchmark.json relative to this module.

    Returns:
        The benchmark dict with keys: date, session_files, reference_boundaries, etc.
    """
    if fixture_path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        fixture_path = os.path.join(here, "tests", "fixtures", "eval_benchmark.json")
    with open(fixture_path, encoding="utf-8") as f:
        benchmark = json.load(f)
    benchmark["_fixture_dir"] = os.path.dirname(os.path.abspath(fixture_path))
    return benchmark


def extract_reference_boundaries(benchmark: dict) -> list[float]:
    """Extract the list of reference boundary timestamps from the benchmark fixture."""
    return [b["timestamp"] for b in benchmark["reference_boundaries"]]


def extract_predicted_boundaries(tasks: list[dict]) -> list[float]:
    """Extract predicted boundary timestamps from segmented tasks.

    A predicted boundary is the start timestamp of each task EXCEPT the first
    (the first task starts at the beginning of the timeline, which is a session
    start, not a task boundary within the timeline).

    Args:
        tasks: list of task dicts from segment(), each with a "start" key.

    Returns:
        List of boundary timestamps (epoch seconds), sorted.
    """
    if not tasks:
        return []
    starts = sorted(t["start"] for t in tasks if t.get("start") is not None)
    # Drop the first — it's the session start, not a task boundary
    return starts[1:] if len(starts) > 1 else []


def load_benchmark_events(benchmark: dict) -> list[float]:
    """Load event timestamps from the benchmark's session files.

    Reads the JSONL session files listed in the benchmark, parses them via
    claude_code_adapter.parse_session, and returns a sorted list of all
    event timestamps that fall on the benchmark date.

    Args:
        benchmark: the benchmark dict from load_benchmark().

    Returns:
        Sorted list of epoch-second timestamps for all events on the benchmark date.
    """
    from claude_code_adapter import parse_session

    target_date = benchmark["date"]
    all_timestamps = []

    for session_path in benchmark["session_files"]:
        path = os.path.expanduser(session_path)
        if not os.path.isabs(path):
            path = os.path.join(benchmark.get("_fixture_dir", ""), path)
        if not os.path.exists(path):
            continue
        for ev in parse_session(path):
            ts = ev.get("timestamp")
            if ts is None:
                continue
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            if dt.strftime("%Y-%m-%d") == target_date:
                all_timestamps.append(ts)

    return sorted(all_timestamps)


def run_eval(benchmark_path: str | None = None, collar_seconds: float = 300,
             use_advanced: bool = True) -> dict:
    """Run the full evaluation: load benchmark, segment, evaluate.

    This is the function called by `python run.py --eval`.

    Args:
        benchmark_path: path to benchmark fixture (None = default).
        collar_seconds: collar tolerance for F1 (default 300s = 5 min).
        use_advanced: whether to use PELT/GMM segmentation (True) or naive (False).

    Returns:
        The evaluation metrics dict from evaluate_segmentation().
    """
    benchmark = load_benchmark(benchmark_path)
    ref_boundaries = extract_reference_boundaries(benchmark)
    timeline = load_benchmark_events(benchmark)

    if not timeline:
        # No session files found — return empty metrics
        return {
            "windowdiff": 0.0,
            "window_k": 0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "tp": 0, "fp": 0, "fn": 0,
            "collar_seconds": collar_seconds,
            "n_ref_boundaries": len(ref_boundaries),
            "n_pred_boundaries": 0,
            "note": "No session files found for the benchmark date.",
        }

    # Run segmentation on the benchmark's events
    from claude_code_adapter import parse_session
    from segment_tasks import segment

    target_date = benchmark["date"]
    events = []
    for session_path in benchmark["session_files"]:
        path = os.path.expanduser(session_path)
        if not os.path.isabs(path):
            path = os.path.join(benchmark.get("_fixture_dir", ""), path)
        if not os.path.exists(path):
            continue
        for ev in parse_session(path):
            ts = ev.get("timestamp")
            if ts is None:
                continue
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            if dt.strftime("%Y-%m-%d") == target_date:
                events.append(ev)

    tasks = segment(events, use_advanced=use_advanced)
    pred_boundaries = extract_predicted_boundaries(tasks)

    metrics = evaluate_segmentation(
        predicted_boundaries=pred_boundaries,
        reference_boundaries=ref_boundaries,
        event_timeline=timeline,
        collar_seconds=collar_seconds,
    )
    metrics["n_predicted_tasks"] = len(tasks)
    return metrics


def format_metrics_report(metrics: dict) -> str:
    """Format the metrics dict as a human-readable report string."""
    lines = [
        "# Segmentation Evaluation Report",
        "",
        f"  WindowDiff:     {metrics['windowdiff']:.4f}  (k={metrics.get('window_k', '?')})",
        f"  Precision:      {metrics['precision']:.4f}  ({metrics.get('tp', 0)} TP / {metrics.get('tp', 0) + metrics.get('fp', 0)} predicted)",
        f"  Recall:         {metrics['recall']:.4f}  ({metrics.get('tp', 0)} TP / {metrics.get('tp', 0) + metrics.get('fn', 0)} reference)",
        f"  F1:             {metrics['f1']:.4f}",
        f"  Collar:         {metrics['collar_seconds']}s",
        f"  Ref boundaries: {metrics['n_ref_boundaries']}",
        f"  Pred boundaries:{metrics['n_pred_boundaries']}",
    ]
    if "n_predicted_tasks" in metrics:
        lines.append(f"  Pred tasks:     {metrics['n_predicted_tasks']}")
    if "note" in metrics:
        lines.append(f"  Note:           {metrics['note']}")
    return "\n".join(lines)
