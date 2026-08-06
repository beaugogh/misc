"""Tests for the --provision auto-provisioning command.

Tests cover:
  - welink-cli: install when missing, auth login when expired, skip when ready
  - git identity: set user.email/name, derive name from email, skip when set
  - --dry-run: prints commands without executing
  - --only: scopes to one source
  - error cases: Node.js missing, git binary missing

All subprocess calls are mocked — no real npm/git/welink-cli invocations.

Run with: python -m unittest discover -s tests -p "test_provision.py" -v
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from contextlib import redirect_stdout, redirect_stderr
import io

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)


class TestProvisionWelinkCli(unittest.TestCase):
    """_provision_welink_cli — install + auth login flow."""

    def _import(self):
        import importlib
        import run as run_mod
        importlib.reload(run_mod)
        return run_mod

    @patch("shutil.which")
    def test_node_missing_returns_false(self, mock_which):
        mock_which.return_value = None  # node not found
        run_mod = self._import()
        with redirect_stdout(io.StringIO()):
            result = run_mod._provision_welink_cli(dry_run=False)
        self.assertFalse(result)

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_installs_welink_when_missing(self, mock_subproc, mock_which):
        """When welink-cli is not in PATH, npm install is called."""
        # First which() call: node → found. Second: welink-cli → not found.
        # Third (verify): welink-cli → found after install.
        mock_which.side_effect = ["/usr/bin/node", None, "/usr/bin/welink-cli"]
        # node --version returns v22
        mock_subproc.return_value = MagicMock(
            returncode=0, stdout="v22.23.1\n", stderr="")
        run_mod = self._import()
        # Mock the adapter's auth_status to return ok after install
        with patch("welink_cli_adapter.WeLinkCLIAdapter") as mock_cls:
            mock_adapter = MagicMock()
            mock_adapter.auth_status.return_value = ("ok", "")
            mock_cls.return_value = mock_adapter
            with redirect_stdout(io.StringIO()):
                result = run_mod._provision_welink_cli(dry_run=False)
        self.assertTrue(result)
        # Verify npm install was called (at least one subprocess call with "npm")
        calls = [c.args[0] for c in mock_subproc.call_args_list]
        npm_calls = [c for c in calls if "npm" in c]
        self.assertTrue(len(npm_calls) > 0, "npm install should be called")

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_auth_login_when_expired(self, mock_subproc, mock_which):
        """When welink-cli is installed but auth expired, auth login is called."""
        mock_which.return_value = "/usr/bin/welink-cli"  # both node and welink-cli found
        mock_subproc.return_value = MagicMock(
            returncode=0, stdout="v22.23.1\n", stderr="")
        run_mod = self._import()
        # First auth_status: not_authenticated. After login: ok.
        with patch("welink_cli_adapter.WeLinkCLIAdapter") as mock_cls:
            mock_adapter = MagicMock()
            mock_adapter.auth_status.side_effect = [
                ("not_authenticated", "token expired"),
                ("ok", ""),
            ]
            mock_cls.return_value = mock_adapter
            with redirect_stdout(io.StringIO()):
                result = run_mod._provision_welink_cli(dry_run=False)
        self.assertTrue(result)
        # Verify auth login was called
        calls = [c.args[0] for c in mock_subproc.call_args_list]
        auth_calls = [c for c in calls if "auth" in c and "login" in c]
        self.assertTrue(len(auth_calls) > 0, "welink-cli auth login should be called")

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_skips_when_already_authenticated(self, mock_subproc, mock_which):
        """When welink-cli is installed and authenticated, no install/login."""
        mock_which.return_value = "/usr/bin/welink-cli"
        mock_subproc.return_value = MagicMock(
            returncode=0, stdout="v22.23.1\n", stderr="")
        run_mod = self._import()
        with patch("welink_cli_adapter.WeLinkCLIAdapter") as mock_cls:
            mock_adapter = MagicMock()
            mock_adapter.auth_status.return_value = ("ok", "")
            mock_cls.return_value = mock_adapter
            with redirect_stdout(io.StringIO()):
                result = run_mod._provision_welink_cli(dry_run=False)
        self.assertTrue(result)
        # No npm install or auth login calls
        calls = [c.args[0] for c in mock_subproc.call_args_list]
        npm_calls = [c for c in calls if "npm" in c]
        auth_calls = [c for c in calls if "auth" in c and "login" in c]
        self.assertEqual(len(npm_calls), 0)
        self.assertEqual(len(auth_calls), 0)

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_node_version_too_old(self, mock_subproc, mock_which):
        """Node.js < 18 should fail."""
        mock_which.return_value = "/usr/bin/node"
        mock_subproc.return_value = MagicMock(
            returncode=0, stdout="v16.20.0\n", stderr="")
        run_mod = self._import()
        with redirect_stdout(io.StringIO()):
            result = run_mod._provision_welink_cli(dry_run=False)
        self.assertFalse(result)

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_dry_run_does_not_execute(self, mock_subproc, mock_which):
        """--dry-run should print commands but not call npm/auth login."""
        # node found, welink-cli not found, then detect() may be called again
        mock_which.side_effect = ["/usr/bin/node", None, None, None, None]
        # node --version is real (not dry-run), returns v22
        mock_subproc.return_value = MagicMock(
            returncode=0, stdout="v22.23.1\n", stderr="")
        run_mod = self._import()
        # Mock the adapter so auth_status doesn't call real detect()
        with patch("welink_cli_adapter.WeLinkCLIAdapter") as mock_cls:
            mock_adapter = MagicMock()
            mock_adapter.auth_status.return_value = ("ok", "")
            mock_cls.return_value = mock_adapter
            with redirect_stdout(io.StringIO()) as buf:
                result = run_mod._provision_welink_cli(dry_run=True)
        # dry-run returns True (assumes success)
        self.assertTrue(result)
        output = buf.getvalue()
        self.assertIn("[dry-run]", output)
        # npm install should NOT have been actually called via subprocess
        calls = [c.args[0] for c in mock_subproc.call_args_list]
        npm_calls = [c for c in calls if "npm" in c]
        self.assertEqual(len(npm_calls), 0)


class TestProvisionGit(unittest.TestCase):
    """_provision_git — set user.email and user.name."""

    def _import(self):
        import importlib
        import run as run_mod
        importlib.reload(run_mod)
        return run_mod

    @patch("shutil.which")
    def test_git_missing_returns_false(self, mock_which):
        mock_which.return_value = None  # git not found
        run_mod = self._import()
        with redirect_stdout(io.StringIO()):
            result = run_mod._provision_git(
                email="bo.gao@huawei.com", name=None, dry_run=False)
        self.assertFalse(result)

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_sets_email_when_not_configured(self, mock_subproc, mock_which):
        """When git user.email is empty, set it via --git-email."""
        mock_which.return_value = "/usr/bin/git"
        # First call: git config --global user.email → empty (rc=1)
        # Second call: git config --global user.email <email> → success
        # Third call: git config --global user.name → empty (rc=1)
        # Fourth call: git config --global user.name <derived> → success
        mock_subproc.side_effect = [
            MagicMock(returncode=1, stdout="", stderr=""),
            MagicMock(returncode=0, stdout="", stderr=""),
            MagicMock(returncode=1, stdout="", stderr=""),
            MagicMock(returncode=0, stdout="", stderr=""),
        ]
        run_mod = self._import()
        with redirect_stdout(io.StringIO()):
            result = run_mod._provision_git(
                email="bo.gao@huawei.com", name=None, dry_run=False)
        self.assertTrue(result)
        # Verify git config --global user.email was set
        calls = [c.args[0] for c in mock_subproc.call_args_list]
        set_email_calls = [
            c for c in calls
            if "config" in c and "user.email" in c and "bo.gao@huawei.com" in c
        ]
        self.assertTrue(len(set_email_calls) > 0, "git config user.email should be set")

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_no_email_and_no_flag_returns_false(self, mock_subproc, mock_which):
        """When email not set and no --git-email provided, should fail."""
        mock_which.return_value = "/usr/bin/git"
        mock_subproc.return_value = MagicMock(
            returncode=1, stdout="", stderr="")
        run_mod = self._import()
        with redirect_stdout(io.StringIO()):
            result = run_mod._provision_git(
                email=None, name=None, dry_run=False)
        self.assertFalse(result)

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_skips_when_email_already_set(self, mock_subproc, mock_which):
        """When git user.email is already set, don't overwrite."""
        mock_which.return_value = "/usr/bin/git"
        # First: user.email → already set. Second: user.name → already set.
        mock_subproc.side_effect = [
            MagicMock(returncode=0, stdout="existing@huawei.com\n", stderr=""),
            MagicMock(returncode=0, stdout="Existing User\n", stderr=""),
        ]
        run_mod = self._import()
        with redirect_stdout(io.StringIO()):
            result = run_mod._provision_git(
                email="new@huawei.com", name="New User", dry_run=False)
        self.assertTrue(result)
        # Should NOT have set user.email (only read it)
        calls = [c.args[0] for c in mock_subproc.call_args_list]
        set_calls = [
            c for c in calls
            if "config" in c and "user.email" in c and "new@huawei.com" in c
        ]
        self.assertEqual(len(set_calls), 0, "should not overwrite existing email")

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_derives_name_from_email(self, mock_subproc, mock_which):
        """When name not provided, derive from email (bo.gao → Bo Gao)."""
        mock_which.return_value = "/usr/bin/git"
        # user.email empty → set. user.name empty → derive.
        mock_subproc.side_effect = [
            MagicMock(returncode=1, stdout="", stderr=""),  # read email
            MagicMock(returncode=0, stdout="", stderr=""),  # set email
            MagicMock(returncode=1, stdout="", stderr=""),  # read name
            MagicMock(returncode=0, stdout="", stderr=""),  # set name
        ]
        run_mod = self._import()
        with redirect_stdout(io.StringIO()) as buf:
            result = run_mod._provision_git(
                email="bo.gao@huawei.com", name=None, dry_run=False)
        self.assertTrue(result)
        output = buf.getvalue()
        self.assertIn("Bo Gao", output)
        self.assertIn("derived from email", output)

    @patch("shutil.which")
    @patch("subprocess.run")
    def test_dry_run_does_not_set(self, mock_subproc, mock_which):
        """--dry-run should print set commands but not execute them."""
        mock_which.return_value = "/usr/bin/git"
        # Reads are real (not dry-run), return empty
        mock_subproc.return_value = MagicMock(
            returncode=1, stdout="", stderr="")
        run_mod = self._import()
        with redirect_stdout(io.StringIO()) as buf:
            result = run_mod._provision_git(
                email="bo.gao@huawei.com", name="Bo Gao", dry_run=True)
        self.assertTrue(result)
        output = buf.getvalue()
        self.assertIn("[dry-run]", output)
        # Only read commands should have been executed (2 calls: email + name reads)
        # Set commands should be dry-run (not executed via subprocess)
        calls = [c.args[0] for c in mock_subproc.call_args_list]
        set_calls = [
            c for c in calls
            if "config" in c and "user.email" in c and "bo.gao@huawei.com" in c
        ]
        self.assertEqual(len(set_calls), 0, "dry-run should not execute set commands")


class TestCmdProvision(unittest.TestCase):
    """cmd_provision — top-level orchestration."""

    def _import(self):
        import importlib
        import run as run_mod
        importlib.reload(run_mod)
        return run_mod

    def test_both_provisioned(self):
        run_mod = self._import()
        with patch.object(run_mod, "_provision_welink_cli", return_value=True), \
             patch.object(run_mod, "_provision_git", return_value=True), \
             redirect_stdout(io.StringIO()):
            rc = run_mod.cmd_provision(
                git_email="bo.gao@huawei.com", git_name=None,
                only=None, dry_run=False)
        self.assertEqual(rc, 0)

    def test_welink_failure_returns_nonzero(self):
        run_mod = self._import()
        with patch.object(run_mod, "_provision_welink_cli", return_value=False), \
             patch.object(run_mod, "_provision_git", return_value=True), \
             redirect_stdout(io.StringIO()):
            rc = run_mod.cmd_provision(
                git_email=None, git_name=None, only=None, dry_run=False)
        self.assertEqual(rc, 1)

    def test_git_failure_returns_nonzero(self):
        run_mod = self._import()
        with patch.object(run_mod, "_provision_welink_cli", return_value=True), \
             patch.object(run_mod, "_provision_git", return_value=False), \
             redirect_stdout(io.StringIO()):
            rc = run_mod.cmd_provision(
                git_email=None, git_name=None, only=None, dry_run=False)
        self.assertEqual(rc, 1)

    def test_only_git_skips_welink(self):
        run_mod = self._import()
        mock_welink = MagicMock(return_value=True)
        mock_git = MagicMock(return_value=True)
        with patch.object(run_mod, "_provision_welink_cli", mock_welink), \
             patch.object(run_mod, "_provision_git", mock_git), \
             redirect_stdout(io.StringIO()):
            rc = run_mod.cmd_provision(
                git_email="bo.gao@huawei.com", git_name=None,
                only="git", dry_run=False)
        self.assertEqual(rc, 0)
        mock_welink.assert_not_called()

    def test_only_welink_skips_git(self):
        run_mod = self._import()
        mock_welink = MagicMock(return_value=True)
        mock_git = MagicMock(return_value=True)
        with patch.object(run_mod, "_provision_welink_cli", mock_welink), \
             patch.object(run_mod, "_provision_git", mock_git), \
             redirect_stdout(io.StringIO()):
            rc = run_mod.cmd_provision(
                git_email=None, git_name=None,
                only="welink", dry_run=False)
        self.assertEqual(rc, 0)
        mock_git.assert_not_called()


if __name__ == "__main__":
    unittest.main()
