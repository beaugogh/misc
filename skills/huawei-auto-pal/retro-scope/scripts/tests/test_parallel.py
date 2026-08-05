"""Tests for parallel-task detection and exclusive-time computation.

Run with:
    cd D:\\workspace\\misc\\skills\\huawei-auto-pal\\retro-scope\\scripts
    python -m unittest tests.test_parallel -v
"""

from __future__ import annotations

import unittest
import os
import sys

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from parallel_tasks import detect_parallel_tasks, compute_exclusive_time, _estimate_active
from sources import make_event


# ---------------------------------------------------------------------------
# Helper: epoch seconds for 2026-07-01T10:00:00Z = 1782900000.0
# Use a base timestamp so fixtures are readable.
# ---------------------------------------------------------------------------

T0 = 1782900000.0  # 2026-07-01T10:00:00Z


def _ts(minutes: float) -> float:
    """Return T0 + minutes*60."""
    return T0 + minutes * 60.0


def _make_task(
    tid: str,
    start: float,
    end: float,
    *,
    flavor: str = "implicit",
    source_kind: str = "ai_session",
    session_id: str = "sess-A",
    cwd: str = "/proj",
    subject: str = "test task",
    tool_calls: int = 0,
    active_seconds: float | None = None,
    tool_names: list[str] | None = None,
) -> dict:
    """Build a synthetic task dict matching the segment() output shape."""
    duration = max(0.0, end - start)
    if active_seconds is None:
        active_seconds = duration
    return {
        "id": tid,
        "flavor": flavor,
        "source": "claude_code",
        "source_kind": source_kind,
        "session_id": session_id,
        "cwd": cwd,
        "git_branch": "main",
        "subject": subject,
        "start": start,
        "end": end,
        "duration_seconds": round(duration, 1),
        "wall_clock_seconds": round(duration, 1),
        "active_seconds": round(active_seconds, 1),
        "event_count": 5,
        "tool_calls": tool_calls,
        "tool_names": tool_names or [],
        "output_tokens": 0,
        "input_tokens": 0,
        "errors": 0,
        "inputs": [],
        "outputs": [],
        "success": None,
        "success_evidence": "n/a",
        "task_status": None,
    }


def _make_event(
    ts: float,
    *,
    kind: str = "tool_use",
    tool_name: str | None = None,
    tool_input: dict | None = None,
    tool_use_id: str | None = None,
    source_kind: str = "ai_session",
    session_id: str = "sess-A",
    cwd: str = "/proj",
    text: str | None = None,
) -> dict:
    """Build a synthetic event dict matching the make_event() shape."""
    return make_event(
        source="claude_code",
        source_kind=source_kind,
        session_id=session_id,
        cwd=cwd,
        git_branch="main",
        timestamp=ts,
        kind=kind,
        tool_name=tool_name,
        tool_input=tool_input,
        tool_use_id=tool_use_id,
        text=text,
    )


class TestBackgroundTaskSplit(unittest.TestCase):
    """10.1.2 Signal 1: Background sub-agent task lifecycle."""

    def test_background_task_split_from_foreground(self):
        """A TaskCreate at T1, foreground continues, TaskStop at T2 -> background
        task interval (T1, T2) overlaps the foreground."""
        t_create = _ts(10)  # 10 min into session
        t_stop = _ts(50)    # 50 min in
        t_session_end = _ts(60)

        # Events: user starts coding, agent fires off a background task,
        # foreground continues working, background stops.
        events = [
            _make_event(_ts(0), kind="user_message", text="code the thing"),
            _make_event(_ts(5), kind="assistant_message"),
            _make_event(t_create, tool_name="TaskCreate",
                        tool_input={"subject": "run tests in background"},
                        tool_use_id="bg-001"),
            _make_event(_ts(20), kind="user_message", text="also fix the docs"),
            _make_event(_ts(30), kind="assistant_message"),
            _make_event(t_stop, tool_name="TaskStop", tool_use_id="bg-001"),
            _make_event(t_session_end, kind="assistant_message"),
        ]

        # One foreground task spanning the whole session.
        tasks = [
            _make_task("implicit-1", _ts(0), t_session_end,
                       subject="code the thing", tool_calls=3),
        ]

        refined = detect_parallel_tasks(tasks, events)

        # Should have 2 tasks: foreground + background.
        self.assertEqual(len(refined), 2)

        bg = [t for t in refined if t["thread_id"].startswith("background:")]
        self.assertEqual(len(bg), 1)
        self.assertAlmostEqual(bg[0]["start"], t_create, places=1)
        self.assertAlmostEqual(bg[0]["end"], t_stop, places=1)
        self.assertEqual(bg[0]["subject"], "run tests in background")

        # The background task overlaps the foreground task.
        fg = [t for t in refined if t["thread_id"] == "foreground"]
        self.assertEqual(len(fg), 1)
        self.assertTrue(bg[0]["start"] < fg[0]["end"])
        self.assertTrue(bg[0]["end"] > fg[0]["start"])

    def test_background_task_no_stop_uses_taskoutput(self):
        """If no TaskStop, the background task end falls back to last TaskOutput."""
        t_create = _ts(10)
        t_output = _ts(40)
        t_end = _ts(60)

        events = [
            _make_event(_ts(0), kind="user_message", text="go"),
            _make_event(t_create, tool_name="TaskCreate",
                        tool_input={"subject": "bg work"},
                        tool_use_id="bg-002"),
            _make_event(_ts(20), kind="assistant_message"),
            _make_event(t_output, tool_name="TaskOutput", tool_use_id="bg-002"),
            _make_event(t_end, kind="assistant_message"),
        ]

        tasks = [_make_task("implicit-1", _ts(0), t_end, tool_calls=2)]
        refined = detect_parallel_tasks(tasks, events)

        bg = [t for t in refined if t["thread_id"].startswith("background:")]
        self.assertEqual(len(bg), 1)
        # End should be the TaskOutput timestamp, not the session end.
        self.assertAlmostEqual(bg[0]["end"], t_output, places=1)

    def test_multiple_background_tasks(self):
        """Two TaskCreate calls produce two separate background tasks."""
        events = [
            _make_event(_ts(0), kind="user_message", text="start"),
            _make_event(_ts(5), tool_name="TaskCreate",
                        tool_input={"subject": "bg task A"},
                        tool_use_id="bg-A"),
            _make_event(_ts(10), tool_name="TaskCreate",
                        tool_input={"subject": "bg task B"},
                        tool_use_id="bg-B"),
            _make_event(_ts(30), tool_name="TaskStop", tool_use_id="bg-A"),
            _make_event(_ts(35), tool_name="TaskStop", tool_use_id="bg-B"),
            _make_event(_ts(40), kind="assistant_message"),
        ]

        tasks = [_make_task("implicit-1", _ts(0), _ts(40), tool_calls=4)]
        refined = detect_parallel_tasks(tasks, events)

        bg = [t for t in refined if t["thread_id"].startswith("background:")]
        self.assertEqual(len(bg), 2)
        threads = {t["thread_id"] for t in bg}
        self.assertIn("background:bg-A", threads)
        self.assertIn("background:bg-B", threads)


class TestConcurrentSessions(unittest.TestCase):
    """10.1.2 Signal 2: Concurrent AI sessions with overlapping ranges."""

    def test_concurrent_sessions_detected(self):
        """Two sessions with overlapping timestamp ranges -> both tagged as parallel."""
        # Session A: 10:00-11:00
        # Session B: 10:30-11:30  (overlaps A)
        t_start_a = _ts(0)
        t_end_a = _ts(60)
        t_start_b = _ts(30)
        t_end_b = _ts(90)

        tasks = [
            _make_task("implicit-1", t_start_a, t_end_a,
                       session_id="sess-A", subject="coding on server"),
            _make_task("implicit-1", t_start_b, t_end_b,
                       session_id="sess-B", subject="coding locally"),
        ]

        events = [
            _make_event(t_start_a, kind="user_message", session_id="sess-A", text="hi"),
            _make_event(t_end_a, kind="assistant_message", session_id="sess-A"),
            _make_event(t_start_b, kind="user_message", session_id="sess-B", text="hello"),
            _make_event(t_end_b, kind="assistant_message", session_id="sess-B"),
        ]

        refined = detect_parallel_tasks(tasks, events)

        # Both tasks should be tagged with session-specific thread_ids.
        session_tagged = [t for t in refined if t["thread_id"].startswith("session:")]
        self.assertEqual(len(session_tagged), 2)
        threads = {t["thread_id"] for t in session_tagged}
        self.assertIn("session:sess-A", threads)
        self.assertIn("session:sess-B", threads)

    def test_non_overlapping_sessions_not_tagged(self):
        """Two sessions with non-overlapping ranges -> no parallel tagging."""
        # Session A: 10:00-10:30, Session B: 11:00-11:30 — no overlap.
        tasks = [
            _make_task("implicit-1", _ts(0), _ts(30), session_id="sess-A"),
            _make_task("implicit-1", _ts(60), _ts(90), session_id="sess-B"),
        ]

        events = [
            _make_event(_ts(0), kind="user_message", session_id="sess-A"),
            _make_event(_ts(30), kind="assistant_message", session_id="sess-A"),
            _make_event(_ts(60), kind="user_message", session_id="sess-B"),
            _make_event(_ts(90), kind="assistant_message", session_id="sess-B"),
        ]

        refined = detect_parallel_tasks(tasks, events)
        # Both should remain foreground (no overlap).
        for t in refined:
            self.assertEqual(t["thread_id"], "foreground")


class TestBrowserDuringCoding(unittest.TestCase):
    """10.1.2 Signal 3: Browser visit during an ai_session coding task."""

    def test_browser_visit_during_coding_split(self):
        """A browser visit within a coding task's span -> separate research task."""
        t_start = _ts(0)
        t_browser = _ts(30)  # 30 min in
        t_end = _ts(60)

        tasks = [
            _make_task("implicit-1", t_start, t_end,
                       source_kind="ai_session",
                       tool_calls=5,
                       tool_names=["Edit", "Bash"],
                       subject="coding task"),
        ]

        events = [
            _make_event(t_start, kind="user_message", text="build the feature"),
            _make_event(_ts(10), tool_name="Edit",
                        tool_input={"file_path": "/proj/app.py"}),
            # Browser visit in the middle of the coding task.
            _make_event(t_browser, source_kind="browser",
                        kind="visit", text="how to do X in python",
                        tool_input={"url": "https://docs.python.org/3/library/x"}),
            _make_event(_ts(40), tool_name="Bash",
                        tool_input={"command": "python test.py"}),
            _make_event(t_end, kind="assistant_message"),
        ]

        refined = detect_parallel_tasks(tasks, events)

        # Should have 2 tasks: the coding task + a browser research task.
        browser = [t for t in refined if t["thread_id"] == "browser"]
        self.assertEqual(len(browser), 1)
        self.assertEqual(browser[0]["source_kind"], "browser")
        self.assertTrue(browser[0]["start"] >= t_start)
        self.assertTrue(browser[0]["end"] <= t_end)

        # The browser task overlaps the coding task.
        coding = [t for t in refined if t["thread_id"] == "foreground"]
        self.assertEqual(len(coding), 1)
        self.assertTrue(_intervals_overlap_simple(
            coding[0]["start"], coding[0]["end"],
            browser[0]["start"], browser[0]["end"],
        ))

    def test_browser_outside_coding_not_split(self):
        """A browser visit outside any coding task -> no new task."""
        t_start = _ts(0)
        t_end = _ts(30)

        tasks = [
            _make_task("implicit-1", t_start, t_end,
                       source_kind="ai_session",
                       tool_calls=2,
                       tool_names=["Edit"],
                       subject="coding"),
        ]

        events = [
            _make_event(t_start, kind="user_message", text="code"),
            _make_event(_ts(10), tool_name="Edit",
                        tool_input={"file_path": "/proj/app.py"}),
            _make_event(t_end, kind="assistant_message"),
            # Browser visit AFTER the coding task ended.
            _make_event(_ts(60), source_kind="browser",
                        kind="visit", text="reading later"),
        ]

        refined = detect_parallel_tasks(tasks, events)
        browser = [t for t in refined if t["thread_id"] == "browser"]
        self.assertEqual(len(browser), 0)


class TestExclusiveTime(unittest.TestCase):
    """10.1.3: Exclusive-time computation."""

    def test_overlapping_intervals_exclusive_is_union(self):
        """Two overlapping intervals: exclusive = union, not sum.

        The spec example: task A (10:00-12:00) + task B (11:00-13:00)
        => exclusive = 3h (10:00-13:00), not 4h.
        """
        # 10:00 = T0, 12:00 = T0+120min, 11:00 = T0+60min, 13:00 = T0+180min
        tasks = [
            _make_task("A", _ts(0), _ts(120), active_seconds=7200),    # 2h
            _make_task("B", _ts(60), _ts(180), active_seconds=7200),   # 2h
        ]

        result = compute_exclusive_time(tasks)

        # Exclusive = 3h = 10800s (10:00 to 13:00).
        self.assertAlmostEqual(result["exclusive_seconds"], 10800.0, places=1)
        # Wall span = 3h = 10800s.
        self.assertAlmostEqual(result["wall_span_seconds"], 10800.0, places=1)
        # Active total = 4h = 14400s (sum, CAN double-count).
        self.assertAlmostEqual(result["active_seconds_total"], 14400.0, places=1)
        # Overlap = 1h = 3600s (11:00-12:00).
        self.assertAlmostEqual(result["overlap_seconds"], 3600.0, places=1)
        # 1 parallel group.
        self.assertEqual(result["n_parallel_groups"], 1)

    def test_sequential_no_overlap_exclusive_is_sum(self):
        """Two sequential (non-overlapping) tasks: exclusive = sum (no double-count)."""
        # Task A: 10:00-11:00, Task B: 11:00-12:00 (touching, not overlapping).
        tasks = [
            _make_task("A", _ts(0), _ts(60), active_seconds=3600),   # 1h
            _make_task("B", _ts(60), _ts(120), active_seconds=3600), # 1h
        ]

        result = compute_exclusive_time(tasks)

        # Exclusive = 2h = 7200s (no overlap, so union = sum).
        self.assertAlmostEqual(result["exclusive_seconds"], 7200.0, places=1)
        # Wall span = 2h = 7200s.
        self.assertAlmostEqual(result["wall_span_seconds"], 7200.0, places=1)
        # Active total = 2h = 7200s.
        self.assertAlmostEqual(result["active_seconds_total"], 7200.0, places=1)
        # No overlap.
        self.assertAlmostEqual(result["overlap_seconds"], 0.0, places=1)
        # No parallel groups (touching intervals don't count as overlapping).
        self.assertEqual(result["n_parallel_groups"], 0)

    def test_three_overlapping_intervals(self):
        """Three tasks all overlapping at the same time."""
        # A: 10:00-12:00, B: 10:30-11:30, C: 10:45-11:15
        tasks = [
            _make_task("A", _ts(0), _ts(120), active_seconds=7200),
            _make_task("B", _ts(30), _ts(90), active_seconds=3600),
            _make_task("C", _ts(45), _ts(75), active_seconds=1800),
        ]

        result = compute_exclusive_time(tasks)

        # Exclusive = 10:00-12:00 = 2h = 7200s.
        self.assertAlmostEqual(result["exclusive_seconds"], 7200.0, places=1)
        # Overlap: from 10:45 to 11:15 (30 min) 3 overlap, plus 10:30-10:45 and
        # 11:15-11:30 (15 min each) 2 overlap.
        # Total overlap = 30 min (3-way) + 30 min (2-way) = 60 min = 3600s.
        # Actually, overlap is the time where 2+ are active:
        #   10:30-10:45: A+B = 2 -> 15 min
        #   10:45-11:15: A+B+C = 3 -> 30 min
        #   11:15-11:30: A+B = 2 -> 15 min
        # Total = 60 min = 3600s.
        self.assertAlmostEqual(result["overlap_seconds"], 3600.0, places=1)
        # 1 parallel group (all three overlap transitively).
        self.assertEqual(result["n_parallel_groups"], 1)

    def test_empty_tasks(self):
        """Empty task list -> all zeros."""
        result = compute_exclusive_time([])
        self.assertEqual(result["exclusive_seconds"], 0.0)
        self.assertEqual(result["wall_span_seconds"], 0.0)
        self.assertEqual(result["active_seconds_total"], 0.0)
        self.assertEqual(result["overlap_seconds"], 0.0)
        self.assertEqual(result["n_parallel_groups"], 0)

    def test_single_task(self):
        """One task: exclusive = duration, no overlap."""
        tasks = [_make_task("A", _ts(0), _ts(60), active_seconds=3600)]
        result = compute_exclusive_time(tasks)
        self.assertAlmostEqual(result["exclusive_seconds"], 3600.0, places=1)
        self.assertAlmostEqual(result["wall_span_seconds"], 3600.0, places=1)
        self.assertAlmostEqual(result["overlap_seconds"], 0.0, places=1)
        self.assertEqual(result["n_parallel_groups"], 0)

    def test_two_separate_parallel_groups(self):
        """Two pairs of overlapping tasks, separated in time -> 2 parallel groups."""
        # Group 1: A 10:00-11:00, B 10:30-11:30 (overlap)
        # Group 2: C 13:00-14:00, D 13:30-14:30 (overlap, separate from group 1)
        tasks = [
            _make_task("A", _ts(0), _ts(60)),
            _make_task("B", _ts(30), _ts(90)),
            _make_task("C", _ts(180), _ts(240)),
            _make_task("D", _ts(210), _ts(270)),
        ]

        result = compute_exclusive_time(tasks)
        self.assertEqual(result["n_parallel_groups"], 2)


class TestEdgeCases(unittest.TestCase):
    """Edge cases and defensive behavior."""

    def test_empty_tasks_returns_empty(self):
        """No tasks -> empty list."""
        result = detect_parallel_tasks([], [])
        self.assertEqual(result, [])

    def test_empty_events_tags_foreground(self):
        """No events -> all tasks tagged foreground."""
        tasks = [_make_task("A", _ts(0), _ts(60))]
        result = detect_parallel_tasks(tasks, [])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["thread_id"], "foreground")

    def test_task_without_end_handled(self):
        """Task missing 'end' field doesn't crash compute_exclusive_time."""
        tasks = [{"start": _ts(0), "active_seconds": 60.0}]
        result = compute_exclusive_time(tasks)
        # Should not crash; the task is skipped (no end).
        self.assertEqual(result["n_parallel_groups"], 0)

    def test_degenerate_interval_skipped(self):
        """Task with end < start is skipped."""
        tasks = [_make_task("A", _ts(60), _ts(0))]
        result = compute_exclusive_time(tasks)
        self.assertEqual(result["exclusive_seconds"], 0.0)

    def test_all_tasks_get_thread_id(self):
        """Every task in the output has a thread_id field."""
        events = [
            _make_event(_ts(0), kind="user_message", text="hi"),
            _make_event(_ts(10), kind="assistant_message"),
        ]
        tasks = [_make_task("A", _ts(0), _ts(10))]
        refined = detect_parallel_tasks(tasks, events)
        for t in refined:
            self.assertIn("thread_id", t)

    def test_original_tasks_not_mutated(self):
        """The caller's task dicts are not mutated."""
        tasks = [_make_task("A", _ts(0), _ts(60))]
        original = dict(tasks[0])
        events = [_make_event(_ts(0), kind="user_message", text="hi")]
        detect_parallel_tasks(tasks, events)
        # Original should not have thread_id added.
        self.assertNotIn("thread_id", tasks[0])
        self.assertEqual(tasks[0], original)


def _intervals_overlap_simple(s1: float, e1: float, s2: float, e2: float) -> bool:
    return not (e1 < s2 or e2 < s1)


class TestC4EventLeakage(unittest.TestCase):
    """C4 (CRITICAL): Background task event leakage between overlapping sub-agents."""

    def test_overlapping_bg_tasks_no_event_leakage(self):
        """Two overlapping background tasks with different tool_use_ids must not
        collect each other's events."""
        # Task A: create at T5, stop at T20 (first create -> first stop)
        # Task B: create at T10, stop at T30 (second create -> second stop)
        # Both overlap in [T10, T20].
        events = [
            _make_event(_ts(0), kind="user_message", text="start"),
            _make_event(_ts(5), tool_name="TaskCreate",
                        tool_input={"subject": "bg task A"},
                        tool_use_id="bg-A"),
            _make_event(_ts(10), tool_name="TaskCreate",
                        tool_input={"subject": "bg task B"},
                        tool_use_id="bg-B"),
            # bg-B's TaskOutput at T15 — falls within bg-A's [T5, T20] window.
            # Old code would leak this into bg-A via the blanket elif.
            _make_event(_ts(15), tool_name="TaskOutput", tool_use_id="bg-B"),
            # bg-A's TaskOutput at T18 — falls within bg-B's [T10, T30] window.
            # Old code would leak this into bg-B via the blanket elif.
            _make_event(_ts(18), tool_name="TaskOutput", tool_use_id="bg-A"),
            _make_event(_ts(20), tool_name="TaskStop", tool_use_id="bg-A"),
            _make_event(_ts(30), tool_name="TaskStop", tool_use_id="bg-B"),
            _make_event(_ts(35), kind="assistant_message"),
        ]

        tasks = [_make_task("implicit-1", _ts(0), _ts(35), tool_calls=6)]
        refined = detect_parallel_tasks(tasks, events)

        bg = [t for t in refined if t["thread_id"].startswith("background:")]
        self.assertEqual(len(bg), 2)

        bg_a = [t for t in bg if t["thread_id"] == "background:bg-A"][0]
        bg_b = [t for t in bg if t["thread_id"] == "background:bg-B"][0]

        # bg-A events: TaskCreate(bg-A), TaskOutput(bg-A), TaskStop(bg-A) = 3 tool_use
        # bg-B events: TaskCreate(bg-B), TaskOutput(bg-B), TaskStop(bg-B) = 3 tool_use
        # If leakage occurred (old elif branch), bg-A would have 5 tool_use events
        # (it would also collect bg-B's TaskCreate and TaskOutput).
        self.assertEqual(bg_a["tool_calls"], 3)
        self.assertEqual(bg_b["tool_calls"], 3)

        # Verify the intervals are correct
        self.assertAlmostEqual(bg_a["start"], _ts(5), places=1)
        self.assertAlmostEqual(bg_a["end"], _ts(20), places=1)
        self.assertAlmostEqual(bg_b["start"], _ts(10), places=1)
        self.assertAlmostEqual(bg_b["end"], _ts(30), places=1)


class TestM4SessionBoundaryPairing(unittest.TestCase):
    """M4: Remove 2h proximity cap; use session boundary for stop pairing."""

    def test_stop_3h_after_create_same_session_paired(self):
        """A TaskStop 3h after TaskCreate in the same session should be paired
        (not treated as zero-length due to the old 2h cap)."""
        t_create = _ts(10)       # 10 min in
        t_stop = _ts(190)        # 190 min in = 3h later
        t_session_end = _ts(200)  # session ends at 200 min

        events = [
            _make_event(_ts(0), kind="user_message", text="start"),
            _make_event(t_create, tool_name="TaskCreate",
                        tool_input={"subject": "long bg task"},
                        tool_use_id="bg-long"),
            _make_event(_ts(60), kind="assistant_message"),
            _make_event(_ts(120), kind="assistant_message"),
            _make_event(t_stop, tool_name="TaskStop", tool_use_id="bg-long"),
            _make_event(t_session_end, kind="assistant_message"),
        ]

        tasks = [_make_task("implicit-1", _ts(0), t_session_end, tool_calls=3)]
        refined = detect_parallel_tasks(tasks, events)

        bg = [t for t in refined if t["thread_id"].startswith("background:")]
        self.assertEqual(len(bg), 1)

        # The background task should span from create to stop (3h), not zero-length.
        self.assertAlmostEqual(bg[0]["start"], t_create, places=1)
        self.assertAlmostEqual(bg[0]["end"], t_stop, places=1)
        # Verify it's not zero-length.
        self.assertGreater(bg[0]["end"], bg[0]["start"])
        self.assertAlmostEqual(bg[0]["duration_seconds"], t_stop - t_create, places=1)


class TestM5InterEventSpanActiveTime(unittest.TestCase):
    """M5: _estimate_active uses inter-event span, not 5-min collar."""

    def test_single_event_active_zero(self):
        """A single-event background task should get active=0, not 5min collar."""
        t = _ts(10)
        events = [_make_event(t, tool_name="TaskCreate",
                              tool_input={"subject": "bg"},
                              tool_use_id="bg-1")]
        active = _estimate_active(events, t, t)
        self.assertEqual(active, 0.0)

    def test_two_events_close_apart(self):
        """Two events 5 min apart should yield 300s active time."""
        events = [
            _make_event(_ts(10), tool_name="TaskCreate",
                        tool_input={"subject": "bg"}, tool_use_id="bg-1"),
            _make_event(_ts(15), tool_name="TaskStop", tool_use_id="bg-1"),
        ]
        active = _estimate_active(events, _ts(10), _ts(15))
        self.assertAlmostEqual(active, 300.0, places=1)

    def test_two_events_far_apart_excluded(self):
        """Two events 45 min apart (>30min gap) should yield 0 active time."""
        events = [
            _make_event(_ts(10), tool_name="TaskCreate",
                        tool_input={"subject": "bg"}, tool_use_id="bg-1"),
            _make_event(_ts(55), tool_name="TaskStop", tool_use_id="bg-1"),
        ]
        active = _estimate_active(events, _ts(10), _ts(55))
        self.assertEqual(active, 0.0)


class TestM6ZeroLengthNoParallelGroup(unittest.TestCase):
    """M6: Zero-length intervals don't inflate n_parallel_groups."""

    def test_zero_length_interval_not_parallel_group(self):
        """A zero-length interval overlapping a real interval should not count
        as a parallel group."""
        # Task A: 10:00-11:00 (real, 1h)
        # Task B: 10:30-10:30 (zero-length — e.g. background task with no stop)
        tasks = [
            _make_task("A", _ts(0), _ts(60), active_seconds=3600),
            _make_task("B", _ts(30), _ts(30), active_seconds=0),
        ]

        result = compute_exclusive_time(tasks)

        # Zero-length interval should not create a parallel group.
        self.assertEqual(result["n_parallel_groups"], 0)

    def test_zero_length_with_non_overlapping_real(self):
        """A zero-length interval and a non-overlapping real interval: 0 groups."""
        tasks = [
            _make_task("A", _ts(0), _ts(30), active_seconds=1800),
            _make_task("B", _ts(60), _ts(60), active_seconds=0),
            _make_task("C", _ts(90), _ts(120), active_seconds=1800),
        ]
        result = compute_exclusive_time(tasks)
        self.assertEqual(result["n_parallel_groups"], 0)


class TestBrowserActiveTimeDeflation(unittest.TestCase):
    """Tests that browser active_seconds is NOT inflated by overnight tabs.

    The old collar formula (min(span, n_events * 300)) inflated tabs-left-open
    by 30×. The inter-event-span method excises gaps >30min, so overnight idle
    time is not counted as active browsing.
    """

    def test_overnight_gaps_excised(self):
        """Browser events spread across 24h with overnight gaps → active time
        reflects only the continuous browsing, not the full span."""
        # 4 browser visits: 2 close together (active), then 10h gap, then 2 more
        t0 = _ts(0)       # 09:00
        t1 = _ts(5)       # 09:05 — 5 min after t0 (active)
        t2 = _ts(600)     # 19:00 — 10h gap (overnight/idle)
        t3 = _ts(605)     # 19:05 — 5 min after t2 (active)
        coding_end = _ts(700)

        tasks = [
            _make_task("implicit-1", t0, coding_end,
                       source_kind="ai_session",
                       tool_calls=5, tool_names=["Edit"],
                       subject="coding"),
        ]
        events = [
            _make_event(t0, source_kind="browser", kind="visit", text="page1",
                        tool_input={"url": "http://a"}),
            _make_event(t1, source_kind="browser", kind="visit", text="page2",
                        tool_input={"url": "http://b"}),
            _make_event(t2, source_kind="browser", kind="visit", text="page3",
                        tool_input={"url": "http://c"}),
            _make_event(t3, source_kind="browser", kind="visit", text="page4",
                        tool_input={"url": "http://d"}),
        ]
        refined = detect_parallel_tasks(tasks, events)
        browser = [t for t in refined if t.get("source_kind") == "browser"]
        self.assertEqual(len(browser), 1)
        bt = browser[0]
        # Active should be ~10 min (5min + 5min), NOT the full ~11h span.
        # The collar formula would have given min(11h, 4*5min=20min) = 20min.
        # The inter-event-span gives 5+5=10min.
        active_min = (bt.get("active_seconds") or 0) / 60
        self.assertLess(active_min, 20,
                        f"Active should be <20min (no collar inflation), got {active_min:.1f}min")
        self.assertGreater(active_min, 5,
                           f"Active should be >5min (real browsing), got {active_min:.1f}min")
        # Wall span should be the full ~11h
        wall_h = (bt.get("wall_clock_seconds") or 0) / 3600
        self.assertGreater(wall_h, 10)
        # Excised gaps should be large (the 10h overnight gap)
        excised_h = (bt.get("excised_gap_seconds") or 0) / 3600
        self.assertGreater(excised_h, 9, f"Overnight gap should be excised, got {excised_h:.1f}h")

    def test_continuous_browsing_not_deflated(self):
        """Browser events with no big gaps → active ≈ wall (genuine research)."""
        # 6 visits, each 5 min apart — continuous 25-min session
        t0 = _ts(0)
        events = []
        for i in range(6):
            events.append(_make_event(_ts(i * 5), source_kind="browser",
                                      kind="visit", text=f"page{i}",
                                      tool_input={"url": f"http://p{i}"}))
        tasks = [
            _make_task("implicit-1", t0, _ts(30),
                       source_kind="ai_session",
                       tool_calls=5, tool_names=["Edit"],
                       subject="coding"),
        ]
        refined = detect_parallel_tasks(tasks, events)
        browser = [t for t in refined if t.get("source_kind") == "browser"]
        self.assertEqual(len(browser), 1)
        bt = browser[0]
        # Active should be ~25 min (5 gaps × 5 min each)
        active_min = (bt.get("active_seconds") or 0) / 60
        self.assertGreater(active_min, 20,
                           f"Continuous browsing should be ~25min, got {active_min:.1f}min")
        # Excised should be ~0 (no gaps > 30min)
        excised_min = (bt.get("excised_gap_seconds") or 0) / 60
        self.assertLess(excised_min, 1,
                        f"No gaps to excise, got {excised_min:.1f}min")

    def test_single_visit_gets_minimum(self):
        """A single browser visit gets a 5-min minimum (we know it happened)."""
        t0 = _ts(0)
        events = [
            _make_event(t0, source_kind="browser", kind="visit", text="page",
                        tool_input={"url": "http://x"}),
        ]
        tasks = [
            _make_task("implicit-1", t0, _ts(60),
                       source_kind="ai_session",
                       tool_calls=5, tool_names=["Edit"],
                       subject="coding"),
        ]
        refined = detect_parallel_tasks(tasks, events)
        browser = [t for t in refined if t.get("source_kind") == "browser"]
        self.assertEqual(len(browser), 1)
        bt = browser[0]
        active_min = (bt.get("active_seconds") or 0) / 60
        self.assertGreaterEqual(active_min, 1,
                                f"Single visit should have non-zero active, got {active_min:.1f}min")


if __name__ == "__main__":
    unittest.main()
