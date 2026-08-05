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


if __name__ == "__main__":
    unittest.main()
