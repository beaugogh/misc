"""Tests for the `--check` environment output (Finding 2 from setup review).

Verifies that --check distinguishes:
  - READY: detected and collection implemented
  - DETECTOR-ONLY: tool detected but collect() yields nothing (placeholder)
  - NOT DETECTED: collection exists but source absent
  - ERROR: detection raised

Run with: python -m unittest discover -s tests -p "test_check_output.py" -v
"""

import unittest
import os
import sys
import io
from contextlib import redirect_stdout
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from more_adapters import ThreeMsAdapter
from unverified_adapters import CloudDevOpsWikiAdapter, W3Adapter


class TestDetectorOnlyAttribute(unittest.TestCase):
    """The three placeholder adapters must carry detector_only=True."""

    def test_3ms_is_detector_only(self):
        self.assertTrue(getattr(ThreeMsAdapter(), "detector_only", False))

    def test_clouddevops_wiki_is_detector_only(self):
        self.assertTrue(getattr(CloudDevOpsWikiAdapter(), "detector_only", False))

    def test_w3_is_detector_only(self):
        self.assertTrue(getattr(W3Adapter(), "detector_only", False))


class TestRealAdaptersNotDetectorOnly(unittest.TestCase):
    """Adapters with real collect() must not be marked detector_only."""

    def test_claude_code_not_detector_only(self):
        from sources import default_registry
        reg = default_registry(session_cwds=[])
        for adapter in reg._adapters:
            if adapter.name == "claude_code":
                self.assertFalse(getattr(adapter, "detector_only", False))
                return
        self.fail("claude_code adapter not found in registry")


class TestCheckOutput(unittest.TestCase):
    """Exercise the --check branch of run.py main()."""

    def _run_check(self):
        """Invoke the --check code path and capture stdout."""
        import run as run_mod
        # Reload to pick up the current source.
        import importlib
        importlib.reload(run_mod)
        buf = io.StringIO()
        with redirect_stdout(buf):
            with patch.object(sys, "argv", ["run.py", "--check"]):
                try:
                    run_mod.main()
                except SystemExit:
                    pass
        return buf.getvalue()

    def test_check_shows_status_legend(self):
        out = self._run_check()
        self.assertIn("READY", out)
        self.assertIn("DETECTOR-ONLY", out)
        self.assertIn("NOT DETECTED", out)

    def test_check_lists_all_registered_adapters(self):
        out = self._run_check()
        # A sampling of adapter names that must appear.
        for name in ("claude_code", "git", "3ms", "clouddevops_wiki", "w3"):
            self.assertIn(name, out)

    def test_check_does_not_say_green_sources(self):
        """The old misleading heading 'Green sources' must be gone."""
        out = self._run_check()
        self.assertNotIn("Green sources", out)

    def test_check_exits_zero(self):
        """--check must exit cleanly without collecting personal activity."""
        import run as run_mod
        import importlib
        importlib.reload(run_mod)
        with redirect_stdout(io.StringIO()):
            with patch.object(sys, "argv", ["run.py", "--check"]):
                with self.assertRaises(SystemExit) as ctx:
                    run_mod.main()
        self.assertEqual(ctx.exception.code, 0)

    def test_detector_only_shown_when_detected(self):
        """If a detector-only adapter's detect() is True, status is DETECTOR-ONLY."""
        import run as run_mod
        import importlib
        importlib.reload(run_mod)
        # Force 3ms detect() to True so we exercise the DETECTOR-ONLY branch
        # even on machines without opencli.
        with patch.object(ThreeMsAdapter, "detect", return_value=True):
            with patch.object(CloudDevOpsWikiAdapter, "detect", return_value=True):
                with patch.object(W3Adapter, "detect", return_value=True):
                    out = self._run_check()
        self.assertIn("3ms                  DETECTOR-ONLY", out)
        self.assertIn("clouddevops_wiki     DETECTOR-ONLY", out)
        self.assertIn("w3                   DETECTOR-ONLY", out)

    def test_detector_only_shows_hint(self):
        """DETECTOR-ONLY lines should still show the setup hint."""
        import run as run_mod
        import importlib
        importlib.reload(run_mod)
        with patch.object(ThreeMsAdapter, "detect", return_value=True):
            out = self._run_check()
        # The hint for 3ms mentions OpenCLI.
        line = [l for l in out.splitlines() if l.strip().startswith("3ms")]
        self.assertEqual(len(line), 1)
        self.assertIn("OpenCLI", line[0])

    def test_not_detected_shows_hint(self):
        """NOT DETECTED lines should show the setup hint."""
        out = self._run_check()
        # icalendar is not detected on most CI machines and has a hint.
        lines = [l for l in out.splitlines() if "icalendar" in l]
        self.assertEqual(len(lines), 1)
        self.assertIn("NOT DETECTED", lines[0])
        self.assertIn("RETRO_SCOPE_ICS_PATHS", lines[0])

    def test_error_branch(self):
        """If detect() raises, --check prints ERROR and continues."""
        import run as run_mod
        import importlib
        importlib.reload(run_mod)

        def boom(self):
            raise RuntimeError("boom")

        with patch.object(ThreeMsAdapter, "detect", boom):
            out = self._run_check()
        self.assertIn("ERROR", out)
        self.assertIn("boom", out)
        # Other adapters still processed.
        self.assertIn("claude_code", out)


if __name__ == "__main__":
    unittest.main()
