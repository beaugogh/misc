"""Tests for the drill-down & root-cause analysis module (Phase 10.2).

Run with: python -m unittest tests.test_drill_down -v
"""

import unittest
import os
import sys

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from sources import make_event
from drill_down import (
    detect_stages,
    detect_markers,
    generate_narrative,
    drill_down,
    _detect_error_clusters,
    _detect_retry_loops,
    _detect_user_corrections,
    _add_time_sink_markers,
    _is_correction_text,
)


# ---------------------------------------------------------------------------
# Helpers — build synthetic tasks and events.
# ---------------------------------------------------------------------------

T0 = 1782900000.0  # base timestamp (2026-07-01 10:00:00 UTC)


def _ev(
    kind="tool_use",
    ts=0.0,
    tool_name=None,
    tool_input=None,
    tool_is_error=None,
    tool_use_id=None,
    text=None,
    cwd="/proj",
    session_id="test-session",
    source="claude_code",
    source_kind="ai_session",
):
    """Build a synthetic event with sensible defaults."""
    return make_event(
        source=source,
        source_kind=source_kind,
        session_id=session_id,
        cwd=cwd,
        git_branch="main",
        timestamp=T0 + ts,
        kind=kind,
        text=text,
        tool_name=tool_name,
        tool_input=tool_input,
        tool_is_error=tool_is_error,
        tool_use_id=tool_use_id,
    )


def _make_task(events, subject="test task", active_seconds=None, duration_seconds=None):
    """Build a minimal task dict with the fields drill_down needs."""
    ts = [e["timestamp"] for e in events if e.get("timestamp") is not None]
    start = min(ts) if ts else 0.0
    end = max(ts) if ts else 0.0
    wall = end - start if end >= start else 0.0
    tool_uses = [e for e in events if e.get("kind") == "tool_use"]
    tool_names = sorted({e.get("tool_name") for e in tool_uses if e.get("tool_name")})
    return {
        "id": "test-1",
        "flavor": "implicit",
        "subject": subject,
        "start": start,
        "end": end,
        "duration_seconds": duration_seconds if duration_seconds is not None else wall,
        "wall_clock_seconds": wall,
        "active_seconds": active_seconds if active_seconds is not None else wall,
        "event_count": len(events),
        "tool_names": tool_names,
        "events": events,
    }


# ---------------------------------------------------------------------------
# Test stage detection
# ---------------------------------------------------------------------------

class TestStageDetection(unittest.TestCase):
    """Tests for detect_stages()."""

    def test_clear_tool_shift_produces_2_stages(self):
        """A task with a clear shift from Edit cluster to WebSearch cluster
        should produce >=2 stages."""
        events = []
        # Stage 1: Edit cluster on a file
        for i in range(12):
            events.append(_ev(
                kind="tool_use", ts=i * 10,
                tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id=f"tu_edit_{i}",
            ))
            events.append(_ev(
                kind="tool_result", ts=i * 10 + 1,
                tool_use_id=f"tu_edit_{i}",
                tool_is_error=False,
            ))
        # Stage 2: WebSearch cluster
        for i in range(12):
            events.append(_ev(
                kind="tool_use", ts=200 + i * 10,
                tool_name="WebSearch",
                tool_input={"query": f"pelt penalty tuning {i}"},
                tool_use_id=f"tu_search_{i}",
            ))
            events.append(_ev(
                kind="tool_result", ts=200 + i * 10 + 1,
                tool_use_id=f"tu_search_{i}",
                tool_is_error=False,
            ))

        task = _make_task(events, subject="edit then search")
        stages = detect_stages(task)

        self.assertGreaterEqual(len(stages), 2, f"Expected >=2 stages, got {len(stages)}")
        # The first stage should have Edit in its tools, the last should have WebSearch.
        self.assertIn("Edit", stages[0]["tool_names"])
        self.assertIn("WebSearch", stages[-1]["tool_names"])

    def test_single_stage_task_with_homogeneous_events(self):
        """A small set of homogeneous events should produce 1 stage."""
        events = [
            _ev(kind="user_message", ts=0, text="do something"),
            _ev(kind="tool_use", ts=10, tool_name="Bash", tool_input={"command": "ls"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1", tool_is_error=False),
        ]
        task = _make_task(events, subject="simple task")
        stages = detect_stages(task)
        self.assertEqual(len(stages), 1)
        self.assertEqual(stages[0]["stage_idx"], 0)
        self.assertEqual(stages[0]["event_count"], 3)

    def test_cwd_shift_creates_boundary(self):
        """Events with a cwd shift should produce >=2 stages."""
        events = [
            _ev(kind="user_message", ts=0, text="work on A", cwd="/projA"),
            _ev(kind="tool_use", ts=10, tool_name="Read", tool_input={"file_path": "/projA/a.py"}, tool_use_id="tu1", cwd="/projA"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1", cwd="/projA"),
            _ev(kind="tool_use", ts=20, tool_name="Read", tool_input={"file_path": "/projB/b.py"}, tool_use_id="tu2", cwd="/projB"),
            _ev(kind="tool_result", ts=21, tool_use_id="tu2", cwd="/projB"),
            _ev(kind="user_message", ts=30, text="now work on B", cwd="/projB"),
        ]
        task = _make_task(events, subject="two projects")
        stages = detect_stages(task)
        self.assertGreaterEqual(len(stages), 2)

    def test_large_gap_creates_boundary(self):
        """A >10min gap between events should produce >=2 stages."""
        events = [
            _ev(kind="user_message", ts=0, text="first part"),
            _ev(kind="tool_use", ts=60, tool_name="Bash", tool_input={"command": "echo hi"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=61, tool_use_id="tu1"),
            # 15min gap
            _ev(kind="user_message", ts=960, text="second part"),
            _ev(kind="tool_use", ts=1020, tool_name="Bash", tool_input={"command": "echo bye"}, tool_use_id="tu2"),
            _ev(kind="tool_result", ts=1021, tool_use_id="tu2"),
        ]
        task = _make_task(events, subject="gap task")
        stages = detect_stages(task)
        self.assertGreaterEqual(len(stages), 2)

    def test_stage_dict_shape(self):
        """Each stage dict has all required fields."""
        events = [
            _ev(kind="user_message", ts=0, text="hello"),
            _ev(kind="tool_use", ts=10, tool_name="Bash", tool_input={"command": "ls"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1"),
        ]
        task = _make_task(events)
        stages = detect_stages(task)
        self.assertEqual(len(stages), 1)
        s = stages[0]
        for field in ("stage_idx", "start", "end", "duration_seconds",
                       "active_seconds", "event_count", "tool_names",
                       "summary", "markers"):
            self.assertIn(field, s, f"Stage missing field: {field}")
        self.assertIsInstance(s["markers"], list)

    def test_stage_summary_includes_dominant_tool(self):
        """The stage summary should mention the dominant tool."""
        events = [
            _ev(kind="user_message", ts=0, text="edit the file"),
            _ev(kind="tool_use", ts=10, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1"),
        ]
        task = _make_task(events)
        stages = detect_stages(task)
        self.assertIn("Edit", stages[0]["summary"])

    def test_empty_task_returns_empty_list(self):
        """A task with no events returns an empty stage list."""
        task = _make_task([], subject="empty")
        stages = detect_stages(task)
        self.assertEqual(stages, [])

    def test_user_correction_creates_boundary(self):
        """A user correction message should create a stage boundary."""
        events = [
            _ev(kind="user_message", ts=0, text="do the thing"),
            _ev(kind="tool_use", ts=10, tool_name="Bash", tool_input={"command": "ls"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1"),
            _ev(kind="assistant_message", ts=20, text="done"),
            _ev(kind="user_message", ts=30, text="no, that's wrong, fix it"),
            _ev(kind="tool_use", ts=40, tool_name="Bash", tool_input={"command": "ls -la"}, tool_use_id="tu2"),
            _ev(kind="tool_result", ts=41, tool_use_id="tu2"),
        ]
        task = _make_task(events, subject="correction task")
        stages = detect_stages(task)
        self.assertGreaterEqual(len(stages), 2)


# ---------------------------------------------------------------------------
# Test error-cluster markers
# ---------------------------------------------------------------------------

class TestErrorClusterMarker(unittest.TestCase):
    """Tests for error cluster detection."""

    def test_3_consecutive_errors_produce_marker(self):
        """3 consecutive is_error tool_results should produce an error_cluster marker."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Bash", tool_input={"command": "bad1"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=1, tool_use_id="tu1", tool_is_error=True),
            _ev(kind="tool_use", ts=2, tool_name="Bash", tool_input={"command": "bad2"}, tool_use_id="tu2"),
            _ev(kind="tool_result", ts=3, tool_use_id="tu2", tool_is_error=True),
            _ev(kind="tool_use", ts=4, tool_name="Bash", tool_input={"command": "bad3"}, tool_use_id="tu3"),
            _ev(kind="tool_result", ts=5, tool_use_id="tu3", tool_is_error=True),
        ]
        markers = _detect_error_clusters(events)
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0]["type"], "error_cluster")
        self.assertEqual(markers[0]["count"], 3)
        self.assertIn("Bash", markers[0]["tools"])

    def test_single_error_no_cluster(self):
        """A single error should NOT produce an error_cluster marker (need >=2)."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Bash", tool_input={"command": "bad"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=1, tool_use_id="tu1", tool_is_error=True),
            _ev(kind="tool_use", ts=2, tool_name="Bash", tool_input={"command": "good"}, tool_use_id="tu2"),
            _ev(kind="tool_result", ts=3, tool_use_id="tu2", tool_is_error=False),
        ]
        markers = _detect_error_clusters(events)
        self.assertEqual(len(markers), 0)

    def test_non_consecutive_errors_no_cluster(self):
        """Errors separated by a success should NOT form a cluster."""
        events = [
            _ev(kind="tool_result", ts=0, tool_use_id="tu1", tool_is_error=True),
            _ev(kind="tool_result", ts=1, tool_use_id="tu2", tool_is_error=False),
            _ev(kind="tool_result", ts=2, tool_use_id="tu3", tool_is_error=True),
        ]
        markers = _detect_error_clusters(events)
        self.assertEqual(len(markers), 0)

    def test_error_cluster_message_format(self):
        """The error_cluster marker message should mention count and tool."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Edit", tool_input={"file_path": "/proj/f.py"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=1, tool_use_id="tu1", tool_is_error=True),
            _ev(kind="tool_use", ts=2, tool_name="Edit", tool_input={"file_path": "/proj/f.py"}, tool_use_id="tu2"),
            _ev(kind="tool_result", ts=3, tool_use_id="tu2", tool_is_error=True),
        ]
        markers = _detect_error_clusters(events)
        self.assertEqual(len(markers), 1)
        msg = markers[0]["message"]
        self.assertIn("2", msg)
        self.assertIn("Edit", msg)


# ---------------------------------------------------------------------------
# Test retry-loop markers
# ---------------------------------------------------------------------------

class TestRetryLoopMarker(unittest.TestCase):
    """Tests for retry loop detection."""

    def test_same_tool_3x_produces_marker(self):
        """Same tool+identical operation attempted 3x within 5 min should produce a retry_loop marker."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu1"),
            _ev(kind="tool_use", ts=60, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu2"),
            _ev(kind="tool_use", ts=120, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu3"),
        ]
        markers = _detect_retry_loops(events)
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0]["type"], "retry_loop")
        self.assertEqual(markers[0]["tool"], "Edit")
        self.assertEqual(markers[0]["count"], 3)

    def test_distinct_edits_same_file_no_retry(self):
        """Two distinct Edits on the same file (different old/new strings) should
        NOT produce a retry_loop marker — they are different operations."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "foo", "new_string": "bar"},
                tool_use_id="tu1"),
            _ev(kind="tool_use", ts=60, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "baz", "new_string": "qux"},
                tool_use_id="tu2"),
        ]
        markers = _detect_retry_loops(events)
        self.assertEqual(len(markers), 0)

    def test_read_excluded_from_retry_detection(self):
        """Re-reading the same file multiple times should NOT produce a retry_loop
        marker — re-reading is a normal reference lookup, not a retry."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Read",
                tool_input={"file_path": "/proj/main.py"},
                tool_use_id="tu1"),
            _ev(kind="tool_use", ts=30, tool_name="Read",
                tool_input={"file_path": "/proj/main.py"},
                tool_use_id="tu2"),
            _ev(kind="tool_use", ts=60, tool_name="Read",
                tool_input={"file_path": "/proj/main.py"},
                tool_use_id="tu3"),
        ]
        markers = _detect_retry_loops(events)
        self.assertEqual(len(markers), 0)

    def test_same_edit_2x_produces_retry(self):
        """The same Edit operation (identical old/new strings) attempted 2x
        within 5 min IS a retry and should produce a marker."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu1"),
            _ev(kind="tool_use", ts=60, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu2"),
        ]
        markers = _detect_retry_loops(events)
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0]["count"], 2)

    def test_different_tools_no_retry(self):
        """Different tools on different targets should NOT produce a retry marker."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Edit",
                tool_input={"file_path": "/proj/a.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu1"),
            _ev(kind="tool_use", ts=60, tool_name="Bash",
                tool_input={"command": "ls"},
                tool_use_id="tu2"),
        ]
        markers = _detect_retry_loops(events)
        self.assertEqual(len(markers), 0)

    def test_retry_outside_window_no_marker(self):
        """Same tool+identical operation but >5min apart should NOT produce a retry marker."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu1"),
            # 6min later — outside the 5min window
            _ev(kind="tool_use", ts=360, tool_name="Edit",
                tool_input={"file_path": "/proj/main.py", "old_string": "a", "new_string": "b"},
                tool_use_id="tu2"),
        ]
        markers = _detect_retry_loops(events)
        self.assertEqual(len(markers), 0)

    def test_retry_message_format(self):
        """The retry_loop marker message should mention tool and count."""
        events = [
            _ev(kind="tool_use", ts=0, tool_name="Bash",
                tool_input={"command": "make test"},
                tool_use_id="tu1"),
            _ev(kind="tool_use", ts=30, tool_name="Bash",
                tool_input={"command": "make test"},
                tool_use_id="tu2"),
        ]
        markers = _detect_retry_loops(events)
        self.assertEqual(len(markers), 1)
        msg = markers[0]["message"]
        self.assertIn("Bash", msg)
        self.assertIn("2", msg)


# ---------------------------------------------------------------------------
# Test user-correction markers
# ---------------------------------------------------------------------------

class TestUserCorrectionMarker(unittest.TestCase):
    """Tests for user correction detection."""

    def test_correction_with_no_do_x_instead(self):
        """A user message with 'no, do X instead' should produce a correction marker."""
        events = [
            _ev(kind="user_message", ts=0, text="no, do X instead"),
        ]
        markers = _detect_user_corrections(events)
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0]["type"], "user_correction")
        self.assertIn("no, do X instead", markers[0]["snippet"])

    def test_chinese_correction(self):
        """A Chinese correction message should be detected."""
        events = [
            _ev(kind="user_message", ts=0, text="不对，应该是另一个方案"),
        ]
        markers = _detect_user_corrections(events)
        self.assertEqual(len(markers), 1)

    def test_non_correction_not_marked(self):
        """A normal user message should NOT produce a correction marker."""
        events = [
            _ev(kind="user_message", ts=0, text="please help me with this task"),
        ]
        markers = _detect_user_corrections(events)
        self.assertEqual(len(markers), 0)

    def test_correction_marker_has_timestamp_and_snippet(self):
        """The correction marker should carry a timestamp and snippet."""
        events = [
            _ev(kind="user_message", ts=42, text="wrong, that's not right"),
        ]
        markers = _detect_user_corrections(events)
        self.assertEqual(len(markers), 1)
        self.assertGreater(markers[0]["ts"], 0)
        self.assertTrue(len(markers[0]["snippet"]) > 0)

    # --- C5 negative tests: phrases that should NOT trigger correction ---

    def test_no_correction_for_fix_the_typo(self):
        """'fix the typo in the README' is a task instruction, NOT a correction."""
        self.assertFalse(_is_correction_text("fix the typo in the README"))

    def test_no_correction_for_no_problem(self):
        """'no problem, go ahead' is an affirmation, NOT a correction."""
        self.assertFalse(_is_correction_text("no problem, go ahead"))

    def test_no_correction_for_please_wait(self):
        """'please wait a moment' is patience, NOT a correction."""
        self.assertFalse(_is_correction_text("please wait a moment"))

    def test_no_correction_for_actually_thats_correct(self):
        """'actually, that's correct' is a confirmation, NOT a correction."""
        self.assertFalse(_is_correction_text("actually, that's correct"))

    def test_no_correction_for_should_be_right(self):
        """'This should be the right approach' is a statement, NOT a correction."""
        self.assertFalse(_is_correction_text("This should be the right approach"))

    def test_no_correction_for_routine_task_text(self):
        """Routine task instructions should not trigger correction markers."""
        self.assertFalse(_is_correction_text("please fix the typo in the README"))

    # --- C5 positive tests: phrases that SHOULD trigger correction ---

    def test_correction_for_no_thats_wrong(self):
        """'no, that's wrong' IS a correction — leads with 'no,'."""
        self.assertTrue(_is_correction_text("no, that's wrong"))

    def test_correction_for_chinese_budui(self):
        """'不对，这里应该是' IS a correction — leads with '不对'."""
        self.assertTrue(_is_correction_text("不对，这里应该是"))

    def test_correction_for_wrong_at_start(self):
        """'wrong, that's not right' IS a correction — leads with 'wrong'."""
        self.assertTrue(_is_correction_text("wrong, that's not right"))

    def test_correction_for_didnt_work(self):
        """'didn't work, try again' IS a correction signal."""
        self.assertTrue(_is_correction_text("didn't work, try again"))

    def test_no_correction_for_keyword_mid_message(self):
        """A correction keyword buried mid-message should NOT trigger —
        'I think we should fix the bug' has 'fix' in the middle, not at the start."""
        self.assertFalse(_is_correction_text("I think we should fix the bug"))


# ---------------------------------------------------------------------------
# Test time-sink markers
# ---------------------------------------------------------------------------

class TestTimeSinkMarker(unittest.TestCase):
    """Tests for time-sink marker detection."""

    def test_idle_stage_produces_time_sink_marker(self):
        """A stage with high wall/low active should produce a time_sink_idle marker."""
        stages = [
            {
                "stage_idx": 0,
                "start": T0,
                "end": T0 + 1200,  # 20min wall
                "duration_seconds": 1200,
                "active_seconds": 60,  # 1min active — ratio 0.05
                "event_count": 3,
                "tool_names": ["Bash"],
                "summary": "Bash cluster",
                "markers": [],
            },
            {
                "stage_idx": 1,
                "start": T0 + 1200,
                "end": T0 + 1800,
                "duration_seconds": 600,
                "active_seconds": 500,
                "event_count": 5,
                "tool_names": ["Edit"],
                "summary": "Edit cluster",
                "markers": [],
            },
        ]
        _add_time_sink_markers(stages, stages)
        idle_markers = [m for m in stages[0]["markers"] if m["type"] == "time_sink_idle"]
        self.assertEqual(len(idle_markers), 1)
        self.assertIn("idle", idle_markers[0]["message"].lower() + idle_markers[0]["type"])

    def test_short_stage_no_idle_marker(self):
        """A stage under 10min should not get an idle marker even with low ratio."""
        stages = [
            {
                "stage_idx": 0,
                "start": T0,
                "end": T0 + 300,  # 5min wall
                "duration_seconds": 300,
                "active_seconds": 10,  # low active but short duration
                "event_count": 2,
                "tool_names": [],
                "summary": "short",
                "markers": [],
            },
        ]
        _add_time_sink_markers(stages, stages)
        idle_markers = [m for m in stages[0]["markers"] if m["type"] == "time_sink_idle"]
        self.assertEqual(len(idle_markers), 0)


# ---------------------------------------------------------------------------
# Test narrative generation
# ---------------------------------------------------------------------------

class TestNarrativeGeneration(unittest.TestCase):
    """Tests for generate_narrative()."""

    def test_no_markers_says_no_stuck_points(self):
        """A simple 1-stage task with no markers should say 'No stuck points detected.'"""
        task = _make_task(
            [_ev(kind="user_message", ts=0, text="hello")],
            subject="simple",
        )
        stages = [{
            "stage_idx": 0,
            "start": T0,
            "end": T0 + 60,
            "duration_seconds": 60,
            "active_seconds": 60,
            "event_count": 1,
            "tool_names": [],
            "summary": "hello",
            "markers": [],
        }]
        narrative = generate_narrative(task, stages)
        self.assertIn("No stuck points detected", narrative)

    def test_narrative_with_markers_mentions_key_events(self):
        """A task with stages+markers should produce a narrative mentioning the key events."""
        task = _make_task(
            [_ev(kind="user_message", ts=0, text="do it")],
            subject="stuck task",
            active_seconds=3 * 3600,  # 3h active — above threshold
            duration_seconds=4 * 3600,
        )
        stages = [
            {
                "stage_idx": 0,
                "start": T0,
                "end": T0 + 1800,
                "duration_seconds": 1800,
                "active_seconds": 1500,
                "event_count": 10,
                "tool_names": ["Edit"],
                "summary": "Edit cluster on main.py",
                "markers": [
                    {"type": "error_cluster", "start": T0 + 100, "count": 3,
                     "tools": ["Edit"], "message": "3 consecutive errors on Edit"},
                ],
            },
            {
                "stage_idx": 1,
                "start": T0 + 1800,
                "end": T0 + 3600,
                "duration_seconds": 1800,
                "active_seconds": 1500,
                "event_count": 5,
                "tool_names": ["Bash"],
                "summary": "Bash cluster",
                "markers": [],
            },
        ]
        narrative = generate_narrative(task, stages)
        self.assertIsInstance(narrative, str)
        self.assertGreater(len(narrative), 20)
        # Should mention stages and/or errors.
        narrative_lower = narrative.lower()
        self.assertTrue(
            "stage" in narrative_lower or "error" in narrative_lower,
            f"Narrative should mention stages or errors: {narrative}"
        )

    def test_narrative_under_5_sentences(self):
        """The narrative should be at most 5 sentences."""
        task = _make_task(
            [_ev(kind="user_message", ts=0, text="big task")],
            subject="big",
            active_seconds=5 * 3600,
            duration_seconds=6 * 3600,
        )
        stages = []
        for i in range(6):
            stages.append({
                "stage_idx": i,
                "start": T0 + i * 3600,
                "end": T0 + (i + 1) * 3600,
                "duration_seconds": 3600,
                "active_seconds": 3000,
                "event_count": 8,
                "tool_names": ["Edit"],
                "summary": f"Stage {i}",
                "markers": [
                    {"type": "error_cluster", "start": T0 + i * 3600 + 100,
                     "count": 2, "tools": ["Edit"],
                     "message": "2 consecutive errors on Edit"},
                    {"type": "retry_loop", "tool": "Edit", "start": T0 + i * 3600 + 200,
                     "count": 2, "target": "/proj/f.py",
                     "message": "Retried Edit 2x on f.py"},
                ],
            })
        narrative = generate_narrative(task, stages)
        sentence_count = narrative.count(". ") + 1  # rough sentence count
        self.assertLessEqual(sentence_count, 6, f"Narrative too long ({sentence_count} sentences): {narrative}")

    def test_narrative_mentions_error_and_retry(self):
        """Narrative should mention errors and retries when present."""
        task = _make_task(
            [_ev(kind="user_message", ts=0, text="task")],
            subject="task with retries",
            active_seconds=3 * 3600,
            duration_seconds=4 * 3600,
        )
        stages = [
            {
                "stage_idx": 0,
                "start": T0,
                "end": T0 + 1800,
                "duration_seconds": 1800,
                "active_seconds": 1500,
                "event_count": 10,
                "tool_names": ["Bash"],
                "summary": "Bash cluster",
                "markers": [
                    {"type": "retry_loop", "tool": "Bash", "start": T0 + 100,
                     "count": 4, "target": "make test",
                     "message": "Retried Bash 4x on make test"},
                ],
            },
            {
                "stage_idx": 1,
                "start": T0 + 1800,
                "end": T0 + 3600,
                "duration_seconds": 1800,
                "active_seconds": 1500,
                "event_count": 5,
                "tool_names": ["Edit"],
                "summary": "Edit cluster",
                "markers": [],
            },
        ]
        narrative = generate_narrative(task, stages)
        self.assertIn("retried", narrative.lower() + narrative)
        self.assertIn("Bash", narrative)

    def test_empty_stages_narrative(self):
        """A task with no stages should still get a valid narrative."""
        task = _make_task(
            [_ev(kind="user_message", ts=0, text="hello")],
            subject="empty stages",
        )
        narrative = generate_narrative(task, [])
        self.assertIsInstance(narrative, str)
        self.assertGreater(len(narrative), 0)


# ---------------------------------------------------------------------------
# Test top-level drill_down()
# ---------------------------------------------------------------------------

class TestDrillDown(unittest.TestCase):
    """Tests for the top-level drill_down() function."""

    def test_drill_down_returns_all_fields(self):
        """drill_down() should return a dict with all required fields."""
        events = [
            _ev(kind="user_message", ts=0, text="do something"),
            _ev(kind="tool_use", ts=10, tool_name="Bash", tool_input={"command": "ls"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1"),
        ]
        task = _make_task(events, subject="test task")
        result = drill_down(task)
        for field in ("task_subject", "total_active_seconds", "total_wall_seconds",
                       "stages", "all_markers", "narrative"):
            self.assertIn(field, result, f"Result missing field: {field}")
        self.assertEqual(result["task_subject"], "test task")
        self.assertIsInstance(result["stages"], list)
        self.assertIsInstance(result["all_markers"], list)
        self.assertIsInstance(result["narrative"], str)

    def test_drill_down_with_stuck_task(self):
        """A synthetic stuck task should produce markers and a meaningful narrative."""
        events = [
            # Initial work
            _ev(kind="user_message", ts=0, text="fix the build"),
            _ev(kind="tool_use", ts=10, tool_name="Bash", tool_input={"command": "make test"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1", tool_is_error=True),
            _ev(kind="tool_use", ts=30, tool_name="Bash", tool_input={"command": "make test"}, tool_use_id="tu2"),
            _ev(kind="tool_result", ts=31, tool_use_id="tu2", tool_is_error=True),
            _ev(kind="tool_use", ts=60, tool_name="Bash", tool_input={"command": "make test"}, tool_use_id="tu3"),
            _ev(kind="tool_result", ts=61, tool_use_id="tu3", tool_is_error=True),
            # User correction
            _ev(kind="user_message", ts=120, text="no, the issue is in config not code"),
            # Fix and succeed
            _ev(kind="tool_use", ts=130, tool_name="Edit",
                tool_input={"file_path": "/proj/config.yml", "old_string": "a", "new_string": "b"},
                tool_use_id="tu4"),
            _ev(kind="tool_result", ts=131, tool_use_id="tu4"),
        ]
        task = _make_task(events, subject="fix build")
        result = drill_down(task)
        # Should have at least one marker (error cluster, retry loop, or correction).
        self.assertGreater(len(result["all_markers"]), 0,
                           "Expected at least one marker for this stuck task")
        # Narrative should be non-empty.
        self.assertGreater(len(result["narrative"]), 10)

    def test_drill_down_simple_task_no_markers(self):
        """A simple task with no errors should produce no markers."""
        events = [
            _ev(kind="user_message", ts=0, text="say hello"),
            _ev(kind="tool_use", ts=10, tool_name="Bash", tool_input={"command": "echo hi"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1", tool_is_error=False),
        ]
        task = _make_task(events, subject="simple")
        result = drill_down(task)
        self.assertEqual(len(result["all_markers"]), 0)
        self.assertIn("No stuck points", result["narrative"])

    def test_drill_down_does_not_mutate_task(self):
        """drill_down() should not modify the input task dict."""
        events = [
            _ev(kind="user_message", ts=0, text="hello"),
            _ev(kind="tool_use", ts=10, tool_name="Bash", tool_input={"command": "ls"}, tool_use_id="tu1"),
            _ev(kind="tool_result", ts=11, tool_use_id="tu1"),
        ]
        task = _make_task(events, subject="test")
        task_copy = dict(task)
        task_copy["events"] = list(task["events"])
        _ = drill_down(task)
        # Original task should be unchanged.
        self.assertEqual(task["subject"], task_copy["subject"])
        self.assertEqual(len(task["events"]), len(task_copy["events"]))
        self.assertEqual(task.get("active_seconds"), task_copy.get("active_seconds"))

    def test_drill_down_stage_count_matches(self):
        """The stages list in the result should match detect_stages output."""
        events = []
        for i in range(12):
            events.append(_ev(
                kind="tool_use", ts=i * 10,
                tool_name="Edit",
                tool_input={"file_path": "/proj/a.py", "old_string": "x", "new_string": "y"},
                tool_use_id=f"tu_a_{i}",
            ))
            events.append(_ev(kind="tool_result", ts=i * 10 + 1, tool_use_id=f"tu_a_{i}"))
        for i in range(12):
            events.append(_ev(
                kind="tool_use", ts=200 + i * 10,
                tool_name="WebSearch",
                tool_input={"query": f"test {i}"},
                tool_use_id=f"tu_b_{i}",
            ))
            events.append(_ev(kind="tool_result", ts=200 + i * 10 + 1, tool_use_id=f"tu_b_{i}"))
        task = _make_task(events, subject="two phases")
        result = drill_down(task)
        self.assertGreaterEqual(len(result["stages"]), 2)

    def test_detect_markers_works_on_any_event_list(self):
        """detect_markers() should work on any list of events, not just a task's."""
        events = [
            _ev(kind="tool_result", ts=0, tool_use_id="tu1", tool_is_error=True),
            _ev(kind="tool_result", ts=1, tool_use_id="tu2", tool_is_error=True),
            _ev(kind="user_message", ts=2, text="no, wrong"),
        ]
        markers = detect_markers(events)
        # Should find at least an error cluster and a user correction.
        types = {m["type"] for m in markers}
        self.assertIn("error_cluster", types)
        self.assertIn("user_correction", types)


if __name__ == "__main__":
    unittest.main()
