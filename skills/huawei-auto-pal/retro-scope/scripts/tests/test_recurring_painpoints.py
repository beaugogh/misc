"""Tests for recurring time-consumption detection across time windows.

Run with:
    cd D:\\workspace\\misc\\skills\\huawei-auto-pal\\retro-scope\\scripts
    python -m unittest tests.test_recurring_painpoints -v
"""

import unittest
import os
import sys

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from recurring_painpoints import (
    split_into_windows,
    _normalize_subject,
    _window_summary,
    generate_recurring_painpoints,
)


def _make_task(subject, start, human_h=0, active_h=0, kind="ai_session", errors=0):
    """Build a minimal task dict for testing."""
    t = {
        "subject": subject,
        "start": start,
        "end": start + 3600,
        "active_seconds": active_h * 3600,
        "wall_clock_seconds": active_h * 3600,
        "source_kind": kind,
        "errors": errors,
        "human_data": {"human_engaged_seconds": human_h * 3600},
    }
    return t


NOW = 1786000000  # fixed timestamp to avoid Date.now()


class TestSplitIntoWindows(unittest.TestCase):

    def test_30d_splits_into_weekly(self):
        tasks = [_make_task("t", NOW - i * 86400, human_h=1) for i in range(30)]
        windows = split_into_windows(tasks, NOW, 30)
        self.assertGreaterEqual(len(windows), 2)
        # Each window should have tasks.
        for label, wt in windows:
            self.assertTrue(len(wt) > 0, f"window {label} has no tasks")

    def test_7d_splits_into_daily(self):
        tasks = [_make_task("t", NOW - i * 86400, human_h=1) for i in range(7)]
        windows = split_into_windows(tasks, NOW, 7)
        self.assertGreaterEqual(len(windows), 2)

    def test_1d_no_split(self):
        tasks = [_make_task("t", NOW - 3600, human_h=1)]
        windows = split_into_windows(tasks, NOW, 1)
        self.assertEqual(windows, [])

    def test_drops_empty_end_windows(self):
        # Tasks only in the oldest 2 days of a 30d range.
        tasks = [_make_task("t", NOW - 29 * 86400, human_h=1),
                 _make_task("t", NOW - 28 * 86400, human_h=1)]
        windows = split_into_windows(tasks, NOW, 30)
        # Only 1 window has data → no comparison possible → empty.
        self.assertEqual(windows, [])

    def test_too_few_windows_returns_empty(self):
        tasks = [_make_task("t", NOW - 3600, human_h=1)]
        windows = split_into_windows(tasks, NOW, 30)
        self.assertEqual(windows, [])


class TestNormalizeSubject(unittest.TestCase):

    def test_strips_timestamps(self):
        self.assertEqual(_normalize_subject("sync git 2026-07-30 14:32"),
                         "sync git")

    def test_strips_uuids(self):
        s = "task abc123de-f456-7890-abcd-ef1234567890 done"
        result = _normalize_subject(s)
        self.assertNotIn("abc123de", result)

    def test_strips_task_ids(self):
        self.assertEqual(_normalize_subject("sync explicit-123"),
                         "sync")

    def test_lowercases(self):
        self.assertEqual(_normalize_subject("Sync Git FETCH"),
                         "sync git fetch")

    def test_empty_subject(self):
        self.assertEqual(_normalize_subject(None), "")
        self.assertEqual(_normalize_subject(""), "")


class TestWindowSummary(unittest.TestCase):

    def test_top_sinks_ranked_by_human_h(self):
        tasks = [
            _make_task("big", NOW, human_h=10, active_h=15),
            _make_task("small", NOW, human_h=1, active_h=2),
        ]
        summ = _window_summary(tasks)
        self.assertEqual(summ["top_sinks"][0]["subject"], "big")
        self.assertEqual(summ["top_sinks"][0]["human_h"], 10)

    def test_top_sinks_exclude_low_human_engagement(self):
        """Tasks with <10min human engagement are NOT time-consumption candidates
        (rubrics 5, 54-60). A 10h autonomous agent run with 2 prompts did NOT
        meaningfully consume the user's time."""
        tasks = [
            _make_task("autonomous", NOW, human_h=0.05, active_h=10),  # 3 min human, 10h active
            _make_task("genuine", NOW, human_h=2, active_h=3),          # 2h human
        ]
        summ = _window_summary(tasks)
        subjects = [s["subject"] for s in summ["top_sinks"]]
        self.assertIn("genuine", subjects)
        self.assertNotIn("autonomous", subjects)

    def test_pain_keywords_removed(self):
        """pain_keywords was dead computation — removed from _window_summary."""
        tasks = [_make_task("git sync failed", NOW, human_h=5, errors=3)]
        summ = _window_summary(tasks)
        self.assertNotIn("pain_keywords", summ)

    def test_totals_computed(self):
        tasks = [
            _make_task("a", NOW, human_h=5, active_h=10),
            _make_task("b", NOW, human_h=3, active_h=6),
        ]
        summ = _window_summary(tasks)
        self.assertAlmostEqual(summ["total_human_h"], 8)
        # active_h and total_active_h/total_wall_h were removed as dead computation.
        self.assertNotIn("total_active_h", summ)
        self.assertNotIn("total_wall_h", summ)


class TestGenerateRecurringPainpoints(unittest.TestCase):

    def test_chronic_time_sink(self):
        """Same subject in top-5 of 3 weekly windows → persistent insight."""
        tasks = []
        # week 0 = oldest (NOW - 21d), week 3 = newest (NOW - 0d)
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            # "git sync" is the top sink every week.
            tasks.append(_make_task("git sync origin", ts,
                                    human_h=10, errors=3))
            # Other tasks to fill the window.
            tasks.append(_make_task(f"other-{week}", ts, human_h=1))
            tasks.append(_make_task(f"misc-{week}", ts, human_h=0.5))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        self.assertTrue(any("持续性时间消耗" in i for i in insights),
                        f"expected persistent insight, got: {insights}")

    def test_resolving_painpoint(self):
        """Top sink in earlier windows, absent from latest → declining insight."""
        tasks = []
        # week 0 = oldest (NOW - 21d), week 3 = newest (NOW - 0d)
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            if week < 3:
                # "build timeout" is the top sink in weeks 0-2 (oldest 3 weeks)
                tasks.append(_make_task("build timeout", ts, human_h=10, errors=2))
            # In week 3 (newest), a different task is the top sink.
            tasks.append(_make_task(f"new-task-{week}", ts,
                                    human_h=15 if week == 3 else 1))
            tasks.append(_make_task(f"filler-{week}", ts, human_h=0.5))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        self.assertTrue(any("已下降" in i for i in insights),
                        f"expected declining insight, got: {insights}")

    def test_worsening_painpoint(self):
        """Human hours on a kind increase ≥50% → increasing insight."""
        tasks = []
        # week 0 = oldest (NOW - 21d), week 3 = newest (NOW - 0d)
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            # coding hours grow from 2h (oldest) → 8h (newest), +300%
            h = 2 + week * 2
            tasks.append(_make_task(f"code-{week}", ts,
                                    human_h=h, kind="ai_session"))
            tasks.append(_make_task(f"fill-{week}", ts,
                                    human_h=0.5, kind="browser"))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        self.assertTrue(any("上升" in i for i in insights),
                        f"expected increasing insight, got: {insights}")

    def test_worsening_label_correct_when_kind_has_gaps(self):
        """Worsening insight labels must reference the windows where the kind
        actually appeared, not the global first/last window labels."""
        tasks = []
        # Window 0 (oldest): browser only
        tasks.append(_make_task("browse-0", NOW - 21 * 86400, human_h=2, kind="browser"))
        # Window 1: ai_session 5h
        tasks.append(_make_task("code-1", NOW - 14 * 86400, human_h=5, kind="ai_session"))
        # Window 2: browser only
        tasks.append(_make_task("browse-2", NOW - 7 * 86400, human_h=2, kind="browser"))
        # Window 3 (newest): ai_session 10h
        tasks.append(_make_task("code-3", NOW, human_h=10, kind="ai_session"))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        worsening = [i for i in insights if "上升" in i and "ai_session" in i]
        self.assertTrue(worsening, f"expected ai_session worsening, got: {insights}")
        # The label must NOT reference window 0's date (where ai_session
        # didn't appear). Window 0 starts at NOW - 30*86400.
        from datetime import datetime, timezone
        w0_label = datetime.fromtimestamp(NOW - 30 * 86400, tz=timezone.utc).strftime("%m-%d")
        self.assertNotIn(w0_label, worsening[0],
                         f"worsening label should NOT include {w0_label} (window 0 has no "
                         f"ai_session), got: {worsening[0]}")
        # It SHOULD reference window 1's start date. Window 1 starts at
        # NOW - 21*86400 (the window covering days 7-14 ago starts at day 21).
        w1_label = datetime.fromtimestamp(NOW - 21 * 86400, tz=timezone.utc).strftime("%m-%d")
        self.assertIn(w1_label, worsening[0],
                      f"worsening label should include {w1_label} (first ai_session window), "
                      f"got: {worsening[0]}")

    def test_automation_candidate(self):
        """Recurrent + high error count → automation candidate insight."""
        tasks = []
        # week 0 = oldest (NOW - 21d), week 3 = newest (NOW - 0d)
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            tasks.append(_make_task("git sync proxy", ts,
                                    human_h=10, errors=5))
            tasks.append(_make_task(f"other-{week}", ts, human_h=1))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        self.assertTrue(any("自动化候选" in i for i in insights),
                        f"expected automation insight, got: {insights}")

    def test_no_recurring_painpoints_found(self):
        """All windows have different top sinks → empty list."""
        tasks = []
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            tasks.append(_make_task(f"unique-{week}", ts, human_h=10))
            tasks.append(_make_task(f"other-{week}", ts, human_h=1))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        # Should have no persistent insights (all subjects are unique per window).
        self.assertFalse(any("持续性时间消耗" in i for i in insights))

    def test_1d_horizon_returns_empty(self):
        """1d horizon can't be split → no insights."""
        tasks = [_make_task("t", NOW, human_h=5)]
        insights = generate_recurring_painpoints(tasks, NOW, 1)
        self.assertEqual(insights, [])

    def test_few_tasks_no_crash(self):
        """0-1 tasks → no crash, no insights."""
        self.assertEqual(generate_recurring_painpoints([], NOW, 30), [])
        self.assertEqual(
            generate_recurring_painpoints([_make_task("t", NOW, human_h=1)], NOW, 30),
            [])

    def test_generates_chinese_text(self):
        """Insights should be in Chinese (rubric 38)."""
        tasks = []
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            tasks.append(_make_task("git sync", ts, human_h=10, errors=3))
            tasks.append(_make_task(f"other-{week}", ts, human_h=1))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        self.assertTrue(len(insights) > 0)
        # At least one insight should contain Chinese characters.
        self.assertTrue(any(ord(c) > 127 for i in insights for c in i))

    def test_all_autonomous_window_excluded(self):
        """A window where ALL tasks have <10min human engagement contributes
        no top_sinks — autonomous agent runs did NOT consume real human time
        (rubrics 5, 54-60)."""
        tasks = []
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            if week == 0:
                # Week 0: all autonomous (below 10min human threshold)
                tasks.append(_make_task("agent-run-1", ts, human_h=0.02, active_h=10))
                tasks.append(_make_task("agent-run-2", ts, human_h=0.03, active_h=8))
            else:
                # Weeks 1-3: genuine human time consumption
                tasks.append(_make_task("git sync", ts, human_h=10, errors=3))
                tasks.append(_make_task(f"other-{week}", ts, human_h=1))
        insights = generate_recurring_painpoints(tasks, NOW, 30)
        # Persistent insight should count 3 windows (weeks 1-3), NOT 4.
        chronic = [i for i in insights if "持续性时间消耗" in i]
        self.assertTrue(chronic, "expected persistent insight")
        self.assertIn("3 个时间窗口", chronic[0],
                      f"persistent should count 3 windows (week 0 excluded), got: {chronic[0]}")


class TestHtmlIntegration(unittest.TestCase):

    def test_recurring_painpoints_section_in_html(self):
        """Recurring time consumption renders as a section in the HTML report."""
        from aggregate import render_html
        tasks = []
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            tasks.append(_make_task("git sync", ts, human_h=10, errors=3))
            tasks.append(_make_task(f"other-{week}", ts, human_h=1))
        # Minimal agg dict for render_html.
        agg = {"2026-W30": {"total_seconds": 3600, "active_seconds": 3600,
                             "human_seconds": 3600, "excised_gap_seconds": 0,
                             "task_count": 8, "success_count": 0,
                             "failure_count": 0, "unknown_count": 8,
                             "gap_count": 0, "by_kind": {}}}
        html = render_html(agg, "week", tasks=tasks,
                           since_ts=NOW - 30 * 86400, until_ts=NOW)
        self.assertIn("反复出现的时间消耗", html)

    def test_recurring_painpoints_section_absent_for_1d(self):
        """1d horizon → no recurring time-consumption section."""
        from aggregate import render_html
        tasks = [_make_task("t", NOW - 3600, human_h=1)]
        agg = {"2026-08-04": {"total_seconds": 3600, "active_seconds": 3600,
                                "human_seconds": 3600, "excised_gap_seconds": 0,
                                "task_count": 1, "success_count": 0,
                                "failure_count": 0, "unknown_count": 1,
                                "gap_count": 0, "by_kind": {}}}
        html = render_html(agg, "day", tasks=tasks,
                           since_ts=NOW - 86400, until_ts=NOW)
        self.assertNotIn("反复出现的时间消耗", html)

    def test_recurring_painpoints_section_absent_when_no_data(self):
        """No recurring time consumption → section absent, not empty."""
        from aggregate import render_html
        tasks = []
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            tasks.append(_make_task(f"unique-{week}", ts, human_h=10))
            tasks.append(_make_task(f"other-{week}", ts, human_h=1))
        agg = {"2026-W30": {"total_seconds": 3600, "active_seconds": 3600,
                             "human_seconds": 3600, "excised_gap_seconds": 0,
                             "task_count": 8, "success_count": 0,
                             "failure_count": 0, "unknown_count": 8,
                             "gap_count": 0, "by_kind": {}}}
        html = render_html(agg, "week", tasks=tasks,
                           since_ts=NOW - 30 * 86400, until_ts=NOW)
        # Section header should not appear when no recurring time consumption found.
        # (The section div might be empty but the <h2> header should be absent.)
        self.assertNotIn("<h2>反复出现的时间消耗</h2>", html)

    def test_no_duplicate_insights_in_html(self):
        """Recurring time-consumption insights must not appear in both the dedicated
        section AND the insights cards (duplicate rendering bug)."""
        from aggregate import render_html
        tasks = []
        for week in range(4):
            ts = NOW - (3 - week) * 7 * 86400
            tasks.append(_make_task("git sync", ts, human_h=10, errors=3))
            tasks.append(_make_task(f"other-{week}", ts, human_h=1))
        agg = {"2026-W30": {"total_seconds": 3600, "active_seconds": 3600,
                             "human_seconds": 3600, "excised_gap_seconds": 0,
                             "task_count": 8, "success_count": 0,
                             "failure_count": 0, "unknown_count": 8,
                             "gap_count": 0, "by_kind": {}}}
        html = render_html(agg, "week", tasks=tasks,
                           since_ts=NOW - 30 * 86400, until_ts=NOW)
        # Each recurring time-consumption insight should appear exactly once —
        # in the dedicated section, NOT also in the insights cards.
        chronic_count = html.count("持续性时间消耗")
        self.assertEqual(chronic_count, 1,
                         f"persistent insight should appear once, found {chronic_count}")


if __name__ == "__main__":
    unittest.main()
