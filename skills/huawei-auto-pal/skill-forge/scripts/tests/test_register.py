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


if __name__ == "__main__":
    unittest.main()
