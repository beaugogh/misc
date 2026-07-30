"""Tests for C7 incremental-mode fix: full-session collection, stable task IDs,
and merge-safe persistence.

Run with:
    python -m unittest tests.test_incremental -v

C7 defect summary:
  - collect_since(watermark) returned only post-watermark events, but segment()
    needs full session context to detect task boundaries (TaskCreate, gaps, cwd).
  - Synthetic task IDs (explicit-N, implicit-N) were re-numbered from 1 each run,
    causing ID collisions in save_tasks(mode='merge').

C7 fix:
  - collect_since() now yields ALL events from sessions that have ANY event after
    the watermark.
  - Task IDs are remapped to stable format: {flavor}-{session_id}-{start_timestamp}.
  - run.py filters out tasks entirely before the watermark (already processed).
  - save_tasks(mode='merge') deduplicates by task ID; stable IDs ensure correct
    dedup across runs.
"""

import unittest
import os
import sys
import json
import tempfile
import shutil

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)


def _make_jsonl_line(line_type, timestamp, message=None, cwd="/tmp", git_branch="main"):
    """Build one JSONL session line."""
    obj = {"type": line_type, "timestamp": timestamp, "cwd": cwd, "gitBranch": git_branch}
    if message is not None:
        obj["message"] = message
    return json.dumps(obj)


def _make_user_message(text):
    return {"role": "user", "content": text}


def _make_assistant_message(text, tool_uses=None, stop_reason="end_turn"):
    msg = {"role": "assistant", "content": [{"type": "text", "text": text}],
           "stop_reason": stop_reason, "usage": {"input_tokens": 10, "output_tokens": 20}}
    if tool_uses:
        msg["content"].extend(tool_uses)
    return msg


def _make_tool_use(name, tool_id, tool_input=None):
    return {"type": "tool_use", "name": name, "id": tool_id, "input": tool_input or {}}


def _make_tool_result(tool_id, text=None, is_error=False):
    content = [{"type": "text", "text": text or "ok"}]
    return {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_id,
                                          "is_error": is_error, "content": content}]}


def _make_task_create(subject):
    """A TaskCreate tool_use wrapped in an assistant message."""
    return _make_assistant_message("creating task", tool_uses=[
        _make_tool_use("TaskCreate", "tc1", {"subject": subject})
    ])


def _make_task_update(status):
    """A TaskUpdate tool_use wrapped in an assistant message."""
    return _make_assistant_message("updating task", tool_uses=[
        _make_tool_use("TaskUpdate", "tu1", {"status": status})
    ])


# ---------------------------------------------------------------------------
# Part 1: Full-session collection for incremental mode (JSONL adapters)
# ---------------------------------------------------------------------------

class TestCollectSinceFullSession(unittest.TestCase):
    """C7 Part 1: collect_since() yields ALL events from sessions with any
    post-watermark event, not just the post-watermark events."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="retro_test_")
        self.projects_dir = os.path.join(self.tmpdir, "projects")
        os.makedirs(self.projects_dir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_session(self, slug, session_id, lines):
        """Write a JSONL session file under the projects dir."""
        slug_dir = os.path.join(self.projects_dir, slug)
        os.makedirs(slug_dir, exist_ok=True)
        path = os.path.join(slug_dir, f"{session_id}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        return path

    def test_collect_since_yields_all_events_from_spanning_session(self):
        """A session with events before AND after the watermark: collect_since
        returns ALL events from that session, not just post-watermark ones."""
        from claude_code_adapter import ClaudeCodeAdapter

        # Session with: user message (t=1000), assistant (t=1001),
        # TaskCreate (t=1002), TaskUpdate(completed) (t=2000)
        # Note: TaskCreate/TaskUpdate are tool_use blocks inside assistant messages,
        # so each expands to: 1 assistant_message + 1 tool_use = 2 events.
        # Total: 1 (user) + 1 (assistant) + 2 (assistant+TaskCreate) + 2 (assistant+TaskUpdate) = 6
        lines = [
            _make_jsonl_line("user", "2026-01-01T00:16:40.000Z",
                             _make_user_message("do something")),
            _make_jsonl_line("assistant", "2026-01-01T00:16:41.000Z",
                             _make_assistant_message("ok")),
            _make_jsonl_line("assistant", "2026-01-01T00:16:42.000Z",
                             _make_task_create("my task")),
            _make_jsonl_line("assistant", "2026-01-01T00:33:20.000Z",
                             _make_task_update("completed")),
        ]
        self._write_session("proj", "sess1", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)

        # Watermark at t=1500 (between TaskCreate and TaskUpdate).
        # 2026-01-01T00:25:00Z = 1767227100.0 epoch seconds.
        # But we can use a simpler approach: the timestamps parse to:
        # 2026-01-01T00:16:40Z = ~1767226600
        # 2026-01-01T00:33:20Z = ~1767227600
        # Set watermark between them.
        watermark = 1767227100.0  # ~00:25:00

        events_since = list(adapter.collect_since(watermark))

        # Should return ALL 6 events (full session), not just the post-watermark ones.
        self.assertEqual(len(events_since), 6,
                         "collect_since should yield ALL events from a spanning session, "
                         f"got {len(events_since)} instead of 6")

    def test_collect_since_skips_fully_old_session(self):
        """A session with ALL events before the watermark: collect_since returns nothing."""
        from claude_code_adapter import ClaudeCodeAdapter

        lines = [
            _make_jsonl_line("user", "2026-01-01T00:00:00.000Z",
                             _make_user_message("old message")),
            _make_jsonl_line("assistant", "2026-01-01T00:00:01.000Z",
                             _make_assistant_message("old reply")),
        ]
        self._write_session("proj", "old_sess", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)
        # Watermark well after these events.
        watermark = 1767227100.0
        events_since = list(adapter.collect_since(watermark))
        self.assertEqual(len(events_since), 0,
                         "collect_since should skip fully-old sessions")

    def test_collect_since_includes_fully_new_session(self):
        """A session with ALL events after the watermark: collect_since returns all."""
        from claude_code_adapter import ClaudeCodeAdapter

        lines = [
            _make_jsonl_line("user", "2026-01-01T01:00:00.000Z",
                             _make_user_message("new message")),
            _make_jsonl_line("assistant", "2026-01-01T01:00:01.000Z",
                             _make_assistant_message("new reply")),
        ]
        self._write_session("proj", "new_sess", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)
        watermark = 1767227100.0  # before these events
        events_since = list(adapter.collect_since(watermark))
        self.assertEqual(len(events_since), 2)

    def test_collect_since_none_returns_all(self):
        """collect_since(None) does full collect."""
        from claude_code_adapter import ClaudeCodeAdapter

        lines = [
            _make_jsonl_line("user", "2026-01-01T00:00:00.000Z",
                             _make_user_message("msg")),
        ]
        self._write_session("proj", "sess1", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)
        events = list(adapter.collect_since(None))
        self.assertEqual(len(events), 1)

    def test_segment_detects_boundary_with_full_session(self):
        """segment() correctly detects a TaskCreate boundary when collect_since
        returns the full session (TaskCreate before watermark, TaskUpdate after)."""
        from claude_code_adapter import ClaudeCodeAdapter
        from segment_tasks import segment

        lines = [
            _make_jsonl_line("user", "2026-01-01T00:16:40.000Z",
                             _make_user_message("start")),
            _make_jsonl_line("assistant", "2026-01-01T00:16:42.000Z",
                             _make_task_create("boundary task")),
            _make_jsonl_line("assistant", "2026-01-01T00:33:20.000Z",
                             _make_task_update("completed")),
        ]
        self._write_session("proj", "sess1", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)
        watermark = 1767227100.0  # between TaskCreate and TaskUpdate

        events = list(adapter.collect_since(watermark))
        tasks = segment(events)

        # Should find 1 explicit task (the TaskCreate/TaskUpdate pair).
        explicit_tasks = [t for t in tasks if t.get("flavor") == "explicit"]
        self.assertEqual(len(explicit_tasks), 1,
                         f"Expected 1 explicit task with full-session context, "
                         f"got {len(explicit_tasks)}. "
                         f"This verifies that segment() can detect the TaskCreate "
                         f"boundary even when it's before the watermark.")
        self.assertEqual(explicit_tasks[0].get("subject"), "boundary task")
        self.assertEqual(explicit_tasks[0].get("task_status"), "completed")


# ---------------------------------------------------------------------------
# Part 1b: CodeagentAdapter (inherits ClaudeCodeAdapter logic)
# ---------------------------------------------------------------------------

class TestCodeagentCollectSince(unittest.TestCase):
    """Verify CodeagentAdapter.collect_since() also returns full sessions."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="retro_test_")
        self.projects_dir = os.path.join(self.tmpdir, "projects")
        os.makedirs(self.projects_dir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_collect_since_yields_all_with_codeagent_source(self):
        from claude_code_adapter import CodeagentAdapter

        lines = [
            _make_jsonl_line("user", "2026-01-01T00:16:40.000Z",
                             _make_user_message("pre-watermark")),
            _make_jsonl_line("assistant", "2026-01-01T00:16:41.000Z",
                             _make_assistant_message("reply")),
            _make_jsonl_line("user", "2026-01-01T00:33:20.000Z",
                             _make_user_message("post-watermark")),
        ]
        slug_dir = os.path.join(self.projects_dir, "proj")
        os.makedirs(slug_dir, exist_ok=True)
        with open(os.path.join(slug_dir, "sess1.jsonl"), "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")

        adapter = CodeagentAdapter(projects_dir=self.projects_dir)
        watermark = 1767227100.0
        events = list(adapter.collect_since(watermark))

        # All 3 events should be returned.
        self.assertEqual(len(events), 3)
        # All should have source="codeagent"
        for ev in events:
            self.assertEqual(ev["source"], "codeagent")


# ---------------------------------------------------------------------------
# Part 2: Stable task IDs
# ---------------------------------------------------------------------------

class TestStableTaskIDs(unittest.TestCase):
    """C7 Part 2: task IDs are stable across runs (same session + start => same ID)."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="retro_test_")
        self.projects_dir = os.path.join(self.tmpdir, "projects")
        os.makedirs(self.projects_dir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_session(self, slug, session_id, lines):
        slug_dir = os.path.join(self.projects_dir, slug)
        os.makedirs(slug_dir, exist_ok=True)
        path = os.path.join(slug_dir, f"{session_id}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        return path

    def test_stable_ids_across_runs(self):
        """Two runs with the same session produce the same task IDs."""
        from claude_code_adapter import ClaudeCodeAdapter
        from segment_tasks import segment
        from run import _remap_task_ids

        lines = [
            _make_jsonl_line("user", "2026-01-01T00:16:40.000Z",
                             _make_user_message("task 1")),
            _make_jsonl_line("assistant", "2026-01-01T00:16:41.000Z",
                             _make_assistant_message("reply 1", stop_reason="end_turn")),
            _make_jsonl_line("user", "2026-01-01T00:33:20.000Z",
                             _make_user_message("task 2")),
            _make_jsonl_line("assistant", "2026-01-01T00:33:21.000Z",
                             _make_assistant_message("reply 2", stop_reason="end_turn")),
        ]
        self._write_session("proj", "sess1", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)

        # Run 1: full collect (no watermark).
        events1 = list(adapter.collect())
        tasks1 = _remap_task_ids(segment(events1))

        # Run 2: same session, same collect.
        events2 = list(adapter.collect())
        tasks2 = _remap_task_ids(segment(events2))

        # IDs should match.
        ids1 = sorted(t["id"] for t in tasks1)
        ids2 = sorted(t["id"] for t in tasks2)
        self.assertEqual(ids1, ids2,
                         "Task IDs should be stable across runs with the same session")
        # Verify the ID format contains session_id and timestamp.
        for tid in ids1:
            self.assertIn("sess1", tid,
                          f"Stable ID '{tid}' should contain the session_id")
            # Should start with "implicit-" (no explicit TaskCreate in this data).
            self.assertTrue(tid.startswith("implicit-"),
                            f"Stable ID '{tid}' should start with 'implicit-'")

    def test_stable_ids_with_explicit_tasks(self):
        """Explicit tasks also get stable IDs."""
        from claude_code_adapter import ClaudeCodeAdapter
        from segment_tasks import segment
        from run import _remap_task_ids

        lines = [
            _make_jsonl_line("user", "2026-01-01T00:16:40.000Z",
                             _make_user_message("start")),
            _make_jsonl_line("assistant", "2026-01-01T00:16:42.000Z",
                             _make_task_create("explicit task")),
            _make_jsonl_line("assistant", "2026-01-01T00:33:20.000Z",
                             _make_task_update("completed")),
        ]
        self._write_session("proj", "sess42", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)
        events = list(adapter.collect())
        tasks = _remap_task_ids(segment(events))

        explicit_tasks = [t for t in tasks if t.get("flavor") == "explicit"]
        self.assertEqual(len(explicit_tasks), 1)
        tid = explicit_tasks[0]["id"]
        self.assertTrue(tid.startswith("explicit-"),
                        f"Explicit task ID should start with 'explicit-', got '{tid}'")
        self.assertIn("sess42", tid,
                       f"Stable ID should contain session_id, got '{tid}'")

    def test_stable_ids_differ_across_sessions(self):
        """Tasks from different sessions get different IDs."""
        from claude_code_adapter import ClaudeCodeAdapter
        from segment_tasks import segment
        from run import _remap_task_ids

        # Two sessions with identical event patterns.
        for sid in ["sessA", "sessB"]:
            lines = [
                _make_jsonl_line("user", "2026-01-01T00:16:40.000Z",
                                 _make_user_message("same message")),
                _make_jsonl_line("assistant", "2026-01-01T00:16:41.000Z",
                                 _make_assistant_message("same reply")),
            ]
            self._write_session("proj", sid, lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)
        events = list(adapter.collect())
        tasks = _remap_task_ids(segment(events))

        ids = [t["id"] for t in tasks]
        self.assertEqual(len(ids), len(set(ids)),
                         "Task IDs should be unique across sessions")
        # Verify each ID contains its session.
        sessA_ids = [i for i in ids if "sessA" in i]
        sessB_ids = [i for i in ids if "sessB" in i]
        self.assertEqual(len(sessA_ids), 1)
        self.assertEqual(len(sessB_ids), 1)

    def test_old_format_ids_dont_collide_with_new(self):
        """Old-format IDs (explicit-N) don't collide with new-format IDs."""
        # Old format: "explicit-1" (2 dash-separated parts, N is a number)
        # New format: "explicit-<session_id>-<timestamp>" (3+ parts, timestamp is a number)
        old_id = "explicit-1"
        new_id = "explicit-sess1-1767226600"
        self.assertNotEqual(old_id, new_id,
                            "Old and new format IDs must not collide")


# ---------------------------------------------------------------------------
# Part 3: Persistence merge safety
# ---------------------------------------------------------------------------

class TestMergePersistence(unittest.TestCase):
    """C7 Part 3: save_tasks(mode='merge') with stable IDs doesn't create duplicates."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="retro_test_")
        # Patch the DATA_DIR so tasks.jsonl goes to our temp dir.
        self._orig_data_dir = None
        import persistence
        self._orig_data_dir = persistence.DATA_DIR
        persistence.DATA_DIR = self.tmpdir
        persistence.TASKS_LOG = os.path.join(self.tmpdir, "tasks.jsonl")
        persistence.WATERMARK_FILE = os.path.join(self.tmpdir, "last_run.txt")

    def tearDown(self):
        import persistence
        persistence.DATA_DIR = self._orig_data_dir
        persistence.TASKS_LOG = os.path.join(self._orig_data_dir, "tasks.jsonl")
        persistence.WATERMARK_FILE = os.path.join(self._orig_data_dir, "last_run.txt")
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_merge_same_id_updates_not_duplicates(self):
        """Merging a task with the same stable ID updates the existing entry,
        not creates a duplicate."""
        from persistence import save_tasks, load_existing_tasks

        task_v1 = {
            "id": "implicit-sess1-1767226600",
            "flavor": "implicit",
            "subject": "original subject",
            "start": 1767226600.0,
            "end": 1767226660.0,
            "event_count": 2,
        }
        save_tasks([task_v1], mode="merge")

        # Same ID, updated subject and event_count.
        task_v2 = {
            "id": "implicit-sess1-1767226600",
            "flavor": "implicit",
            "subject": "updated subject",
            "start": 1767226600.0,
            "end": 1767226700.0,
            "event_count": 5,
        }
        save_tasks([task_v2], mode="merge")

        loaded = load_existing_tasks()
        self.assertEqual(len(loaded), 1,
                         "Merge with same stable ID should update, not duplicate")
        self.assertEqual(loaded[0]["subject"], "updated subject")
        self.assertEqual(loaded[0]["event_count"], 5)

    def test_merge_different_ids_keeps_both(self):
        """Merging tasks with different stable IDs keeps both."""
        from persistence import save_tasks, load_existing_tasks

        task_a = {"id": "implicit-sessA-1000", "flavor": "implicit", "subject": "A"}
        task_b = {"id": "implicit-sessB-2000", "flavor": "implicit", "subject": "B"}
        save_tasks([task_a], mode="merge")
        save_tasks([task_b], mode="merge")

        loaded = load_existing_tasks()
        self.assertEqual(len(loaded), 2,
                         "Different stable IDs should both be kept")

    def test_merge_incremental_run_no_duplicates(self):
        """Simulate two incremental runs: run 1 has task A (fully old, filtered out
        by run.py), run 2 has task A (updated, spanning boundary) + task B (new).
        After merge, there should be 2 tasks, not 3."""
        from persistence import save_tasks, load_existing_tasks

        # Run 1: task A was discovered.
        task_a_v1 = {
            "id": "explicit-sess1-1000",
            "flavor": "explicit",
            "subject": "task A",
            "start": 1000.0,
            "end": 1500.0,
        }
        save_tasks([task_a_v1], mode="merge")

        # Run 2: task A updated (same ID, now extends past watermark) + task B (new).
        task_a_v2 = {
            "id": "explicit-sess1-1000",
            "flavor": "explicit",
            "subject": "task A (updated)",
            "start": 1000.0,
            "end": 2000.0,  # extended
        }
        task_b = {
            "id": "implicit-sess1-1600",
            "flavor": "implicit",
            "subject": "task B (new)",
            "start": 1600.0,
            "end": 1800.0,
        }
        save_tasks([task_a_v2, task_b], mode="merge")

        loaded = load_existing_tasks()
        self.assertEqual(len(loaded), 2,
                         "Incremental merge should have 2 tasks (A updated + B new), "
                         f"got {len(loaded)}")
        ids = sorted(t["id"] for t in loaded)
        self.assertEqual(ids, ["explicit-sess1-1000", "implicit-sess1-1600"])

    def test_merge_old_format_does_not_collide(self):
        """Old-format IDs in the log don't collide with new-format IDs."""
        from persistence import save_tasks, load_existing_tasks

        # Simulate an old-format task already in the log.
        old_task = {"id": "explicit-1", "flavor": "explicit", "subject": "old"}
        save_tasks([old_task], mode="merge")

        # New-format task with a different session.
        new_task = {"id": "explicit-sess1-1000", "flavor": "explicit", "subject": "new"}
        save_tasks([new_task], mode="merge")

        loaded = load_existing_tasks()
        self.assertEqual(len(loaded), 2,
                         "Old and new format IDs should coexist without collision")


# ---------------------------------------------------------------------------
# Part 1 + 2 + 3 integration: full incremental cycle
# ---------------------------------------------------------------------------

class TestIncrementalIntegration(unittest.TestCase):
    """Integration test: full incremental cycle with spanning task."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="retro_test_")
        self.projects_dir = os.path.join(self.tmpdir, "projects")
        os.makedirs(self.projects_dir)

        # Patch persistence DATA_DIR.
        import persistence
        self._orig_data_dir = persistence.DATA_DIR
        persistence.DATA_DIR = self.tmpdir
        persistence.TASKS_LOG = os.path.join(self.tmpdir, "tasks.jsonl")
        persistence.WATERMARK_FILE = os.path.join(self.tmpdir, "last_run.txt")

    def tearDown(self):
        import persistence
        persistence.DATA_DIR = self._orig_data_dir
        persistence.TASKS_LOG = os.path.join(self._orig_data_dir, "tasks.jsonl")
        persistence.WATERMARK_FILE = os.path.join(self._orig_data_dir, "last_run.txt")
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_session(self, slug, session_id, lines):
        slug_dir = os.path.join(self.projects_dir, slug)
        os.makedirs(slug_dir, exist_ok=True)
        path = os.path.join(slug_dir, f"{session_id}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        return path

    def test_spanning_task_survives_incremental(self):
        """A task whose TaskCreate is before the watermark and TaskUpdate is after
        should be correctly segmented in incremental mode, get a stable ID, and
        merge correctly across two runs."""
        from claude_code_adapter import ClaudeCodeAdapter
        from segment_tasks import segment
        from run import _remap_task_ids, _filter_tasks_by_watermark
        from persistence import save_tasks, load_existing_tasks

        # Session: TaskCreate at t~1002, TaskUpdate(completed) at t~2000.
        lines = [
            _make_jsonl_line("user", "2026-01-01T00:16:40.000Z",
                             _make_user_message("start")),
            _make_jsonl_line("assistant", "2026-01-01T00:16:42.000Z",
                             _make_task_create("spanning task")),
            _make_jsonl_line("assistant", "2026-01-01T00:33:20.000Z",
                             _make_task_update("completed")),
        ]
        self._write_session("proj", "sess_int", lines)

        adapter = ClaudeCodeAdapter(projects_dir=self.projects_dir)

        # Run 1: full collect (no watermark).
        events1 = list(adapter.collect())
        tasks1 = _remap_task_ids(segment(events1))
        save_tasks(tasks1, mode="merge")

        # Run 1 produces an explicit task (TaskCreate/TaskUpdate pair).
        # The initial user message before TaskCreate may also form an implicit task.
        explicit1 = [t for t in tasks1 if t.get("flavor") == "explicit"]
        self.assertGreaterEqual(len(explicit1), 1,
                                "Should find at least the explicit spanning task")
        explicit1_id = explicit1[0]["id"]
        self.assertIn("sess_int", explicit1_id)
        self.assertEqual(explicit1[0].get("task_status"), "completed")

        # Run 2: incremental with watermark between TaskCreate and TaskUpdate.
        watermark = 1767227100.0  # ~00:25:00, between the two events.
        events2 = list(adapter.collect_since(watermark))
        tasks2 = _remap_task_ids(segment(events2))
        tasks2 = _filter_tasks_by_watermark(tasks2, watermark)

        # The spanning explicit task should still be detected (full session context).
        explicit2 = [t for t in tasks2 if t.get("flavor") == "explicit"]
        self.assertGreaterEqual(len(explicit2), 1,
                                "Spanning explicit task should be detected in incremental mode")
        self.assertEqual(explicit2[0]["id"], explicit1_id,
                         "Same task should get the same stable ID across runs")
        self.assertEqual(explicit2[0].get("task_status"), "completed")

        # Merge should not duplicate the explicit task.
        save_tasks(tasks2, mode="merge")
        loaded = load_existing_tasks()
        loaded_explicit = [t for t in loaded if t.get("flavor") == "explicit"
                          and t["id"] == explicit1_id]
        self.assertEqual(len(loaded_explicit), 1,
                         "Merge with stable ID should not duplicate the explicit task")

    def test_filter_removes_fully_old_tasks(self):
        """_filter_tasks_by_watermark removes tasks entirely before the watermark."""
        from run import _filter_tasks_by_watermark

        tasks = [
            {"id": "implicit-sess1-1000", "start": 1000.0, "end": 1100.0},
            {"id": "implicit-sess1-2000", "start": 2000.0, "end": 2100.0},
            {"id": "implicit-sess1-1500", "start": 1500.0, "end": 2500.0},  # spans
        ]
        watermark = 1800.0
        filtered = _filter_tasks_by_watermark(tasks, watermark)

        # Task 1 (end=1100 < 1800) should be filtered out.
        # Task 2 (end=2100 > 1800) should be kept.
        # Task 3 (end=2500 > 1800) should be kept (spans boundary).
        ids = sorted(t["id"] for t in filtered)
        self.assertEqual(ids, ["implicit-sess1-1500", "implicit-sess1-2000"])


# ---------------------------------------------------------------------------
# Part 1c: Legacy codeagent adapter (SQL-based)
# ---------------------------------------------------------------------------

class TestLegacyCodeagentCollectSince(unittest.TestCase):
    """C7 Part 1 for legacy codeagent: collect_since yields ALL messages from
    sessions that have any post-watermark message."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="retro_test_")
        import persistence
        self._orig_data_dir = persistence.DATA_DIR

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _create_test_db(self, db_path):
        """Create a minimal ngagent.db with two sessions.
        Session A: messages at t=1000 and t=3000 (spans watermark at 2000).
        Session B: messages at t=500 and t=600 (fully before watermark).
        """
        import sqlite3
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE session (id TEXT PRIMARY KEY, directory TEXT, "
                  "project_id TEXT, time_created INTEGER, time_updated INTEGER)")
        c.execute("CREATE TABLE message (id TEXT PRIMARY KEY, session_id TEXT, "
                  "time_created INTEGER, time_updated INTEGER, data TEXT)")
        c.execute("CREATE TABLE part (id TEXT PRIMARY KEY, message_id TEXT, "
                  "session_id TEXT, time_created INTEGER, time_updated INTEGER, data TEXT)")

        # Session A: messages at t=1000000ms and t=3000000ms
        c.execute("INSERT INTO session VALUES ('sessA', '/tmp/proj', NULL, 1000000, 3000000)")
        c.execute("INSERT INTO message VALUES ('msgA1', 'sessA', 1000000, 1000000, "
                  "'{\"role\":\"user\"}')")
        c.execute("INSERT INTO message VALUES ('msgA2', 'sessA', 3000000, 3000000, "
                  "'{\"role\":\"assistant\"}')")

        # Session B: messages at t=500000ms and t=600000ms (fully old)
        c.execute("INSERT INTO session VALUES ('sessB', '/tmp/other', NULL, 500000, 600000)")
        c.execute("INSERT INTO message VALUES ('msgB1', 'sessB', 500000, 500000, "
                  "'{\"role\":\"user\"}')")
        c.execute("INSERT INTO message VALUES ('msgB2', 'sessB', 600000, 600000, "
                  "'{\"role\":\"assistant\"}')")

        conn.commit()
        conn.close()

    def test_collect_since_yields_full_session(self):
        """collect_since with a spanning session yields ALL messages from that session,
        and excludes fully-old sessions."""
        from legacy_codeagent_adapter import LegacyCodeagentAdapter

        db_path = os.path.join(self.tmpdir, "ngagent.db")
        self._create_test_db(db_path)

        adapter = LegacyCodeagentAdapter(db_path=db_path)
        # Watermark at 2000 seconds = 2000000 ms.
        events = list(adapter.collect_since(2000.0))

        # Session A has a post-watermark message (msgA2 at 3000s).
        # Should yield ALL messages from session A (msgA1 + msgA2).
        # Session B is fully before watermark — should be excluded.
        sess_a_events = [e for e in events if e.get("session_id") == "sessA"]
        sess_b_events = [e for e in events if e.get("session_id") == "sessB"]

        self.assertGreater(len(sess_a_events), 0,
                          "Session A (has post-watermark message) should be included")
        self.assertEqual(len(sess_b_events), 0,
                         "Session B (fully old) should be excluded")

        # Verify we get BOTH messages from session A, not just the post-watermark one.
        # msgA1 is a user_message, msgA2 is an assistant_message.
        kinds = sorted(e["kind"] for e in sess_a_events)
        self.assertIn("user_message", kinds,
                      "Pre-watermark message from spanning session should be included")
        self.assertIn("assistant_message", kinds,
                      "Post-watermark message from spanning session should be included")

    def test_collect_since_none_returns_all(self):
        """collect_since(None) returns all events from all sessions."""
        from legacy_codeagent_adapter import LegacyCodeagentAdapter

        db_path = os.path.join(self.tmpdir, "ngagent.db")
        self._create_test_db(db_path)

        adapter = LegacyCodeagentAdapter(db_path=db_path)
        events_none = list(adapter.collect_since(None))
        events_all = list(adapter.collect())

        self.assertEqual(len(events_none), len(events_all))


if __name__ == "__main__":
    unittest.main()
