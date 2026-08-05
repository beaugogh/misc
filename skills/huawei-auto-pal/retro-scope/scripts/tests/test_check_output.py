"""Tests for the `--check` environment output (setup review findings 2 + 1).

Two layers:
  1. render_check_output() — pure function tests with fake adapters (no real
     environment access, no collect() calls, fully deterministic).
  2. CLI wiring — one test that runs `run.main(['--check'])` with a mocked
     registry and asserts no adapter collect() is called (finding 1 regression).

Run with: python -m unittest discover -s tests -p "test_check_output.py" -v
"""

import unittest
import os
import sys
import io
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)


# ---------------------------------------------------------------------------
# Fake adapters for deterministic testing
# ---------------------------------------------------------------------------

class _FakeAdapter:
    """Minimal adapter stub for testing render_check_output."""

    def __init__(self, name, detect_result, detector_only=False, raises=None):
        self.name = name
        self._detect_result = detect_result
        self.detector_only = detector_only
        self._raises = raises
        self.collect_called = False

    def detect(self):
        if self._raises:
            raise self._raises
        return self._detect_result

    def collect(self):
        self.collect_called = False
        return
        yield  # never reached


class _FakeReadyAdapter(_FakeAdapter):
    def __init__(self, name="fake_ready"):
        super().__init__(name, detect_result=True, detector_only=False)


class _FakeDetectorOnlyAdapter(_FakeAdapter):
    def __init__(self, name="fake_detector_only"):
        super().__init__(name, detect_result=True, detector_only=True)


class _FakeAbsentAdapter(_FakeAdapter):
    def __init__(self, name="fake_absent"):
        super().__init__(name, detect_result=False, detector_only=False)


class _FakeErrorAdapter(_FakeAdapter):
    def __init__(self, name="fake_error"):
        super().__init__(name, detect_result=False, raises=RuntimeError("boom"))


# ---------------------------------------------------------------------------
# Detector-only attribute on real adapters
# ---------------------------------------------------------------------------

class TestDetectorOnlyAttribute(unittest.TestCase):
    """The three placeholder adapters must carry detector_only=True."""

    def test_3ms_is_detector_only(self):
        from more_adapters import ThreeMsAdapter
        self.assertTrue(getattr(ThreeMsAdapter(), "detector_only", False))

    def test_clouddevops_wiki_is_detector_only(self):
        from unverified_adapters import CloudDevOpsWikiAdapter
        self.assertTrue(getattr(CloudDevOpsWikiAdapter(), "detector_only", False))

    def test_w3_is_detector_only(self):
        from unverified_adapters import W3Adapter
        self.assertTrue(getattr(W3Adapter(), "detector_only", False))

    def test_real_adapter_not_detector_only(self):
        from more_adapters import WeLinkRecordingsAdapter
        a = WeLinkRecordingsAdapter()
        self.assertFalse(getattr(a, "detector_only", False))


# ---------------------------------------------------------------------------
# render_check_output — pure function tests
# ---------------------------------------------------------------------------

class TestRenderCheckOutput(unittest.TestCase):
    """Test the pure rendering function with fake adapters."""

    def _render(self, adapters, hints=None):
        import run as run_mod
        return run_mod.render_check_output(adapters, hints=hints)

    def test_shows_status_legend(self):
        out = self._render([])
        self.assertIn("READY", out)
        self.assertIn("DETECTOR-ONLY", out)
        self.assertIn("NOT DETECTED", out)

    def _adapter_line(self, out, name):
        """Extract the data line for a named adapter from rendered output."""
        for line in out.splitlines():
            if line.strip().startswith(name):
                return line
        return ""

    def test_ready_adapter(self):
        out = self._render([_FakeReadyAdapter()])
        line = self._adapter_line(out, "fake_ready")
        self.assertIn("READY", line)
        self.assertNotIn("DETECTOR-ONLY", line)
        self.assertNotIn("NOT DETECTED", line)

    def test_detector_only_adapter(self):
        out = self._render([_FakeDetectorOnlyAdapter()])
        line = self._adapter_line(out, "fake_detector_only")
        self.assertIn("DETECTOR-ONLY", line)
        self.assertNotIn("READY", line)

    def test_detector_only_shows_hint(self):
        hints = {"fake_detector_only": "setup hint here"}
        out = self._render([_FakeDetectorOnlyAdapter()], hints=hints)
        self.assertIn("setup hint here", out)

    def test_not_detected_shows_hint(self):
        hints = {"fake_absent": "install X to enable Y"}
        out = self._render([_FakeAbsentAdapter()], hints=hints)
        self.assertIn("fake_absent", out)
        self.assertIn("NOT DETECTED", out)
        self.assertIn("install X to enable Y", out)

    def test_not_detected_no_hint(self):
        out = self._render([_FakeAbsentAdapter()], hints={})
        self.assertIn("fake_absent", out)
        self.assertIn("NOT DETECTED", out)
        # No hint parenthetical on the fake_absent line.
        fake_line = [l for l in out.splitlines() if "fake_absent" in l][0]
        self.assertNotIn("(", fake_line)

    def test_error_branch(self):
        out = self._render([_FakeErrorAdapter()])
        self.assertIn("ERROR", out)
        self.assertIn("boom", out)

    def test_error_does_not_stop_other_adapters(self):
        adapters = [_FakeErrorAdapter(), _FakeReadyAdapter()]
        out = self._render(adapters)
        self.assertIn("ERROR", out)
        self.assertIn("READY", out)

    def test_all_statuses_together(self):
        hints = {"fake_absent": "hint-A", "fake_detector_only": "hint-D"}
        adapters = [
            _FakeReadyAdapter(),
            _FakeDetectorOnlyAdapter(),
            _FakeAbsentAdapter(),
            _FakeErrorAdapter(),
        ]
        out = self._render(adapters, hints=hints)
        self.assertIn("READY", out)
        self.assertIn("DETECTOR-ONLY", out)
        self.assertIn("NOT DETECTED", out)
        self.assertIn("ERROR", out)
        self.assertIn("hint-A", out)
        self.assertIn("hint-D", out)

    def test_no_green_sources_heading(self):
        """The old misleading heading 'Green sources' must be gone."""
        out = self._render([])
        self.assertNotIn("Green sources", out)

    def test_does_not_call_collect(self):
        """render_check_output must never call collect() on any adapter."""
        adapter = _FakeReadyAdapter()
        adapter.collect_called = False
        original_collect = adapter.collect

        def tracking_collect():
            adapter.collect_called = True
            return
            yield  # pragma: no cover

        adapter.collect = tracking_collect
        self._render([adapter])
        self.assertFalse(adapter.collect_called)


# ---------------------------------------------------------------------------
# CLI wiring — --check must not collect personal data (finding 1 regression)
# ---------------------------------------------------------------------------

class TestCheckNoCollection(unittest.TestCase):
    """--check must not call any adapter's collect() method."""

    def test_check_does_not_collect_claude_sessions(self):
        """Regression test: --check used to call ClaudeCodeAdapter.collect()."""
        import run as run_mod
        import importlib
        importlib.reload(run_mod)

        from claude_code_adapter import ClaudeCodeAdapter
        with patch.object(ClaudeCodeAdapter, "collect") as mock_collect:
            mock_collect.return_value = iter([])
            with redirect_stdout(io.StringIO()):
                with patch.object(sys, "argv", ["run.py", "--check"]):
                    try:
                        run_mod.main()
                    except SystemExit:
                        pass
        mock_collect.assert_not_called()

    def test_check_exits_zero(self):
        import run as run_mod
        import importlib
        importlib.reload(run_mod)
        with redirect_stdout(io.StringIO()):
            with patch.object(sys, "argv", ["run.py", "--check"]):
                with self.assertRaises(SystemExit) as ctx:
                    run_mod.main()
        self.assertEqual(ctx.exception.code, 0)

    def test_check_lists_real_adapter_names(self):
        """--check output should mention real adapters from the registry."""
        import run as run_mod
        import importlib
        importlib.reload(run_mod)
        with redirect_stdout(io.StringIO()) as buf:
            with patch.object(sys, "argv", ["run.py", "--check"]):
                try:
                    run_mod.main()
                except SystemExit:
                    pass
        out = buf.getvalue()
        for name in ("claude_code", "git", "3ms", "clouddevops_wiki", "w3"):
            self.assertIn(name, out)


if __name__ == "__main__":
    unittest.main()
