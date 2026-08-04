"""Tests for agent-edit tagging (rubric 68).

Files edited by an AI agent (Edit/Write/NotebookEdit tool calls in ai_session
events) must NOT be attributed to the human in filesystem file_edit events.
"""
import unittest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from cross_source import tag_agent_file_edits
from human_involvement import is_human_action


def _ai_edit(ts, file_path):
    """Build an ai_session Edit tool_use event."""
    return {
        "source_kind": "ai_session", "kind": "tool_use", "tool_name": "Edit",
        "timestamp": ts, "tool_input": {"file_path": file_path},
        "source": "claude_code", "session_id": "s1", "cwd": "/p",
        "git_branch": None, "timestamp_raw": None, "role": "assistant",
        "usage": None, "stop_reason": None, "text": None, "tool_use_id": "tu1",
        "tool_is_error": False,
    }


def _fs_edit(ts, filename, resource=""):
    """Build a filesystem file_edit event (VSCode History style)."""
    return {
        "source_kind": "filesystem", "kind": "file_edit", "timestamp": ts,
        "text": filename,
        "tool_input": {"resource": resource or f"file:///C:/proj/{filename}",
                       "entry_id": "e1", "source": ""},
        "source": "vscode_history", "session_id": None, "cwd": "/p",
        "git_branch": None, "timestamp_raw": str(int(ts * 1000)),
        "role": None, "usage": None, "stop_reason": None,
        "tool_name": None, "tool_use_id": None, "tool_is_error": None,
    }


class TestTagAgentFileEdits(unittest.TestCase):
    def test_tags_matching_file_edit(self):
        """A filesystem edit within the time window of an AI Edit tool call → tagged."""
        events = [
            _ai_edit(1000.0, "C:\\proj\\fix-ccr-code.ps1"),
            _fs_edit(1005.0, "fix-ccr-code.ps1", "file:///C:/proj/fix-ccr-code.ps1"),
        ]
        events = tag_agent_file_edits(events)
        self.assertTrue(events[1].get("agent_edited"),
                        "filesystem edit matching an AI edit must be tagged agent_edited")

    def test_does_not_tag_unrelated_file(self):
        """A filesystem edit for a file NOT edited by the agent → not tagged."""
        events = [
            _ai_edit(1000.0, "C:\\proj\\script.py"),
            _fs_edit(1005.0, "notes.md", "file:///C:/proj/notes.md"),
        ]
        events = tag_agent_file_edits(events)
        self.assertFalse(events[1].get("agent_edited", False))

    def test_does_not_tag_outside_window(self):
        """A filesystem edit far outside the AI edit time window → not tagged."""
        events = [
            _ai_edit(1000.0, "C:\\proj\\fix-ccr-code.ps1"),
            _fs_edit(1000.0 + 7200, "fix-ccr-code.ps1", "file:///C:/proj/fix-ccr-code.ps1"),
        ]
        events = tag_agent_file_edits(events)
        self.assertFalse(events[1].get("agent_edited", False))

    def test_matches_by_basename_when_no_resource(self):
        """Fallback: match by basename when resource path is empty."""
        events = [
            _ai_edit(1000.0, "C:\\proj\\fix-ccr-code.ps1"),
            _fs_edit(1005.0, "fix-ccr-code.ps1", ""),  # no resource
        ]
        events = tag_agent_file_edits(events)
        self.assertTrue(events[1].get("agent_edited"))

    def test_write_tool_also_tags(self):
        """Write tool calls also trigger tagging (not just Edit)."""
        events = [
            {"source_kind": "ai_session", "kind": "tool_use", "tool_name": "Write",
             "timestamp": 1000.0, "tool_input": {"file_path": "C:\\proj\\new.py"}},
            _fs_edit(1003.0, "new.py", "file:///C:/proj/new.py"),
        ]
        events = tag_agent_file_edits(events)
        self.assertTrue(events[1].get("agent_edited"))

    def test_no_ai_edits_no_tagging(self):
        """When there are no AI edit events, nothing is tagged (no crash)."""
        events = [_fs_edit(1000.0, "file.py", "file:///C:/proj/file.py")]
        events = tag_agent_file_edits(events)
        self.assertFalse(events[0].get("agent_edited", False))


class TestHumanInvolvementExcludesAgentEdits(unittest.TestCase):
    def test_agent_edited_file_not_human_action(self):
        """An agent-edited filesystem event is NOT a human action (rubric 68)."""
        ev = _fs_edit(1000.0, "fix-ccr-code.ps1", "file:///C:/proj/fix-ccr-code.ps1")
        ev["agent_edited"] = True
        self.assertFalse(is_human_action(ev))

    def test_normal_file_edit_is_human_action(self):
        """A normal (non-agent) filesystem event IS a human action."""
        ev = _fs_edit(1000.0, "notes.md", "file:///C:/proj/notes.md")
        self.assertTrue(is_human_action(ev))


if __name__ == "__main__":
    unittest.main()
