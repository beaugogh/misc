"""Tests for the content-driven root-cause summarizer (summarize.py).

Verifies that narratives are grounded in actual event content (user prompts,
assistant diagnostics, error texts, browser titles, meeting subjects) rather
than generic pattern-bucket labels.

Run with: python -m unittest discover -s scripts/tests
"""

import unittest
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from summarize import (
    summarize_root_cause,
    _clean_user_goal,
    _extract_diagnostic_sentences,
    _pair_errors_with_commands,
    _describe_tool_call,
    _clean_retry_target,
    _summarize_ai_session,
    _summarize_browser,
    _summarize_meeting,
    _summarize_comm,
    _summarize_vcs,
    _summarize_filesystem,
)


def _ev(kind, text=None, tool_name=None, tool_input=None, tool_is_error=None,
        tool_use_id=None, source_kind="ai_session", timestamp=1000000.0,
        extra=None):
    """Build a minimal normalized event for testing."""
    ev = {
        "source": "test",
        "source_kind": source_kind,
        "session_id": "s1",
        "cwd": "/proj",
        "git_branch": "main",
        "timestamp": timestamp,
        "kind": kind,
        "text": text,
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_is_error": tool_is_error,
        "tool_use_id": tool_use_id,
    }
    if extra:
        ev["extra"] = extra
    return ev


def _task(source_kind="ai_session", active=3600, wall=3600, excised=0,
          errors=0, context=None, subject="test", **kw):
    """Build a minimal task dict for testing."""
    t = {
        "id": "test-1",
        "source_kind": source_kind,
        "active_seconds": active,
        "wall_clock_seconds": wall,
        "excised_gap_seconds": excised,
        "errors": errors,
        "tool_calls": 10,
        "subject": subject,
        "context": context or {},
    }
    t.update(kw)
    return t


class TestCleanUserGoal(unittest.TestCase):
    def test_plain_goal(self):
        self.assertEqual(_clean_user_goal("fix the login bug"), "fix the login bug")

    def test_strips_command_wrapper(self):
        text = '<command-name>/goal</command-name>\n<command-args>pull and synch with remote</command-args>'
        result = _clean_user_goal(text)
        self.assertIn("pull and synch", result)

    def test_strips_system_reminder(self):
        text = '<system-reminder>some metadata</system-reminder>\nactual goal here'
        # The system-reminder line is stripped, leaving "actual goal here"
        result = _clean_user_goal(text)
        self.assertIn("actual goal", result)

    def test_first_sentence_only(self):
        text = "Do the first thing. Then do another thing."
        result = _clean_user_goal(text)
        self.assertEqual(result, "Do the first thing")

    def test_empty(self):
        self.assertEqual(_clean_user_goal(None), "")
        self.assertEqual(_clean_user_goal(""), "")


class TestExtractDiagnostics(unittest.TestCase):
    def test_finds_struggle_sentences(self):
        texts = ["The fetch failed with a 407 proxy auth error. Let me check the proxy config."]
        diags = _extract_diagnostic_sentences(texts)
        self.assertTrue(len(diags) >= 1)
        self.assertIn("407", diags[0])

    def test_ignores_non_diagnostic(self):
        texts = ["Here is the summary of what was done. The file was created successfully."]
        diags = _extract_diagnostic_sentences(texts)
        # "failed" / "error" etc. not present → no diagnostics
        self.assertEqual(len(diags), 0)

    def test_dedupes(self):
        texts = ["The fetch failed. The fetch failed. The fetch failed."]
        diags = _extract_diagnostic_sentences(texts)
        self.assertEqual(len(diags), 1)

    def test_caps_at_three(self):
        texts = [f"Error {i}: something failed with code {i}." for i in range(10)]
        diags = _extract_diagnostic_sentences(texts)
        self.assertLessEqual(len(diags), 3)


class TestPairErrorsWithCommands(unittest.TestCase):
    def test_pairs_error_to_command(self):
        events = [
            _ev("tool_use", tool_name="Bash", tool_input={"command": "git fetch origin"},
                tool_use_id="tu_1"),
            _ev("tool_result", text="Exit code 128\nfatal: unable to access",
                tool_is_error=True, tool_use_id="tu_1"),
        ]
        pairs = _pair_errors_with_commands(events)
        self.assertEqual(len(pairs), 1)
        cmd, err = pairs[0]
        self.assertIn("git fetch", cmd)
        self.assertIn("unable to access", err)
        # Exit code prefix should be stripped.
        self.assertFalse(err.startswith("Exit code"))

    def test_strips_tool_use_error_tags(self):
        events = [
            _ev("tool_use", tool_name="Edit", tool_input={"file_path": "/p/README.md"},
                tool_use_id="tu_2"),
            _ev("tool_result", text="<tool_use_error>File has not been read yet.</tool_use_error>",
                tool_is_error=True, tool_use_id="tu_2"),
        ]
        pairs = _pair_errors_with_commands(events)
        self.assertEqual(len(pairs), 1)
        _, err = pairs[0]
        self.assertNotIn("<tool_use_error>", err)
        self.assertIn("File has not been read", err)

    def test_no_errors_returns_empty(self):
        events = [
            _ev("tool_use", tool_name="Bash", tool_input={"command": "echo hello"},
                tool_use_id="tu_3"),
            _ev("tool_result", text="hello", tool_is_error=False, tool_use_id="tu_3"),
        ]
        pairs = _pair_errors_with_commands(events)
        self.assertEqual(len(pairs), 0)


class TestDescribeToolCall(unittest.TestCase):
    def test_bash_strips_timeout_prefix(self):
        desc = _describe_tool_call("Bash", {"command": "timeout 30 git fetch origin"})
        self.assertEqual(desc, "git fetch origin")

    def test_bash_takes_first_command_before_pipe(self):
        desc = _describe_tool_call("Bash", {"command": "git fetch origin && git status"})
        self.assertEqual(desc, "git fetch origin")

    def test_bash_collapses_multiline(self):
        desc = _describe_tool_call("Bash", {"command": "npm install foo \\\n  --registry=bar"})
        self.assertNotIn("\\", desc)
        self.assertNotIn("\n", desc)

    def test_edit_uses_basename(self):
        desc = _describe_tool_call("Edit", {"file_path": "/path/to/SKILL.md"})
        self.assertEqual(desc, "edit SKILL.md")


class TestCleanRetryTarget(unittest.TestCase):
    def test_parses_tool_on_target_count(self):
        result = _clean_retry_target("Edit on SKILL.md (44×)")
        self.assertEqual(result, "Edit SKILL.md (44×)")

    def test_cleans_bash_command(self):
        result = _clean_retry_target('Bash on proxyuk.huawei.com:8080" && export HTTP_PROXY="http (8×)')
        self.assertIn("Bash", result)
        self.assertIn("(8×)", result)
        # The messy "&& export" part should be stripped.
        self.assertNotIn("&&", result)

    def test_empty(self):
        self.assertEqual(_clean_retry_target(""), "")


class TestSummarizeAISession(unittest.TestCase):
    def test_produces_goal_and_failure(self):
        events = [
            _ev("user_message", text="sync local main branch with remote"),
            _ev("assistant_message", text="The fetch failed with a 407 proxy auth error."),
            _ev("tool_use", tool_name="Bash", tool_input={"command": "git fetch origin"},
                tool_use_id="tu_1"),
            _ev("tool_result", text="Exit code 128\nfatal: unable to access 'url': CONNECT tunnel failed, response 407",
                tool_is_error=True, tool_use_id="tu_1"),
        ]
        task = _task(active=10 * 3600, wall=20 * 3600, excised=34 * 3600, errors=1)
        narrative = _summarize_ai_session(events, task)
        self.assertIn("Goal:", narrative)
        self.assertIn("sync local", narrative)
        self.assertIn("407", narrative)
        self.assertIn("git fetch", narrative)

    def test_continuation_goal_skipped(self):
        events = [
            _ev("user_message", text="yes, continue"),
            _ev("assistant_message", text="Working on it."),
        ]
        task = _task(active=3600)
        narrative = _summarize_ai_session(events, task)
        # Should not start with "Goal: yes, continue"
        self.assertNotIn("Goal: yes", narrative)

    def test_error_pair_takes_precedence_over_blocker(self):
        """When error-command pairs are available, they're more informative than the blocker."""
        events = [
            _ev("user_message", text="do something"),
            _ev("tool_use", tool_name="Bash", tool_input={"command": "bad cmd"}, tool_use_id="tu_1"),
            _ev("tool_result", text="Exit code 1\nsome error", tool_is_error=True, tool_use_id="tu_1"),
        ]
        task = _task(active=3600, errors=1,
                     context={"blocker": "command failed (exit 1) (1 of 1 errors)"})
        narrative = _summarize_ai_session(events, task)
        # The error pair (Failed: 'bad cmd' → some error) should take precedence
        # over the generic blocker label — it's grounded in the actual command.
        self.assertIn("bad cmd", narrative)
        self.assertIn("some error", narrative)

    def test_blocker_fallback_when_no_error_pairs(self):
        """When no error-command pairs can be built, fall back to the blocker label."""
        events = [
            _ev("user_message", text="do something"),
            # Error with no matching tool_use_id → no pair can be built.
            _ev("tool_result", text="Exit code 1\nsome error", tool_is_error=True, tool_use_id=None),
        ]
        task = _task(active=3600, errors=1,
                     context={"blocker": "command failed (exit 1) (1 of 1 errors)"})
        narrative = _summarize_ai_session(events, task)
        self.assertIn("command failed", narrative)

    def test_idle_time_explained(self):
        events = [
            _ev("user_message", text="do the thing"),
            _ev("assistant_message", text="Done."),
        ]
        task = _task(active=2 * 3600, wall=10 * 3600, excised=8 * 3600)
        narrative = _summarize_ai_session(events, task)
        self.assertIn("idle/overnight", narrative)

    def test_empty_events_returns_empty(self):
        task = _task()
        narrative = _summarize_ai_session([], task)
        # May have a time line, but no goal/failure
        self.assertNotIn("Goal:", narrative)


class TestSummarizeBrowser(unittest.TestCase):
    def test_lists_visited_pages(self):
        task = _task(source_kind="browser", active=3 * 3600, wall=3 * 3600,
                     context={"top_titles": ["mem0 - Google Search", "mem0ai/mem0"],
                              "top_urls": [], "queries": [], "downloads": 2, "n_visits": 185})
        narrative = _summarize_browser([], task)
        self.assertIn("Visited:", narrative)
        self.assertIn("mem0", narrative)
        self.assertIn("Downloaded 2", narrative)

    def test_idle_tabs_explained(self):
        task = _task(source_kind="browser", active=0.5 * 3600, wall=29 * 3600,
                     excised=25 * 3600,
                     context={"top_titles": ["AI进展.xlsx"], "top_urls": [],
                              "queries": [], "downloads": 0, "n_visits": 50})
        narrative = _summarize_browser([], task)
        self.assertIn("idle/overnight", narrative)

    def test_search_query_shown(self):
        task = _task(source_kind="browser", active=3600, wall=3600,
                     context={"top_titles": [], "top_urls": [], "queries": ["python asyncio tutorial"],
                              "downloads": 0, "n_visits": 5})
        narrative = _summarize_browser([], task)
        self.assertIn("Searched for", narrative)
        self.assertIn("asyncio", narrative)


class TestSummarizeMeeting(unittest.TestCase):
    def test_all_day_marker(self):
        task = _task(source_kind="meeting", active=0, wall=24 * 3600,
                     context={"is_all_day": True, "subject": "月末周六工作日"})
        narrative = _summarize_meeting([], task)
        self.assertIn("all-day calendar marker", narrative)
        self.assertIn("0h real", narrative)

    def test_multi_day_capped(self):
        task = _task(source_kind="meeting", active=8 * 3600, wall=24 * 3600,
                     excised=40 * 3600,
                     context={"subject": "集中研讨", "organizer": "Cherry",
                              "location": "杭州：Z5-2-A30R"})
        narrative = _summarize_meeting([], task)
        self.assertIn("Multi-day", narrative)
        self.assertIn("capped", narrative)
        self.assertIn("Cherry", narrative)
        self.assertIn("杭州", narrative)

    def test_normal_meeting(self):
        task = _task(source_kind="meeting", active=3.8 * 3600, wall=3.8 * 3600,
                     context={"subject": "H1自评述职"})
        narrative = _summarize_meeting([], task)
        self.assertIn("H1自评述职", narrative)
        self.assertIn("3.8h", narrative)

    def test_long_single_day_meeting_not_multi_day(self):
        """A 9h single-day workshop must NOT be labeled 'Multi-day'."""
        task = _task(source_kind="meeting", active=9 * 3600, wall=9 * 3600,
                     excised=0,
                     context={"subject": "Full-day workshop", "organizer": "Alice"})
        narrative = _summarize_meeting([], task)
        self.assertNotIn("Multi-day", narrative)
        self.assertNotIn("capped", narrative)
        self.assertIn("9.0h meeting", narrative)

    def test_12h_single_day_meeting_not_multi_day(self):
        """A 12h single-day meeting (hackathon) must NOT be labeled 'Multi-day'."""
        task = _task(source_kind="meeting", active=12 * 3600, wall=12 * 3600,
                     excised=0,
                     context={"subject": "Hackathon"})
        narrative = _summarize_meeting([], task)
        self.assertNotIn("Multi-day", narrative)


class TestSummarizeComm(unittest.TestCase):
    def test_email_with_reply(self):
        task = _task(source_kind="comm", active=0,
                     context={"subjects": ["RE: patent draft"], "senders": ["Bogao"],
                              "has_reply": True})
        narrative = _summarize_comm([], task)
        self.assertIn("patent draft", narrative)
        self.assertIn("Bogao", narrative)
        self.assertIn("Reply sent", narrative)

    def test_email_no_reply(self):
        task = _task(source_kind="comm", active=0,
                     context={"subjects": ["FW: notice"], "senders": ["Alice"],
                              "has_reply": False})
        narrative = _summarize_comm([], task)
        self.assertIn("No reply", narrative)


class TestSummarizeVCS(unittest.TestCase):
    def test_commit_subject_shown(self):
        task = _task(source_kind="vcs", active=1.6 * 3600,
                     context={"commit_subjects": ["mcp-tools: add huawei-github"]})
        narrative = _summarize_vcs([], task)
        self.assertIn("mcp-tools", narrative)
        self.assertIn("1.6h", narrative)


class TestSummarizeFilesystem(unittest.TestCase):
    def test_files_listed(self):
        task = _task(source_kind="filesystem", active=1.4 * 3600,
                     context={"files": ["/p/CodeAgent.exe", "/p/README.md"]})
        narrative = _summarize_filesystem([], task)
        self.assertIn("CodeAgent.exe", narrative)
        self.assertIn("1.4h", narrative)


class TestSummarizeRootCause(unittest.TestCase):
    def test_dispatches_by_source_kind(self):
        # ai_session
        events = [_ev("user_message", text="fix the bug")]
        task = _task(source_kind="ai_session", active=3600)
        narrative = summarize_root_cause(task, events)
        self.assertIn("fix the bug", narrative)

    def test_unknown_source_kind_returns_empty(self):
        task = _task(source_kind="unknown_kind")
        narrative = summarize_root_cause(task, [])
        self.assertEqual(narrative, "")

    def test_caps_length(self):
        # Very long goal + diagnostics.
        events = [
            _ev("user_message", text="A" * 500),
            _ev("assistant_message", text="Error: " + "B" * 500),
        ]
        task = _task(active=3600)
        narrative = summarize_root_cause(task, events)
        self.assertLessEqual(len(narrative), 600)


if __name__ == "__main__":
    unittest.main()
