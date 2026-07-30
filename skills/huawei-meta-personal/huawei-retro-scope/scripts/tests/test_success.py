"""Tests for the three-valued success attribution model (Phase 10.3).

Tests:
  - _determine_success returns "succeeded" / "failed" / "unknown" strings
  - Per-type signals (vcs, research, meeting, email, conversation)
  - AI-coding signals (explicit TaskUpdate, implicit end_turn, error clusters)
  - refine_success upgrades unknown based on cross-task context
  - aggregate() excludes unknown from the success-rate denominator
  - render_report shows "n/a" instead of "0%" when all tasks are unknown

Run with: python -m unittest tests.test_success -v
"""

import unittest
import os
import sys

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from segment_tasks import (
    _determine_success,
    _make_task,
    refine_success,
    _compute_active_seconds,
    _is_correction,
    _commit_is_meaningful,
    _has_semantic_overlap,
    _significant_tokens,
    MAX_MEETING_DURATION,
    SUCCESS_SUCCEEDED,
    SUCCESS_FAILED,
    SUCCESS_UNKNOWN,
)
from aggregate import aggregate, render_report, render_markdown, render_table, render_html


# ---------------------------------------------------------------------------
# Helpers: synthetic event builders
# ---------------------------------------------------------------------------

def _ev(kind="tool_use", ts=1000.0, **kw):
    """Build a minimal synthetic event dict."""
    e = {"kind": kind, "timestamp": ts}
    e.update(kw)
    return e


def _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
          subject="(test)", tool_names=None, event_count=5, git_commits=None,
          flavor="implicit", **kw):
    """Build a minimal synthetic task dict."""
    t = {
        "id": "test-1",
        "flavor": flavor,
        "source": "claude_code",
        "source_kind": source_kind,
        "session_id": "s1",
        "cwd": "/proj",
        "git_branch": "main",
        "subject": subject,
        "start": start,
        "end": end,
        "duration_seconds": end - start,
        "wall_clock_seconds": end - start,
        "active_seconds": end - start,
        "event_count": event_count,
        "tool_calls": 0,
        "tool_names": tool_names or [],
        "output_tokens": 0,
        "input_tokens": 0,
        "errors": 0,
        "inputs": [],
        "outputs": [],
        "success": success,
        "success_evidence": "(test)",
        "task_status": None,
    }
    if git_commits is not None:
        t["git_commits"] = git_commits
    t.update(kw)
    return t


# ---------------------------------------------------------------------------
# Test AI-coding signals (existing logic, now three-valued)
# ---------------------------------------------------------------------------

class TestAICodingSuccess(unittest.TestCase):
    """Test that the existing AI-coding signals map to the new three-valued strings."""

    def test_explicit_completed_no_errors(self):
        """TaskUpdate(completed) + no errors → succeeded."""
        events = [
            _ev(kind="tool_use", tool_name="TaskCreate", ts=1000.0),
            _ev(kind="tool_use", tool_name="TaskUpdate", ts=2000.0,
                tool_input={"status": "completed"}),
        ]
        success, evidence = _determine_success("explicit", events, "completed", "ai_session")
        self.assertEqual(success, SUCCESS_SUCCEEDED)
        self.assertIn("completed", evidence)

    def test_explicit_deleted(self):
        """TaskUpdate(deleted) → failed."""
        events = [
            _ev(kind="tool_use", tool_name="TaskCreate", ts=1000.0),
        ]
        success, evidence = _determine_success("explicit", events, "deleted", "ai_session")
        self.assertEqual(success, SUCCESS_FAILED)

    def test_explicit_no_terminal_update(self):
        """No terminal TaskUpdate → unknown (NOT failed)."""
        events = [
            _ev(kind="tool_use", tool_name="TaskCreate", ts=1000.0),
        ]
        success, evidence = _determine_success("explicit", events, "unknown", "ai_session")
        self.assertEqual(success, SUCCESS_UNKNOWN)

    def test_implicit_end_turn_no_errors(self):
        """Implicit: end_turn + no errors + no corrections → succeeded."""
        events = [
            _ev(kind="user_message", text="do it", ts=1000.0),
            _ev(kind="assistant_message", stop_reason="end_turn", ts=1100.0),
        ]
        success, evidence = _determine_success("implicit", events, None, "ai_session")
        self.assertEqual(success, SUCCESS_SUCCEEDED)
        self.assertIn("end_turn", evidence)

    def test_implicit_errors_and_correction(self):
        """Implicit: errors + user correction → failed."""
        events = [
            _ev(kind="user_message", text="do it", ts=1000.0),
            _ev(kind="tool_use", ts=1100.0, tool_is_error=True),
            _ev(kind="user_message", text="no, fix it", ts=1200.0),
        ]
        success, evidence = _determine_success("implicit", events, None, "ai_session")
        self.assertEqual(success, SUCCESS_FAILED)
        self.assertIn("correction", evidence)

    def test_implicit_end_turn_with_errors(self):
        """Implicit: end_turn but errors → unknown (not failed)."""
        events = [
            _ev(kind="user_message", text="do it", ts=1000.0),
            _ev(kind="tool_use", ts=1100.0, tool_is_error=True),
            _ev(kind="assistant_message", stop_reason="end_turn", ts=1200.0),
        ]
        success, evidence = _determine_success("implicit", events, None, "ai_session")
        self.assertEqual(success, SUCCESS_UNKNOWN)

    def test_explicit_completed_with_errors_still_succeeded(self):
        """TaskUpdate(completed) with errors → still succeeded (completed despite errors)."""
        events = [
            _ev(kind="tool_use", tool_name="TaskCreate", ts=1000.0),
            _ev(kind="tool_use", ts=1100.0, tool_is_error=True),
        ]
        success, evidence = _determine_success("explicit", events, "completed", "ai_session")
        self.assertEqual(success, SUCCESS_SUCCEEDED)
        self.assertIn("error", evidence)


# ---------------------------------------------------------------------------
# Test per-type signals
# ---------------------------------------------------------------------------

class TestPerTypeSuccess(unittest.TestCase):
    """Test per-type success signals for vcs, research, meeting, email, conversation."""

    def test_vcs_commit_landed(self):
        """VCS task with a commit event → succeeded."""
        events = [_ev(kind="commit", ts=1000.0)]
        success, evidence = _determine_success("implicit", events, None, "vcs")
        self.assertEqual(success, SUCCESS_SUCCEEDED)
        self.assertIn("commit", evidence)

    def test_vcs_no_commit(self):
        """VCS task with no commit → unknown."""
        events = [_ev(kind="tool_use", ts=1000.0)]
        success, evidence = _determine_success("implicit", events, None, "vcs")
        self.assertEqual(success, SUCCESS_UNKNOWN)

    def test_vcs_reverted_commit(self):
        """VCS task with a revert → failed."""
        events = [
            _ev(kind="commit", ts=1000.0),
            _ev(kind="commit", ts=1100.0, text="Revert: previous commit"),
        ]
        success, evidence = _determine_success("implicit", events, None, "vcs")
        self.assertEqual(success, SUCCESS_FAILED)
        self.assertIn("revert", evidence)

    def test_research_with_artifact(self):
        """Research (browser) task that produced a Write/Edit → succeeded."""
        events = [
            _ev(kind="tool_use", tool_name="WebSearch", ts=1000.0),
            _ev(kind="tool_use", tool_name="Write", ts=1100.0,
                tool_input={"file_path": "/proj/notes.md"}),
        ]
        success, evidence = _determine_success("implicit", events, None, "browser")
        self.assertEqual(success, SUCCESS_SUCCEEDED)
        self.assertIn("artifact", evidence)

    def test_research_browsing_only(self):
        """Research (browser) with no artifact → unknown."""
        events = [
            _ev(kind="tool_use", tool_name="WebSearch", ts=1000.0),
            _ev(kind="tool_use", tool_name="WebFetch", ts=1100.0),
        ]
        success, evidence = _determine_success("implicit", events, None, "browser")
        self.assertEqual(success, SUCCESS_UNKNOWN)

    def test_meeting_no_signal(self):
        """Meeting task → unknown (no in-task signal)."""
        events = [_ev(kind="meeting", ts=1000.0)]
        success, evidence = _determine_success("implicit", events, None, "meeting")
        self.assertEqual(success, SUCCESS_UNKNOWN)

    def test_email_reply_sent(self):
        """Email thread with received then sent → succeeded."""
        events = [
            _ev(kind="email", ts=1000.0, tool_input={"direction": "received"}),
            _ev(kind="email", ts=2000.0, tool_input={"direction": "sent"}),
        ]
        success, evidence = _determine_success("implicit", events, None, "comm")
        self.assertEqual(success, SUCCESS_SUCCEEDED)
        self.assertIn("reply", evidence)

    def test_email_no_reply(self):
        """Email thread with only received → unknown."""
        events = [
            _ev(kind="email", ts=1000.0, tool_input={"direction": "received"}),
        ]
        success, evidence = _determine_success("implicit", events, None, "comm")
        self.assertEqual(success, SUCCESS_UNKNOWN)


# ---------------------------------------------------------------------------
# Test refine_success (cross-task context signals)
# ---------------------------------------------------------------------------

class TestRefineSuccess(unittest.TestCase):
    """Test refine_success upgrades 'unknown' based on cross-task context."""

    def test_git_commit_linked_upgrades_to_succeeded(self):
        """A task with git_commits attached by cross_source → succeeded (with semantic overlap)."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
                  subject="fix bug in parser",
                  git_commits=[{"hash": "abc123def", "subject": "fix parser bug"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)
        self.assertIn("git commit", tasks[0]["success_evidence"])

    def test_research_followed_by_coding_within_1h(self):
        """Research (browser) followed by coding task within 1h → succeeded."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN, source_kind="browser",
                  subject="research"),
            _task(start=2100.0, end=3000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
                  subject="code", tool_names=["Write", "Edit"]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)
        self.assertIn("coding task", tasks[0]["success_evidence"])

    def test_research_followed_by_coding_after_1h_stays_unknown(self):
        """Research followed by coding after >1h gap → stays unknown."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN, source_kind="browser",
                  subject="research"),
            # >1h later (3601s gap)
            _task(start=2000.0 + 3601.0, end=5000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
                  subject="code", tool_names=["Write"]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_UNKNOWN)

    def test_meeting_with_followup_referencing_subject(self):
        """Meeting with follow-up task referencing subject keywords within 24h → succeeded."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN, source_kind="meeting",
                  subject="Q3 planning review"),
            _task(start=3000.0, end=4000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
                  subject="work on planning docs", tool_names=["Write"]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)
        self.assertIn("follow-up", tasks[0]["success_evidence"])

    def test_meeting_no_followup_stays_unknown(self):
        """Meeting with no follow-up referencing subject → stays unknown."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN, source_kind="meeting",
                  subject="random topic"),
            _task(start=3000.0, end=4000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
                  subject="completely different work", tool_names=["Write"]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_UNKNOWN)

    def test_conversation_followed_by_coding(self):
        """Conversation (no tools, few events) followed by coding → succeeded."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
                  subject="chat", tool_names=[], event_count=2),
            _task(start=2100.0, end=3000.0, success=SUCCESS_UNKNOWN, source_kind="ai_session",
                  subject="code", tool_names=["Bash", "Edit"]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_already_succeeded_not_changed(self):
        """A task already succeeded is not modified by refine_success."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_SUCCEEDED,
                  source_kind="ai_session", git_commits=[{"hash": "abc", "subject": "x"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_already_failed_not_changed(self):
        """A task already failed is not modified by refine_success."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_FAILED,
                  source_kind="ai_session", git_commits=[{"hash": "abc", "subject": "x"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_FAILED)


# ---------------------------------------------------------------------------
# Test aggregation: unknown excluded from denominator
# ---------------------------------------------------------------------------

class TestAggregationUnknownExcluded(unittest.TestCase):
    """Test that aggregate() excludes unknown from the success-rate denominator."""

    def test_success_rate_excludes_unknown(self):
        """success_rate = succeeded / (succeeded + failed), unknown excluded."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_SUCCEEDED, tool_names=["Edit"]),
            _task(start=1782967200.0, success=SUCCESS_FAILED, tool_names=["Edit"]),
            _task(start=1782967200.0, success=SUCCESS_UNKNOWN, tool_names=["Edit"]),
            _task(start=1782967200.0, success=SUCCESS_UNKNOWN, tool_names=["Edit"]),
        ]
        agg = aggregate(tasks, "day")
        period = list(agg.values())[0]
        self.assertEqual(period["success_count"], 1)
        self.assertEqual(period["failure_count"], 1)
        self.assertEqual(period["unknown_count"], 2)
        self.assertEqual(period["task_count"], 4)

    def test_all_unknown_renders_na(self):
        """A category with all unknown tasks renders 'n/a', NOT '0%'."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_UNKNOWN, source_kind="meeting",
                  subject="standup"),
            _task(start=1782967200.0 + 3600, success=SUCCESS_UNKNOWN, source_kind="meeting",
                  subject="review"),
        ]
        agg = aggregate(tasks, "day")
        report = render_report(agg, "day")
        self.assertIn("n/a", report)
        self.assertNotIn("0% success", report)

    def test_mixed_known_unknown_renders_both(self):
        """Mixed known/unknown renders both success% and unknown%."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_SUCCEEDED, tool_names=["Edit"]),
            _task(start=1782967200.0 + 100, success=SUCCESS_FAILED, tool_names=["Edit"]),
            _task(start=1782967200.0 + 200, success=SUCCESS_UNKNOWN, tool_names=["Edit"]),
        ]
        agg = aggregate(tasks, "day")
        report = render_report(agg, "day")
        # success% over known = 1/(1+1) = 50%
        self.assertIn("50% success", report)
        # unknown% = 1/3 = 33%
        self.assertIn("33% unknown", report)

    def test_per_kind_unknown_tracking(self):
        """by_kind stats track successes, failures, unknowns separately."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_SUCCEEDED, tool_names=["Edit"]),
            _task(start=1782967200.0 + 100, success=SUCCESS_UNKNOWN, tool_names=["Edit"]),
        ]
        agg = aggregate(tasks, "day")
        period = list(agg.values())[0]
        coding = period["by_kind"]["coding"]
        self.assertEqual(coding["successes"], 1)
        self.assertEqual(coding["failures"], 0)
        self.assertEqual(coding["unknowns"], 1)

    def test_markdown_renders_na_for_all_unknown(self):
        """Markdown output also shows 'n/a' for all-unknown categories."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_UNKNOWN, source_kind="meeting",
                  subject="standup"),
        ]
        agg = aggregate(tasks, "day")
        md = render_markdown(agg, "day")
        self.assertIn("n/a", md)

    def test_table_renders_na_for_all_unknown(self):
        """Table output also shows 'n/a' for all-unknown categories."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_UNKNOWN, source_kind="meeting",
                  subject="standup"),
        ]
        agg = aggregate(tasks, "day")
        tbl = render_table(agg, "day")
        self.assertIn("n/a", tbl)

    def test_html_renders_na_for_all_unknown(self):
        """HTML output also shows 'n/a' for all-unknown categories."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_UNKNOWN, source_kind="meeting",
                  subject="standup"),
        ]
        agg = aggregate(tasks, "day")
        htm = render_html(agg, "day")
        self.assertIn("n/a", htm)

    def test_success_rate_calculation(self):
        """Verify exact success rate: 3 succeeded, 1 failed, 2 unknown → 75% success."""
        tasks = [
            _task(start=1782967200.0, success=SUCCESS_SUCCEEDED, tool_names=["Edit"]),
            _task(start=1782967200.0 + 100, success=SUCCESS_SUCCEEDED, tool_names=["Edit"]),
            _task(start=1782967200.0 + 200, success=SUCCESS_SUCCEEDED, tool_names=["Edit"]),
            _task(start=1782967200.0 + 300, success=SUCCESS_FAILED, tool_names=["Edit"]),
            _task(start=1782967200.0 + 400, success=SUCCESS_UNKNOWN, tool_names=["Edit"]),
            _task(start=1782967200.0 + 500, success=SUCCESS_UNKNOWN, tool_names=["Edit"]),
        ]
        agg = aggregate(tasks, "day")
        report = render_report(agg, "day")
        # 3/(3+1) = 75% success, 2/6 = 33% unknown
        self.assertIn("75% success", report)
        self.assertIn("33% unknown", report)


# ---------------------------------------------------------------------------
# Test _make_task integration
# ---------------------------------------------------------------------------

class TestMakeTaskIntegration(unittest.TestCase):
    """Test that _make_task stores the three-valued success string on the task dict."""

    def test_make_task_stores_string_success(self):
        """_make_task stores 'succeeded'/'failed'/'unknown', not bool/None."""
        events = [
            _ev(kind="tool_use", tool_name="TaskCreate", ts=1000.0,
                tool_input={"subject": "test"}),
            _ev(kind="tool_use", tool_name="TaskUpdate", ts=2000.0,
                tool_input={"status": "completed"}),
        ]
        task = _make_task("explicit-1", "explicit", events, "test", "completed")
        self.assertIsInstance(task["success"], str)
        self.assertEqual(task["success"], SUCCESS_SUCCEEDED)
        self.assertIsInstance(task["success_evidence"], str)

    def test_make_task_implicit_unknown(self):
        """_make_task for implicit with no clear signal → unknown string."""
        events = [
            _ev(kind="user_message", text="hello", ts=1000.0),
        ]
        task = _make_task("implicit-1", "implicit", events, "hello")
        self.assertEqual(task["success"], SUCCESS_UNKNOWN)

    def test_make_task_vcs_source_kind(self):
        """_make_task with vcs source_kind uses vcs success logic."""
        events = [
            _ev(kind="commit", ts=1000.0, source_kind="vcs"),
        ]
        task = _make_task("implicit-1", "implicit", events, "commit")
        self.assertEqual(task["source_kind"], "vcs")
        self.assertEqual(task["success"], SUCCESS_SUCCEEDED)

# ---------------------------------------------------------------------------
# C2: Unbounded real_end — corrupt timestamp clamped
# ---------------------------------------------------------------------------

class TestC2CorruptTimestampClamp(unittest.TestCase):
    """Test that corrupt end_ts values are clamped to MAX_MEETING_DURATION."""

    def test_normal_meeting_duration_preserved(self):
        """A normal 1h meeting should return its real duration."""
        events = [
            _ev(kind="meeting", ts=1000.0, extra={"end_ts": 1000.0 + 3600}),
        ]
        active, excised = _compute_active_seconds(events)
        self.assertAlmostEqual(active, 3600.0, places=1)
        self.assertEqual(excised, 0.0)

    def test_long_meeting_under_limit_preserved(self):
        """A 20h meeting (under 24h limit) should be preserved."""
        events = [
            _ev(kind="meeting", ts=1000.0, extra={"end_ts": 1000.0 + 20 * 3600}),
        ]
        active, _ = _compute_active_seconds(events)
        self.assertAlmostEqual(active, 20 * 3600, places=1)

    def test_corrupt_end_ts_clamped_to_24h(self):
        """A corrupt end_ts (years later) should be clamped to 24h."""
        events = [
            _ev(kind="meeting", ts=1000.0, extra={"end_ts": 1000.0 + 99999999}),
        ]
        active, _ = _compute_active_seconds(events)
        self.assertAlmostEqual(active, MAX_MEETING_DURATION, places=1)
        self.assertLess(active, 99999999)

    def test_corrupt_end_ts_does_not_poison_total(self):
        """Multiple events — one corrupt — should not produce absurd duration."""
        events = [
            _ev(kind="meeting", ts=1000.0, extra={"end_ts": 1000.0 + 3600}),
            _ev(kind="meeting", ts=1100.0, extra={"end_ts": 1000.0 + 99999999}),
        ]
        active, _ = _compute_active_seconds(events)
        # Should be clamped to 24h, not ~99999999
        self.assertAlmostEqual(active, MAX_MEETING_DURATION, places=1)

    def test_excised_gap_seconds_from_mid_task_gap(self):
        """Inter-event gaps > threshold are counted as excised_gap_seconds."""
        events = [
            _ev(kind="user_message", ts=1000.0),
            _ev(kind="assistant_message", ts=1100.0),
            # 1h gap > 30min threshold
            _ev(kind="user_message", ts=1000.0 + 3600),
            _ev(kind="assistant_message", ts=1000.0 + 3700),
        ]
        active, excised = _compute_active_seconds(events)
        # active = 100 + 100 = 200
        self.assertAlmostEqual(active, 200.0, places=1)
        # excised = 3600 - 100 = 3500 (gap from 1100 to 4600)
        self.assertAlmostEqual(excised, 3500.0, places=1)


# ---------------------------------------------------------------------------
# C3: False success attribution — commit filtering
# ---------------------------------------------------------------------------

class TestC3CommitFiltering(unittest.TestCase):
    """Test that non-success commits and unrelated commits don't upgrade tasks."""

    def test_revert_commit_does_not_upgrade(self):
        """A revert commit should NOT upgrade unknown → succeeded."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  git_commits=[{"hash": "abc123", "subject": "Revert: fix parser bug"}],
                  errors=0),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_UNKNOWN)

    def test_wip_commit_does_not_upgrade(self):
        """A WIP commit should NOT upgrade unknown → succeeded."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  git_commits=[{"hash": "abc123", "subject": "WIP: parser fix"}],
                  errors=0),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_UNKNOWN)

    def test_fixup_commit_does_not_upgrade(self):
        """A fixup commit should NOT upgrade unknown → succeeded."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  git_commits=[{"hash": "abc123", "subject": "fixup! fix parser bug"}],
                  errors=0),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_UNKNOWN)

    def test_unrelated_commit_no_overlap_does_not_upgrade(self):
        """A commit with no semantic overlap to the task subject should NOT upgrade."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  git_commits=[{"hash": "abc123", "subject": "update README docs"}],
                  errors=0),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_UNKNOWN)

    def test_commit_with_token_overlap_does_upgrade(self):
        """A meaningful commit with semantic overlap SHOULD upgrade."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  git_commits=[{"hash": "abc123", "subject": "fix parser bug for edge case"}],
                  errors=0),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_commit_with_no_task_subject_upgrades(self):
        """If task has no subject, commit should still upgrade (skip overlap check)."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject=None,
                  git_commits=[{"hash": "abc123", "subject": "implement feature"}],
                  errors=0),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_errors_block_commit_upgrade(self):
        """If task has errors > 0, commit should NOT upgrade (error signal is negative)."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  git_commits=[{"hash": "abc123", "subject": "fix parser bug"}],
                  errors=3),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_UNKNOWN)

    def test_mixed_commits_one_meaningful_upgrades(self):
        """If some commits are WIP/revert but one is meaningful, upgrade via the meaningful one."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  git_commits=[
                      {"hash": "aaa", "subject": "WIP: experiment"},
                      {"hash": "bbb", "subject": "fix parser bug properly"},
                  ],
                  errors=0),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_commit_is_meaningful_helper(self):
        """Test the _commit_is_meaningful helper."""
        self.assertTrue(_commit_is_meaningful({"subject": "fix bug"}))
        self.assertFalse(_commit_is_meaningful({"subject": "Revert: fix bug"}))
        self.assertFalse(_commit_is_meaningful({"subject": "wip: work in progress"}))
        self.assertFalse(_commit_is_meaningful({"subject": "tmp: temporary"}))
        self.assertFalse(_commit_is_meaningful({"subject": "fixup! old commit"}))
        self.assertFalse(_commit_is_meaningful({"subject": "squash! merge"}))

    def test_semantic_overlap_helper(self):
        """Test the _has_semantic_overlap helper."""
        self.assertTrue(_has_semantic_overlap("fix parser bug",
                                              {"subject": "fix parser bug edge case"}))
        self.assertFalse(_has_semantic_overlap("fix parser bug",
                                               {"subject": "update README docs"}))
        self.assertTrue(_has_semantic_overlap(None, {"subject": "anything"}))
        self.assertTrue(_has_semantic_overlap("fix parser bug",
                                              {"subject": "fix"}))  # 'fix' is 3 chars, significant

    def test_significant_tokens_helper(self):
        """Test the _significant_tokens helper."""
        tokens = _significant_tokens("fix the parser bug")
        self.assertIn("fix", tokens)
        self.assertIn("parser", tokens)
        self.assertIn("bug", tokens)
        self.assertNotIn("the", tokens)  # stopword
        self.assertNotIn("x", tokens)  # too short (< 3 chars)


# ---------------------------------------------------------------------------
# M7: Cross-task revert detection
# ---------------------------------------------------------------------------

class TestM7CrossTaskRevert(unittest.TestCase):
    """Test that a revert in a later task downgrades a succeeded task."""

    def test_cross_task_revert_downgrades_to_failed(self):
        """A revert commit in a later task (same cwd, within 7 days) downgrades succeeded → failed."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "abc123", "subject": "fix parser bug"}]),
            _task(start=2000.0 + 86400, end=2000.0 + 90000, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="revert work",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "def456", "subject": "Revert: fix parser bug"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_FAILED)
        self.assertIn("downgraded", tasks[0]["success_evidence"])

    def test_cross_task_revert_different_cwd_no_downgrade(self):
        """A revert in a later task with different cwd should NOT downgrade."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  cwd="/projA", errors=0,
                  git_commits=[{"hash": "abc123", "subject": "fix parser bug"}]),
            _task(start=2000.0 + 86400, end=2000.0 + 90000, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="revert work",
                  cwd="/projB", errors=0,
                  git_commits=[{"hash": "def456", "subject": "Revert: fix parser bug"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_cross_task_revert_after_7_days_no_downgrade(self):
        """A revert more than 7 days later should NOT downgrade."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "abc123", "subject": "fix parser bug"}]),
            _task(start=2000.0 + 8 * 86400, end=2000.0 + 8 * 86400 + 1000,
                  success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="revert work",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "def456", "subject": "Revert: fix parser bug"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_cross_task_non_revert_commit_no_downgrade(self):
        """A non-revert commit in a later task should NOT downgrade."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="fix parser bug",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "abc123", "subject": "fix parser bug"}]),
            _task(start=2000.0 + 86400, end=2000.0 + 90000, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="more work",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "def456", "subject": "add feature for parser"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_SUCCEEDED)

    def test_already_failed_not_downgraded_by_revert(self):
        """A task already failed should not be affected by the revert pass."""
        tasks = [
            _task(start=1000.0, end=2000.0, success=SUCCESS_FAILED,
                  source_kind="ai_session", subject="fix parser bug",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "abc123", "subject": "fix parser bug"}]),
            _task(start=2000.0 + 86400, end=2000.0 + 90000, success=SUCCESS_UNKNOWN,
                  source_kind="ai_session", subject="revert work",
                  cwd="/proj", errors=0,
                  git_commits=[{"hash": "def456", "subject": "Revert: fix parser bug"}]),
        ]
        refine_success(tasks)
        self.assertEqual(tasks[0]["success"], SUCCESS_FAILED)


# ---------------------------------------------------------------------------
# M8: Correction false positives — continuation words
# ---------------------------------------------------------------------------

class TestM8CorrectionFalsePositives(unittest.TestCase):
    """Test that continuation phrases don't trigger correction detection."""

    def test_chinese_continuation_words_not_correction(self):
        """Chinese continuation words (再, 另外, 还有) should NOT trigger correction."""
        self.assertFalse(_is_correction("再来一次"))
        self.assertFalse(_is_correction("另外还有一个问题"))
        self.assertFalse(_is_correction("还有一件事"))
        self.assertFalse(_is_correction("改一下这个"))

    def test_english_continuation_words_not_correction(self):
        """English continuation words (wait, actually) should NOT trigger correction."""
        self.assertFalse(_is_correction("please wait for me"))
        self.assertFalse(_is_correction("actually that is correct"))
        self.assertFalse(_is_correction("and also fix the typo"))

    def test_true_correction_still_detected(self):
        """True correction signals should still be detected."""
        self.assertTrue(_is_correction("no, fix it"))
        self.assertTrue(_is_correction("wrong, that is not right"))
        self.assertTrue(_is_correction("incorrect, try again"))
        self.assertTrue(_is_correction("didn't work, try instead"))
        self.assertTrue(_is_correction("instead use the other approach"))

    def test_chinese_true_corrections_still_detected(self):
        """Chinese true corrections should still be detected."""
        self.assertTrue(_is_correction("不对，这里有问题"))
        self.assertTrue(_is_correction("错了，重新做"))
        self.assertTrue(_is_correction("又错了"))
        self.assertTrue(_is_correction("不要这样做"))

    def test_correction_near_start_only(self):
        """Correction signal must be near the START (first 5 words)."""
        # "wrong" at position 6+ should NOT trigger
        self.assertFalse(_is_correction("I was working on the wrong thing today"))
        # "wrong" at start SHOULD trigger
        self.assertTrue(_is_correction("wrong approach, let me fix"))

    def test_word_boundary_matching(self):
        """'no' as a bare substring in 'knowledge' should NOT trigger."""
        self.assertFalse(_is_correction("knowledge is power"))
        self.assertFalse(_is_correction("nobody knows"))
        # But "no" as a word at start SHOULD trigger (via "no," signal)
        self.assertTrue(_is_correction("no, that is wrong"))

    def test_fix_not_in_correction_signals(self):
        """'fix' alone should NOT trigger correction (it's in task instructions)."""
        self.assertFalse(_is_correction("fix the typo in line 5"))
        self.assertFalse(_is_correction("can you fix this?"))

    def test_missing_not_in_correction_signals(self):
        """'missing' alone should NOT trigger correction."""
        self.assertFalse(_is_correction("missing import statement"))
        self.assertFalse(_is_correction("the file is missing"))


if __name__ == "__main__":
    unittest.main()
