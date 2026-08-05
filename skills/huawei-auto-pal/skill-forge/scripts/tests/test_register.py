"""Tests for register.py — the registration helper entry point.

Run with: python -m unittest discover -s tests -p "test_register.py" -v
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

import register
from agent_targets import AgentTarget


class TestFindOutputSkills(unittest.TestCase):
    """Test _find_output_skills scans output/ correctly."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="reg_test_")

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _make_skill(self, name):
        d = Path(self._tmp, name)
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text("---\nname: %s\n---\n# %s\n" % (name, name), encoding="utf-8")
        return d

    def test_finds_skills_with_skill_md(self):
        self._make_skill("skill-a")
        self._make_skill("skill-b")
        skills = register._find_output_skills(self._tmp)
        self.assertEqual(sorted(skills), ["skill-a", "skill-b"])

    def test_ignores_dirs_without_skill_md(self):
        self._make_skill("real-skill")
        Path(self._tmp, "not-a-skill").mkdir()
        skills = register._find_output_skills(self._tmp)
        self.assertEqual(skills, ["real-skill"])

    def test_ignores_internal_dirs(self):
        self._make_skill("real-skill")
        for skip in (".skill-forge-backups", "session_records", "personal-context"):
            d = Path(self._tmp, skip)
            d.mkdir()
            (d / "SKILL.md").write_text("---\nname: skip\n---\n", encoding="utf-8")
        skills = register._find_output_skills(self._tmp)
        self.assertEqual(skills, ["real-skill"])

    def test_empty_output_dir(self):
        skills = register._find_output_skills(self._tmp)
        self.assertEqual(skills, [])

    def test_nonexistent_dir(self):
        skills = register._find_output_skills("/nonexistent/path")
        self.assertEqual(skills, [])


class TestIsInstalled(unittest.TestCase):
    """Test _is_installed checks agent skills dirs."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="inst_test_")

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _agent(self, skills_dir):
        from agent_targets import AgentTarget
        return AgentTarget(
            agent_id="test", display_name="Test",
            skills_dir=skills_dir, memory_dir=None,
            memory_format="none", detect_path="",
        )

    def test_installed(self):
        skills_dir = Path(self._tmp, "skills")
        (skills_dir / "my-skill").mkdir(parents=True)
        agent = self._agent(str(skills_dir))
        self.assertTrue(register._is_installed("my-skill", agent))

    def test_not_installed(self):
        agent = self._agent(str(Path(self._tmp, "skills")))
        self.assertFalse(register._is_installed("my-skill", agent))

    def test_none_skills_dir(self):
        agent = self._agent(None)
        self.assertFalse(register._is_installed("my-skill", agent))


class TestRegisterList(unittest.TestCase):
    """Test the --list command output."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="reg_list_")
        self._patch_output = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch_output.start()
        # No agents detected by default.
        self._patch_agents = patch.object(register, "discover_agents", return_value=[])
        self._patch_agents.start()

    def tearDown(self):
        self._patch_output.stop()
        self._patch_agents.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _make_skill(self, name):
        d = Path(self._tmp, name)
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: %s\n---\n" % name, encoding="utf-8")

    def test_list_no_skills(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_list(None, [], [])
        out = buf.getvalue()
        self.assertIn("No skills found", out)

    def test_list_with_skills(self):
        import io
        from contextlib import redirect_stdout
        self._make_skill("test-skill")
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_list(None, [], ["test-skill"])
        out = buf.getvalue()
        self.assertIn("test-skill", out)
        self.assertIn("not registered", out)


class TestDownloadsDir(unittest.TestCase):
    """Test _downloads_dir returns a valid path."""

    def test_returns_path_with_downloads(self):
        path = register._downloads_dir()
        self.assertIn("Downloads", path)

    def test_path_is_under_home(self):
        import os
        path = register._downloads_dir()
        home = os.path.expanduser("~")
        # On all platforms the Downloads dir is under home.
        self.assertTrue(path.startswith(home))


class TestCmdArchive(unittest.TestCase):
    """Test the --archive command."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="archive_test_")
        self._old_output = register._OUTPUT_DIR
        self._old_cwd = os.getcwd()
        # Patch _OUTPUT_DIR to a temp dir with sample files.
        self._output = os.path.join(self._tmp, "output")
        os.makedirs(self._output)
        with open(os.path.join(self._output, "report.html"), "w") as f:
            f.write("<html>test</html>")
        os.makedirs(os.path.join(self._output, "npm-corporate-proxy"))
        with open(os.path.join(self._output, "npm-corporate-proxy", "SKILL.md"), "w") as f:
            f.write("---\nname: npm-corporate-proxy\n---\n# test\n")
        # Patch _downloads_dir to return a temp downloads dir.
        self._downloads = os.path.join(self._tmp, "Downloads")
        self._patch = patch.object(register, "_downloads_dir", return_value=self._downloads)
        self._patch.start()
        register._OUTPUT_DIR = self._output

    def tearDown(self):
        self._patch.stop()
        register._OUTPUT_DIR = self._old_output
        os.chdir(self._old_cwd)
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_dry_run_does_not_write(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_archive(
                type("Args", (), {"dry_run": True})(), [], []
            )
        out = buf.getvalue()
        self.assertIn("Would zip", out)
        # No zip created.
        zips = [f for f in os.listdir(self._downloads) if f.endswith(".zip")] if os.path.isdir(self._downloads) else []
        self.assertEqual(len(zips), 0)

    def test_creates_zip_in_downloads(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_archive(
                type("Args", (), {"dry_run": False})(), [], []
            )
        out = buf.getvalue()
        self.assertIn("archived to:", out)
        self.assertIn(self._downloads, out)
        # Zip file exists.
        zips = [f for f in os.listdir(self._downloads) if f.endswith(".zip")]
        self.assertEqual(len(zips), 1)
        # Verify zip contents.
        import zipfile
        zip_path = os.path.join(self._downloads, zips[0])
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            self.assertIn("report.html", names)
            self.assertIn("npm-corporate-proxy/SKILL.md", names)

    def test_zip_excludes_pycache(self):
        # Create __pycache__ in output.
        pycache = os.path.join(self._output, "__pycache__")
        os.makedirs(pycache)
        with open(os.path.join(pycache, "junk.pyc"), "wb") as f:
            f.write(b"\x00\x00")
        register.cmd_archive(
            type("Args", (), {"dry_run": False})(), [], []
        )
        zips = [f for f in os.listdir(self._downloads) if f.endswith(".zip")]
        self.assertEqual(len(zips), 1)
        import zipfile
        zip_path = os.path.join(self._downloads, zips[0])
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            self.assertNotIn("__pycache__/junk.pyc", names)

    def test_zip_excludes_backups(self):
        backup = os.path.join(self._output, ".skill-forge-backups")
        os.makedirs(backup)
        with open(os.path.join(backup, "old.md"), "w") as f:
            f.write("old")
        register.cmd_archive(
            type("Args", (), {"dry_run": False})(), [], []
        )
        zips = [f for f in os.listdir(self._downloads) if f.endswith(".zip")]
        import zipfile
        zip_path = os.path.join(self._downloads, zips[0])
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            self.assertFalse(any(".skill-forge-backups" in n for n in names))

    def test_missing_output_dir(self):
        register._OUTPUT_DIR = "/nonexistent/path/output"
        with self.assertRaises(SystemExit):
            register.cmd_archive(
                type("Args", (), {"dry_run": False})(), [], []
            )

    def test_archive_reports_skill_count(self):
        """Archive output should report how many skills were included."""
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_archive(
                type("Args", (), {"dry_run": False})(), [], ["npm-corporate-proxy"]
            )
        out = buf.getvalue()
        self.assertIn("1 skill(s) included", out)
        self.assertIn("npm-corporate-proxy", out)

    def test_archive_warns_when_no_skills(self):
        """Archive should warn when output/ has no skills (only reports/records)."""
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_archive(
                type("Args", (), {"dry_run": False})(), [], []
            )
        out = buf.getvalue()
        self.assertIn("No skills found", out)


class TestCmdDist(unittest.TestCase):
    """Test the --dist command — zips the whole skill folder for sharing."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="dist_test_")
        self._old_root = register._SKILL_ROOT
        self._old_output = register._OUTPUT_DIR
        # Build a fake skill root: <tmp>/huawei-auto-pal/...
        self._skill_root = os.path.join(self._tmp, "huawei-auto-pal")
        os.makedirs(self._skill_root)
        # Core skill files.
        with open(os.path.join(self._skill_root, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("---\nname: huawei-auto-pal\n---\n# test\n")
        # Subdirectory with code.
        sub = os.path.join(self._skill_root, "skill-forge", "scripts")
        os.makedirs(sub)
        with open(os.path.join(sub, "register.py"), "w", encoding="utf-8") as f:
            f.write("# test code\n")
        # Personal output (must be excluded).
        out = os.path.join(self._skill_root, "output")
        os.makedirs(out)
        with open(os.path.join(out, "report.html"), "w", encoding="utf-8") as f:
            f.write("<html>personal</html>")
        # .env (must be excluded — credentials).
        with open(os.path.join(self._skill_root, ".env"), "w", encoding="utf-8") as f:
            f.write("GITHUB_TOKEN=secret\n")
        # .gitignore files (hidden files — AgentCenter rejects them).
        with open(os.path.join(self._skill_root, ".gitignore"), "w", encoding="utf-8") as f:
            f.write("output/\n.env\n")
        with open(os.path.join(sub, ".gitignore"), "w", encoding="utf-8") as f:
            f.write("__pycache__/\n")
        # env.example (non-hidden, safe template — must be included).
        with open(os.path.join(self._skill_root, "env.example"), "w", encoding="utf-8") as f:
            f.write("# template\n")
        # __pycache__ (must be excluded).
        pycache = os.path.join(sub, "__pycache__")
        os.makedirs(pycache)
        with open(os.path.join(pycache, "junk.pyc"), "wb") as f:
            f.write(b"\x00\x00")
        # Patch _SKILL_ROOT and _downloads_dir.
        self._downloads = os.path.join(self._tmp, "Downloads")
        self._patch = patch.object(register, "_downloads_dir", return_value=self._downloads)
        self._patch.start()
        register._SKILL_ROOT = self._skill_root

    def tearDown(self):
        self._patch.stop()
        register._SKILL_ROOT = self._old_root
        register._OUTPUT_DIR = self._old_output
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _run_dist(self, dry_run=False):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_dist(type("Args", (), {"dry_run": dry_run})(), [], [])
        return buf.getvalue()

    def _zip_names(self):
        import zipfile
        zips = [f for f in os.listdir(self._downloads) if f.endswith(".zip")]
        self.assertEqual(len(zips), 1)
        zip_path = os.path.join(self._downloads, zips[0])
        with zipfile.ZipFile(zip_path, "r") as zf:
            return zf.namelist(), zip_path

    def test_dry_run_does_not_write(self):
        out = self._run_dist(dry_run=True)
        self.assertIn("Would zip", out)
        self.assertFalse(os.path.isdir(self._downloads) and os.listdir(self._downloads))

    def test_creates_zip_in_downloads(self):
        out = self._run_dist()
        self.assertIn("Skill package saved to:", out)
        self.assertIn("AgentCenter", out)
        names, _ = self._zip_names()
        # Skill code is included, rooted under the skill folder name.
        self.assertTrue(any(n == "huawei-auto-pal/SKILL.md" for n in names))
        self.assertTrue(any(n.endswith("register.py") for n in names))

    def test_excludes_output_dir(self):
        self._run_dist()
        names, _ = self._zip_names()
        leaked = [n for n in names if n.startswith("huawei-auto-pal/output/")]
        self.assertFalse(leaked, f"output/ dir leaked: {leaked}")

    def test_excludes_env_file(self):
        self._run_dist()
        names, _ = self._zip_names()
        self.assertFalse(any(n.endswith(".env") for n in names), f".env leaked: {names}")

    def test_excludes_all_hidden_files(self):
        """AgentCenter rejects hidden files — all dotfiles must be excluded."""
        self._run_dist()
        names, _ = self._zip_names()
        leaked = [n for n in names if os.path.basename(n).startswith(".")]
        self.assertFalse(leaked, f"hidden files leaked: {leaked}")

    def test_includes_non_hidden_env_example(self):
        """env.example (non-hidden template) must be included for colleagues."""
        self._run_dist()
        names, _ = self._zip_names()
        self.assertTrue(any(n.endswith("env.example") for n in names),
                        f"env.example missing: {names}")

    def test_excludes_pycache_and_pyc(self):
        self._run_dist()
        names, _ = self._zip_names()
        self.assertFalse(any("__pycache__" in n for n in names), f"pycache leaked: {names}")
        self.assertFalse(any(n.endswith(".pyc") for n in names), f"pyc leaked: {names}")

    def test_zip_extracts_to_single_dir(self):
        """The zip should extract into a single huawei-auto-pal/ dir for colleagues."""
        self._run_dist()
        names, zip_path = self._zip_names()
        # Every path starts with the skill folder name.
        for n in names:
            self.assertTrue(n.startswith("huawei-auto-pal/"),
                            f"path not under skill dir: {n}")

    def test_missing_skill_root(self):
        register._SKILL_ROOT = "/nonexistent/skill/root"
        with self.assertRaises(SystemExit):
            register.cmd_dist(type("Args", (), {"dry_run": False})(), [], [])


class TestMutualExclusivity(unittest.TestCase):
    """Test that --archive/--dist/--install/--install-memory cannot combine."""

    def _run_main(self, *cli_args):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        old_argv = sys.argv
        sys.argv = ["register.py"] + list(cli_args)
        buf_out, buf_err = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                register.main()
        except SystemExit as e:
            sys.argv = old_argv
            return e.code, buf_out.getvalue(), buf_err.getvalue()
        sys.argv = old_argv
        return 0, buf_out.getvalue(), buf_err.getvalue()

    def test_archive_and_dist_rejected(self):
        code, out, err = self._run_main("--archive", "--dist", "--dry-run")
        self.assertNotEqual(code, 0)
        self.assertIn("mutually exclusive", err)

    def test_dist_and_install_rejected(self):
        code, out, err = self._run_main("--dist", "--install", "some-skill", "--dry-run")
        self.assertNotEqual(code, 0)
        self.assertIn("mutually exclusive", err)

    def test_single_mode_accepted(self):
        # --dist alone should not trigger the mutual-exclusivity guard.
        # It may exit for other reasons (e.g. no skill root), but not with
        # the "mutually exclusive" message.
        code, out, err = self._run_main("--dist", "--dry-run")
        self.assertNotIn("mutually exclusive", err)


class TestProposalSummary(unittest.TestCase):
    """Test _proposal_summary extracts problem summary from PROPOSAL.md."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="prop_sum_")
        self._patch = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _make_skill(self, name, with_proposal=True, problem_line="Something broke."):
        d = Path(self._tmp, name)
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: %s\ndescription: A fallback description.\n---\n# %s\n" % (name, name),
            encoding="utf-8",
        )
        if with_proposal:
            (d / "PROPOSAL.md").write_text(
                "# Proposal: %s\n\n## Problem\n\n%s\n\n## Evidence\n\nData\n" % (name, problem_line),
                encoding="utf-8",
            )

    def test_extracts_problem_from_proposal(self):
        self._make_skill("my-skill", problem_line="npm hangs forever on large packages.")
        summary, has_proposal = register._proposal_summary("my-skill")
        self.assertTrue(has_proposal)
        self.assertIn("npm hangs", summary)

    def test_falls_back_to_description_without_proposal(self):
        self._make_skill("legacy-skill", with_proposal=False)
        summary, has_proposal = register._proposal_summary("legacy-skill")
        self.assertFalse(has_proposal)
        self.assertIn("fallback description", summary)

    def test_returns_default_when_nothing_available(self):
        summary, has_proposal = register._proposal_summary("nonexistent")
        self.assertFalse(has_proposal)
        self.assertIn("no description", summary)


class TestCmdDescribe(unittest.TestCase):
    """Test the --describe command."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="desc_")
        self._patch = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _make_skill(self, name, with_proposal=True, proposal_body="Full proposal text."):
        d = Path(self._tmp, name)
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: %s\ndescription: Desc fallback.\n---\n# %s\n" % (name, name),
            encoding="utf-8",
        )
        if with_proposal:
            (d / "PROPOSAL.md").write_text(proposal_body, encoding="utf-8")

    def _run_describe(self, name):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        args = type("A", (), {"describe": name})()
        with redirect_stdout(buf):
            register.cmd_describe(args, [], [])
        return buf.getvalue()

    def test_prints_full_proposal(self):
        self._make_skill("my-skill", proposal_body="# Proposal: my-skill\n\nBilingual text here.")
        out = self._run_describe("my-skill")
        self.assertIn("Bilingual text here.", out)

    def test_falls_back_to_description(self):
        self._make_skill("legacy", with_proposal=False)
        out = self._run_describe("legacy")
        self.assertIn("Desc fallback.", out)
        self.assertIn("No detailed PROPOSAL.md", out)

    def test_missing_skill_exits(self):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        buf_err = io.StringIO()
        args = type("A", (), {"describe": "nonexistent"})()
        with self.assertRaises(SystemExit):
            with redirect_stderr(buf_err):
                register.cmd_describe(args, [], [])


class TestListWithProposal(unittest.TestCase):
    """Test that --list output includes problem summaries."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="list_prop_")
        self._patch_output = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch_output.start()
        self._patch_agents = patch.object(register, "discover_agents", return_value=[])
        self._patch_agents.start()

    def tearDown(self):
        self._patch_output.stop()
        self._patch_agents.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_list_shows_proposal_summary(self):
        d = Path(self._tmp, "my-skill")
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: my-skill\n---\n", encoding="utf-8")
        (d / "PROPOSAL.md").write_text(
            "# Proposal\n\n## Problem\n\nnpm hangs forever.\n", encoding="utf-8",
        )
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_list(None, [], ["my-skill"])
        out = buf.getvalue()
        self.assertIn("npm hangs", out)
        self.assertIn("Problem:", out)

    def test_list_shows_description_fallback(self):
        d = Path(self._tmp, "legacy")
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: legacy\ndescription: A legacy skill desc.\n---\n", encoding="utf-8",
        )
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            register.cmd_list(None, [], ["legacy"])
        out = buf.getvalue()
        self.assertIn("legacy skill desc", out)
        self.assertIn("from description", out)


class TestInstallWithAgentFlag(unittest.TestCase):
    """Test --install --agent selects specific agents."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="install_agent_")
        self._patch_output = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch_output.start()
        # Create a fake skill to install.
        d = Path(self._tmp, "test-skill")
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: test-skill\n---\n# test\n", encoding="utf-8")
        # Fake agents: claude_code and codeagent, both with skills dirs.
        self.claude_skills = Path(self._tmp, "claude", "skills")
        self.claude_skills.mkdir(parents=True)
        self.cac_skills = Path(self._tmp, "cac", "skills")
        self.cac_skills.mkdir(parents=True)
        self.agents = [
            AgentTarget(agent_id="claude_code", display_name="Claude Code",
                        skills_dir=str(self.claude_skills), memory_dir=None,
                        memory_format="none", detect_path=""),
            AgentTarget(agent_id="codeagent", display_name="CodeAgent",
                        skills_dir=str(self.cac_skills), memory_dir=None,
                        memory_format="none", detect_path=""),
        ]
        self._patch_agents = patch.object(register, "discover_agents", return_value=self.agents)
        self._patch_agents.start()

    def tearDown(self):
        self._patch_output.stop()
        self._patch_agents.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _run_install(self, *extra_args):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        old_argv = sys.argv
        sys.argv = ["register.py", "--install", "test-skill"] + list(extra_args)
        buf_out, buf_err = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                register.main()
        except SystemExit as e:
            sys.argv = old_argv
            return e.code, buf_out.getvalue(), buf_err.getvalue()
        sys.argv = old_argv
        return 0, buf_out.getvalue(), buf_err.getvalue()

    def test_installs_into_selected_agent_only(self):
        code, out, err = self._run_install("--agent", "codeagent")
        self.assertEqual(code, 0)
        # Installed into CodeAgent.
        self.assertTrue((self.cac_skills / "test-skill" / "SKILL.md").is_file())
        # NOT installed into Claude Code.
        self.assertFalse((self.claude_skills / "test-skill").exists())

    def test_installs_into_multiple_agents(self):
        code, out, err = self._run_install("--agent", "codeagent,claude_code")
        self.assertEqual(code, 0)
        self.assertTrue((self.cac_skills / "test-skill" / "SKILL.md").is_file())
        self.assertTrue((self.claude_skills / "test-skill" / "SKILL.md").is_file())

    def test_unknown_agent_id_errors(self):
        code, out, err = self._run_install("--agent", "nonexistent")
        self.assertNotEqual(code, 0)
        self.assertIn("unknown or undetected", err)

    def test_no_agent_flag_lists_and_exits(self):
        code, out, err = self._run_install()
        self.assertEqual(code, 0)
        self.assertIn("Select an agent", out)
        # Nothing installed.
        self.assertFalse((self.cac_skills / "test-skill").exists())
        self.assertFalse((self.claude_skills / "test-skill").exists())


class TestInstallMemoryWithAgentFlag(unittest.TestCase):
    """Test --install-memory --agent selects specific agents."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="install_mem_agent_")
        self._patch_output = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch_output.start()
        # Create personal-context memory.
        pc = Path(self._tmp, "personal-context")
        pc.mkdir()
        (pc / "SKILL.md").write_text("---\nname: personal-context\n---\n# Personal Context\n",
                                     encoding="utf-8")
        # Fake agents.
        self.claude_mem = Path(self._tmp, "claude", "projects", "slug", "memory")
        self.claude_mem.mkdir(parents=True)
        self.cac_mem = Path(self._tmp, "cac", "projects", "slug", "memory")
        self.cac_mem.mkdir(parents=True)
        self.agents = [
            AgentTarget(agent_id="claude_code", display_name="Claude Code",
                        skills_dir=None, memory_dir=str(self.claude_mem),
                        memory_format="claude_memory", detect_path=""),
            AgentTarget(agent_id="codeagent", display_name="CodeAgent",
                        skills_dir=None, memory_dir=str(self.cac_mem),
                        memory_format="claude_memory", detect_path=""),
        ]
        self._patch_agents = patch.object(register, "discover_agents", return_value=self.agents)
        self._patch_agents.start()

    def tearDown(self):
        self._patch_output.stop()
        self._patch_agents.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _run_install_memory(self, *extra_args):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        old_argv = sys.argv
        sys.argv = ["register.py", "--install-memory"] + list(extra_args)
        buf_out, buf_err = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                register.main()
        except SystemExit as e:
            sys.argv = old_argv
            return e.code, buf_out.getvalue(), buf_err.getvalue()
        sys.argv = old_argv
        return 0, buf_out.getvalue(), buf_err.getvalue()

    def test_installs_memory_into_selected_agent(self):
        code, out, err = self._run_install_memory("--agent", "codeagent")
        self.assertEqual(code, 0)
        self.assertIn("CodeAgent", out)

    def test_no_agent_flag_lists_and_exits(self):
        code, out, err = self._run_install_memory()
        self.assertEqual(code, 0)
        self.assertIn("Select an agent", out)


class TestMutualExclusivityWithDescribe(unittest.TestCase):
    """Test --describe participates in mutual exclusivity."""

    def _run_main(self, *cli_args):
        import io
        from contextlib import redirect_stdout, redirect_stderr
        old_argv = sys.argv
        sys.argv = ["register.py"] + list(cli_args)
        buf_out, buf_err = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                register.main()
        except SystemExit as e:
            sys.argv = old_argv
            return e.code, buf_out.getvalue(), buf_err.getvalue()
        sys.argv = old_argv
        return 0, buf_out.getvalue(), buf_err.getvalue()

    def test_describe_and_install_rejected(self):
        code, out, err = self._run_main("--describe", "x", "--install", "y")
        self.assertNotEqual(code, 0)
        self.assertIn("mutually exclusive", err)


class TestSafeOutputSubpath(unittest.TestCase):
    """Test that _safe_output_subpath blocks path traversal."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="safe_path_")
        self._patch = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_valid_name_resolves(self):
        resolved = register._safe_output_subpath("my-skill")
        self.assertTrue(resolved.startswith(self._tmp))

    def test_traversal_blocked(self):
        with self.assertRaises(SystemExit):
            register._safe_output_subpath("../etc")

    def test_deep_traversal_blocked(self):
        with self.assertRaises(SystemExit):
            register._safe_output_subpath("../../../../etc")


class TestReadFrontmatterFoldedScalar(unittest.TestCase):
    """Test _read_frontmatter_description handles folded scalars (>-)."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="fm_fold_")

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_folded_scalar_returns_description(self):
        d = Path(self._tmp, "my-skill")
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: >-\n  This is a long description\n  spanning lines.\n---\n# my-skill\n",
            encoding="utf-8",
        )
        desc = register._read_frontmatter_description(str(d))
        self.assertIsNotNone(desc)
        self.assertIn("long description", desc)

    def test_plain_scalar_returns_description(self):
        d = Path(self._tmp, "my-skill")
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: A plain desc.\n---\n# my-skill\n",
            encoding="utf-8",
        )
        desc = register._read_frontmatter_description(str(d))
        self.assertEqual(desc, "A plain desc.")

    def test_dashes_in_value_not_split(self):
        d = Path(self._tmp, "my-skill")
        d.mkdir()
        (d / "SKILL.md").write_text(
            '---\nname: my-skill\ndescription: "a---b"\n---\n# my-skill\n',
            encoding="utf-8",
        )
        desc = register._read_frontmatter_description(str(d))
        self.assertEqual(desc, "a---b")


if __name__ == "__main__":
    unittest.main()
