"""Tests for skill_installer.py — skill copy and memory insertion.

All tests use temp directories — no real agent directories are touched.

Run with: python -m unittest discover -s tests -p "test_skill_installer.py" -v
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from agent_targets import AgentTarget
from skill_installer import (
    install_skill,
    install_memory,
    _parse_personal_context,
    InstallResult,
)


class TestInstallSkill(unittest.TestCase):
    """Test skill folder installation."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="install_test_")
        # A fake source skill.
        self.source = Path(self._tmp, "source", "test-skill")
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: A test skill\n---\n# test-skill\n",
            encoding="utf-8",
        )
        # A fake agent skills dir.
        self.skills_dir = Path(self._tmp, "agent", "skills")
        self.skills_dir.mkdir(parents=True)
        self.agent = AgentTarget(
            agent_id="claude_code",
            display_name="Claude Code",
            skills_dir=str(self.skills_dir),
            memory_dir=None,
            memory_format="none",
            detect_path="",
        )

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_successful_copy(self):
        result = install_skill(str(self.source), self.agent)
        self.assertTrue(result.success)
        self.assertEqual(result.action, "copied")
        self.assertTrue((self.skills_dir / "test-skill" / "SKILL.md").is_file())

    def test_dry_run_does_not_write(self):
        result = install_skill(str(self.source), self.agent, dry_run=True)
        self.assertTrue(result.success)
        self.assertEqual(result.action, "dry_run")
        self.assertFalse((self.skills_dir / "test-skill").exists())

    def test_conflict_when_skill_exists(self):
        # Pre-install the skill.
        shutil.copytree(self.source, self.skills_dir / "test-skill")
        result = install_skill(str(self.source), self.agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "conflict")

    def test_source_missing_skill_md(self):
        bad = Path(self._tmp, "bad-skill")
        bad.mkdir()
        result = install_skill(str(bad), self.agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "error")

    def test_source_dir_does_not_exist(self):
        result = install_skill("/nonexistent/path/skill", self.agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "error")

    def test_unsupported_agent(self):
        no_skills_agent = AgentTarget(
            agent_id="codex",
            display_name="Codex",
            skills_dir=None,
            memory_dir=None,
            memory_format="none",
            detect_path="",
        )
        result = install_skill(str(self.source), no_skills_agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "unsupported")

    def test_copy_includes_subdirs(self):
        # Add scripts/ and references/ to the source skill.
        (self.source / "scripts").mkdir()
        (self.source / "scripts" / "helper.py").write_text("# helper", encoding="utf-8")
        (self.source / "references").mkdir()
        (self.source / "references" / "guide.md").write_text("# guide", encoding="utf-8")

        result = install_skill(str(self.source), self.agent)
        self.assertTrue(result.success)
        self.assertTrue((self.skills_dir / "test-skill" / "scripts" / "helper.py").is_file())
        self.assertTrue((self.skills_dir / "test-skill" / "references" / "guide.md").is_file())

    def test_copy_creates_skills_dir_if_missing(self):
        # Remove the skills dir — installer should create it.
        shutil.rmtree(self.skills_dir)
        result = install_skill(str(self.source), self.agent)
        self.assertTrue(result.success)
        self.assertTrue((self.skills_dir / "test-skill" / "SKILL.md").is_file())

    def test_rejects_path_traversal_name(self):
        """A source dir named '..' must be rejected, not copied into the parent."""
        bad_source = Path(self._tmp, "..")
        # Create a SKILL.md in the parent to make it look like a skill.
        (bad_source / "SKILL.md").write_text("---\nname: bad\n---\n# bad\n", encoding="utf-8")
        result = install_skill(str(bad_source), self.agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "error")

    def test_rejects_invalid_skill_name(self):
        """A source dir with invalid characters must be rejected."""
        bad_source = Path(self._tmp, "bad name with spaces")
        bad_source.mkdir()
        (bad_source / "SKILL.md").write_text("---\nname: bad\n---\n# bad\n", encoding="utf-8")
        result = install_skill(str(bad_source), self.agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "error")


class TestParsePersonalContext(unittest.TestCase):
    """Test parsing of personal-context/SKILL.md into memory facts."""

    def test_parses_multiple_sections(self):
        content = """# Personal Context

## Proxy preference
User prefers NO_PROXY for intranet hosts.

## Environment
Windows 11 with Git Bash.
"""
        facts = _parse_personal_context(content)
        self.assertEqual(len(facts), 2)
        self.assertEqual(facts[0]["title"], "Proxy preference")
        self.assertEqual(facts[1]["title"], "Environment")

    def test_derives_slug_from_title(self):
        content = "# Personal Context\n\n## Proxy Preference\nUses NO_PROXY.\n"
        facts = _parse_personal_context(content)
        self.assertEqual(facts[0]["name"], "proxy-preference")

    def test_no_sections_returns_empty(self):
        content = "# Personal Context\nJust a title, no sections.\n"
        facts = _parse_personal_context(content)
        self.assertEqual(len(facts), 0)

    def test_description_is_first_sentence(self):
        content = "# PC\n\n## My Fact\nThis is a fact. It has two sentences.\n"
        facts = _parse_personal_context(content)
        self.assertIn("This is a fact", facts[0]["description"])

    def test_non_ascii_title_produces_slug(self):
        """Non-ASCII titles (Chinese, Japanese) must produce a meaningful slug, not 'unnamed-fact'."""
        content = "# PC\n\n## 代理设置\n使用 NO_PROXY。\n"
        facts = _parse_personal_context(content)
        self.assertEqual(len(facts), 1)
        self.assertNotEqual(facts[0]["name"], "unnamed-fact")
        self.assertTrue(len(facts[0]["name"]) > 0)

    def test_code_fence_heading_not_split(self):
        """## inside a code fence must not be treated as a new section."""
        content = (
            "# PC\n\n"
            "## Real fact\nSome text.\n\n"
            "```\n## Not a fact\nThis is code.\n```\n\n"
            "## Another fact\nMore text.\n"
        )
        facts = _parse_personal_context(content)
        self.assertEqual(len(facts), 2)
        self.assertEqual(facts[0]["title"], "Real fact")
        self.assertEqual(facts[1]["title"], "Another fact")


class TestInstallMemoryClaude(unittest.TestCase):
    """Test memory installation for Claude-style agents (MEMORY.md + per-fact .md)."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="mem_test_")
        self.memory_dir = Path(self._tmp, "memory")
        self.memory_dir.mkdir(parents=True)

        self.pc_path = Path(self._tmp, "personal-context", "SKILL.md")
        self.pc_path.parent.mkdir(parents=True)
        self.pc_path.write_text(
            "# Personal Context\n\n"
            "## Proxy preference\nUser prefers NO_PROXY for intranet hosts.\n\n"
            "## Environment\nWindows 11 with Git Bash.\n",
            encoding="utf-8",
        )
        self.agent = AgentTarget(
            agent_id="claude_code",
            display_name="Claude Code",
            skills_dir=None,
            memory_dir=str(self.memory_dir),
            memory_format="claude_memory",
            detect_path="",
        )

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_creates_memory_files(self):
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        self.assertTrue((self.memory_dir / "proxy-preference.md").is_file())
        self.assertTrue((self.memory_dir / "environment.md").is_file())
        self.assertTrue((self.memory_dir / "MEMORY.md").is_file())

    def test_memory_file_has_frontmatter(self):
        install_memory(str(self.pc_path), self.agent)
        content = (self.memory_dir / "proxy-preference.md").read_text(encoding="utf-8")
        self.assertIn("---", content)
        self.assertIn("name: proxy-preference", content)
        self.assertIn("node_type: memory", content)
        self.assertIn("type: project", content)

    def test_memory_index_has_entries(self):
        install_memory(str(self.pc_path), self.agent)
        index = (self.memory_dir / "MEMORY.md").read_text(encoding="utf-8")
        self.assertIn("proxy-preference.md", index)
        self.assertIn("environment.md", index)

    def test_dry_run_does_not_write(self):
        result = install_memory(str(self.pc_path), self.agent, dry_run=True)
        self.assertTrue(result.success)
        self.assertEqual(result.action, "dry_run")
        self.assertFalse((self.memory_dir / "proxy-preference.md").exists())

    def test_updates_existing_fact(self):
        # Pre-create a fact file.
        (self.memory_dir / "proxy-preference.md").write_text("OLD CONTENT", encoding="utf-8")
        (self.memory_dir / "MEMORY.md").write_text(
            "# Memory Index\n\n- [Proxy preference](proxy-preference.md) — old desc\n",
            encoding="utf-8",
        )
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        new_content = (self.memory_dir / "proxy-preference.md").read_text(encoding="utf-8")
        self.assertNotIn("OLD CONTENT", new_content)
        self.assertIn("NO_PROXY", new_content)

    def test_does_not_duplicate_index_entries(self):
        # Pre-create MEMORY.md with an entry.
        (self.memory_dir / "MEMORY.md").write_text(
            "# Memory Index\n\n- [Proxy preference](proxy-preference.md) — old\n",
            encoding="utf-8",
        )
        install_memory(str(self.pc_path), self.agent)
        index = (self.memory_dir / "MEMORY.md").read_text(encoding="utf-8")
        # Should appear exactly once.
        self.assertEqual(index.count("proxy-preference.md"), 1)

    def test_unsupported_agent(self):
        no_mem_agent = AgentTarget(
            agent_id="opencode",
            display_name="OpenCode",
            skills_dir=None,
            memory_dir=None,
            memory_format="none",
            detect_path="",
        )
        result = install_memory(str(self.pc_path), no_mem_agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "unsupported")

    def test_missing_personal_context(self):
        result = install_memory("/nonexistent/path/SKILL.md", self.agent)
        self.assertFalse(result.success)
        self.assertEqual(result.action, "error")


class TestInstallMemoryInstructions(unittest.TestCase):
    """Test memory installation for Codex-style agents (instructions.md)."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="codex_mem_")
        self.inst_path = Path(self._tmp, "instructions.md")

        self.pc_path = Path(self._tmp, "personal-context", "SKILL.md")
        self.pc_path.parent.mkdir(parents=True)
        self.pc_path.write_text(
            "# Personal Context\n\n"
            "## Proxy preference\nUser prefers NO_PROXY.\n",
            encoding="utf-8",
        )
        self.agent = AgentTarget(
            agent_id="codex",
            display_name="Codex",
            skills_dir=None,
            memory_dir=str(self.inst_path),
            memory_format="instructions_md",
            detect_path="",
        )

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_creates_instructions_file(self):
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        content = self.inst_path.read_text(encoding="utf-8")
        self.assertIn("Personal Context", content)
        self.assertIn("Proxy preference", content)
        self.assertIn("NO_PROXY", content)

    def test_appends_to_existing_instructions(self):
        self.inst_path.write_text("# Instructions\n\n## Coding style\nUse 4 spaces.\n", encoding="utf-8")
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        content = self.inst_path.read_text(encoding="utf-8")
        self.assertIn("Coding style", content)
        self.assertIn("Personal Context", content)

    def test_replaces_existing_personal_context_section(self):
        self.inst_path.write_text(
            "# Instructions\n\n## Personal Context\n\n### Old fact\nOld content.\n\n## Other\nOther.\n",
            encoding="utf-8",
        )
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        content = self.inst_path.read_text(encoding="utf-8")
        self.assertNotIn("Old content", content)
        self.assertIn("NO_PROXY", content)
        self.assertIn("Other", content)

    def test_dry_run_does_not_write(self):
        result = install_memory(str(self.pc_path), self.agent, dry_run=True)
        self.assertTrue(result.success)
        self.assertFalse(self.inst_path.exists())


class TestInstallMemoryAgentsMd(unittest.TestCase):
    """Test memory installation for Codex (AGENTS.md in project root)."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="agents_md_")
        self._old_cwd = os.getcwd()
        os.chdir(self._tmp)

        self.pc_path = Path(self._tmp, "personal-context", "SKILL.md")
        self.pc_path.parent.mkdir(parents=True)
        self.pc_path.write_text(
            "# Personal Context\n\n"
            "## Proxy preference\nUser prefers NO_PROXY.\n",
            encoding="utf-8",
        )
        self.agent = AgentTarget(
            agent_id="codex",
            display_name="Codex",
            skills_dir=None,
            memory_dir=None,
            memory_format="agents_md",
            detect_path="",
        )

    def tearDown(self):
        os.chdir(self._old_cwd)
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_creates_agents_md(self):
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        agents_md = Path(self._tmp, "AGENTS.md")
        self.assertTrue(agents_md.is_file())
        content = agents_md.read_text(encoding="utf-8")
        self.assertIn("Personal Context", content)
        self.assertIn("Proxy preference", content)

    def test_appends_to_existing_agents_md(self):
        agents_md = Path(self._tmp, "AGENTS.md")
        agents_md.write_text("# Agents\n\n## Coding style\nUse 4 spaces.\n", encoding="utf-8")
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        content = agents_md.read_text(encoding="utf-8")
        self.assertIn("Coding style", content)
        self.assertIn("Personal Context", content)

    def test_dry_run_does_not_write(self):
        result = install_memory(str(self.pc_path), self.agent, dry_run=True)
        self.assertTrue(result.success)
        self.assertFalse(Path(self._tmp, "AGENTS.md").exists())


class TestInstallMemoryUserMd(unittest.TestCase):
    """Test memory installation for OpenClaw (USER.md in workspace)."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="user_md_")
        self.workspace = Path(self._tmp, "workspace")
        self.workspace.mkdir()

        self.pc_path = Path(self._tmp, "personal-context", "SKILL.md")
        self.pc_path.parent.mkdir(parents=True)
        self.pc_path.write_text(
            "# Personal Context\n\n"
            "## Proxy preference\nUser prefers NO_PROXY.\n",
            encoding="utf-8",
        )
        self.agent = AgentTarget(
            agent_id="openclaw",
            display_name="OpenClaw",
            skills_dir=None,
            memory_dir=str(self.workspace),
            memory_format="user_md",
            detect_path="",
        )

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_creates_user_md(self):
        result = install_memory(str(self.pc_path), self.agent)
        self.assertTrue(result.success)
        user_md = self.workspace / "USER.md"
        self.assertTrue(user_md.is_file())
        content = user_md.read_text(encoding="utf-8")
        self.assertIn("Proxy preference", content)
        self.assertIn("NO_PROXY", content)

    def test_dry_run_does_not_write(self):
        result = install_memory(str(self.pc_path), self.agent, dry_run=True)
        self.assertTrue(result.success)
        self.assertFalse((self.workspace / "USER.md").exists())


if __name__ == "__main__":
    unittest.main()
