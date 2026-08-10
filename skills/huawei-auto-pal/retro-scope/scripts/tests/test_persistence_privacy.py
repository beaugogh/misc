"""Persistence and sensitive-output regression tests."""

from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

import persistence
from run import _export_session_records


class TestNamespacedPersistence(unittest.TestCase):
    def test_retro_watermark_is_namespaced_atomic_and_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            watermark = os.path.join(tmp, "retro_scope_last_run.txt")
            tasks_log = os.path.join(tmp, "tasks.jsonl")
            legacy = os.path.join(tmp, "last_run.txt")
            with patch.multiple(
                persistence,
                OUTPUT_DIR=tmp,
                WATERMARK_FILE=watermark,
                TASKS_LOG=tasks_log,
                LEGACY_WATERMARK_FILE=legacy,
            ):
                persistence.persist_run([{"id": "task-1"}], 1234.5)
                self.assertEqual(persistence.read_watermark(), 1234.5)
                self.assertEqual(persistence.load_existing_tasks(), [{"id": "task-1"}])
                if os.name != "nt":
                    self.assertEqual(stat.S_IMODE(os.stat(watermark).st_mode), 0o600)
                    self.assertEqual(stat.S_IMODE(os.stat(tasks_log).st_mode), 0o600)

    def test_legacy_milliseconds_are_not_read_as_seconds(self):
        with tempfile.TemporaryDirectory() as tmp:
            legacy = os.path.join(tmp, "last_run.txt")
            with open(legacy, "w", encoding="utf-8") as f:
                f.write("1785900000000")
            with patch.multiple(
                persistence,
                OUTPUT_DIR=tmp,
                WATERMARK_FILE=os.path.join(tmp, "retro_scope_last_run.txt"),
                LEGACY_WATERMARK_FILE=legacy,
            ):
                self.assertIsNone(persistence.read_watermark())


class TestPrivateEvidenceExport(unittest.TestCase):
    def test_export_redacts_secrets_and_email(self):
        task = {
            "id": "task-1",
            "subject": "contact person@example.com",
            "source_kind": "ai_session",
            "source": "claude_code",
            "session_id": "session-1",
            "cwd": "D:\\Projects\\myproject",
            "git_branch": "main",
            "start": 1000.0,
            "end": 1010.0,
            "human_data": {
                "is_genuine_time_sink": True,
                "human_engaged_seconds": 600,
            },
        }
        events = [{
            "timestamp": 1005.0,
            "session_id": "session-1",
            "kind": "user_message",
            "text": "api_key=super-secret person@example.com",
        }]
        with tempfile.TemporaryDirectory() as tmp:
            _export_session_records([task], events, tmp)
            records_dir = os.path.join(tmp, "session_records")
            paths = [os.path.join(records_dir, name) for name in os.listdir(records_dir)]
            self.assertEqual(len(paths), 1)
            with open(paths[0], encoding="utf-8") as f:
                import json as _json
                record = _json.load(f)
            # Secret redaction
            self.assertNotIn("super-secret", _json.dumps(record))
            self.assertNotIn("person@example.com", _json.dumps(record))
            self.assertIn("[REDACTED]", _json.dumps(record))
            self.assertIn("[REDACTED_EMAIL]", _json.dumps(record))
            # Identity fields present (rubric 12: self-describing records)
            self.assertEqual(record["source"], "claude_code")
            self.assertEqual(record["session_id"], "session-1")
            self.assertEqual(record["cwd"], "D:\\Projects\\myproject")
            self.assertEqual(record["git_branch"], "main")
            if os.name != "nt":
                self.assertEqual(stat.S_IMODE(os.stat(paths[0]).st_mode), 0o600)

    def test_export_filters_by_source_kind(self):
        """A browser task (session_id=None) must not include AI session events
        that fall in the same time window. Without source_kind filtering, the
        session_id=None filter lets all events through."""
        task = {
            "id": "browser-1000",
            "subject": "research",
            "source_kind": "browser",
            "source": "browser",
            "session_id": None,
            "cwd": None,
            "git_branch": None,
            "start": 1000.0,
            "end": 2000.0,
            "human_data": {
                "is_genuine_time_sink": True,
                "human_engaged_seconds": 600,
            },
        }
        events = [
            # Browser events — should be included.
            {"timestamp": 1000.0, "session_id": None, "source_kind": "browser",
             "kind": "visit", "text": "GitHub",
             "tool_input": {"url": "https://example.com", "title": "Example"}},
            {"timestamp": 1100.0, "session_id": None, "source_kind": "browser",
             "kind": "download", "text": "file.zip",
             "tool_input": {"target_path": "C:\\file.zip", "total_bytes": 100}},
            # AI session events in the same time window — should be EXCLUDED.
            {"timestamp": 1200.0, "session_id": "ai-session-abc",
             "source_kind": "ai_session", "kind": "user_message",
             "text": "help me with this"},
            {"timestamp": 1300.0, "session_id": "ai-session-abc",
             "source_kind": "ai_session", "kind": "assistant_message",
             "text": "sure, let me check"},
            {"timestamp": 1400.0, "session_id": "ai-session-abc",
             "source_kind": "ai_session", "kind": "tool_use",
             "tool_name": "Bash", "tool_input": {"command": "ls"}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            _export_session_records([task], events, tmp)
            records_dir = os.path.join(tmp, "session_records")
            paths = [os.path.join(records_dir, name) for name in os.listdir(records_dir)]
            self.assertEqual(len(paths), 1)
            with open(paths[0], encoding="utf-8") as f:
                import json as _json
                record = _json.load(f)
            timeline = record.get("event_timeline", [])
            kinds = [e["kind"] for e in timeline]
            # Browser events present.
            self.assertIn("visit", kinds)
            self.assertIn("download", kinds)
            # AI session events EXCLUDED.
            self.assertNotIn("user_message", kinds)
            self.assertNotIn("assistant_message", kinds)
            self.assertNotIn("tool_use", kinds)

    def test_filesystem_task_excludes_other_sources(self):
        """A filesystem task (session_id=None) must not include AI, browser,
        or vcs events from the same time window."""
        task = {
            "id": "implicit-nosession-1000",
            "subject": "editing files",
            "source_kind": "filesystem",
            "source": "windows_recent",
            "session_id": None,
            "cwd": None,
            "git_branch": None,
            "start": 1000.0,
            "end": 2000.0,
            "human_data": {
                "is_genuine_time_sink": True,
                "human_engaged_seconds": 600,
            },
        }
        events = [
            {"timestamp": 1000.0, "session_id": None, "source_kind": "filesystem",
             "kind": "file_open", "text": "D:\\proj\\main.py",
             "tool_input": {"file_path": "D:\\proj\\main.py"}},
            {"timestamp": 1100.0, "session_id": None, "source_kind": "filesystem",
             "kind": "file_open", "text": "D:\\proj\\utils.py",
             "tool_input": {"file_path": "D:\\proj\\utils.py"}},
            # AI session events — should be EXCLUDED.
            {"timestamp": 1200.0, "session_id": "ai-abc",
             "source_kind": "ai_session", "kind": "assistant_message", "text": "let me help"},
            {"timestamp": 1300.0, "session_id": "ai-abc",
             "source_kind": "ai_session", "kind": "tool_use", "tool_name": "Bash"},
            # Browser events — should be EXCLUDED.
            {"timestamp": 1400.0, "session_id": None, "source_kind": "browser",
             "kind": "visit", "text": "Google",
             "tool_input": {"url": "https://google.com", "title": "Google"}},
            # VCS events — should be EXCLUDED.
            {"timestamp": 1500.0, "session_id": None, "source_kind": "vcs",
             "kind": "commit", "text": "fix: stuff",
             "tool_input": {"hash": "abc123", "subject": "fix: stuff"}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            _export_session_records([task], events, tmp)
            records_dir = os.path.join(tmp, "session_records")
            paths = [os.path.join(records_dir, name) for name in os.listdir(records_dir)]
            self.assertEqual(len(paths), 1)
            with open(paths[0], encoding="utf-8") as f:
                import json as _json
                record = _json.load(f)
            timeline = record.get("event_timeline", [])
            kinds = [e["kind"] for e in timeline]
            # Only filesystem events.
            self.assertIn("file_open", kinds)
            self.assertEqual(len(kinds), 2)  # exactly the 2 file_open events
            # No contamination.
            self.assertNotIn("assistant_message", kinds)
            self.assertNotIn("tool_use", kinds)
            self.assertNotIn("visit", kinds)
            self.assertNotIn("commit", kinds)

    def test_vcs_task_excludes_other_sources(self):
        """A vcs task (session_id=None) must not include AI or browser events."""
        task = {
            "id": "implicit-nosession-2000",
            "subject": "commits",
            "source_kind": "vcs",
            "source": "git",
            "session_id": None,
            "cwd": "D:\\proj",
            "git_branch": "main",
            "start": 2000.0,
            "end": 3000.0,
            "human_data": {
                "is_genuine_time_sink": True,
                "human_engaged_seconds": 600,
            },
        }
        events = [
            {"timestamp": 2000.0, "session_id": None, "source_kind": "vcs",
             "kind": "commit", "text": "fix: bug",
             "tool_input": {"hash": "def456", "subject": "fix: bug"}},
            {"timestamp": 2100.0, "session_id": None, "source_kind": "vcs",
             "kind": "branch_checkout", "text": "main -> feature/x",
             "tool_input": {"from_branch": "main", "to_branch": "feature/x"}},
            # AI session events — should be EXCLUDED.
            {"timestamp": 2200.0, "session_id": "ai-xyz",
             "source_kind": "ai_session", "kind": "user_message", "text": "help"},
            {"timestamp": 2300.0, "session_id": "ai-xyz",
             "source_kind": "ai_session", "kind": "tool_use", "tool_name": "Read"},
            # Browser events — should be EXCLUDED.
            {"timestamp": 2400.0, "session_id": None, "source_kind": "browser",
             "kind": "visit", "text": "Stack Overflow",
             "tool_input": {"url": "https://stackoverflow.com", "title": "SO"}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            _export_session_records([task], events, tmp)
            records_dir = os.path.join(tmp, "session_records")
            paths = [os.path.join(records_dir, name) for name in os.listdir(records_dir)]
            self.assertEqual(len(paths), 1)
            with open(paths[0], encoding="utf-8") as f:
                import json as _json
                record = _json.load(f)
            timeline = record.get("event_timeline", [])
            kinds = [e["kind"] for e in timeline]
            # Only vcs events.
            self.assertIn("commit", kinds)
            self.assertIn("branch_checkout", kinds)
            self.assertEqual(len(kinds), 2)
            # No contamination.
            self.assertNotIn("user_message", kinds)
            self.assertNotIn("tool_use", kinds)
            self.assertNotIn("visit", kinds)


if __name__ == "__main__":
    unittest.main()
