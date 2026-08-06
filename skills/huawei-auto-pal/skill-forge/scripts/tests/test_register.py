"""Tests for register.py — the registration helper entry point.

Run with: python -m unittest discover -s tests -p "test_register.py" -v
"""

import unittest
import os
import sys
import json
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


class TestPyYAMLFallback(unittest.TestCase):
    """Test that register.py works without PyYAML installed.

    register.py uses import yaml inside _read_skill_version and
    _read_frontmatter_description. If PyYAML is not installed, the import
    must fail gracefully and fall back to line-scraping.
    """

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="yaml_test_")

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _hide_yaml(self):
        """Return a context manager that makes 'import yaml' raise ImportError."""
        import builtins
        real_import = builtins.__import__
        def mock_import(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError("No module named 'yaml' (simulated)")
            return real_import(name, *args, **kwargs)
        return patch("builtins.__import__", side_effect=mock_import)

    def test_read_skill_version_without_yaml(self):
        """_read_skill_version falls back to line-scrape without PyYAML."""
        skill_md = os.path.join(self._tmp, "SKILL.md")
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write("---\nname: test\nversion: 1.2.3\n---\n# test\n")
        with patch.object(register, "_SKILL_ROOT", self._tmp):
            with self._hide_yaml():
                ver = register._read_skill_version()
        self.assertEqual(ver, "1.2.3")

    def test_read_frontmatter_description_without_yaml(self):
        """_read_frontmatter_description falls back to line-scrape without PyYAML."""
        skill_dir = self._tmp
        skill_md = os.path.join(skill_dir, "SKILL.md")
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write("---\nname: test\ndescription: A simple skill\n---\n# test\n")
        with self._hide_yaml():
            desc = register._read_frontmatter_description(skill_dir)
        self.assertEqual(desc, "A simple skill")


class TestSessionTrace(unittest.TestCase):
    """Test session trace capture for diagnostic archives."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="trace_test_")

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _make_session_jsonl(self, lines):
        """Write a fake session JSONL file and return its path."""
        import json as _json
        path = os.path.join(self._tmp, "fake-session.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for obj in lines:
                f.write(_json.dumps(obj, ensure_ascii=False) + "\n")
        return path

    def _patch_jsonl(self, src_path):
        """Context managers that patch discovery to return (agent, path)."""
        return (
            patch.object(register, "_find_jsonl_session", return_value=("test", src_path)),
            patch.object(register, "_find_legacy_codeagent_session", return_value=None),
        )

    def test_truncates_tool_results(self):
        """Tool results over 500 chars are truncated in the output."""
        long_result = "x" * 5000
        src = self._make_session_jsonl([
            {"type": "user", "message": {"role": "user", "content": "hello"}},
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}
            ]}},
            {"type": "user", "message": {"role": "user", "content": [
                {"type": "tool_result", "content": long_result}
            ]}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        self.assertIsNotNone(dest)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        self.assertEqual(len(lines), 3)
        tr = lines[2]["message"]["content"][0]
        self.assertIn("[...truncated", tr["content"])
        self.assertLess(len(tr["content"]), 600)

    def test_keeps_tool_use_input_full(self):
        """Tool use inputs (commands, file paths) are NOT truncated."""
        long_cmd = "python " + "arg " * 200  # ~1200 chars
        src = self._make_session_jsonl([
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": long_cmd}}
            ]}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        tu = lines[0]["message"]["content"][0]
        self.assertEqual(tu["input"]["command"], long_cmd)

    def test_skips_file_history_snapshots(self):
        """file-history-snapshot entries are skipped entirely."""
        src = self._make_session_jsonl([
            {"type": "file-history-snapshot", "snapshot": {"trackedFileBackups": {}}},
            {"type": "user", "message": {"role": "user", "content": "test"}},
            {"type": "file-history-snapshot", "snapshot": {"trackedFileBackups": {}}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["type"], "user")

    def test_returns_none_when_no_session(self):
        """Returns None when no session trace is found."""
        with patch.object(register, "_find_jsonl_session", return_value=None), \
             patch.object(register, "_find_legacy_codeagent_session", return_value=None):
            result = register._write_session_trace(self._tmp)
        self.assertIsNone(result)

    def test_truncates_nested_tool_result_text(self):
        """Tool results with list content (text blocks) are also truncated."""
        long_text = "y" * 3000
        src = self._make_session_jsonl([
            {"type": "user", "message": {"role": "user", "content": [
                {"type": "tool_result", "content": [
                    {"type": "text", "text": long_text}
                ]}
            ]}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        tr = lines[0]["message"]["content"][0]
        sub = tr["content"][0]
        self.assertIn("[...truncated", sub["text"])
        self.assertLess(len(sub["text"]), 600)

    def test_truncates_assistant_text_blocks(self):
        """Assistant text blocks over 1000 chars are truncated."""
        long_text = "z" * 5000
        src = self._make_session_jsonl([
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "text", "text": long_text}
            ]}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        block = lines[0]["message"]["content"][0]
        self.assertIn("[...truncated", block["text"])
        self.assertLess(len(block["text"]), 1100)

    def test_truncates_thinking_blocks(self):
        """Thinking blocks over 1000 chars are truncated."""
        long_thinking = "w" * 5000
        src = self._make_session_jsonl([
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "thinking", "thinking": long_thinking}
            ]}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        block = lines[0]["message"]["content"][0]
        self.assertIn("[...truncated", block["thinking"])
        self.assertLess(len(block["thinking"]), 1100)

    def test_truncates_base64_image_data(self):
        """Base64 image data in tool_result and toolUseResult is replaced."""
        large_b64 = "A" * 5000
        src = self._make_session_jsonl([
            {"type": "user", "message": {"role": "user", "content": [
                {"type": "tool_result", "content": [
                    {"type": "image", "source": {"type": "base64", "data": large_b64}}
                ]}
            ]}},
            {"type": "user", "toolUseResult": {"file": {"base64": large_b64}}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        img_block = lines[0]["message"]["content"][0]["content"][0]
        self.assertIn("[base64 image data:", img_block["source"]["data"])
        tur = lines[1].get("toolUseResult", {})
        self.assertIn("[base64 image data:", tur["file"]["base64"])

    def test_skips_metadata_types(self):
        """Metadata entry types (mode, attachment, etc.) are skipped."""
        src = self._make_session_jsonl([
            {"type": "mode", "mode": "normal"},
            {"type": "user", "message": {"role": "user", "content": "hello"}},
            {"type": "attachment", "attachment": {"type": "agent_listing_delta"}},
            {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "text", "text": "hi"}
            ]}},
        ])
        p1, p2 = self._patch_jsonl(src)
        with p1, p2:
            dest = register._write_session_trace(self._tmp)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        types = [l.get("type") for l in lines]
        self.assertEqual(types, ["user", "assistant"])

    def test_truncates_legacy_codeagent_parts(self):
        """Legacy codeagent part data (state.output, text) is truncated."""
        long_output = "x" * 3000
        long_text = "y" * 3000
        src = self._make_session_jsonl([
            {"type": "assistant", "data": {"role": "assistant"}, "parts": [
                {"id": "p1", "data": {"type": "text", "text": long_text}},
                {"id": "p2", "data": {"type": "tool", "tool": "Bash",
                  "state": {"status": "completed", "output": long_output,
                            "input": "ls -la"}}},
            ]},
        ])
        # Patch to use legacy codeagent path (no JSONL, use legacy result)
        with patch.object(register, "_find_jsonl_session", return_value=None), \
             patch.object(register, "_find_legacy_codeagent_session",
                          return_value=("/fake/db.db", "ses_test")), \
             patch.object(register, "_export_legacy_codeagent_session",
                          return_value=[json.dumps({"type": "assistant",
                              "data": {"role": "assistant"},
                              "parts": [
                                  {"id": "p1", "data": {"type": "text", "text": long_text}},
                                  {"id": "p2", "data": {"type": "tool", "tool": "Bash",
                                    "state": {"status": "completed", "output": long_output,
                                              "input": "ls -la"}}},
                              ]})]):
            dest = register._write_session_trace(self._tmp)
        self.assertIsNotNone(dest)
        import json as _json
        with open(dest, encoding="utf-8") as f:
            lines = [_json.loads(l) for l in f if l.strip()]
        self.assertEqual(len(lines), 1)
        # Text part should be truncated
        text_part = lines[0]["parts"][0]["data"]
        self.assertIn("[...truncated", text_part["text"])
        # Tool state.output should be truncated
        tool_part = lines[0]["parts"][1]["data"]
        self.assertIn("[...truncated", tool_part["state"]["output"])
        # Tool state.input should be kept full (short)
        self.assertEqual(tool_part["state"]["input"], "ls -la")


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


class TestUserId(unittest.TestCase):
    """Test _user_id returns a non-empty identifier."""

    def test_returns_non_empty(self):
        uid = register._user_id()
        self.assertIsNotNone(uid)
        self.assertTrue(len(uid) > 0)

    def test_archive_zip_name_contains_user_id(self):
        """Archive filename should include the user ID."""
        uid = register._user_id()
        self.assertIsNotNone(uid)
        # Simulate the filename construction from cmd_archive.
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        user_part = f"{uid}-" if uid else ""
        zip_name = f"huawei-auto-pal-output-{user_part}{timestamp}.zip"
        self.assertIn(uid, zip_name)


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

    def test_skips_en_zh_markers(self):
        """With the new [EN]/[ZH] format, the marker must not be returned as the summary."""
        d = Path(self._tmp, "marker-skill")
        d.mkdir()
        (d / "SKILL.md").write_text("---\nname: marker\n---\n# marker\n", encoding="utf-8")
        (d / "PROPOSAL.md").write_text(
            "# Proposal: marker\n\n## Problem\n\n[EN]\nThe real problem text.\n\n[ZH]\n真正的问题。\n",
            encoding="utf-8",
        )
        summary, has_proposal = register._proposal_summary("marker-skill")
        self.assertTrue(has_proposal)
        self.assertNotIn("[EN]", summary)
        self.assertNotIn("[ZH]", summary)
        self.assertIn("real problem", summary)

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

    def test_present_and_install_rejected(self):
        code, out, err = self._run_main("--present", "--install", "y")
        self.assertNotEqual(code, 0)
        self.assertIn("mutually exclusive", err)


class TestCmdPresent(unittest.TestCase):
    """Test the --present command prints all proposals."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="present_")
        self._patch_output = patch.object(register, "_OUTPUT_DIR", self._tmp)
        self._patch_output.start()
        self._patch_agents = patch.object(register, "discover_agents", return_value=[])
        self._patch_agents.start()

    def tearDown(self):
        self._patch_output.stop()
        self._patch_agents.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _make_skill(self, name, with_proposal=True, problem_line="Something broke."):
        d = Path(self._tmp, name)
        d.mkdir()
        (d / "SKILL.md").write_text(
            "---\nname: %s\ndescription: A fallback.\n---\n# %s\n" % (name, name),
            encoding="utf-8",
        )
        if with_proposal:
            (d / "PROPOSAL.md").write_text(
                "# Proposal: %s\n\n## Problem\n\n%s\n" % (name, problem_line),
                encoding="utf-8",
            )

    def _run_present(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        args = type("A", (), {"present": True})()
        with redirect_stdout(buf):
            register.cmd_present(args, [], register._find_output_skills(self._tmp))
        return buf.getvalue()

    def test_prints_all_proposals(self):
        self._make_skill("skill-a", problem_line="Problem A.")
        self._make_skill("skill-b", problem_line="Problem B.")
        out = self._run_present()
        self.assertIn("Problem A.", out)
        self.assertIn("Problem B.", out)
        self.assertIn("skill-a", out)
        self.assertIn("skill-b", out)

    def test_includes_bilingual_header(self):
        self._make_skill("my-skill")
        out = self._run_present()
        self.assertIn("中文", out)

    def test_shows_install_instructions(self):
        self._make_skill("my-skill")
        out = self._run_present()
        self.assertIn("--install", out)

    def test_no_skills_message(self):
        out = self._run_present()
        self.assertIn("Nothing to present", out)

    def test_includes_fallback_for_missing_proposal(self):
        self._make_skill("legacy", with_proposal=False)
        out = self._run_present()
        self.assertIn("fallback", out.lower())


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
