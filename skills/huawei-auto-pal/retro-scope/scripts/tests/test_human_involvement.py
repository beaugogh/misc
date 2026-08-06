"""Tests for the human-involvement detector (human_involvement.py).

Verifies that human actions are correctly identified and that human-engaged
time is computed separately from machine/autonomous time.

Run with: python -m unittest discover -s scripts/tests
"""

import unittest
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from human_involvement import (
    is_human_action,
    compute_human_involvement,
    compute_actual_working_hours,
    describe_human_involvement,
    HUMAN_ENGAGEMENT_GAP,
)


def _ev(kind, text=None, tool_name=None, tool_input=None, tool_is_error=None,
        tool_use_id=None, source_kind="ai_session", timestamp=1000000.0):
    ev = {
        "source": "test",
        "source_kind": source_kind,
        "session_id": "s1",
        "timestamp": timestamp,
        "kind": kind,
        "text": text,
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_is_error": tool_is_error,
        "tool_use_id": tool_use_id,
    }
    return ev


class TestIsHumanAction(unittest.TestCase):
    def test_user_message_is_human(self):
        self.assertTrue(is_human_action(_ev("user_message", text="do something")))

    def test_assistant_message_is_not_human(self):
        self.assertFalse(is_human_action(_ev("assistant_message", text="working on it")))

    def test_tool_use_is_not_human(self):
        self.assertFalse(is_human_action(_ev("tool_use", tool_name="Bash",
                                             tool_input={"command": "git fetch"})))

    def test_tool_result_success_is_not_human(self):
        self.assertFalse(is_human_action(_ev("tool_result", text="done",
                                             tool_is_error=False)))

    def test_user_rejection_is_human(self):
        ev = _ev("tool_result", text="The user doesn't want to proceed with this tool use.",
                 tool_is_error=True)
        self.assertTrue(is_human_action(ev))

    def test_tool_error_not_rejection_is_not_human(self):
        ev = _ev("tool_result", text="Exit code 128\nfatal: unable to access",
                 tool_is_error=True)
        self.assertFalse(is_human_action(ev))

    def test_browser_revisit_is_human(self):
        ev = _ev("visit", tool_input={"url": "https://example.com", "visit_count": 5})
        self.assertTrue(is_human_action(ev))

    def test_browser_single_visit_is_not_human(self):
        ev = _ev("visit", tool_input={"url": "https://example.com", "visit_count": 1})
        self.assertFalse(is_human_action(ev))

    def test_email_sent_is_human(self):
        ev = _ev("email", tool_input={"direction": "sent", "subject": "RE: test"})
        self.assertTrue(is_human_action(ev))

    def test_email_received_is_not_human(self):
        ev = _ev("email", tool_input={"direction": "received", "subject": "FW: test"})
        self.assertFalse(is_human_action(ev))

    def test_commit_is_human(self):
        self.assertTrue(is_human_action(_ev("commit", source_kind="vcs")))

    def test_filesystem_event_is_human(self):
        self.assertTrue(is_human_action(_ev("event", source_kind="filesystem")))


class TestComputeHumanInvolvement(unittest.TestCase):
    def _task(self, active=3600, **kw):
        t = {"active_seconds": active, "wall_clock_seconds": active}
        t.update(kw)
        return t

    def test_no_human_actions_returns_none(self):
        events = [_ev("tool_use", tool_name="Bash", timestamp=1000.0),
                  _ev("assistant_message", text="working", timestamp=1001.0)]
        hd = compute_human_involvement(events, self._task(active=3600))
        self.assertEqual(hd["human_involvement"], "none")
        self.assertEqual(hd["human_action_count"], 0)
        self.assertEqual(hd["human_engaged_seconds"], 0.0)

    def test_high_involvement(self):
        # 60 user messages within 30s of each other = high involvement.
        events = [_ev("user_message", text=f"msg {i}", timestamp=1000.0 + i * 10)
                  for i in range(60)]
        hd = compute_human_involvement(events, self._task(active=600))
        self.assertEqual(hd["human_involvement"], "high")
        self.assertEqual(hd["human_action_count"], 60)
        # Engaged time: 59 intervals × 10s = 590s.
        self.assertAlmostEqual(hd["human_engaged_seconds"], 590.0, delta=1.0)

    def test_low_involvement(self):
        # 3 user messages, 500 tool_uses — mostly autonomous.
        events = [_ev("user_message", text="msg", timestamp=1000.0 + i * 60)
                  for i in range(3)]
        events += [_ev("tool_use", tool_name="Bash", timestamp=1000.0 + i * 5)
                   for i in range(500)]
        hd = compute_human_involvement(events, self._task(active=36000))
        self.assertEqual(hd["human_involvement"], "low")
        self.assertEqual(hd["human_action_count"], 3)

    def test_gaps_over_30min_excluded(self):
        # 3 user messages: t=0, t=10min, t=2h later. Only the first 10min interval counts.
        events = [_ev("user_message", text="msg", timestamp=1000.0),
                  _ev("user_message", text="msg", timestamp=1000.0 + 600),   # 10 min later
                  _ev("user_message", text="msg", timestamp=1000.0 + 7200)]  # 2h later
        hd = compute_human_involvement(events, self._task(active=7200))
        # Engaged: only the 600s interval. The 6600s gap is excluded.
        self.assertAlmostEqual(hd["human_engaged_seconds"], 600.0, delta=1.0)

    def test_single_human_action_gets_minimum(self):
        events = [_ev("user_message", text="one msg", timestamp=1000.0)]
        hd = compute_human_involvement(events, self._task(active=3600))
        self.assertEqual(hd["human_action_count"], 1)
        # Single action → 5 min minimum engaged.
        self.assertEqual(hd["human_engaged_seconds"], 300.0)

    def test_action_types_collected(self):
        events = [
            _ev("user_message", text="msg", timestamp=1000.0),
            _ev("visit", tool_input={"visit_count": 3}, timestamp=1001.0),
            _ev("email", tool_input={"direction": "sent"}, timestamp=1002.0),
        ]
        hd = compute_human_involvement(events, self._task(active=3600))
        types_str = " ".join(hd["human_action_types"])
        self.assertIn("prompt", types_str)
        self.assertIn("click", types_str)
        self.assertIn("email", types_str)

    def test_machine_autonomous_computed(self):
        # 2 human actions (10 min apart), active=2h. Autonomous = 2h - 10min.
        events = [_ev("user_message", text="msg", timestamp=1000.0),
                  _ev("user_message", text="msg", timestamp=1000.0 + 600)]
        hd = compute_human_involvement(events, self._task(active=7200))
        self.assertAlmostEqual(hd["human_engaged_seconds"], 600.0, delta=1.0)
        self.assertAlmostEqual(hd["machine_autonomous_seconds"], 6600.0, delta=1.0)

    def test_forgotten_tab_browser(self):
        """Browser task with 3.5h wall but only 0.1h active is a forgotten tab."""
        # 5 visits (enough to pass the normal genuine threshold), but all within
        # 5 minutes, in a 3.5h wall-clock window.
        events = [_ev("visit", tool_input={"visit_count": 5}, timestamp=1000.0 + i * 60)
                  for i in range(5)]
        task = self._task(active=360, wall_clock_seconds=12600)  # 0.1h active, 3.5h wall
        task["source_kind"] = "browser"
        hd = compute_human_involvement(events, task)
        self.assertTrue(hd.get("forgotten_tab"))
        self.assertFalse(hd.get("is_genuine_time_sink"))

    def test_forgotten_tab_not_triggered_for_short_wall(self):
        """Short wall clock (< 2h) doesn't trigger forgotten-tab even with low active ratio."""
        events = [_ev("visit", tool_input={"visit_count": 5}, timestamp=1000.0 + i * 60)
                  for i in range(5)]
        task = self._task(active=360, wall_clock_seconds=3600)  # 0.1h active, 1h wall
        task["source_kind"] = "browser"
        hd = compute_human_involvement(events, task)
        self.assertFalse(hd.get("forgotten_tab"))

    def test_forgotten_tab_not_triggered_for_non_browser(self):
        """Forgotten-tab detection only applies to browser tasks."""
        events = [_ev("user_message", text="msg", timestamp=1000.0 + i * 60)
                  for i in range(5)]
        task = self._task(active=360, wall_clock_seconds=12600)  # 0.1h active, 3.5h wall
        task["source_kind"] = "ai_session"
        hd = compute_human_involvement(events, task)
        self.assertFalse(hd.get("forgotten_tab"))


class TestComputeActualWorkingHours(unittest.TestCase):
    def test_no_human_activity_returns_zero(self):
        tasks = [{"start": 1000.0, "human_data": {"human_engaged_seconds": 0}}]
        self.assertEqual(compute_actual_working_hours(tasks), 0.0)

    def test_returns_engaged_hours(self):
        tasks = [
            {"start": 1000.0, "human_data": {"human_engaged_seconds": 7200}},  # 2h
            {"start": 2000.0, "human_data": {"human_engaged_seconds": 10800}}, # 3h
        ]
        # 5h total engaged
        self.assertAlmostEqual(compute_actual_working_hours(tasks), 5.0, delta=0.01)

    def test_minimum_one_hour_average_per_active_day(self):
        # 2 tasks on different days, but only 30min engaged each.
        # The period has 2h minimum total over 2 active days: 1h/day average.
        tasks = [
            {"start": 1780000000.0, "human_data": {"human_engaged_seconds": 1800}},  # 0.5h
            {"start": 1780000000.0 + 86400, "human_data": {"human_engaged_seconds": 1800}},  # 0.5h next day
        ]
        result = compute_actual_working_hours(tasks)
        self.assertAlmostEqual(result, 1.0, delta=0.01)


class TestDescribeHumanInvolvement(unittest.TestCase):
    def test_none_involvement_meeting(self):
        hd = {"human_involvement": "none", "human_action_count": 0,
              "human_engaged_seconds": 0, "human_action_types": []}
        task = {"source_kind": "meeting", "active_seconds": 8 * 3600}
        desc = describe_human_involvement(hd, task)
        self.assertIn("No human interaction", desc)
        self.assertIn("calendar", desc)

    def test_none_involvement_browser(self):
        hd = {"human_involvement": "none", "human_action_count": 0,
              "human_engaged_seconds": 0, "human_action_types": []}
        task = {"source_kind": "browser", "active_seconds": 0,
                "wall_clock_seconds": 30 * 3600}
        desc = describe_human_involvement(hd, task)
        self.assertIn("tabs", desc.lower())
        self.assertIn("left open", desc)

    def test_high_involvement(self):
        hd = {"human_involvement": "high", "human_action_count": 100,
              "human_engaged_seconds": 5 * 3600, "machine_autonomous_seconds": 0,
              "human_action_types": ["100 prompt(s)"]}
        task = {"active_seconds": 5 * 3600}
        desc = describe_human_involvement(hd, task)
        self.assertIn("heavy involvement", desc)
        self.assertIn("5.0h", desc)

    def test_low_involvement(self):
        hd = {"human_involvement": "low", "human_action_count": 3,
              "human_engaged_seconds": 300, "machine_autonomous_seconds": 9 * 3600,
              "human_action_types": ["3 prompt(s)"]}
        task = {"active_seconds": 10 * 3600}
        desc = describe_human_involvement(hd, task)
        self.assertIn("mostly autonomous", desc)
        self.assertIn("9.0h", desc)


if __name__ == "__main__":
    unittest.main()
