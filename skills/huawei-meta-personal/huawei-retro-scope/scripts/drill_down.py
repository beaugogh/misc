"""Drill-down & root-cause analysis for individual tasks (Phase 10.2).

Takes a single task dict (the output of ``segment_tasks.segment()``) and produces a
multi-resolution stage-by-stage breakdown that answers "what exactly got stuck in
this task?"

Three main entry points:

- ``detect_stages(task)`` — splits a task's events into sub-stages using PELT (when
  available) or a heuristic fallback (cwd shift, tool-cluster change, user
  correction, >10min gap).
- ``detect_markers(events)`` — scans events for error clusters, retry loops, user
  corrections, and time-sink signals.
- ``drill_down(task)`` — ties it together: stages + markers + a generated narrative.

This module is a pure post-processor. It takes task/event dicts and returns dicts —
no side effects, no file I/O. It does NOT modify the task passed to it.
"""

from __future__ import annotations

import hashlib
import logging
import re
from collections import Counter
from typing import Any

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants — mirror advanced_segment.py's thresholds where applicable.
# ---------------------------------------------------------------------------

# Minimum events for PELT to be meaningful (same as advanced_segment.py).
MIN_EVENTS_FOR_PELT = 20
# Maximum events for PELT — beyond this it's too slow.
MAX_EVENTS_FOR_PELT = 5000

# PELT penalty for stage detection — LOWER than task-boundary penalty because
# stages are finer-grained than tasks. The task-boundary penalty in
# advanced_segment.py is ``10 * n_features``; we use ``2 * n_features``.
STAGE_PELT_PENALTY_FACTOR = 2

# Heuristic fallback thresholds.
GAP_THRESHOLD_SECONDS = 10 * 60  # 10 min gap => new stage (lower than task's 30min)

# User-correction signal keywords (English + Chinese).
# Curated to exclude ambiguous bare words that are common in non-correction
# contexts (e.g. "fix" in task instructions, "wait" in patience phrases,
# "actually" in confirmations, "should be" in statements).
_CORRECTION_SIGNALS = [
    # English — strong correction signals only
    "no,", "wrong", "not right", "incorrect", "didn't", "did not",
    "instead", "not what i asked",
    # Chinese — true corrections only (removed continuation words 再/另外/还有/改/重新/不是)
    "不对", "错了", "又错", "不要",
]

# Retry-loop window: same tool+similar input within this window = retry.
RETRY_WINDOW_SECONDS = 5 * 60  # 5 min

# Time-sink thresholds.
TIME_SINK_MIN_DURATION = 10 * 60  # 10 min
TIME_SINK_IDLE_RATIO = 0.3  # active/wall < 0.3 = idle/stuck

# Narrative thresholds — only generate detailed narrative for substantial tasks.
NARRATIVE_ACTIVE_THRESHOLD = 2 * 3600  # 2h active
NARRATIVE_WALL_THRESHOLD = 4 * 3600  # 4h wall


# ---------------------------------------------------------------------------
# Imports — conditional, same pattern as advanced_segment.py.
# ---------------------------------------------------------------------------

def _try_import_ruptures():
    """Return the ruptures module or None if unavailable."""
    try:
        import ruptures
        return ruptures
    except ImportError:
        return None


def _try_import_numpy():
    """Return the numpy module or None if unavailable."""
    try:
        import numpy
        return numpy
    except ImportError:
        return None


# ---------------------------------------------------------------------------
# Active-seconds computation (mirrors segment_tasks._compute_active_seconds
# but standalone so we don't import from segment_tasks — pure function).
# ---------------------------------------------------------------------------

def _compute_active_seconds(events: list[dict], gap_threshold: float = 30 * 60) -> float:
    """Estimate active work time using interval union with 5-min collars."""
    ACTIVE_COLLAR = 5 * 60
    ts_list = sorted(e["timestamp"] for e in events if e.get("timestamp") is not None)
    if not ts_list:
        return 0.0
    wall_clock = ts_list[-1] - ts_list[0]
    intervals = [(max(0, t - ACTIVE_COLLAR), t + ACTIVE_COLLAR) for t in ts_list]
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + gap_threshold:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    active = sum(end - start for start, end in merged)
    if wall_clock > 0:
        return min(active, wall_clock)
    return active


# ---------------------------------------------------------------------------
# Task 10.2.1: Stage detection within a task
# ---------------------------------------------------------------------------

def detect_stages(task: dict) -> list[dict]:
    """Split a task's events into sub-stages.

    Uses PELT (ruptures) on the task's events when available and the task has
    enough events (>= ``MIN_EVENTS_FOR_PELT``). Otherwise falls back to a
    heuristic that splits on:

    - (a) cwd shift,
    - (b) tool-cluster change (different primary tool),
    - (c) user correction (user_message containing correction signals),
    - (d) >10min gap between consecutive events.

    Each stage dict has the shape::

        {
            "stage_idx": int,
            "start": float,
            "end": float,
            "duration_seconds": float,
            "active_seconds": float,
            "event_count": int,
            "tool_names": list[str],
            "summary": str,
            "markers": list[dict],
        }
    """
    events = task.get("events") or []
    if not events:
        return []

    # Ensure events are sorted by timestamp.
    events = sorted(events, key=lambda e: e.get("timestamp") or 0.0)

    # Decide which method to use.
    ruptures = _try_import_ruptures()
    numpy = _try_import_numpy()
    use_pelt = (
        ruptures is not None
        and numpy is not None
        and MIN_EVENTS_FOR_PELT <= len(events) <= MAX_EVENTS_FOR_PELT
    )

    if use_pelt:
        boundary_indices = _pelt_stage_boundaries(events, ruptures, numpy)
    else:
        boundary_indices = _heuristic_stage_boundaries(events)

    # Build stage event slices from boundary indices.
    # boundary_indices are START indices of new stages (0 is implicit).
    cuts = sorted(set(boundary_indices) | {0, len(events)})
    stages: list[dict] = []
    for si in range(len(cuts) - 1):
        start_idx = cuts[si]
        end_idx = cuts[si + 1]
        stage_events = events[start_idx:end_idx]
        if not stage_events:
            continue
        stages.append(_build_stage(stage_events, si))

    # If PELT/heuristic produced only 1 stage and the task is large, try the
    # heuristic as a secondary fallback to ensure we don't miss obvious shifts.
    if len(stages) <= 1 and len(events) > 5:
        boundary_indices = _heuristic_stage_boundaries(events)
        if boundary_indices:
            cuts = sorted(set(boundary_indices) | {0, len(events)})
            stages = []
            for si in range(len(cuts) - 1):
                start_idx = cuts[si]
                end_idx = cuts[si + 1]
                stage_events = events[start_idx:end_idx]
                if not stage_events:
                    continue
                stages.append(_build_stage(stage_events, si))

    # Attach markers to each stage.
    for stage in stages:
        stage_events = _get_stage_events(events, stage)
        stage["markers"] = detect_markers(stage_events)

    return stages


def _pelt_stage_boundaries(
    events: list[dict], ruptures, numpy
) -> list[int]:
    """Detect stage boundaries using PELT on multivariate features.

    Features per event: normalized timestamp, one-hot of kind, one-hot of
    tool_name. Uses a LOWER penalty than task-boundary detection (stages are
    finer than tasks).
    """
    kinds = sorted({e.get("kind") or "?" for e in events})
    kind_idx = {k: i for i, k in enumerate(kinds)}
    tool_names = sorted({e.get("tool_name") or "" for e in events})
    tool_idx = {t: i for i, t in enumerate(tool_names)}
    cwds = sorted({e.get("cwd") or "" for e in events})
    cwd_idx = {c: i for i, c in enumerate(cwds)}

    n_features = 1 + len(kinds) + len(tool_names) + len(cwds)
    signals = numpy.zeros((len(events), n_features))

    ts_list = [e.get("timestamp", 0) for e in events]
    ts_min, ts_max = min(ts_list), max(ts_list)
    ts_range = ts_max - ts_min or 1

    for i, e in enumerate(events):
        signals[i, 0] = (e.get("timestamp", 0) - ts_min) / ts_range
        k = kind_idx.get(e.get("kind", "?"), 0)
        if k < len(kinds):
            signals[i, 1 + k] = 1
        t = tool_idx.get(e.get("tool_name", ""), 0)
        if t < len(tool_names):
            signals[i, 1 + len(kinds) + t] = 1
        c = cwd_idx.get(e.get("cwd", ""), 0)
        if c < len(cwds):
            signals[i, 1 + len(kinds) + len(tool_names) + c] = 1

    try:
        algo = ruptures.Pelt(model="l2", min_size=3).fit(signals)
        penalty = STAGE_PELT_PENALTY_FACTOR * n_features
        change_points = algo.predict(pen=penalty)
        # ruptures returns END of each segment; convert to start-of-new-stage.
        boundaries = [cp for cp in change_points if 0 < cp < len(events)]
        return boundaries
    except Exception as e:
        log.debug(f"PELT stage detection failed: {e}, falling back to heuristic")
        return _heuristic_stage_boundaries(events)


def _heuristic_stage_boundaries(events: list[dict]) -> list[int]:
    """Detect stage boundaries using simple heuristics.

    Splits on: cwd shift, tool-cluster change, user correction, >10min gap.
    """
    boundaries: list[int] = []
    last_ts: float | None = None
    last_cwd: str | None = None
    # Track the dominant tool in the current cluster.
    current_tool_cluster: Counter = Counter()

    for i, ev in enumerate(events):
        ts = ev.get("timestamp")
        is_boundary = False

        if i > 0 and last_ts is not None and ts is not None:
            # (d) >10min gap
            if ts - last_ts > GAP_THRESHOLD_SECONDS:
                is_boundary = True

        # (a) cwd shift
        if i > 0 and ev.get("cwd") and last_cwd and ev.get("cwd") != last_cwd:
            is_boundary = True

        # (c) user correction
        if ev.get("kind") == "user_message" and _is_correction_text(ev.get("text")):
            # A correction starts a new stage (the redirect).
            if i > 0:
                is_boundary = True

        # (b) tool-cluster change — detect when the primary tool shifts.
        if ev.get("kind") == "tool_use" and ev.get("tool_name"):
            current_tool_cluster[ev["tool_name"]] += 1
            # Check every few tool calls if the dominant tool has changed.
            if i > 0 and sum(current_tool_cluster.values()) >= 3:
                dominant = current_tool_cluster.most_common(1)[0][0]
                # If this event's tool is different from the dominant and the
                # dominant has >3 occurrences, it might be a shift.
                # We check: has the dominant tool changed from the previous dominant?
                # Simple approach: if the last 3 tool_uses are a different tool
                # than the most common so far, split.
                pass  # handled by the cluster-change check below

        if is_boundary:
            boundaries.append(i)

        if ts is not None:
            last_ts = ts
        if ev.get("cwd"):
            last_cwd = ev.get("cwd")

    # (b) Tool-cluster change — post-process: look for shifts in the primary tool.
    boundaries.extend(_detect_tool_cluster_shifts(events))
    # Deduplicate and sort.
    boundaries = sorted(set(boundaries))
    # Remove 0 (it's the implicit start).
    boundaries = [b for b in boundaries if b > 0]
    return boundaries


def _detect_tool_cluster_shifts(events: list[dict]) -> list[int]:
    """Detect boundaries where the primary tool changes between windows.

    Uses a sliding window approach: compare the dominant tool in the current
    window vs the previous window. If they differ, emit a boundary.
    """
    boundaries: list[int] = []
    tool_uses = [(i, e.get("tool_name")) for i, e in enumerate(events)
                 if e.get("kind") == "tool_use" and e.get("tool_name")]
    if len(tool_uses) < 6:
        return boundaries

    window_size = max(3, len(tool_uses) // 6)
    prev_dominant: str | None = None
    for w_start in range(0, len(tool_uses), window_size):
        w_end = min(w_start + window_size, len(tool_uses))
        window_tools = [t for _, t in tool_uses[w_start:w_end]]
        if not window_tools:
            continue
        dominant = Counter(window_tools).most_common(1)[0][0]
        if prev_dominant is not None and dominant != prev_dominant:
            # Boundary at the event index where the new window starts.
            event_idx = tool_uses[w_start][0]
            if event_idx > 0:
                boundaries.append(event_idx)
        prev_dominant = dominant

    return boundaries


def _is_correction_text(text: str | None) -> bool:
    """Check if a user message text contains correction signals.

    Uses word-boundary matching to avoid false positives from bare substrings
    (e.g. "fix" in "fix the typo", "wait" in "please wait"). Additionally
    requires the correction keyword to appear near the START of the message
    (first 5 words) OR be the first sentence — real corrections lead with
    the signal ("no, do X instead", "wrong, that's not right").
    """
    if not text:
        return False
    t = text.strip().lower()

    # Extract the lead portion: first 5 words OR first sentence (whichever
    # covers less), so we only match correction signals at the start.
    # Split into sentences using a simple heuristic.
    first_sentence = re.split(r'[.!?]\s', t, maxsplit=1)[0].strip()
    first_words = first_sentence.split()[:5]
    lead = ' '.join(first_words)

    # Also include the full first sentence for Chinese (where word-splitting
    # on spaces doesn't work). Use the first ~20 chars as the "lead" for
    # Chinese text.
    lead_chinese = first_sentence[:20]

    for sig in _CORRECTION_SIGNALS:
        # Word-boundary matching for English keywords.
        if re.search(r'\b' + re.escape(sig) + r'\b', lead):
            return True
        # For Chinese keywords, check if the signal appears in the lead portion.
        # Chinese doesn't use word boundaries, so substring check in the lead
        # is appropriate.
        if sig in lead_chinese:
            return True
    return False


def _build_stage(stage_events: list[dict], stage_idx: int) -> dict:
    """Build a stage dict from its events."""
    ts = [e["timestamp"] for e in stage_events if e.get("timestamp") is not None]
    start = min(ts) if ts else 0.0
    end = max(ts) if ts else 0.0
    duration = end - start if end >= start else 0.0
    active = _compute_active_seconds(stage_events)
    tool_uses = [e for e in stage_events if e.get("kind") == "tool_use"]
    tool_names = sorted({e.get("tool_name") for e in tool_uses if e.get("tool_name")})
    summary = _generate_stage_summary(stage_events, tool_names)
    return {
        "stage_idx": stage_idx,
        "start": start,
        "end": end,
        "duration_seconds": round(duration, 1),
        "active_seconds": round(active, 1),
        "event_count": len(stage_events),
        "tool_names": tool_names,
        "summary": summary,
        "markers": [],  # populated by detect_stages() after building all stages
    }


def _generate_stage_summary(stage_events: list[dict], tool_names: list[str]) -> str:
    """Generate a one-line description of a stage.

    Uses the dominant tool + first user message or primary file target.
    Examples: "Edit cluster on segment_tasks.py" or "WebSearch for 'pelt penalty tuning'"
    """
    # Find the dominant tool.
    tool_counter = Counter(
        e.get("tool_name") for e in stage_events
        if e.get("kind") == "tool_use" and e.get("tool_name")
    )
    dominant_tool = tool_counter.most_common(1)[0][0] if tool_counter else None

    # Find the first user message in the stage.
    first_user_msg = None
    for e in stage_events:
        if e.get("kind") == "user_message" and e.get("text"):
            first_user_msg = e["text"].strip().replace("\n", " ")
            if len(first_user_msg) > 80:
                first_user_msg = first_user_msg[:80] + "..."
            break

    # Find the primary file target from tool inputs.
    file_target = None
    for e in stage_events:
        if e.get("kind") != "tool_use":
            continue
        ti = e.get("tool_input") or {}
        fp = ti.get("file_path")
        if fp:
            file_target = fp
            break

    # Find search query.
    search_query = None
    for e in stage_events:
        if e.get("kind") != "tool_use":
            continue
        ti = e.get("tool_input") or {}
        q = ti.get("query")
        if q:
            search_query = q
            break

    # Build summary.
    if dominant_tool and file_target:
        # Shorten the file path to basename.
        import os
        basename = os.path.basename(file_target)
        return f"{dominant_tool} cluster on {basename}"
    elif dominant_tool == "WebSearch" and search_query:
        return f"WebSearch for '{search_query[:60]}'"
    elif dominant_tool and first_user_msg:
        return f"{dominant_tool} — {first_user_msg}"
    elif dominant_tool:
        return f"{dominant_tool} cluster"
    elif first_user_msg:
        return first_user_msg
    else:
        return "(no activity)"


def _get_stage_events(all_events: list[dict], stage: dict) -> list[dict]:
    """Extract the events belonging to a stage from the full event list."""
    start = stage["start"]
    end = stage["end"]
    return [
        e for e in all_events
        if start <= (e.get("timestamp") or 0) <= end
    ]


# ---------------------------------------------------------------------------
# Task 10.2.2: Root-cause markers
# ---------------------------------------------------------------------------

def detect_markers(events: list[dict]) -> list[dict]:
    """Scan a list of events for root-cause markers.

    Detects:
    - **Error clusters:** N consecutive (>=2) tool_result events with
      ``tool_is_error=True``.
    - **Retry loops:** same ``tool_name`` + similar ``tool_input`` attempted
      >1x within 5 min.
    - **User corrections:** a ``user_message`` event whose text contains
      correction signals.
    - **Time sinks:** computed at the stage level (not here) — but if called
      on a stage's events, this function does NOT produce time-sink markers
      (those require stage-level duration/active comparison). Time-sink
      markers are added by ``_add_time_sink_markers()`` in ``detect_stages()``.

    Returns a list of marker dicts.
    """
    markers: list[dict] = []
    markers.extend(_detect_error_clusters(events))
    markers.extend(_detect_retry_loops(events))
    markers.extend(_detect_user_corrections(events))
    return markers


def _detect_error_clusters(events: list[dict]) -> list[dict]:
    """Detect consecutive (>=2) tool_result events with is_error=True."""
    markers: list[dict] = []
    # We need to find runs of consecutive error tool_results.
    # "Consecutive" means adjacent tool_result events (ignoring non-tool_result
    # events in between? No — the spec says "N consecutive tool_result events").
    # We look at tool_result events in order and find runs of is_error=True.
    tool_results = [
        (i, e) for i, e in enumerate(events)
        if e.get("kind") == "tool_result"
    ]

    if len(tool_results) < 2:
        return markers

    current_run: list[tuple[int, dict]] = []
    for idx, ev in tool_results:
        if ev.get("tool_is_error") is True:
            current_run.append((idx, ev))
        else:
            if len(current_run) >= 2:
                markers.append(_make_error_cluster_marker(current_run, events))
            current_run = []
    # Handle trailing run.
    if len(current_run) >= 2:
        markers.append(_make_error_cluster_marker(current_run, events))

    return markers


def _make_error_cluster_marker(
    run: list[tuple[int, dict]], all_events: list[dict]
) -> dict:
    """Build an error_cluster marker from a run of consecutive error results."""
    count = len(run)
    # Get the tools that produced these errors — look at the tool_use that
    # corresponds to each tool_result via tool_use_id.
    tools: list[str] = []
    for _, ev in run:
        tuid = ev.get("tool_use_id")
        if tuid:
            for e in all_events:
                if (e.get("kind") == "tool_use"
                        and e.get("tool_use_id") == tuid
                        and e.get("tool_name")):
                    tools.append(e["tool_name"])
                    break
    # Fallback: use tool_name on the result itself if present.
    if not tools:
        for _, ev in run:
            if ev.get("tool_name"):
                tools.append(ev["tool_name"])
    tool_str = tools[0] if tools else "unknown"
    if len(set(tools)) > 1:
        tool_str = "/".join(sorted(set(tools)))

    ts = run[0][1].get("timestamp", 0.0)
    return {
        "type": "error_cluster",
        "start": ts,
        "count": count,
        "tools": sorted(set(tools)) if tools else [],
        "message": f"{count} consecutive errors on {tool_str}",
    }


def _detect_retry_loops(events: list[dict]) -> list[dict]:
    """Detect same tool_name + similar tool_input attempted >1x within 5 min.

    Read tool_use events are excluded from retry detection (re-reading a file
    is a normal reference lookup, not a retry). For all other tools, a retry
    is flagged when the same tool+target is attempted >=2 times within 5 min
    (for identical operations) or >=3 times (for the same tool on the same
    target with different content).
    """
    markers: list[dict] = []
    retry_window = RETRY_WINDOW_SECONDS

    # Collect tool_use events with their identifying info.
    # target_key is None for Read (excluded from retry detection).
    tool_uses: list[tuple[int, dict, str, str]] = []  # (idx, ev, tool_name, target_key)
    for i, e in enumerate(events):
        if e.get("kind") != "tool_use" or not e.get("tool_name"):
            continue
        tool_name = e["tool_name"]
        target_key = _extract_retry_target(e)
        if target_key is not None:
            tool_uses.append((i, e, tool_name, target_key))

    # Group by (tool_name, target_key) and check for retries within the window.
    groups: dict[tuple[str, str], list[tuple[int, dict]]] = {}
    for idx, ev, tool_name, target_key in tool_uses:
        key = (tool_name, target_key)
        groups.setdefault(key, []).append((idx, ev))

    for (tool_name, target_key), occurrences in groups.items():
        if len(occurrences) < 2:
            continue
        # Sort by timestamp.
        occurrences.sort(key=lambda x: x[1].get("timestamp", 0.0))
        # Find clusters within the retry window.
        cluster_start = 0
        for j in range(1, len(occurrences)):
            ts_prev = occurrences[j - 1][1].get("timestamp", 0.0)
            ts_curr = occurrences[j][1].get("timestamp", 0.0)
            if ts_curr - ts_prev <= retry_window:
                # Part of the same retry cluster — continue.
                continue
            else:
                # Cluster boundary — check if the completed cluster has >1.
                cluster_len = j - cluster_start
                if cluster_len >= 2:
                    markers.append(_make_retry_marker(
                        tool_name, target_key, cluster_len,
                        occurrences[cluster_start][1]
                    ))
                cluster_start = j
        # Handle trailing cluster.
        cluster_len = len(occurrences) - cluster_start
        if cluster_len >= 2:
            markers.append(_make_retry_marker(
                tool_name, target_key, cluster_len,
                occurrences[cluster_start][1]
            ))

    return markers


def _extract_retry_target(ev: dict) -> str | None:
    """Extract a 'target' key from a tool_use event for retry detection.

    For Edit: file_path + hash of old_string+new_string, so distinct edits on
        the same file are NOT grouped as retries.
    For Write: file_path + hash of content, so a retry writes the same content.
    For Read: returns None — re-reading a file is a normal reference lookup,
        not a retry.
    For NotebookEdit: file_path + hash of old_string+new_string (same as Edit).
    For Bash: the command (first 100 chars).
    For WebSearch: the query.
    For WebFetch: the url.
    For Grep: the pattern.
    For others: stringified tool_input (first 100 chars).
    """
    ti = ev.get("tool_input") or {}
    name = ev.get("tool_name") or ""

    if name == "Edit" and ti.get("file_path"):
        old_str = str(ti.get("old_string", ""))
        new_str = str(ti.get("new_string", ""))
        content_hash = hashlib.md5((old_str + new_str).encode()).hexdigest()[:8]
        return f"{ti['file_path']}#{content_hash}"

    if name == "Write" and ti.get("file_path"):
        content = str(ti.get("content", ""))
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{ti['file_path']}#{content_hash}"

    if name == "Read":
        # Re-reading a file is a normal reference lookup, not a retry.
        return None

    if name == "NotebookEdit" and ti.get("notebook_path"):
        old_str = str(ti.get("old_string", ""))
        new_str = str(ti.get("new_string", ""))
        content_hash = hashlib.md5((old_str + new_str).encode()).hexdigest()[:8]
        return f"{ti['notebook_path']}#{content_hash}"

    if name == "Bash" and ti.get("command"):
        return str(ti["command"])[:100]

    if name == "WebSearch" and ti.get("query"):
        return ti["query"]

    if name == "WebFetch" and ti.get("url"):
        return ti["url"]

    if name == "Grep" and ti.get("pattern"):
        return ti["pattern"]

    # Generic fallback.
    return str(ti)[:100]


def _make_retry_marker(
    tool_name: str, target: str, count: int, first_ev: dict
) -> dict:
    """Build a retry_loop marker."""
    # Shorten the target for the message.
    import os
    display = target
    if "/" in display or "\\" in display:
        display = os.path.basename(display)
    if len(display) > 60:
        display = display[:60] + "..."
    ts = first_ev.get("timestamp", 0.0)
    return {
        "type": "retry_loop",
        "tool": tool_name,
        "start": ts,
        "count": count,
        "target": target,
        "message": f"Retried {tool_name} {count}x on {display}",
    }


def _detect_user_corrections(events: list[dict]) -> list[dict]:
    """Detect user messages that contain correction signals."""
    markers: list[dict] = []
    for ev in events:
        if ev.get("kind") != "user_message":
            continue
        text = ev.get("text")
        if not text:
            continue
        if _is_correction_text(text):
            snippet = text.strip().replace("\n", " ")[:100]
            ts = ev.get("timestamp", 0.0)
            markers.append({
                "type": "user_correction",
                "ts": ts,
                "snippet": snippet,
                "message": f"User corrected direction: {snippet}",
            })
    return markers


def _add_time_sink_markers(stages: list[dict], all_stages: list[dict]) -> None:
    """Add time-sink markers to stages based on duration/active ratios.

    - ``time_sink_idle``: duration > 10min AND active/wall ratio < 0.3 = stuck/idle.
    - ``time_sink_hard``: active_seconds in the top quartile of all stages = genuinely hard work.

    Modifies stages in place (appends to ``markers`` list).
    """
    if not all_stages:
        return

    # Compute the top-quartile threshold for active_seconds.
    active_values = sorted(s.get("active_seconds", 0) for s in all_stages)
    if active_values:
        q3_idx = int(len(active_values) * 0.75)
        q3_threshold = active_values[q3_idx] if q3_idx < len(active_values) else active_values[-1]
    else:
        q3_threshold = 0

    for stage in all_stages:
        duration = stage.get("duration_seconds", 0)
        active = stage.get("active_seconds", 0)
        ratio = active / duration if duration > 0 else 1.0

        # Idle/stuck: high wall, low active.
        if duration > TIME_SINK_MIN_DURATION and ratio < TIME_SINK_IDLE_RATIO:
            stage["markers"].append({
                "type": "time_sink_idle",
                "stage_idx": stage.get("stage_idx", 0),
                "duration_seconds": duration,
                "active_seconds": active,
                "ratio": round(ratio, 2),
                "message": (
                    f"Stage {stage.get('stage_idx', 0)+1} idle/stuck: "
                    f"{duration/60:.0f}min wall, {active/60:.0f}min active "
                    f"(ratio {ratio:.2f})"
                ),
            })

        # Genuinely hard: top quartile active time.
        if active > 0 and active >= q3_threshold and len(all_stages) >= 4:
            stage["markers"].append({
                "type": "time_sink_hard",
                "stage_idx": stage.get("stage_idx", 0),
                "active_seconds": active,
                "message": (
                    f"Stage {stage.get('stage_idx', 0)+1} is genuinely hard work: "
                    f"{active/60:.0f}min active (top quartile)"
                ),
            })


# ---------------------------------------------------------------------------
# Task 10.2.3: Narrative generation
# ---------------------------------------------------------------------------

def generate_narrative(task: dict, stages: list[dict]) -> str:
    """Produce a human-readable root-cause narrative.

    Only generates a detailed narrative for tasks with >2h active time or >4h
    wall time. For smaller tasks, returns a simpler summary.

    The narrative connects stages and markers into a story, kept under 5
    sentences. If no markers, says "No stuck points detected."
    """
    active = task.get("active_seconds") or 0
    wall = task.get("duration_seconds") or task.get("wall_clock_seconds") or 0

    is_long = active > NARRATIVE_ACTIVE_THRESHOLD or wall > NARRATIVE_WALL_THRESHOLD

    # Collect all markers across stages.
    all_markers: list[dict] = []
    for s in stages:
        all_markers.extend(s.get("markers", []))

    if not stages:
        # No stages — can't generate a narrative.
        if not all_markers:
            return "No stuck points detected — steady progression through 0 stages."
        # Shouldn't happen, but handle gracefully.
        return f"Task had {len(all_markers)} marker(s) but no stages detected."

    n_stages = len(stages)

    if not all_markers:
        return f"No stuck points detected — steady progression through {n_stages} stage(s)."

    # Build the narrative.
    sentences: list[str] = []

    # Sentence 1: overall summary.
    active_h = active / 3600
    wall_h = wall / 3600
    if is_long:
        sentences.append(
            f"This task took {active_h:.1f}h active ({wall_h:.1f}h wall) "
            f"across {n_stages} stages."
        )
    else:
        sentences.append(
            f"Task across {n_stages} stage(s) "
            f"({active/60:.0f}min active, {wall/60:.0f}min wall)."
        )

    # Sentence 2+: describe markers in stage context.
    error_clusters = [m for m in all_markers if m["type"] == "error_cluster"]
    retry_loops = [m for m in all_markers if m["type"] == "retry_loop"]
    corrections = [m for m in all_markers if m["type"] == "user_correction"]
    idle_sinks = [m for m in all_markers if m["type"] == "time_sink_idle"]
    hard_sinks = [m for m in all_markers if m["type"] == "time_sink_hard"]

    fragments: list[str] = []

    if error_clusters:
        # Find which stage each error cluster belongs to.
        parts: list[str] = []
        for ec in error_clusters:
            stage_idx = _find_stage_for_marker(ec, stages)
            stage_ref = f"stage {stage_idx+1}" if stage_idx is not None else "the task"
            parts.append(f"{stage_ref} hit {ec['count']} consecutive errors on {ec.get('tools', ['unknown'])[0] if ec.get('tools') else 'unknown'}")
        fragments.append(", then ".join(parts) if len(parts) > 1 else parts[0])

    if retry_loops:
        parts = []
        for rl in retry_loops:
            stage_idx = _find_stage_for_marker(rl, stages)
            stage_ref = f"stage {stage_idx+1}" if stage_idx is not None else "the task"
            parts.append(f"{stage_ref} retried {rl['tool']} {rl['count']}x")
        fragments.append(", then ".join(parts) if len(parts) > 1 else parts[0])

    if corrections:
        parts = []
        for uc in corrections:
            stage_idx = _find_stage_for_marker(uc, stages)
            stage_ref = f"stage {stage_idx+1}" if stage_idx is not None else "the task"
            snippet = uc.get("snippet", "")[:50]
            parts.append(f"a user correction in {stage_ref} redirected ({snippet}...)")
        fragments.append(", then ".join(parts) if len(parts) > 1 else parts[0])

    if idle_sinks:
        parts = []
        for ts in idle_sinks:
            stage_idx = ts.get("stage_idx", 0)
            parts.append(f"stage {stage_idx+1} was stuck/idle ({ts['duration_seconds']/60:.0f}min wall, {ts['active_seconds']/60:.0f}min active)")
        fragments.append(", then ".join(parts) if len(parts) > 1 else parts[0])

    if hard_sinks:
        parts = []
        for ts in hard_sinks:
            stage_idx = ts.get("stage_idx", 0)
            parts.append(f"stage {stage_idx+1} was genuinely hard work ({ts['active_seconds']/60:.0f}min active)")
        fragments.append(", then ".join(parts) if len(parts) > 1 else parts[0])

    if fragments:
        sentences.append(", and ".join(fragments) + ".")

    # Final sentence: which stage succeeded (if identifiable).
    # The last stage with no error markers is the "success" stage.
    if stages:
        last_stage = stages[-1]
        last_stage_markers = last_stage.get("markers", [])
        has_errors = any(m["type"] in ("error_cluster", "retry_loop") for m in last_stage_markers)
        if not has_errors:
            last_duration = last_stage.get("duration_seconds", 0)
            if last_duration > 0:
                sentences.append(
                    f"Stage {len(stages)} completed in {last_duration/60:.0f}min."
                )

    # Cap at 5 sentences.
    return " ".join(sentences[:5])


def _find_stage_for_marker(marker: dict, stages: list[dict]) -> int | None:
    """Find which stage index a marker belongs to based on its timestamp."""
    marker_ts = marker.get("start") or marker.get("ts") or 0.0
    for s in stages:
        if s["start"] <= marker_ts <= s["end"]:
            return s.get("stage_idx", 0)
    return None


# ---------------------------------------------------------------------------
# Task 10.2.4: Top-level function
# ---------------------------------------------------------------------------

def drill_down(task: dict) -> dict:
    """Produce a full drill-down analysis for a single task.

    Calls ``detect_stages()``, attaches markers (including time-sink markers
    that require cross-stage comparison), generates a narrative, and returns:

    ::

        {
            "task_subject": str,
            "total_active_seconds": float,
            "total_wall_seconds": float,
            "stages": list[dict],
            "all_markers": list[dict],
            "narrative": str,
        }
    """
    # Detect stages (this also attaches per-stage markers).
    stages = detect_stages(task)

    # Add time-sink markers (requires cross-stage comparison).
    _add_time_sink_markers(stages, stages)

    # Collect all markers.
    all_markers: list[dict] = []
    for s in stages:
        all_markers.extend(s.get("markers", []))

    # Generate narrative.
    narrative = generate_narrative(task, stages)

    return {
        "task_subject": task.get("subject") or "(no subject)",
        "total_active_seconds": task.get("active_seconds") or 0.0,
        "total_wall_seconds": task.get("duration_seconds")
            or task.get("wall_clock_seconds") or 0.0,
        "stages": stages,
        "all_markers": all_markers,
        "narrative": narrative,
    }
