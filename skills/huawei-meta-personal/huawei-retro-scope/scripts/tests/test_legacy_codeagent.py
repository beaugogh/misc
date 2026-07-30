"""Tests for the legacy codeagent (ngagent.db) adapter.

Run with: python -m unittest tests.test_legacy_codeagent -v

Creates a synthetic ngagent.db in a temp dir, inserts rows matching the verified schema,
and verifies that the adapter emits correctly normalized events.
"""

import unittest
import os
import sys
import json
import sqlite3
import tempfile

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from legacy_codeagent_adapter import LegacyCodeagentAdapter, iter_db_events


def _create_synthetic_db(path: str):
    """Create a synthetic ngagent.db with the verified schema and sample data."""
    conn = sqlite3.connect(path)
    c = conn.cursor()

    # Create tables matching the real schema.
    c.execute("""CREATE TABLE session (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        parent_id TEXT,
        slug TEXT NOT NULL,
        directory TEXT NOT NULL,
        title TEXT NOT NULL,
        version TEXT NOT NULL,
        share_url TEXT,
        summary_additions INTEGER,
        summary_deletions INTEGER,
        summary_files INTEGER,
        summary_diffs TEXT,
        revert TEXT,
        permission TEXT,
        time_created INTEGER NOT NULL,
        time_updated INTEGER NOT NULL,
        time_compacting INTEGER,
        time_archived INTEGER,
        workspace_id TEXT,
        has_origin_session INTEGER,
        origin_session_version TEXT,
        origin_session TEXT,
        compaction_count INTEGER,
        extra_info TEXT DEFAULT ''
    )""")

    c.execute("""CREATE TABLE project (
        id TEXT PRIMARY KEY,
        worktree TEXT,
        vcs TEXT,
        name TEXT,
        icon_url TEXT,
        icon_color TEXT,
        time_created INTEGER NOT NULL,
        time_updated INTEGER NOT NULL,
        time_initialized INTEGER,
        sandboxes TEXT NOT NULL,
        commands TEXT
    )""")

    c.execute("""CREATE TABLE message (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        time_created INTEGER NOT NULL,
        time_updated INTEGER NOT NULL,
        data TEXT NOT NULL,
        has_origin_message INTEGER,
        origin_message_version TEXT,
        origin_message TEXT,
        FOREIGN KEY (session_id) REFERENCES session(id) ON DELETE CASCADE
    )""")

    c.execute("""CREATE TABLE part (
        id TEXT PRIMARY KEY,
        message_id TEXT NOT NULL,
        session_id TEXT NOT NULL,
        time_created INTEGER NOT NULL,
        time_updated INTEGER NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE
    )""")

    # Insert a project.
    c.execute("""INSERT INTO project (id, worktree, vcs, name, time_created, time_updated, sandboxes)
        VALUES ('proj_1', '/workspace/myproj', 'main', 'myproj', 1783740000000, 1783740000000, '[]')""")

    # Insert a session.
    c.execute("""INSERT INTO session (id, project_id, slug, directory, title, version, time_created, time_updated)
        VALUES ('ses_1', 'proj_1', 'test-session', 'C:\\\\workspace\\\\myproj', 'Test Session', '1.2.27',
                1783741000000, 1783747000000)""")

    # --- Message 1: user says "hello" ---
    user_msg_data = json.dumps({
        "role": "user",
        "time": {"created": 1783741000000},
        "path": {"cwd": "C:\\workspace\\myproj", "root": "/"},
    })
    c.execute("""INSERT INTO message (id, session_id, time_created, time_updated, data)
        VALUES ('msg_1', 'ses_1', 1783741000000, 1783741000000, ?)""", (user_msg_data,))
    # Text part for the user message.
    c.execute("""INSERT INTO part (id, message_id, session_id, time_created, time_updated, data)
        VALUES ('prt_1', 'msg_1', 'ses_1', 1783741000000, 1783741000000, ?)""",
        (json.dumps({"type": "text", "text": "hello"}),))

    # --- Message 2: assistant responds + calls a tool ---
    asst_msg_data = json.dumps({
        "role": "assistant",
        "time": {"created": 1783741005000, "completed": 1783741010000},
        "path": {"cwd": "C:\\workspace\\myproj"},
        "modelID": "test-model",
        "providerID": "test-provider",
        "tokens": {
            "total": 1000,
            "input": 800,
            "output": 200,
            "reasoning": 50,
            "cache": {"read": 500, "write": 10}
        },
        "finish": "tool-calls"
    })
    c.execute("""INSERT INTO message (id, session_id, time_created, time_updated, data)
        VALUES ('msg_2', 'ses_1', 1783741005000, 1783741010000, ?)""", (asst_msg_data,))
    # Text part (assistant text)
    c.execute("""INSERT INTO part (id, message_id, session_id, time_created, time_updated, data)
        VALUES ('prt_2', 'msg_2', 'ses_1', 1783741005000, 1783741005000, ?)""",
        (json.dumps({"type": "text", "text": "Let me check that for you."}),))
    # Tool part (completed bash call)
    c.execute("""INSERT INTO part (id, message_id, session_id, time_created, time_updated, data)
        VALUES ('prt_3', 'msg_2', 'ses_1', 1783741008000, 1783741009000, ?)""",
        (json.dumps({
            "type": "tool",
            "callID": "call_abc123",
            "tool": "bash",
            "state": {
                "status": "completed",
                "input": {"command": "ls -la"},
                "output": "total 0\ndrwxr-xr-x 2 user user 4096 .",
                "title": "ls -la",
                "time": {"start": 1783741008000, "end": 1783741009000}
            }
        }),))

    # --- Message 3: assistant calls a tool that errors ---
    asst_msg_data2 = json.dumps({
        "role": "assistant",
        "time": {"created": 1783741010000, "completed": 1783741012000},
        "path": {"cwd": "C:\\workspace\\myproj"},
        "tokens": {"total": 500, "input": 400, "output": 100},
        "finish": "stop"
    })
    c.execute("""INSERT INTO message (id, session_id, time_created, time_updated, data)
        VALUES ('msg_3', 'ses_1', 1783741010000, 1783741012000, ?)""", (asst_msg_data2,))
    # Tool part (errored bash call)
    c.execute("""INSERT INTO part (id, message_id, session_id, time_created, time_updated, data)
        VALUES ('prt_4', 'msg_3', 'ses_1', 1783741011000, 1783741012000, ?)""",
        (json.dumps({
            "type": "tool",
            "callID": "call_def456",
            "tool": "bash",
            "state": {
                "status": "error",
                "input": {"command": "bad-command"},
                "output": "command not found: bad-command",
                "title": "bad-command"
            }
        }),))

    # --- Message 4: reasoning part ---
    asst_msg_data3 = json.dumps({
        "role": "assistant",
        "time": {"created": 1783741020000, "completed": 1783741025000},
        "finish": "stop"
    })
    c.execute("""INSERT INTO message (id, session_id, time_created, time_updated, data)
        VALUES ('msg_4', 'ses_1', 1783741020000, 1783741025000, ?)""", (asst_msg_data3,))
    c.execute("""INSERT INTO part (id, message_id, session_id, time_created, time_updated, data)
        VALUES ('prt_5', 'msg_4', 'ses_1', 1783741020000, 1783741020000, ?)""",
        (json.dumps({"type": "reasoning", "text": "The user wants to know about the directory structure."}),))
    c.execute("""INSERT INTO part (id, message_id, session_id, time_created, time_updated, data)
        VALUES ('prt_6', 'msg_4', 'ses_1', 1783741020000, 1783741020000, ?)""",
        (json.dumps({"type": "text", "text": "Here's what I found."}),))

    conn.commit()
    conn.close()


class TestLegacyCodeagentAdapter(unittest.TestCase):
    """Tests for the LegacyCodeagentAdapter against a synthetic ngagent.db."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmpdir, "ngagent.db")
        _create_synthetic_db(self.db_path)
        self.adapter = LegacyCodeagentAdapter(db_path=self.db_path)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_detect_true_when_db_exists(self):
        """detect() returns True when ngagent.db exists at the configured path."""
        self.assertTrue(self.adapter.detect())

    def test_detect_false_when_db_missing(self):
        """detect() returns False when ngagent.db doesn't exist."""
        a = LegacyCodeagentAdapter(db_path="/nonexistent/path/ngagent.db")
        self.assertFalse(a.detect())

    def test_user_message_emitted(self):
        """A user message with a text part yields kind=user_message with the text."""
        events = list(self.adapter.collect())
        user_msgs = [e for e in events if e["kind"] == "user_message"]
        self.assertEqual(len(user_msgs), 1)
        self.assertEqual(user_msgs[0]["text"], "hello")
        self.assertEqual(user_msgs[0]["role"], "user")
        self.assertEqual(user_msgs[0]["source"], "legacy_codeagent")
        self.assertEqual(user_msgs[0]["source_kind"], "ai_session")

    def test_assistant_message_emitted_with_text(self):
        """An assistant message yields kind=assistant_message with text from its parts."""
        events = list(self.adapter.collect())
        asst_msgs = [e for e in events if e["kind"] == "assistant_message"]
        self.assertEqual(len(asst_msgs), 3)  # msg_2, msg_3, msg_4
        texts = [e["text"] for e in asst_msgs if e.get("text")]
        self.assertIn("Let me check that for you.", texts)
        self.assertIn("Here's what I found.", texts)

    def test_tool_use_event_carries_name_input_id(self):
        """A tool part yields a tool_use event with tool_name, tool_input, tool_use_id."""
        events = list(self.adapter.collect())
        tool_uses = [e for e in events if e["kind"] == "tool_use"]
        self.assertEqual(len(tool_uses), 2)  # completed + errored

        # Check the completed bash call.
        bash_tu = next(e for e in tool_uses if e["tool_use_id"] == "call_abc123")
        self.assertEqual(bash_tu["tool_name"], "bash")
        self.assertEqual(bash_tu["tool_input"], {"command": "ls -la"})

    def test_tool_result_event_with_error_flag(self):
        """A tool part with status=error yields a tool_result with is_error=True."""
        events = list(self.adapter.collect())
        tool_results = [e for e in events if e["kind"] == "tool_result"]
        self.assertEqual(len(tool_results), 2)  # one per tool part

        # The errored tool result.
        err_result = next(e for e in tool_results if e["tool_use_id"] == "call_def456")
        self.assertTrue(err_result["tool_is_error"])
        self.assertIn("command not found", err_result["text"])

        # The completed tool result.
        ok_result = next(e for e in tool_results if e["tool_use_id"] == "call_abc123")
        self.assertFalse(ok_result["tool_is_error"])
        self.assertIn("total 0", ok_result["text"])

    def test_timestamp_normalization_millis_to_seconds(self):
        """Millisecond-epoch timestamps are normalized to seconds."""
        events = list(self.adapter.collect())
        # msg_1 has time_created=1783741000000 ms -> 1783741000.0 s
        user_msgs = [e for e in events if e["kind"] == "user_message"]
        self.assertAlmostEqual(user_msgs[0]["timestamp"], 1783741000.0, places=3)
        # timestamp_raw should be the original millis string.
        self.assertEqual(user_msgs[0]["timestamp_raw"], "1783741000000")

    def test_session_id_and_cwd_extracted(self):
        """Session ID and cwd are extracted from the session/message data."""
        events = list(self.adapter.collect())
        user_msgs = [e for e in events if e["kind"] == "user_message"]
        self.assertEqual(user_msgs[0]["session_id"], "ses_1")
        # cwd comes from message.data.path.cwd, falling back to session.directory.
        self.assertIn("myproj", user_msgs[0]["cwd"])

    def test_git_branch_from_project(self):
        """git_branch is extracted from the project table's vcs column."""
        events = list(self.adapter.collect())
        user_msgs = [e for e in events if e["kind"] == "user_message"]
        self.assertEqual(user_msgs[0]["git_branch"], "main")

    def test_usage_extraction(self):
        """Token usage is extracted from message.data.tokens and normalized."""
        events = list(self.adapter.collect())
        asst_msgs = [e for e in events if e["kind"] == "assistant_message"]
        # msg_2 has tokens: total=1000, input=800, output=200, reasoning=50, cache read=500, write=10
        msg2 = next(e for e in asst_msgs if e.get("usage"))
        usage = msg2["usage"]
        self.assertEqual(usage["input_tokens"], 800)
        self.assertEqual(usage["output_tokens"], 200)
        self.assertEqual(usage["total_tokens"], 1000)
        self.assertEqual(usage["reasoning_tokens"], 50)
        self.assertEqual(usage["cache_read_input_tokens"], 500)
        self.assertEqual(usage["cache_creation_input_tokens"], 10)

    def test_stop_reason_extracted(self):
        """Stop reason is extracted from message.data.finish."""
        events = list(self.adapter.collect())
        asst_msgs = [e for e in events if e["kind"] == "assistant_message"]
        # msg_2 has finish="tool-calls", msg_3 has finish="stop", msg_4 has finish="stop"
        stops = [e["stop_reason"] for e in asst_msgs]
        self.assertIn("tool-calls", stops)
        self.assertIn("stop", stops)

    def test_reasoning_event_emitted(self):
        """A reasoning-type part yields a reasoning event."""
        events = list(self.adapter.collect())
        reasoning = [e for e in events if e["kind"] == "reasoning"]
        self.assertEqual(len(reasoning), 1)
        self.assertIn("directory structure", reasoning[0]["text"])

    def test_collect_since_watermark_filters(self):
        """collect_since(watermark) returns ALL messages from sessions with any
        post-watermark message (C7 fix: full-session context for segmentation)."""
        # Watermark at 1783741005.0 seconds = 1783741005000 ms.
        # All 4 messages are in session ses_1. Since msg_3 (1783741010000) and
        # msg_4 (1783741020000) are after the watermark, ALL messages from ses_1
        # are returned — including pre-watermark ones — so segment() has full
        # session context to detect task boundaries.
        events_since = list(self.adapter.collect_since(1783741005.0))
        # msg_1 (user_message) is now included because it's in the same session
        # as post-watermark messages.
        user_msgs = [e for e in events_since if e["kind"] == "user_message"]
        self.assertEqual(len(user_msgs), 1)
        # All 3 assistant messages (msg_2, msg_3, msg_4) are included.
        asst_msgs = [e for e in events_since if e["kind"] == "assistant_message"]
        self.assertEqual(len(asst_msgs), 3)

    def test_collect_since_none_returns_all(self):
        """collect_since(None) returns all events (same as collect())."""
        all_events = list(self.adapter.collect())
        none_events = list(self.adapter.collect_since(None))
        self.assertEqual(len(all_events), len(none_events))

    def test_collect_since_excludes_exactly_at_watermark(self):
        """C7 fix: sessions with any post-watermark message return ALL messages.
        With all 4 messages in the same session and msg_3/msg_4 after the watermark,
        all messages from ses_1 are returned (full session context)."""
        # Watermark at exactly msg_2's time_created (1783741005.0 s = 1783741005000 ms).
        events_since = list(self.adapter.collect_since(1783741005.0))
        # All 3 assistant messages are included (full session context).
        asst_msgs = [e for e in events_since if e["kind"] == "assistant_message"]
        self.assertEqual(len(asst_msgs), 3)

    def test_tool_input_truncation(self):
        """Large tool inputs are truncated to avoid memory blowup."""
        # Create a DB with a huge tool input.
        db_path = os.path.join(self.tmpdir, "ngagent_big.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Minimal tables.
        c.execute("CREATE TABLE session (id TEXT PRIMARY KEY, directory TEXT, project_id TEXT, slug TEXT, title TEXT, version TEXT, time_created INTEGER, time_updated INTEGER)")
        c.execute("CREATE TABLE message (id TEXT PRIMARY KEY, session_id TEXT, time_created INTEGER, time_updated INTEGER, data TEXT)")
        c.execute("CREATE TABLE part (id TEXT PRIMARY KEY, message_id TEXT, session_id TEXT, time_created INTEGER, time_updated INTEGER, data TEXT)")
        c.execute("CREATE TABLE project (id TEXT PRIMARY KEY, worktree TEXT, vcs TEXT, name TEXT, time_created INTEGER, time_updated INTEGER, sandboxes TEXT)")

        c.execute("INSERT INTO project VALUES ('p1', '/', 'main', 'test', 1000, 1000, '[]')")
        c.execute("INSERT INTO session VALUES ('s1', '/proj', 'p1', 'slug', 'title', 'v1', 1000, 1000)")

        big_text = "x" * 5000
        msg_data = json.dumps({"role": "assistant", "finish": "stop"})
        c.execute("INSERT INTO message VALUES ('m1', 's1', 1000, 1000, ?)", (msg_data,))
        c.execute("INSERT INTO part VALUES ('p1', 'm1', 's1', 1000, 1000, ?)",
                  (json.dumps({
                      "type": "tool",
                      "callID": "call_big",
                      "tool": "write",
                      "state": {
                          "status": "completed",
                          "input": {"file_path": "/big.txt", "content": big_text},
                          "output": "done"
                      }
                  }),))
        conn.commit()
        conn.close()

        adapter = LegacyCodeagentAdapter(db_path=db_path)
        events = list(adapter.collect())
        tool_uses = [e for e in events if e["kind"] == "tool_use"]
        self.assertTrue(len(tool_uses) >= 1)
        tu = tool_uses[0]
        self.assertTrue(tu["tool_input"].get("_truncated"))
        # Truncated value should be much shorter than the original.
        self.assertLess(len(tu["tool_input"]["content"]), 300)

    def test_missing_part_table_does_not_crash(self):
        """If the part table is missing, message-level events are still emitted."""
        db_path = os.path.join(self.tmpdir, "ngagent_noparts.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE session (id TEXT PRIMARY KEY, directory TEXT, project_id TEXT, slug TEXT, title TEXT, version TEXT, time_created INTEGER, time_updated INTEGER)")
        c.execute("CREATE TABLE message (id TEXT PRIMARY KEY, session_id TEXT, time_created INTEGER, time_updated INTEGER, data TEXT)")
        c.execute("INSERT INTO session VALUES ('s1', '/proj', 'p1', 'slug', 'title', 'v1', 1000, 1000)")
        c.execute("INSERT INTO message VALUES ('m1', 's1', 1000, 1000, ?)",
                  (json.dumps({"role": "user", "path": {"cwd": "/proj"}}),))
        conn.commit()
        conn.close()

        adapter = LegacyCodeagentAdapter(db_path=db_path)
        events = list(adapter.collect())
        # Should still get the user_message event, just without text.
        user_msgs = [e for e in events if e["kind"] == "user_message"]
        self.assertEqual(len(user_msgs), 1)

    def test_missing_message_table_returns_empty(self):
        """If the message table is missing, no events are yielded (no crash)."""
        db_path = os.path.join(self.tmpdir, "ngagent_empty.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE session (id TEXT PRIMARY KEY)")
        conn.commit()
        conn.close()

        adapter = LegacyCodeagentAdapter(db_path=db_path)
        events = list(adapter.collect())
        self.assertEqual(len(events), 0)


class TestLiveDetection(unittest.TestCase):
    """Test detect() against the real ngagent.db on this machine (if present)."""

    def test_detect_finds_real_db(self):
        """On the author's machine, detect() should find the real ngagent.db."""
        from legacy_codeagent_adapter import _find_db
        found = _find_db()
        if found:
            adapter = LegacyCodeagentAdapter()
            self.assertTrue(adapter.detect())
        else:
            self.skipTest("ngagent.db not found on this machine")


if __name__ == "__main__":
    unittest.main()
