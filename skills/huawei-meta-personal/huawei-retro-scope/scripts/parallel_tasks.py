"""Parallel-task detection and exclusive-time computation.

Post-processor for ``segment()``: takes the flat, non-overlapping task list and
refines it into a model that permits overlapping intervals.

The current ``segment()`` output assumes tasks are sequential — each event belongs
to exactly one task, and tasks are ordered by start time.  Real AI-assisted work
is not sequential:

  - A background sub-agent (``TaskCreate`` / ``TaskOutput`` / ``TaskStop``) runs
    while the foreground session continues — two tasks, overlapping in time.
  - Two AI-session JSONL files with overlapping timestamp ranges = two parallel
    work streams (e.g. one on a server, one locally).
  - A ``browser`` visit during an ``ai_session`` coding task = the person
    researching in the foreground while the agent codes in the background.

This module splits the flat task list into *threads* (``thread_id``) and computes
*exclusive time* — the union of all task intervals, with no double-counting.

Public API
----------
    detect_parallel_tasks(tasks, events) -> list[dict]
    compute_exclusive_time(tasks) -> dict
"""

from __future__ import annotations

# Tool names that mark the lifecycle of a background sub-agent task.
# TaskCreate spawns the agent; TaskOutput polls/receives output; TaskStop ends it.
BACKGROUND_LIFECYCLE_TOOLS = frozenset({"TaskCreate", "TaskOutput", "TaskStop"})


# ---------------------------------------------------------------------------
# 10.1.1 + 10.1.2  Parallel-task detection
# ---------------------------------------------------------------------------

def detect_parallel_tasks(tasks: list[dict], events: list[dict]) -> list[dict]:
    """Refine a flat task list into overlapping intervals tagged with ``thread_id``.

    Parameters
    ----------
    tasks : list[dict]
        Output of ``segment()`` — non-overlapping task dicts.
    events : list[dict]
        The normalized events that produced *tasks* (same list passed to
        ``segment()``).  Used to identify background-task boundaries and
        interleave foreground/background streams.

    Returns
    -------
    list[dict]
        A new list of task dicts.  Each task gains a ``thread_id`` field:
          - ``"foreground"`` — the default for tasks with no parallel overlap.
          - ``"background:<tool_use_id>"`` — a background sub-agent task.
          - ``"session:<session_id>"`` — a concurrent AI session.
          - ``"browser"`` — a browser-research task split from a coding task.

        The returned list may contain *more* tasks than the input (background
        and browser splits create new task dicts) and task intervals may
        overlap.

        Tasks that don't overlap anything keep ``thread_id="foreground"``.
    """
    if not tasks:
        return []
    if not events:
        # No events to analyze for parallelism — tag everything as foreground.
        for t in tasks:
            t = dict(t)
            t["thread_id"] = "foreground"
        return [dict(t, thread_id="foreground") for t in tasks]

    # Work on copies so we never mutate the caller's dicts.
    refined: list[dict] = [dict(t) for t in tasks]

    # ------------------------------------------------------------------
    # Signal 1: Background sub-agent tasks (TaskCreate / TaskStop lifecycle)
    # ------------------------------------------------------------------
    background_tasks = _detect_background_tasks(events, refined)

    # ------------------------------------------------------------------
    # Signal 2: Concurrent sessions (overlapping timestamp ranges)
    # ------------------------------------------------------------------
    _tag_concurrent_sessions(refined)

    # ------------------------------------------------------------------
    # Signal 3: Browser visits during an ai_session coding task
    # ------------------------------------------------------------------
    browser_tasks = _detect_browser_during_coding(events, refined)

    # Merge: original tasks (with thread_id) + new background + browser tasks.
    result = refined + background_tasks + browser_tasks

    # Ensure every task has a thread_id (default = foreground).
    for t in result:
        t.setdefault("thread_id", "foreground")

    # Sort by start time for readability.
    result.sort(key=lambda t: (t.get("start") or 0.0, t.get("thread_id") or ""))
    return result


def _detect_background_tasks(events: list[dict], refined: list[dict]) -> list[dict]:
    """Split background sub-agent tasks from the foreground stream.

    Looks for ``TaskCreate`` / ``TaskStop`` (or ``TaskOutput`` as a fallback
    end marker) tool calls.  Each background task becomes its own task interval
    that overlaps the foreground session.

    Returns a list of new task dicts (one per background task).  The foreground
    tasks in *refined* are tagged ``"foreground"`` if not already tagged.
    """
    # Collect background-lifecycle events with tool_use_id and session_id.
    # (phase, name, ts, uid, session_id)
    lifecycle: list[tuple[str, str, float, str | None, str | None]] = []
    for ev in events:
        name = ev.get("tool_name")
        ts = ev.get("timestamp")
        if name in BACKGROUND_LIFECYCLE_TOOLS and ts is not None:
            phase = "create" if name == "TaskCreate" else ("stop" if name == "TaskStop" else "output")
            lifecycle.append((phase, name, ts, ev.get("tool_use_id"), ev.get("session_id")))

    if not lifecycle:
        return []

    # Group lifecycle events into (create_ts, end_ts) pairs.
    # CAUTION: TaskCreate and TaskStop CANNOT be reliably paired by any shared ID.
    # TaskCreate returns a per-session integer ("Task #1"), while TaskStop carries
    # an alphanumeric background-process ID ("b7b6zw9ki") — they are different task
    # systems. Pairing "first TaskStop after this TaskCreate" across sessions produces
    # absurd durations (125h+) when stops from days later get matched.
    #
    # Correct approach: only pair a stop/output that is in the SAME session and
    # within the session boundary (session_max_ts). No arbitrary time cap — the
    # session boundary is the natural bound. If no stop/output is found in the
    # same session, the background task's end is unknowable from event data —
    # use start_ts (zero-length: we know it started, not how long it ran).

    # Build session_id -> max_timestamp map for session-boundary detection.
    session_max_ts: dict[str, float] = {}
    for ev in events:
        sid = ev.get("session_id")
        ts = ev.get("timestamp")
        if sid and ts is not None:
            if sid not in session_max_ts or ts > session_max_ts[sid]:
                session_max_ts[sid] = ts

    lifecycle.sort(key=lambda x: x[2])

    bg_tasks: list[dict] = []
    used_ends: set[int] = set()  # indices of lifecycle events consumed as ends

    for i, (phase, name, start_ts, uid, sid) in enumerate(lifecycle):
        if phase != "create":
            continue

        # Find a stop in the SAME session, bounded by the session's max timestamp.
        # No arbitrary time cap — the session boundary is the natural bound.
        session_bound = session_max_ts.get(sid, float("inf")) if sid else float("inf")
        end_ts: float | None = None
        for j in range(i + 1, len(lifecycle)):
            if j in used_ends:
                continue
            j_phase, _, j_ts, _, j_sid = lifecycle[j]
            if j_ts > session_bound:
                break  # sorted by ts; nothing after this is within the session
            if j_sid != sid:
                continue  # different session — don't pair across sessions
            if j_phase == "stop":
                end_ts = j_ts
                used_ends.add(j)
                break
        if end_ts is None:
            # Fallback: last TaskOutput in the same session within the session boundary.
            for j in range(i + 1, len(lifecycle)):
                if j in used_ends:
                    continue
                j_phase, _, j_ts, _, j_sid = lifecycle[j]
                if j_ts > session_bound:
                    break
                if j_sid != sid:
                    continue
                if j_phase == "output":
                    end_ts = j_ts  # keep scanning — we want the LAST one
            if end_ts is not None:
                # Mark the used output (the last matching one)
                for j in range(len(lifecycle) - 1, i, -1):
                    if j in used_ends:
                        continue
                    j_phase, _, j_ts, _, j_sid = lifecycle[j]
                    if j_ts == end_ts and j_sid == sid:
                        used_ends.add(j)
                        break
        if end_ts is None:
            # No stop/output in the same session. The background task's
            # duration is unknowable from event data — the sub-agent ran in a
            # separate process whose lifecycle isn't recorded in this JSONL.
            # Use start_ts as the end (zero-length: we know it started, not
            # how long it ran). Do NOT reach across sessions.
            end_ts = start_ts

        # Build a thread_id from the tool_use_id if available, else the start ts.
        thread_label = uid if uid else f"bg-{int(start_ts)}"
        thread_id = f"background:{thread_label}"

        # Extract subject from the TaskCreate's tool_input.
        subject = None
        for ev in events:
            if (ev.get("tool_name") == "TaskCreate"
                    and ev.get("timestamp") == start_ts
                    and ev.get("tool_use_id") == uid):
                ti = ev.get("tool_input") or {}
                subject = ti.get("subject") or ti.get("description")
                break

        # Collect events belonging to this background task.  We identify them
        # by tool_use_id when available (the TaskCreate's uid links to its
        # results).  We do NOT blanket-collect lifecycle events in the time
        # window — that leaks other sub-agents' events when tasks overlap.
        bg_events: list[dict] = []
        used_event_indices: set[int] = set()
        for idx, ev in enumerate(events):
            ts = ev.get("timestamp")
            if ts is None:
                continue
            if ts < start_ts or ts > end_ts:
                continue
            # Only collect events whose tool_use_id matches this TaskCreate's uid.
            ev_uid = ev.get("tool_use_id")
            if uid and ev_uid == uid:
                bg_events.append(ev)
                used_event_indices.add(idx)

        # Fallback: if no uid-matched events were found, collect lifecycle events
        # in the SAME session within [start_ts, end_ts]. Track used indices to
        # avoid double-claiming events across overlapping background tasks.
        if not bg_events:
            fallback: list[dict] = []
            for idx, ev in enumerate(events):
                if idx in used_event_indices:
                    continue
                ts = ev.get("timestamp")
                if ts is None:
                    continue
                if ts < start_ts or ts > end_ts:
                    continue
                if ev.get("tool_name") not in BACKGROUND_LIFECYCLE_TOOLS:
                    continue
                # Restrict to the SAME session to avoid cross-session leakage.
                if sid and ev.get("session_id") != sid:
                    continue
                fallback.append(ev)
                used_event_indices.add(idx)
            bg_events = fallback

        # Build the background task dict, preserving key fields from the
        # foreground task that contains this interval (for cwd, session, etc.).
        parent_task = _find_containing_task(refined, start_ts)
        bg_task = _make_background_task(
            thread_id=thread_id,
            start=start_ts,
            end=end_ts,
            subject=subject or "(background sub-agent)",
            events=bg_events,
            parent=parent_task,
        )
        bg_tasks.append(bg_task)

    # Tag foreground tasks that contain background tasks.
    if bg_tasks:
        for t in refined:
            t.setdefault("thread_id", "foreground")
            for bg in bg_tasks:
                if _intervals_overlap(
                    t.get("start", 0), t.get("end", 0),
                    bg["start"], bg["end"],
                ):
                    t["thread_id"] = "foreground"
                    break

    return bg_tasks


def _find_containing_task(tasks: list[dict], ts: float) -> dict | None:
    """Find the task whose [start, end] contains timestamp *ts*."""
    best = None
    for t in tasks:
        start = t.get("start") or 0.0
        end = t.get("end") or 0.0
        if start <= ts <= end:
            # Prefer the tightest containing interval.
            if best is None or (end - start) < (best.get("end", 0) - best.get("start", 0)):
                best = t
    return best


def _make_background_task(
    *,
    thread_id: str,
    start: float,
    end: float,
    subject: str,
    events: list[dict],
    parent: dict | None,
) -> dict:
    """Build a task dict for a background sub-agent interval."""
    duration = max(0.0, end - start)
    tool_names = sorted({
        e.get("tool_name") for e in events
        if e.get("tool_name")
    })
    # Inherit cwd and session from the parent (foreground) task.
    cwd = parent.get("cwd") if parent else None
    session_id = parent.get("session_id") if parent else None
    source = parent.get("source", "claude_code") if parent else "claude_code"
    source_kind = parent.get("source_kind", "ai_session") if parent else "ai_session"

    # Estimate active_seconds for the background task.
    active = _estimate_active(events, start, end)

    return {
        "id": thread_id.replace(":", "-"),
        "flavor": "background",
        "source": source,
        "source_kind": source_kind,
        "session_id": session_id,
        "cwd": cwd,
        "git_branch": parent.get("git_branch") if parent else None,
        "subject": subject,
        "start": start,
        "end": end,
        "duration_seconds": round(duration, 1),
        "wall_clock_seconds": round(duration, 1),
        "active_seconds": round(active, 1),
        "event_count": len(events),
        "tool_calls": sum(1 for e in events if e.get("kind") == "tool_use"),
        "tool_names": tool_names,
        "output_tokens": 0,
        "input_tokens": 0,
        "errors": sum(1 for e in events if e.get("tool_is_error") is True),
        "inputs": [],
        "outputs": [],
        "success": None,
        "success_evidence": "background task — success not measured",
        "task_status": None,
        "thread_id": thread_id,
        "parent_task_id": parent.get("id") if parent else None,
    }


def _estimate_active(events: list[dict], start: float, end: float) -> float:
    """Estimate active work time for a background task using inter-event spans.

    Mirrors the approach in ``segment_tasks._compute_active_seconds``: sum the
    deltas between consecutive event timestamps that are below a gap threshold
    (30 min).  Gaps above the threshold are treated as idle and excluded.
    A single event yields 0 active seconds — we know it happened, not how long
    it took.  No per-event collar or other fabrication.
    """
    if not events:
        return 0.0
    GAP_THRESHOLD = 30 * 60  # 30 min — same as segment_tasks.GAP_THRESHOLD_SECONDS
    ts_list = sorted(e["timestamp"] for e in events if e.get("timestamp") is not None)
    if not ts_list:
        return 0.0
    if len(ts_list) < 2:
        return 0.0
    active = 0.0
    for i in range(1, len(ts_list)):
        delta = ts_list[i] - ts_list[i - 1]
        if delta <= GAP_THRESHOLD:
            active += delta
    return active


def _tag_concurrent_sessions(tasks: list[dict]) -> None:
    """Tag tasks from concurrent (overlapping) AI sessions.

    Two tasks from *different* ``session_id`` values with overlapping
    [start, end] ranges are concurrent sessions.  Each gets
    ``thread_id = "session:<session_id>"``.
    """
    # Group tasks by session_id.
    by_session: dict[str, list[dict]] = {}
    for t in tasks:
        sid = t.get("session_id")
        if sid is None:
            continue
        by_session.setdefault(sid, []).append(t)

    if len(by_session) < 2:
        # Only one (or zero) sessions — no concurrency possible.
        return

    # Compute the time range per session.
    session_ranges: dict[str, tuple[float, float]] = {}
    for sid, tsks in by_session.items():
        starts = [t.get("start") or 0.0 for t in tsks]
        ends = [t.get("end") or 0.0 for t in tsks]
        if starts and ends:
            session_ranges[sid] = (min(starts), max(ends))

    # Find overlapping session pairs.
    sids = list(session_ranges.keys())
    overlapping_sessions: set[str] = set()
    for i in range(len(sids)):
        for j in range(i + 1, len(sids)):
            s1, e1 = session_ranges[sids[i]]
            s2, e2 = session_ranges[sids[j]]
            if _intervals_overlap(s1, e1, s2, e2):
                overlapping_sessions.add(sids[i])
                overlapping_sessions.add(sids[j])

    # Tag tasks in overlapping sessions.
    for sid in overlapping_sessions:
        for t in by_session[sid]:
            # Only tag as session:<id> if not already tagged as background.
            if t.get("thread_id", "foreground") == "foreground":
                t["thread_id"] = f"session:{sid}"


def _detect_browser_during_coding(events: list[dict], refined: list[dict]) -> list[dict]:
    """Split browser visits during ai_session coding into separate research tasks.

    A ``browser`` visit whose timestamp falls within an ``ai_session`` coding
    task's [start, end] is split into a separate ``browser`` thread task that
    overlaps the coding task.

    Returns a list of new browser-task dicts.
    """
    # Find browser events.
    browser_events = [
        ev for ev in events
        if ev.get("source_kind") == "browser" and ev.get("timestamp") is not None
    ]
    if not browser_events:
        return []

    # Find ai_session coding tasks (tasks with tool_calls > 0 or source_kind == ai_session).
    coding_tasks = [
        t for t in refined
        if t.get("source_kind") == "ai_session"
        and (t.get("tool_calls") or 0) > 0
    ]
    if not coding_tasks:
        return []

    # For each coding task, find browser events that fall within its span.
    browser_tasks: list[dict] = []
    claimed_browser_events: set[int] = set()  # indices in browser_events

    for ct in coding_tasks:
        ct_start = ct.get("start") or 0.0
        ct_end = ct.get("end") or 0.0

        overlapping_browser = []
        for idx, bev in enumerate(browser_events):
            if idx in claimed_browser_events:
                continue
            bts = bev.get("timestamp") or 0.0
            if ct_start <= bts <= ct_end:
                overlapping_browser.append(bev)
                claimed_browser_events.add(idx)

        if not overlapping_browser:
            continue

        # Build a browser research task spanning the overlapping visits.
        b_start = min(e["timestamp"] for e in overlapping_browser)
        b_end = max(e["timestamp"] for e in overlapping_browser)
        # Add a small collar so a single visit has a non-zero duration.
        if b_end - b_start < 1.0:
            b_end = b_start + 60.0  # 1 min minimum

        # Subject from the first browser event's text or URL.
        subject = "(browser research)"
        first_ev = overlapping_browser[0]
        if first_ev.get("text"):
            subject = first_ev["text"][:120]
        elif first_ev.get("tool_input") and isinstance(first_ev["tool_input"], dict):
            url = first_ev["tool_input"].get("url") or ""
            if url:
                subject = f"research: {url[:100]}"

        b_task = {
            "id": f"browser-{int(b_start)}",
            "flavor": "browser_research",
            "source": "browser",
            "source_kind": "browser",
            "session_id": None,
            "cwd": ct.get("cwd"),
            "git_branch": None,
            "subject": subject,
            "start": b_start,
            "end": b_end,
            "duration_seconds": round(b_end - b_start, 1),
            "wall_clock_seconds": round(b_end - b_start, 1),
            "active_seconds": round(min(b_end - b_start, len(overlapping_browser) * 300), 1),
            "event_count": len(overlapping_browser),
            "tool_calls": 0,
            "tool_names": [],
            "output_tokens": 0,
            "input_tokens": 0,
            "errors": 0,
            "inputs": [],
            "outputs": [],
            "success": None,
            "success_evidence": "browser research — success not measured",
            "task_status": None,
            "thread_id": "browser",
            "parent_task_id": ct.get("id"),
        }
        browser_tasks.append(b_task)

        # Ensure the coding task is tagged as foreground.
        ct.setdefault("thread_id", "foreground")

    return browser_tasks


# ---------------------------------------------------------------------------
# 10.1.3  Exclusive-time computation
# ---------------------------------------------------------------------------

def compute_exclusive_time(tasks: list[dict]) -> dict:
    """Compute exclusive time, wall-clock span, active time, and overlap.

    Parameters
    ----------
    tasks : list[dict]
        Task dicts with ``start``, ``end``, and optionally ``active_seconds``
        fields.  These may overlap (e.g. output of ``detect_parallel_tasks``).

    Returns
    -------
    dict
        ``{
            "exclusive_seconds": float,        # union of all [start, end] — no double-count
            "wall_span_seconds": float,        # max(end) - min(start)
            "active_seconds_total": float,     # sum of active_seconds (CAN double-count)
            "overlap_seconds": float,          # time where 2+ tasks overlap
            "n_parallel_groups": int,          # number of distinct overlapping clusters
        }``

    Exclusive time
    --------------
    The union of all task intervals [start, end] as a set of non-overlapping
    intervals.  This is the person's actual bandwidth — no double-counting.
    If task A (10:00-12:00) and task B (11:00-13:00) overlap, exclusive time =
    3h (10:00-13:00), not 4h.

    Computed via a sweep line: sort all start/end endpoints, walk through them
    tracking how many tasks are active.  When the active count goes from 0 to 1,
    start a new exclusive interval.  When it goes from 1 to 0, close it.

    Wall-clock span
    ---------------
    ``max(end) - min(start)`` — the total elapsed time from the first task's
    start to the last task's end.

    Active time
    -----------
    Sum of each task's ``active_seconds``.  Note: this **can** double-count
    overlapping active work — if two tasks are both active in the same window,
    both contribute to the sum.  This is intentional: it measures total active
    engagement, which may exceed wall-clock when parallel work is happening.

    Overlap time
    ------------
    The portion of the timeline where 2+ tasks are active simultaneously.
    This measures coordination/context-switching overhead.
    """
    if not tasks:
        return {
            "exclusive_seconds": 0.0,
            "wall_span_seconds": 0.0,
            "active_seconds_total": 0.0,
            "overlap_seconds": 0.0,
            "n_parallel_groups": 0,
        }

    # Extract intervals, filtering degenerate ones.
    intervals: list[tuple[float, float]] = []
    active_seconds_total = 0.0
    for t in tasks:
        start = t.get("start")
        end = t.get("end")
        if start is None or end is None:
            continue
        if end < start:
            continue
        intervals.append((start, end))
        active_seconds_total += float(t.get("active_seconds") or 0.0)

    if not intervals:
        return {
            "exclusive_seconds": 0.0,
            "wall_span_seconds": 0.0,
            "active_seconds_total": round(active_seconds_total, 1),
            "overlap_seconds": 0.0,
            "n_parallel_groups": 0,
        }

    # --- Exclusive time via sweep line (interval union) ---
    # Build endpoint events: (+1 for start, -1 for end).
    endpoints: list[tuple[float, int]] = []
    for start, end in intervals:
        endpoints.append((start, 1))
        endpoints.append((end, -1))
    # Sort by timestamp; when timestamps are equal, process ends (-1) before
    # starts (+1) so that touching intervals (A.end == B.start) don't count
    # as overlapping.
    endpoints.sort(key=lambda x: (x[0], x[1]))

    exclusive_seconds = 0.0
    overlap_seconds = 0.0
    active_count = 0
    exclusive_start: float | None = None

    for ts, delta in endpoints:
        prev_count = active_count
        active_count += delta

        # Track exclusive intervals (count transitions between 0 and 1).
        if prev_count == 0 and active_count == 1:
            # Entering an active period.
            exclusive_start = ts
        elif prev_count == 1 and active_count == 0:
            # Leaving the active period.
            if exclusive_start is not None:
                exclusive_seconds += ts - exclusive_start
                exclusive_start = None

        # Track overlap: time where 2+ tasks are active.
        # We need to measure the time *between* consecutive endpoints where
        # active_count >= 2.
        # This is handled in a second pass below for clarity.

    # --- Overlap time: time where 2+ intervals overlap ---
    # Re-sweep, measuring the duration where active_count >= 2.
    endpoints2: list[tuple[float, int]] = []
    for start, end in intervals:
        endpoints2.append((start, 1))
        endpoints2.append((end, -1))
    endpoints2.sort(key=lambda x: (x[0], x[1]))

    active_count = 0
    prev_ts: float | None = None
    for ts, delta in endpoints2:
        if prev_ts is not None and active_count >= 2:
            overlap_seconds += ts - prev_ts
        active_count += delta
        prev_ts = ts

    # --- Wall-clock span ---
    all_starts = [s for s, _ in intervals]
    all_ends = [e for _, e in intervals]
    wall_span = max(all_ends) - min(all_starts)

    # --- Parallel groups: connected components of overlapping intervals ---
    # Filter out zero-length intervals (end == start) — they don't represent
    # real work and would inflate the parallel-group count.
    nonzero_intervals = [(s, e) for s, e in intervals if e > s]
    n_parallel_groups = _count_parallel_groups(nonzero_intervals)

    return {
        "exclusive_seconds": round(exclusive_seconds, 1),
        "wall_span_seconds": round(wall_span, 1),
        "active_seconds_total": round(active_seconds_total, 1),
        "overlap_seconds": round(overlap_seconds, 1),
        "n_parallel_groups": n_parallel_groups,
    }


def _count_parallel_groups(intervals: list[tuple[float, float]]) -> int:
    """Count connected components of overlapping intervals.

    A *parallel group* is a maximal set of intervals where each overlaps at
    least one other in the set (transitive closure).  Two non-overlapping
    sequential tasks form zero parallel groups (they don't overlap).
    """
    if len(intervals) < 2:
        return 0

    # Sort by start time.
    sorted_ivs = sorted(intervals, key=lambda x: x[0])

    groups = 0
    i = 0
    while i < len(sorted_ivs):
        # Start a potential group with interval i.
        group_max_end = sorted_ivs[i][1]
        group_size = 1
        j = i + 1
        while j < len(sorted_ivs) and sorted_ivs[j][0] < group_max_end:
            # Interval j overlaps the current group.
            group_max_end = max(group_max_end, sorted_ivs[j][1])
            group_size += 1
            j += 1
        if group_size >= 2:
            groups += 1
        i = j

    return groups


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _intervals_overlap(s1: float, e1: float, s2: float, e2: float) -> bool:
    """Return True if [s1, e1] and [s2, e2] overlap (touching counts)."""
    return not (e1 < s2 or e2 < s1)
