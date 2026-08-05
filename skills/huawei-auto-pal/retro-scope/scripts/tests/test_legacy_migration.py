"""Tests for legacy output migration detection (setup review finding 3).

Verifies that detect_legacy_output() correctly distinguishes:
  - none: no output anywhere (true first run)
  - legacy_only: old huawei-auto-buddy/output/ exists, new doesn't
  - current_only: only the current path exists (existing user)
  - both: both paths exist (conflict, must not auto-merge)

And that the function never reads personal file contents.

Run with: python -m unittest discover -s tests -p "test_legacy_migration.py" -v
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

import persistence


class TestDetectLegacyOutput(unittest.TestCase):
    """Test the migration detection function with temp directories."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="legacy_test_")
        self.current_dir = os.path.join(self._tmp, "current", "output")
        self.legacy_dir = os.path.join(self._tmp, "legacy", "huawei-auto-buddy", "output")

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _patch_paths(self):
        return patch.multiple(
            persistence,
            OUTPUT_DIR=self.current_dir,
            _LEGACY_OUTPUT_DIR=self.legacy_dir,
        )

    def test_none_when_neither_exists(self):
        with self._patch_paths():
            info = persistence.detect_legacy_output()
        self.assertEqual(info["status"], "none")
        self.assertIsNone(info["legacy_path"])
        self.assertEqual(info["legacy_files"], [])

    def test_legacy_only(self):
        os.makedirs(self.legacy_dir)
        # Create some fake legacy files (contents don't matter).
        open(os.path.join(self.legacy_dir, "tasks.jsonl"), "w").close()
        open(os.path.join(self.legacy_dir, "retro_scope_last_run.txt"), "w").close()
        with self._patch_paths():
            info = persistence.detect_legacy_output()
        self.assertEqual(info["status"], "legacy_only")
        self.assertEqual(info["legacy_path"], self.legacy_dir)
        self.assertEqual(len(info["legacy_files"]), 2)
        self.assertIn("tasks.jsonl", info["legacy_files"])

    def test_current_only(self):
        os.makedirs(self.current_dir)
        open(os.path.join(self.current_dir, "tasks.jsonl"), "w").close()
        with self._patch_paths():
            info = persistence.detect_legacy_output()
        self.assertEqual(info["status"], "current_only")
        self.assertIsNone(info["legacy_path"])
        self.assertEqual(info["legacy_files"], [])

    def test_both_paths_exist(self):
        os.makedirs(self.legacy_dir)
        os.makedirs(self.current_dir)
        open(os.path.join(self.legacy_dir, "old.txt"), "w").close()
        open(os.path.join(self.current_dir, "new.txt"), "w").close()
        with self._patch_paths():
            info = persistence.detect_legacy_output()
        self.assertEqual(info["status"], "both")
        self.assertEqual(info["legacy_path"], self.legacy_dir)
        self.assertEqual(len(info["legacy_files"]), 1)

    def test_does_not_read_file_contents(self):
        """The function must list filenames but never read file contents."""
        os.makedirs(self.legacy_dir)
        # Write a file with identifiable content.
        with open(os.path.join(self.legacy_dir, "secret.txt"), "w") as f:
            f.write("SENSITIVE_CONTENT_SHOULD_NOT_APPEAR")
        with self._patch_paths():
            info = persistence.detect_legacy_output()
            report = persistence.format_legacy_report(info)
        self.assertIn("secret.txt", info["legacy_files"])
        self.assertNotIn("SENSITIVE_CONTENT_SHOULD_NOT_APPEAR", report)

    def test_format_legacy_report_none(self):
        info = {"status": "none", "legacy_path": None,
                "current_path": "/x", "legacy_files": []}
        report = persistence.format_legacy_report(info)
        self.assertIn("first run", report.lower())

    def test_format_legacy_report_current_only(self):
        info = {"status": "current_only", "legacy_path": None,
                "current_path": "/x", "legacy_files": []}
        report = persistence.format_legacy_report(info)
        self.assertIn("Not a first run", report)

    def test_format_legacy_report_legacy_only(self):
        info = {"status": "legacy_only", "legacy_path": "/old",
                "current_path": "/new", "legacy_files": ["a.txt", "b.txt"]}
        report = persistence.format_legacy_report(info)
        self.assertIn("OLD", report)
        self.assertIn("/old", report)
        self.assertIn("approval", report.lower())

    def test_format_legacy_report_both(self):
        info = {"status": "both", "legacy_path": "/old",
                "current_path": "/new", "legacy_files": ["a.txt"]}
        report = persistence.format_legacy_report(info)
        self.assertIn("BOTH", report)
        self.assertIn("NOT auto-merge", report)
        self.assertIn("which to keep", report.lower())


if __name__ == "__main__":
    unittest.main()
