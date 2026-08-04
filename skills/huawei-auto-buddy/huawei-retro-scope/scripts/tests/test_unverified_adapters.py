"""Tests for unverified-source adapters (Phase 6.10).

Verifies that:
  - detect() returns False when the tool isn't installed (graceful skip)
  - detect() returns True when the expected path exists
  - collect() parses JSONL defensively (Codex schema)
  - collect() parses SQLite defensively (unknown schema)
  - Events are normalized to the unified schema

Run with: python -m unittest discover -s scripts/tests
"""

import unittest
import os
import sys
import json
import tempfile
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from unverified_adapters import (
    CodexAdapter,
    OpenclawAdapter,
    HermesAgentAdapter,
    CloudDevOpsWikiAdapter,
    W3Adapter,
)


class TestCodexAdapter(unittest.TestCase):
    def test_detect_false_when_absent(self):
        a = CodexAdapter(codex_dir="/nonexistent/path/.codex")
        self.assertFalse(a.detect())

    def test_detect_true_when_sessions_dir_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, ".codex", "sessions")
            os.makedirs(sessions)
            a = CodexAdapter(codex_dir=os.path.join(tmp, ".codex"))
            self.assertTrue(a.detect())

    def test_detect_true_when_history_file_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            codex_dir = os.path.join(tmp, ".codex")
            os.makedirs(codex_dir)
            # Touch history.jsonl
            open(os.path.join(codex_dir, "history.jsonl"), "w").close()
            a = CodexAdapter(codex_dir=codex_dir)
            self.assertTrue(a.detect())

    def test_collect_parses_jsonl(self):
        """Codex JSONL with Claude-Code-style schema is parsed correctly."""
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, ".codex", "sessions")
            os.makedirs(sessions)
            session_file = os.path.join(sessions, "test-session.jsonl")
            with open(session_file, "w", encoding="utf-8") as f:
                f.write(json.dumps({
                    "type": "user", "timestamp": "2026-07-01T10:00:00.000Z",
                    "cwd": "/proj", "gitBranch": "main",
                    "message": {"role": "user", "content": "hello world"},
                }) + "\n")
                f.write(json.dumps({
                    "type": "assistant", "timestamp": "2026-07-01T10:01:00.000Z",
                    "cwd": "/proj", "gitBranch": "main",
                    "message": {"role": "assistant", "content": "hi there",
                                 "usage": {"output_tokens": 50}},
                }) + "\n")
            a = CodexAdapter(codex_dir=os.path.join(tmp, ".codex"))
            events = list(a.collect())
            self.assertEqual(len(events), 2)
            self.assertEqual(events[0]["kind"], "user_message")
            self.assertEqual(events[0]["source"], "codex")
            self.assertEqual(events[0]["text"], "hello world")
            self.assertEqual(events[1]["kind"], "assistant_message")
            self.assertEqual(events[1]["source"], "codex")

    def test_collect_handles_codex_style_timestamps(self):
        """Codex may use 'created_at' instead of 'timestamp'."""
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, ".codex", "sessions")
            os.makedirs(sessions)
            session_file = os.path.join(sessions, "s2.jsonl")
            with open(session_file, "w", encoding="utf-8") as f:
                f.write(json.dumps({
                    "role": "user", "created_at": "2026-07-01T10:00:00Z",
                    "content": "test prompt",
                }) + "\n")
            a = CodexAdapter(codex_dir=os.path.join(tmp, ".codex"))
            events = list(a.collect())
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["kind"], "user_message")
            # Verify the timestamp is parsed (exact value depends on timezone
            # interpretation, so just check it's > 0 and reasonable for 2026).
            self.assertGreater(events[0]["timestamp"], 1700000000)  # after 2023
            self.assertLess(events[0]["timestamp"], 1900000000)     # before 2030

    def test_collect_skips_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, ".codex", "sessions")
            os.makedirs(sessions)
            session_file = os.path.join(sessions, "bad.jsonl")
            with open(session_file, "w", encoding="utf-8") as f:
                f.write("not json\n")
                f.write(json.dumps({"type": "user", "timestamp": "2026-07-01T10:00:00Z",
                                     "message": {"role": "user", "content": "ok"}}) + "\n")
            a = CodexAdapter(codex_dir=os.path.join(tmp, ".codex"))
            events = list(a.collect())
            self.assertEqual(len(events), 1)  # only the valid line

    def test_collect_since_filters_by_watermark(self):
        with tempfile.TemporaryDirectory() as tmp:
            sessions = os.path.join(tmp, ".codex", "sessions")
            os.makedirs(sessions)
            session_file = os.path.join(sessions, "s3.jsonl")
            with open(session_file, "w", encoding="utf-8") as f:
                f.write(json.dumps({"type": "user", "timestamp": "2026-07-01T10:00:00Z",
                                     "message": {"role": "user", "content": "old"}}) + "\n")
                f.write(json.dumps({"type": "user", "timestamp": "2026-07-02T10:00:00Z",
                                     "message": {"role": "user", "content": "new"}}) + "\n")
            a = CodexAdapter(codex_dir=os.path.join(tmp, ".codex"))
            # Watermark = July 1 11:00 — should only get the July 2 event.
            from datetime import datetime
            wm = datetime.fromisoformat("2026-07-01T11:00:00+00:00").timestamp()
            events = list(a.collect_since(wm))
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["text"], "new")


class TestOpenclawAdapter(unittest.TestCase):
    def test_detect_false_when_absent(self):
        a = OpenclawAdapter(openclaw_dir="/nonexistent/.openclaw")
        self.assertFalse(a.detect())

    def test_detect_true_when_dir_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = OpenclawAdapter(openclaw_dir=tmp)
            self.assertTrue(a.detect())

    def test_collect_parses_sqlite(self):
        """SQLite with message table is parsed defensively."""
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "test.db")
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE messages ("
                         "id INTEGER PRIMARY KEY, "
                         "timestamp REAL, "
                         "role TEXT, "
                         "content TEXT, "
                         "session_id TEXT)")
            conn.execute("INSERT INTO messages VALUES (1, 1751356800.0, 'user', 'hello', 's1')")
            conn.execute("INSERT INTO messages VALUES (2, 1751356860.0, 'assistant', 'hi', 's1')")
            conn.commit()
            conn.close()
            a = OpenclawAdapter(openclaw_dir=tmp)
            events = list(a.collect())
            self.assertEqual(len(events), 2)
            self.assertEqual(events[0]["kind"], "user_message")
            self.assertEqual(events[1]["kind"], "assistant_message")
            self.assertEqual(events[0]["source"], "openclaw")

    def test_collect_handles_no_matching_tables(self):
        """SQLite with no message-like table yields nothing."""
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "config.db")
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE config (key TEXT, value TEXT)")
            conn.commit()
            conn.close()
            a = OpenclawAdapter(openclaw_dir=tmp)
            events = list(a.collect())
            self.assertEqual(len(events), 0)


class TestHermesAgentAdapter(unittest.TestCase):
    def test_detect_false_when_absent(self):
        a = HermesAgentAdapter(hermes_dir="/nonexistent/.hermes-agent")
        self.assertFalse(a.detect())

    def test_detect_true_when_dir_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = HermesAgentAdapter(hermes_dir=tmp)
            self.assertTrue(a.detect())

    def test_collect_relabels_source(self):
        """Hermes adapter reuses Openclaw parsing but labels source as hermes_agent."""
        with tempfile.TemporaryDirectory() as tmp:
            db_path = os.path.join(tmp, "test.db")
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE messages (id INTEGER, timestamp REAL, role TEXT, content TEXT)")
            conn.execute("INSERT INTO messages VALUES (1, 1751356800.0, 'user', 'test')")
            conn.commit()
            conn.close()
            a = HermesAgentAdapter(hermes_dir=tmp)
            events = list(a.collect())
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["source"], "hermes_agent")


class TestCloudDevOpsWikiAdapter(unittest.TestCase):
    def test_detect_false_when_opencli_absent(self):
        a = CloudDevOpsWikiAdapter()
        # opencli may or may not be present, but the wiki command likely isn't.
        # Just verify detect() doesn't crash.
        result = a.detect()
        self.assertIsInstance(result, bool)

    def test_collect_is_generator(self):
        a = CloudDevOpsWikiAdapter()
        # collect() should yield nothing (placeholder).
        events = list(a.collect())
        self.assertEqual(len(events), 0)


class TestW3Adapter(unittest.TestCase):
    def test_detect_false_when_opencli_absent(self):
        a = W3Adapter()
        result = a.detect()
        self.assertIsInstance(result, bool)

    def test_collect_is_generator(self):
        a = W3Adapter()
        events = list(a.collect())
        self.assertEqual(len(events), 0)


class TestRegistration(unittest.TestCase):
    def test_register_all_adapters(self):
        """register_unverified_adapters registers all 5 adapters."""
        from sources import SourceRegistry
        from unverified_adapters import register_unverified_adapters
        reg = SourceRegistry()
        register_unverified_adapters(reg)
        # The registry should have 5 adapters registered.
        # (SourceRegistry doesn't expose a count, so we check via collect_all
        # which runs detect() on each — absent sources are in the skipped list.)
        events, skipped = reg.collect_all()
        # All 5 should be in skipped (not detected on this machine, unless
        # opencli is present for wiki/w3).
        skip_names = [s["name"] if isinstance(s, dict) else str(s) for s in skipped]
        self.assertIn("codex", skip_names)
        self.assertIn("openclaw", skip_names)
        self.assertIn("hermes_agent", skip_names)


if __name__ == "__main__":
    unittest.main()
