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


if __name__ == "__main__":
    unittest.main()
