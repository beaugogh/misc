"""Tests for agent_targets.py — agent discovery and slug derivation.

All tests use mocked HOME directories — no real environment access.

Run with: python -m unittest discover -s tests -p "test_agent_targets.py" -v
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

import agent_targets


class TestDeriveProjectSlug(unittest.TestCase):
    """Test the project slug algorithm used by Claude Code / CodeAgent."""

    def test_windows_path(self):
        # Windows drive colon + backslash → double dash, preserved by Claude Code.
        self.assertEqual(
            agent_targets.derive_project_slug("D:\\workspace\\misc"),
            "D--workspace-misc",
        )

    def test_windows_deep_path(self):
        self.assertEqual(
            agent_targets.derive_project_slug("D:\\workspace\\misc\\skills\\foo"),
            "D--workspace-misc-skills-foo",
        )

    def test_unix_path(self):
        self.assertEqual(
            agent_targets.derive_project_slug("/home/user/project"),
            "home-user-project",
        )

    def test_mac_path(self):
        self.assertEqual(
            agent_targets.derive_project_slug("/Users/bob/dev/proj"),
            "Users-bob-dev-proj",
        )

    def test_uses_cwd_if_none(self):
        slug = agent_targets.derive_project_slug()
        self.assertIsInstance(slug, str)
        self.assertTrue(len(slug) > 0)

    def test_double_dashes_preserved(self):
        # Claude Code uses D--workspace-misc, not D-workspace-misc.
        # D:\\workspace\\misc (escaped) = D:\workspace\misc → D--workspace-misc
        # D:\\\\workspace\\\\misc (escaped) = D:\\workspace:\\misc → D---workspace--misc
        self.assertEqual(
            agent_targets.derive_project_slug("D:\\\\workspace\\\\misc"),
            "D---workspace--misc",
        )

    def test_trailing_dashes_stripped(self):
        self.assertEqual(
            agent_targets.derive_project_slug("D:\\workspace\\misc\\"),
            "D--workspace-misc",
        )


class TestDiscoverAgents(unittest.TestCase):
    """Test agent discovery with mocked HOME."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="agent_test_")
        self._patch = patch.object(agent_targets, "HOME", Path(self._tmp))
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _mkdir(self, *parts):
        p = Path(self._tmp, *parts)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def test_no_agents(self):
        agents = agent_targets.discover_agents()
        self.assertEqual(agents, [])

    def test_detects_claude_code(self):
        self._mkdir(".claude", "projects")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("claude_code", ids)
        cc = [a for a in agents if a.agent_id == "claude_code"][0]
        self.assertIsNotNone(cc.skills_dir)
        self.assertTrue(cc.skills_dir.replace("\\", "/").endswith(".claude/skills"))

    def test_detects_codeagent(self):
        self._mkdir(".cac", "projects")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("codeagent", ids)

    def test_detects_opencode(self):
        self._mkdir(".config", "opencode")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("opencode", ids)
        oc = [a for a in agents if a.agent_id == "opencode"][0]
        self.assertEqual(oc.memory_format, "none")

    def test_detects_codex(self):
        self._mkdir(".codex")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("codex", ids)
        codex = [a for a in agents if a.agent_id == "codex"][0]
        self.assertIsNotNone(codex.skills_dir)  # Codex DOES support skills
        self.assertTrue(codex.skills_dir.replace("\\", "/").endswith(".codex/skills"))
        self.assertEqual(codex.memory_format, "agents_md")

    def test_detects_openclaw(self):
        self._mkdir(".openclaw")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("openclaw", ids)
        claw = [a for a in agents if a.agent_id == "openclaw"][0]
        self.assertIsNotNone(claw.skills_dir)

    def test_detects_openclaw_with_workspace(self):
        self._mkdir(".openclaw", "workspace", "skills")
        agents = agent_targets.discover_agents()
        claw = [a for a in agents if a.agent_id == "openclaw"][0]
        self.assertIn("workspace", claw.skills_dir)
        self.assertEqual(claw.memory_format, "user_md")

    def test_detects_openclaw_alt_dir(self):
        self._mkdir(".open-claw")

    def test_detects_openclaw_alt_dir(self):
        self._mkdir(".open-claw")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("openclaw", ids)

    def test_detects_hermes(self):
        self._mkdir(".hermes-agent")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("hermes", ids)

    def test_detects_hermes_alt_dir(self):
        self._mkdir(".hermes")
        agents = agent_targets.discover_agents()
        ids = [a.agent_id for a in agents]
        self.assertIn("hermes", ids)

    def test_detects_multiple_agents(self):
        self._mkdir(".claude", "projects")
        self._mkdir(".cac", "projects")
        self._mkdir(".config", "opencode")
        agents = agent_targets.discover_agents()
        ids = {a.agent_id for a in agents}
        self.assertEqual(ids, {"claude_code", "codeagent", "opencode"})

    def test_claude_memory_dir_when_project_exists(self):
        self._mkdir(".claude", "projects", "D-test-proj", "memory")
        agents = agent_targets.discover_agents(cwd="D:\\test\\proj")
        cc = [a for a in agents if a.agent_id == "claude_code"][0]
        self.assertIsNotNone(cc.memory_dir)
        self.assertEqual(cc.memory_format, "claude_memory")
        self.assertIn("memory", cc.memory_dir)

    def test_claude_memory_none_when_no_projects(self):
        self._mkdir(".claude")  # no projects/ dir
        agents = agent_targets.discover_agents()
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0].memory_format, "none")

    def test_format_agents_report_empty(self):
        report = agent_targets.format_agents_report([])
        self.assertIn("No AI agents", report)

    def test_format_agents_report_with_agents(self):
        self._mkdir(".claude", "projects")
        agents = agent_targets.discover_agents()
        report = agent_targets.format_agents_report(agents)
        self.assertIn("Claude Code", report)
        self.assertIn("skills:", report)


class TestDetectionIsReadOnly(unittest.TestCase):
    """Discovery must not read personal file contents."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="agent_ro_")
        self._patch = patch.object(agent_targets, "HOME", Path(self._tmp))
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_does_not_read_session_files(self):
        """Even with personal session files present, discovery only checks dirs."""
        proj_dir = Path(self._tmp, ".claude", "projects", "D-test", "memory")
        proj_dir.mkdir(parents=True, exist_ok=True)
        # Write a fake personal file.
        (proj_dir / "secret.md").write_text("SENSITIVE_DATA", encoding="utf-8")
        agents = agent_targets.discover_agents(cwd="D:\\test")
        # Discovery should work without reading the file.
        self.assertEqual(len(agents), 1)
        # The secret content must not appear in any agent target field.
        for a in agents:
            for attr in (a.skills_dir, a.memory_dir, a.display_name, a.agent_id):
                self.assertNotIn("SENSITIVE_DATA", str(attr))


if __name__ == "__main__":
    unittest.main()
