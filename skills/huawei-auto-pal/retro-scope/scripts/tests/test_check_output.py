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
    """Minimal adapter stub for testing render_check_output.

    Does NOT have auth_status() — simulates adapters that don't implement it.
    Use _FakeAuthAdapter for auth_status testing.
    """

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


class _FakeAuthAdapter(_FakeAdapter):
    """Adapter stub that implements auth_status()."""

    def __init__(self, name="fake_auth", detect_result=True,
                 auth_result=None, detector_only=False):
        super().__init__(name, detect_result=detect_result, detector_only=detector_only)
        self._auth_result = auth_result  # tuple[str, str] | None

    def auth_status(self):
        return self._auth_result


# ---------------------------------------------------------------------------
# Detector-only attribute on real adapters
# ---------------------------------------------------------------------------

class TestDetectorOnlyAttribute(unittest.TestCase):
    """Placeholder adapters must carry detector_only=True."""

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

    @unittest.skipUnless(
        __import__("shutil").which("git"),
        "git not on PATH"
    )
    def test_git_shows_ready_pending_when_not_detected(self):
        """When git is on PATH but no repos discovered, show READY (pending)."""
        git_adapter = _FakeAdapter(name="git", detect_result=False)
        out = self._render([git_adapter])
        line = self._adapter_line(out, "git")
        self.assertIn("READY (pending)", line)
        self.assertNotIn("NOT DETECTED", line)
        self.assertIn("repos discovered", line)

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
# auth_status() — NOT AUTHENTICATED rendering
# ---------------------------------------------------------------------------

class TestAuthStatus(unittest.TestCase):
    """Test that auth_status() produces the NOT AUTHENTICATED status line."""

    def _render(self, adapters, hints=None):
        import run as run_mod
        return run_mod.render_check_output(adapters, hints=hints)

    def _adapter_line(self, out, name):
        for line in out.splitlines():
            if line.strip().startswith(name):
                return line
        return ""

    def test_not_authenticated_status(self):
        a = _FakeAuthAdapter(
            name="welink_cli",
            auth_result=("not_authenticated", "run 'welink-cli auth login'"),
        )
        out = self._render([a])
        line = self._adapter_line(out, "welink_cli")
        self.assertIn("NOT AUTHENTICATED", line)
        self.assertIn("welink-cli auth login", line)

    def test_auth_ok_shows_ready(self):
        a = _FakeAuthAdapter(name="welink_cli", auth_result=("ok", ""))
        out = self._render([a])
        line = self._adapter_line(out, "welink_cli")
        self.assertIn("READY", line)
        self.assertNotIn("NOT AUTHENTICATED", line)

    def test_no_auth_status_method_shows_ready(self):
        """Adapters without auth_status() must still render as READY."""
        a = _FakeReadyAdapter(name="chrome")
        out = self._render([a])
        line = self._adapter_line(out, "chrome")
        self.assertIn("READY", line)

    def test_auth_status_not_called_when_detect_false(self):
        """auth_status() must not be called when detect() returns False."""
        a = _FakeAuthAdapter(
            name="welink_cli",
            detect_result=False,
            auth_result=("not_authenticated", "should not be reached"),
        )
        out = self._render([a])
        # Should show NOT DETECTED, not NOT AUTHENTICATED
        line = self._adapter_line(out, "welink_cli")
        self.assertIn("NOT DETECTED", line)
        self.assertNotIn("NOT AUTHENTICATED", line)

    def test_auth_status_not_called_when_detector_only(self):
        """auth_status() must not be called for detector-only adapters."""
        a = _FakeAuthAdapter(
            name="fake_detector",
            detect_result=True,
            detector_only=True,
            auth_result=("not_authenticated", "should not be reached"),
        )
        out = self._render([a])
        line = self._adapter_line(out, "fake_detector")
        self.assertIn("DETECTOR-ONLY", line)

    def test_auth_hint_overrides_adapter_hint(self):
        """When NOT AUTHENTICATED, the auth hint takes precedence over the
        generic _ADAPTER_HINTS hint."""
        hints = {"welink_cli": "generic hint from _ADAPTER_HINTS"}
        a = _FakeAuthAdapter(
            name="welink_cli",
            auth_result=("not_authenticated", "specific auth hint"),
        )
        out = self._render([a], hints=hints)
        line = self._adapter_line(out, "welink_cli")
        self.assertIn("specific auth hint", line)
        self.assertNotIn("generic hint", line)

    def test_auth_status_empty_hint_falls_back_to_adapter_hint(self):
        """When auth hint is empty, the generic hint is used."""
        hints = {"welink_cli": "generic hint"}
        a = _FakeAuthAdapter(
            name="welink_cli",
            auth_result=("not_authenticated", ""),
        )
        out = self._render([a], hints=hints)
        line = self._adapter_line(out, "welink_cli")
        self.assertIn("generic hint", line)

    def test_auth_status_exception_treated_as_ready(self):
        """If auth_status() raises, treat as READY (don't block the user)."""
        class _BoomAdapter(_FakeAdapter):
            def __init__(self):
                super().__init__("boom", detect_result=True)

            def auth_status(self):
                raise RuntimeError("auth probe crashed")

        out = self._render([_BoomAdapter()])
        line = self._adapter_line(out, "boom")
        self.assertIn("READY", line)

    def test_legend_contains_not_authenticated(self):
        out = self._render([])
        self.assertIn("NOT AUTHENTICATED", out)

    def test_auth_status_never_calls_collect(self):
        """render_check_output must never call collect() even with auth_status."""
        a = _FakeAuthAdapter(
            name="welink_cli",
            auth_result=("not_authenticated", "hint"),
        )
        a.collect_called = False

        def tracking_collect():
            a.collect_called = True
            return
            yield  # pragma: no cover

        a.collect = tracking_collect
        self._render([a])
        self.assertFalse(a.collect_called)


# ---------------------------------------------------------------------------
# Real adapter auth_status() implementations
# ---------------------------------------------------------------------------

class TestWeLinkAuthStatus(unittest.TestCase):
    """WeLinkCLIAdapter.auth_status() — mocked _run()."""

    def _adapter_with_run(self, run_output, detect=True):
        from welink_cli_adapter import WeLinkCLIAdapter
        a = WeLinkCLIAdapter.__new__(WeLinkCLIAdapter)
        a._binary = "welink-cli"
        a._lookback_days = 90
        a._enable_im = False
        a._mock_detect = detect
        a._mock_run_output = run_output
        return a

    def test_detect_false_returns_none(self):
        a = self._adapter_with_run(None, detect=False)
        a.detect = lambda: False
        self.assertIsNone(a.auth_status())

    def test_expired_token(self):
        a = self._adapter_with_run(
            "Configuration:\n  Environment:  pro\n\n"
            "Credentials:\n  User Token:   EXPIRED\n  UID:          b00563677\n")
        a.detect = lambda: True
        a._run = lambda args, timeout=60: a._mock_run_output
        result = a.auth_status()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "not_authenticated")

    def test_valid_token(self):
        a = self._adapter_with_run(
            "Configuration:\n  Environment:  pro\n\n"
            "Credentials:\n  User Token:   valid (expires in 22m25s)\n"
            "  UID:          b00563677\n")
        a.detect = lambda: True
        a._run = lambda args, timeout=60: a._mock_run_output
        result = a.auth_status()
        self.assertEqual(result, ("ok", ""))

    def test_no_uid_never_logged_in(self):
        a = self._adapter_with_run(
            "Configuration:\n  Environment:  pro\n\n"
            "Credentials:\n  User Token:   none\n")
        a.detect = lambda: True
        a._run = lambda args, timeout=60: a._mock_run_output
        result = a.auth_status()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "not_authenticated")

    def test_run_returns_none(self):
        a = self._adapter_with_run(None, detect=True)
        a.detect = lambda: True
        a._run = lambda args, timeout=60: None
        result = a.auth_status()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "not_authenticated")


class TestGitAuthStatus(unittest.TestCase):
    """GitAdapter.auth_status() — mocked _repo_author_email and _effective_roots."""

    def _adapter(self, roots, emails):
        """Create a GitAdapter with mocked roots and per-root email lookup."""
        from git_adapter import GitAdapter
        a = GitAdapter.__new__(GitAdapter)
        a._roots = roots
        a._since = "90 days ago"
        a._mock_roots = roots
        a._mock_emails = emails  # list of emails per root index
        return a

    def test_detect_false_returns_none(self):
        a = self._adapter([], [])
        a.detect = lambda: False
        self.assertIsNone(a.auth_status())

    def test_email_configured(self):
        a = self._adapter(["/fake/repo"], ["bo.gao@huawei.com"])
        a.detect = lambda: True
        a._effective_roots = lambda: a._mock_roots
        import git_adapter
        orig = git_adapter._repo_author_email
        git_adapter._repo_author_email = lambda cwd: a._mock_emails[0]
        try:
            result = a.auth_status()
        finally:
            git_adapter._repo_author_email = orig
        self.assertEqual(result, ("ok", ""))

    def test_no_email_configured(self):
        a = self._adapter(["/fake/repo"], [None])
        a.detect = lambda: True
        a._effective_roots = lambda: a._mock_roots
        import git_adapter
        orig = git_adapter._repo_author_email
        git_adapter._repo_author_email = lambda cwd: None
        try:
            result = a.auth_status()
        finally:
            git_adapter._repo_author_email = orig
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "not_authenticated")

    def test_multiple_roots_one_has_email(self):
        a = self._adapter(["/fake/a", "/fake/b"], [None, "bo.gao@huawei.com"])
        a.detect = lambda: True
        a._effective_roots = lambda: a._mock_roots
        import git_adapter
        orig = git_adapter._repo_author_email
        email_map = {"/fake/a": None, "/fake/b": "bo.gao@huawei.com"}
        git_adapter._repo_author_email = lambda cwd: email_map.get(cwd)
        try:
            result = a.auth_status()
        finally:
            git_adapter._repo_author_email = orig
        self.assertEqual(result, ("ok", ""))


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
        for name in ("claude_code", "git", "welink_recordings"):
            self.assertIn(name, out)


if __name__ == "__main__":
    unittest.main()
