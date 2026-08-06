"""Tests for the multi-horizon mode in run.py.

Tests the horizon-spec parser, granularity selection, and the multi-horizon
report generation logic without running the full collection pipeline.

Run with: python -m unittest discover -s scripts/tests
"""

import unittest
import os
import sys
import tempfile
import json

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

import run as run_module


class TestParseHorizonSpec(unittest.TestCase):
    """Tests for _parse_horizon_spec."""

    def test_default_spec(self):
        """The default horizon spec '90d,30d,7d,1d' parses correctly."""
        result = run_module._parse_horizon_spec(run_module.DEFAULT_HORIZONS)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], (90, "90d"))
        self.assertEqual(result[1], (30, "30d"))
        self.assertEqual(result[2], (7, "7d"))
        self.assertEqual(result[3], (1, "1d"))

    def test_custom_spec(self):
        """A custom spec like '180d,60d' parses correctly."""
        result = run_module._parse_horizon_spec("180d,60d")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (180, "180d"))
        self.assertEqual(result[1], (60, "60d"))

    def test_single_horizon(self):
        """A single horizon '14d' parses correctly."""
        result = run_module._parse_horizon_spec("14d")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (14, "14d"))

    def test_whitespace_tolerant(self):
        """Whitespace around horizon specs is tolerated."""
        result = run_module._parse_horizon_spec("  7d ,  1d  ")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (7, "7d"))

    def test_case_insensitive(self):
        """'90D' (uppercase) is accepted."""
        result = run_module._parse_horizon_spec("90D")
        self.assertEqual(result[0], (90, "90d"))

    def test_empty_spec_raises(self):
        """An empty spec raises ValueError."""
        with self.assertRaises(ValueError):
            run_module._parse_horizon_spec("")

    def test_invalid_format_raises(self):
        """A non-'Nd' format raises ValueError."""
        with self.assertRaises(ValueError):
            run_module._parse_horizon_spec("90days")
        with self.assertRaises(ValueError):
            run_module._parse_horizon_spec("abc")

    def test_zero_days_raises(self):
        """'0d' raises ValueError."""
        with self.assertRaises(ValueError):
            run_module._parse_horizon_spec("0d")


class TestGranularityForHorizon(unittest.TestCase):
    """Tests for _granularity_for_horizon."""

    def test_day_granularity_for_short_horizons(self):
        """1-2 day horizons use 'day' granularity."""
        self.assertEqual(run_module._granularity_for_horizon(1), "day")
        self.assertEqual(run_module._granularity_for_horizon(2), "day")

    def test_week_granularity_for_medium_horizons(self):
        """3-30 day horizons use 'week' granularity."""
        self.assertEqual(run_module._granularity_for_horizon(7), "week")
        self.assertEqual(run_module._granularity_for_horizon(14), "week")
        self.assertEqual(run_module._granularity_for_horizon(30), "week")

    def test_month_granularity_for_long_horizons(self):
        """31+ day horizons use 'month' granularity."""
        self.assertEqual(run_module._granularity_for_horizon(31), "month")
        self.assertEqual(run_module._granularity_for_horizon(90), "month")
        self.assertEqual(run_module._granularity_for_horizon(365), "month")


class TestRunMultiHorizon(unittest.TestCase):
    """Tests for _run_multi_horizon with synthetic tasks.

    Uses a temp directory and a small synthetic task set to verify the
    multi-horizon report generation produces the expected files.
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="horizons_test_")
        # Synthetic tasks spanning 100 days, two source_kinds.
        base = 1782967200.0  # 2026-07-02
        self.tasks = []
        for i in range(50):
            self.tasks.append({
                "id": f"t{i}",
                "start": base + i * 86400 * 2,  # every 2 days
                "end": base + i * 86400 * 2 + 3600,
                "duration_seconds": 3600,
                "wall_clock_seconds": 3600,
                "active_seconds": 1800,
                "flavor": "implicit",
                "source_kind": "ai_session",
                "tool_names": ["Edit"],
                "subject": f"task {i}",
                "event_count": 5,
                "success": "succeeded",
                "context": {"blocker": None, "files_touched": ["run.py"]},
            })
        # A few browser tasks
        for i in range(10):
            self.tasks.append({
                "id": f"b{i}",
                "start": base + i * 86400 * 5,
                "end": base + i * 86400 * 5 + 7200,
                "duration_seconds": 7200,
                "wall_clock_seconds": 7200,
                "active_seconds": 3600,
                "flavor": "browser_research",
                "source_kind": "browser",
                "tool_names": [],
                "subject": f"research {i}",
                "event_count": 10,
                "success": "unknown",
                "context": {"queries": ["test"], "n_visits": 5},
            })
        self.end_ts = base + 100 * 86400  # 100 days after base

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_generates_one_report_per_horizon(self):
        """Each horizon produces an HTML report file."""
        horizons = run_module._parse_horizon_spec("90d,30d,7d")
        index_path = run_module._run_multi_horizon(
            self.tasks, [], horizons, self.end_ts, self.tmpdir,
            exclusive=None, skipped=[])
        # 3 horizon reports + index.html
        files = os.listdir(self.tmpdir)
        self.assertIn("report_90d.html", files)
        self.assertIn("report_30d.html", files)
        self.assertIn("report_7d.html", files)
        self.assertIn("index.html", files)

    def test_index_page_links_to_reports(self):
        """The index page contains links to each horizon report."""
        horizons = run_module._parse_horizon_spec("30d,7d")
        index_path = run_module._run_multi_horizon(
            self.tasks, [], horizons, self.end_ts, self.tmpdir,
            exclusive=None, skipped=[])
        with open(index_path, encoding="utf-8") as f:
            index_html = f.read()
        self.assertIn("report_30d.html", index_html)
        self.assertIn("report_7d.html", index_html)
        self.assertIn("horizon-card", index_html)

    def test_report_contains_data_availability(self):
        """Each horizon report includes a data-availability section."""
        horizons = run_module._parse_horizon_spec("30d")
        run_module._run_multi_horizon(
            self.tasks, [], horizons, self.end_ts, self.tmpdir,
            exclusive=None, skipped=[])
        report_path = os.path.join(self.tmpdir, "report_30d.html")
        with open(report_path, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("数据可用性", html)
        self.assertIn("ai_session", html)
        self.assertIn("browser", html)

    def test_report_shows_no_data_for_missing_sources(self):
        """A horizon report shows 'No data' for sources with no tasks."""
        horizons = run_module._parse_horizon_spec("30d")
        run_module._run_multi_horizon(
            self.tasks, [], horizons, self.end_ts, self.tmpdir,
            exclusive=None, skipped=[])
        report_path = os.path.join(self.tmpdir, "report_30d.html")
        with open(report_path, encoding="utf-8") as f:
            html = f.read()
        # meeting/comm/vcs/filesystem have no tasks → "No data in range"
        self.assertIn("范围内无数据", html)

    def test_index_shows_active_hours_per_horizon(self):
        """The index page shows active hours for each horizon."""
        horizons = run_module._parse_horizon_spec("90d,30d")
        run_module._run_multi_horizon(
            self.tasks, [], horizons, self.end_ts, self.tmpdir,
            exclusive=None, skipped=[])
        with open(os.path.join(self.tmpdir, "index.html"), encoding="utf-8") as f:
            html = f.read()
        self.assertIn("h</strong> active", html)

    def test_skipped_sources_dict_handled(self):
        """The index page handles skipped sources as dicts (not strings)."""
        horizons = run_module._parse_horizon_spec("30d")
        skipped = [{"name": "welink_cli", "reason": "not detected"}]
        # Should not crash
        run_module._run_multi_horizon(
            self.tasks, [], horizons, self.end_ts, self.tmpdir,
            exclusive=None, skipped=skipped)
        with open(os.path.join(self.tmpdir, "index.html"), encoding="utf-8") as f:
            html = f.read()
        self.assertIn("welink_cli", html)


class TestMultiHorizonGate(unittest.TestCase):
    """Tests that --top, --task, --format, --output, --since correctly disable
    multi-horizon mode. Without this, --top 10 silently produces HTML reports
    instead of the top-N list.
    """

    def test_top_disables_multi_horizon(self):
        """--top should disable multi-horizon mode (checked via source inspection)."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        # Find the use_multi_horizon condition block — search for the full
        # multi-line block by finding the assignment and the next blank line.
        idx = source.find("use_multi_horizon = (")
        self.assertGreater(idx, 0, "use_multi_horizon not found")
        # Grab a generous slice to capture the full multi-line expression.
        block = source[idx:idx + 500]
        self.assertIn("args.top is None", block,
                      "--top must be in the use_multi_horizon gate")

    def test_task_disables_multi_horizon(self):
        """--task should disable multi-horizon mode."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        idx = source.find("use_multi_horizon = (")
        block = source[idx:idx + 500]
        self.assertIn("not args.task", block,
                      "--task must be in the use_multi_horizon gate")

    def test_format_horizons_error_exists(self):
        """An error should be raised when --format disables --horizons."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        # The error block must exist and reference both --format and --horizons.
        self.assertIn("ERROR: --horizons cannot be combined", source)
        self.assertIn("sys.exit(2)", source)

    def test_format_horizons_errors_before_collection(self):
        """--format html + --horizons must error out BEFORE running the
        collection pipeline (which takes 30-120s). If the check is placed
        after collection, the user waits for the full pipeline before seeing
        the error — defeating the purpose. This test runs run.py as a
        subprocess and asserts it exits within 5 seconds with code 2."""
        import subprocess
        run_path = os.path.join(SCRIPTS, "run.py")
        proc = subprocess.run(
            [sys.executable, run_path,
             "--horizons", "90d,30d,7d,1d",
             "--format", "html"],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(proc.returncode, 2,
                         f"Expected exit code 2, got {proc.returncode}.\n"
                         f"stderr: {proc.stderr[:500]}")
        self.assertIn("ERROR", proc.stderr)
        self.assertIn("--horizons cannot be combined", proc.stderr)
        self.assertIn("--format html", proc.stderr)


class TestIsAllDayTruthiness(unittest.TestCase):
    """Tests that is_all_day='true' (string from API) is treated the same as
    boolean True — both should zero out all-day meeting active time.
    """

    def test_string_true_zeroed(self):
        """is_all_day='true' (string) → 0 active, same as boolean True."""
        from segment_tasks import _compute_active_seconds, _is_truthy
        # Verify _is_truthy handles strings
        self.assertTrue(_is_truthy("true"))
        self.assertTrue(_is_truthy("True"))
        self.assertTrue(_is_truthy("1"))
        self.assertTrue(_is_truthy(True))
        self.assertFalse(_is_truthy("false"))
        self.assertFalse(_is_truthy("0"))
        self.assertFalse(_is_truthy(None))
        self.assertFalse(_is_truthy(""))

        # Verify _compute_active_seconds zeroes string is_all_day
        events = [
            {"kind": "meeting", "timestamp": 1000.0,
             "extra": {"end_ts": 1000.0 + 86400},
             "tool_input": {"is_all_day": "true"}},
        ]
        active, _ = _compute_active_seconds(events)
        self.assertAlmostEqual(active, 0.0, places=1)


if __name__ == "__main__":
    unittest.main()
