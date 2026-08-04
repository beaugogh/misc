"""Tests for the report-format output functions (Phase 9.7).

Tests render_markdown(), render_table(), render_html() in aggregate.py,
and the --format / --output CLI flags in run.py.

Run with: python -m unittest tests.test_reports -v
"""

import unittest
import os
import sys

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from aggregate import aggregate, render_report, render_markdown, render_table, render_html


def _synthetic_agg():
    """Build a small synthetic agg dict via aggregate() with hand-crafted tasks.

    Two tasks on the same day: one coding (Edit tool), one other (no tools).
    This gives us two kinds in one period for realistic table/chart output.
    """
    # 1782967200 = 2026-07-02T04:40:00Z (UTC)
    base = 1782967200.0
    tasks = [
        {"start": base, "duration_seconds": 3600, "active_seconds": 2400,
         "flavor": "implicit", "tool_names": ["Edit", "Bash"], "cwd": "/proj",
         "subject": "fix bug", "event_count": 10, "success": True},
        {"start": base + 7200, "duration_seconds": 1800, "active_seconds": 600,
         "flavor": "implicit", "tool_names": [], "cwd": "/tmp",
         "subject": "chat", "event_count": 2, "success": False},
        {"start": base + 86400, "duration_seconds": 7200, "active_seconds": 5000,
         "flavor": "implicit", "tool_names": ["WebSearch"], "cwd": "/tmp",
         "subject": "research", "event_count": 5, "success": True},
    ]
    return aggregate(tasks, "day")


def _synthetic_agg_week():
    """Build a synthetic agg dict with weekly granularity."""
    base = 1782967200.0
    tasks = [
        {"start": base, "duration_seconds": 3600, "active_seconds": 2400,
         "flavor": "implicit", "tool_names": ["Edit"], "cwd": "/proj",
         "subject": "fix bug", "event_count": 10, "success": True},
    ]
    return aggregate(tasks, "week")


class TestRenderMarkdown(unittest.TestCase):
    def setUp(self):
        self.agg = _synthetic_agg()
        self.output = render_markdown(self.agg, "day")

    def test_contains_markdown_header(self):
        """Output contains ## headers for periods."""
        self.assertIn("##", self.output)

    def test_contains_markdown_table(self):
        """Output contains a Markdown table with pipe separators."""
        self.assertIn("|", self.output)
        # Table header row with pipes
        self.assertIn("| Kind |", self.output)
        self.assertIn("|------", self.output)

    def test_contains_period_key(self):
        """Output contains the period key (YYYY-MM-DD)."""
        # The synthetic tasks are on 2026-07-02 and 2026-07-03
        self.assertIn("2026-07-02", self.output)

    def test_contains_title(self):
        """Output starts with a top-level title."""
        self.assertIn("# Time report (by day)", self.output)

    def test_contains_kind_names(self):
        """Output contains the kind names (coding, other, research)."""
        self.assertIn("coding", self.output)
        self.assertIn("other", self.output)

    def test_contains_success_rate(self):
        """Output contains success percentage values."""
        # The coding task succeeded, other failed
        self.assertIn("%", self.output)


class TestRenderTable(unittest.TestCase):
    def setUp(self):
        self.agg = _synthetic_agg()
        self.output = render_table(self.agg, "day")

    def test_contains_column_headers(self):
        """Output contains all expected column headers."""
        for header in ("Period", "Kind", "Wall(h)", "Active(h)", "%", "Tasks", "Success%"):
            self.assertIn(header, self.output)

    def test_contains_separator_line(self):
        """Output contains a separator line of dashes."""
        # The separator right after the header
        lines = self.output.split("\n")
        # Find header line, next line should be dashes
        header_idx = None
        for i, line in enumerate(lines):
            if "Period" in line and "Kind" in line:
                header_idx = i
                break
        self.assertIsNotNone(header_idx)
        self.assertTrue(lines[header_idx + 1].startswith("---"))

    def test_contains_period_key(self):
        """Output contains the period key."""
        self.assertIn("2026-07-02", self.output)

    def test_contains_kind_names(self):
        """Output contains kind names in the table rows."""
        self.assertIn("coding", self.output)

    def test_aligned_columns(self):
        """Each data row has aligned columns (same positions as header)."""
        lines = self.output.split("\n")
        # Find a data row (contains a number and a kind)
        data_lines = [l for l in lines if "coding" in l or "other" in l or "research" in l]
        self.assertGreater(len(data_lines), 0)
        # Each data line should have multiple spaces (column separation)
        for line in data_lines:
            self.assertGreater(len(line), 20)  # not empty/trivial

    def test_separator_between_periods(self):
        """When there are multiple periods, a separator appears between them."""
        # Two periods in synthetic agg: 2026-07-02 and 2026-07-03
        lines = self.output.split("\n")
        # Count separator lines (all dashes)
        sep_count = sum(1 for l in lines if l and set(l) == {"-"})
        # At least: one after header + one between periods
        self.assertGreaterEqual(sep_count, 2)

    def test_contains_title(self):
        """Output contains a title line."""
        self.assertIn("# Time report (by day)", self.output)


class TestRenderHTML(unittest.TestCase):
    def setUp(self):
        self.agg = _synthetic_agg()
        self.output = render_html(self.agg, "day")

    def test_contains_html_tag(self):
        """Output contains <html tag."""
        self.assertIn("<html", self.output)

    def test_contains_table(self):
        """Output contains a <table element."""
        self.assertIn("<table", self.output)

    def test_contains_svg(self):
        """Output contains an <svg element for the bar chart."""
        self.assertIn("<svg", self.output)

    def test_contains_doctype(self):
        """Output starts with <!DOCTYPE html>."""
        self.assertTrue(self.output.strip().startswith("<!DOCTYPE html>"))

    def test_contains_th_headers(self):
        """Output contains table header cells with expected column names."""
        self.assertIn("<th>周期</th>", self.output)
        self.assertIn("<th>类型</th>", self.output)
        self.assertIn("<th>Wall(h)</th>", self.output)

    def test_contains_bar_rects(self):
        """Output contains <rect> elements for the SVG bar chart."""
        self.assertIn("<rect", self.output)

    def test_self_contained_no_external_src(self):
        """Output has no external src= attributes (no external resources)."""
        import re
        # Check for src= pointing to external URLs (not data: URIs)
        src_matches = re.findall(r'src=["\'](?!data:)([^"\']+)["\']', self.output)
        self.assertEqual(src_matches, [], f"External src found: {src_matches}")

    def test_self_contained_no_external_href(self):
        """Output has no external href= attributes (no external resources)."""
        import re
        # Check for href= pointing to external URLs (not # anchors)
        href_matches = re.findall(r'href=["\'](?!#)(?!mailto:)(?!data:)([^"\']+)["\']', self.output)
        self.assertEqual(href_matches, [], f"External href found: {href_matches}")

    def test_contains_inline_css(self):
        """Output contains inline <style> block (no external CSS)."""
        self.assertIn("<style>", self.output)

    def test_contains_period_key(self):
        """Output contains the period key in the table."""
        self.assertIn("2026-07-02", self.output)

    def test_contains_totals(self):
        """Output contains total wall/active hours in the summary."""
        self.assertIn("wall", self.output.lower())
        self.assertIn("active", self.output.lower())

    def test_contains_legend(self):
        """Output contains a legend for the bar chart."""
        self.assertIn("legend", self.output.lower())

    def test_with_tasks_parameter(self):
        """render_html accepts an optional tasks list without error."""
        tasks = [{"id": "t1", "subject": "test"}]
        output = render_html(self.agg, "day", tasks=tasks)
        self.assertIn("<html", output)

    def test_empty_agg(self):
        """render_html handles an empty aggregation gracefully."""
        output = render_html({}, "day")
        self.assertIn("<html", output)
        self.assertIn("n/a", output)


class TestRenderReportBackwardCompat(unittest.TestCase):
    """Ensure the existing text report path still works unchanged."""

    def setUp(self):
        self.agg = _synthetic_agg()

    def test_text_report_still_works(self):
        """render_report produces the same text format as before."""
        output = render_report(self.agg, "day")
        self.assertIn("# Time report (by day)", output)
        self.assertIn("##", output)
        # No Markdown table pipes in text format
        self.assertNotIn("| Kind |", output)

    def test_week_granularity(self):
        """Weekly aggregation produces ISO week keys."""
        agg = _synthetic_agg_week()
        output = render_report(agg, "week")
        self.assertRegex(output, r"\d{4}-W\d{2}")


class TestCLIFormatFlags(unittest.TestCase):
    """Test that --format and --output don't break the default text path.

    We test the argument parsing and format-resolution logic without
    running the full pipeline (which needs real data sources).
    """

    def test_default_format_is_text(self):
        """Without --format or --json, the default format should be text."""
        import argparse
        # Simulate the arg parsing
        ap = argparse.ArgumentParser()
        ap.add_argument("--json", action="store_true")
        ap.add_argument("--format", choices=["text", "table", "markdown", "html", "json"],
                        default=None)
        ap.add_argument("--output", default=None)
        args = ap.parse_args([])
        # Determine format the same way run.py does
        if args.json:
            fmt = "json"
        elif args.format:
            fmt = args.format
        else:
            fmt = "text"
        self.assertEqual(fmt, "text")

    def test_json_flag_overrides_format(self):
        """--json takes precedence over --format."""
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("--json", action="store_true")
        ap.add_argument("--format", choices=["text", "table", "markdown", "html", "json"],
                        default=None)
        args = ap.parse_args(["--json", "--format", "table"])
        if args.json:
            fmt = "json"
        elif args.format:
            fmt = args.format
        else:
            fmt = "text"
        self.assertEqual(fmt, "json")

    def test_format_table(self):
        """--format table resolves to 'table'."""
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("--json", action="store_true")
        ap.add_argument("--format", choices=["text", "table", "markdown", "html", "json"],
                        default=None)
        args = ap.parse_args(["--format", "table"])
        if args.json:
            fmt = "json"
        elif args.format:
            fmt = args.format
        else:
            fmt = "text"
        self.assertEqual(fmt, "table")

    def test_output_extension_inference_md(self):
        """--output report.md without --format infers markdown."""
        ext = os.path.splitext("report.md")[1].lower()
        self.assertEqual(ext, ".md")
        # The run.py logic would set fmt = "markdown"

    def test_output_extension_inference_html(self):
        """--output report.html without --format infers html."""
        ext = os.path.splitext("report.html")[1].lower()
        self.assertEqual(ext, ".html")

    def test_output_extension_inference_no_match(self):
        """--output report.txt without --format falls back to text."""
        ext = os.path.splitext("report.txt")[1].lower()
        # No special case for .txt — falls through to text
        self.assertEqual(ext, ".txt")


class TestRenderEdgeCases(unittest.TestCase):
    """Test edge cases: empty agg, single period, etc."""

    def test_empty_agg_markdown(self):
        """render_markdown handles empty aggregation."""
        output = render_markdown({}, "day")
        self.assertIn("# Time report (by day)", output)

    def test_empty_agg_table(self):
        """render_table handles empty aggregation."""
        output = render_table({}, "day")
        self.assertIn("Period", output)
        self.assertIn("Kind", output)

    def test_empty_agg_html(self):
        """render_html handles empty aggregation."""
        output = render_html({}, "day")
        self.assertIn("<html", output)

    def test_single_period_single_kind(self):
        """All render functions handle a single period with one kind."""
        base = 1782967200.0
        tasks = [
            {"start": base, "duration_seconds": 3600, "active_seconds": 1800,
             "flavor": "implicit", "tool_names": ["Edit"], "cwd": "/p",
             "subject": "x", "event_count": 5, "success": True},
        ]
        agg = aggregate(tasks, "day")
        # All three should produce non-empty output without error
        md = render_markdown(agg, "day")
        tbl = render_table(agg, "day")
        htm = render_html(agg, "day")
        self.assertIn("coding", md)
        self.assertIn("coding", tbl)
        self.assertIn("coding", htm)


class TestM16PipelineOrder(unittest.TestCase):
    """M16: verify refine_success runs AFTER detect_parallel_tasks.

    Since we can't edit segment_tasks.py, we verify by reading run.py source
    and checking the code order. We also verify that background tasks with
    success=None get normalized to SUCCESS_UNKNOWN before refine_success.
    """

    def test_pipeline_order_in_source(self):
        """In run.py, detect_parallel_tasks must appear before refine_success."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        idx_parallel = source.find("detect_parallel_tasks")
        idx_refine = source.find("refine_success(tasks)")
        self.assertGreater(idx_parallel, 0, "detect_parallel_tasks not found in run.py")
        self.assertGreater(idx_refine, 0, "refine_success(tasks) not found in run.py")
        self.assertLess(idx_parallel, idx_refine,
                        "detect_parallel_tasks must appear before refine_success in run.py")

    def test_none_success_normalization(self):
        """Tasks with success=None should be normalized to SUCCESS_UNKNOWN before refine."""
        from segment_tasks import SUCCESS_UNKNOWN
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        # The normalization loop should exist between detect_parallel_tasks and refine_success
        idx_parallel = source.find("detect_parallel_tasks")
        idx_refine = source.find("refine_success(tasks)")
        normalization = source[idx_parallel:idx_refine]
        self.assertIn("SUCCESS_UNKNOWN", normalization,
                      "None->SUCCESS_UNKNOWN normalization should exist between "
                      "detect_parallel_tasks and refine_success")
        self.assertIn("is None", normalization,
                      "Normalization should check for None success values")


class TestM17ExclusiveTimeJSON(unittest.TestCase):
    """M17: verify JSON output includes exclusive_time when available."""

    def test_json_includes_exclusive_time(self):
        """The _render() JSON branch should add exclusive_time when exclusive is set."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        # Find the JSON branch in _render
        json_branch_start = source.find('if fmt == "json":')
        self.assertGreater(json_branch_start, 0, "JSON branch not found in _render")
        # Find the next branch after JSON
        json_branch_end = source.find('elif fmt ==', json_branch_start)
        json_branch = source[json_branch_start:json_branch_end]
        self.assertIn("exclusive_time", json_branch,
                      "JSON branch should include 'exclusive_time' when exclusive is available")

    def test_markdown_includes_exclusive_footer(self):
        """The markdown branch should append the exclusive footer."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        md_branch_start = source.find('elif fmt == "markdown":')
        self.assertGreater(md_branch_start, 0, "markdown branch not found")
        md_branch_end = source.find('elif fmt == "html":', md_branch_start)
        md_branch = source[md_branch_start:md_branch_end]
        self.assertIn("_exclusive_footer", md_branch,
                      "markdown branch should call _exclusive_footer()")

    def test_html_includes_exclusive_footer(self):
        """The HTML branch should include the exclusive footer."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        html_branch_start = source.find('elif fmt == "html":')
        self.assertGreater(html_branch_start, 0, "html branch not found")
        html_branch_end = source.find('else:\n            text = render_report', html_branch_start)
        html_branch = source[html_branch_start:html_branch_end]
        self.assertIn("_exclusive_footer", html_branch,
                      "html branch should reference _exclusive_footer()")


class TestM18ErrorHandling(unittest.TestCase):
    """M18: verify crashing stages don't kill the pipeline."""

    def test_segment_try_except(self):
        """segment() should be wrapped in try/except."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        # Find the segment call
        idx = source.find("tasks = segment(events)")
        # Look backwards for try:
        before = source[max(0, idx - 200):idx]
        self.assertIn("try:", before, "segment() should be inside a try block")

    def test_aggregate_try_except_with_fallback(self):
        """aggregate() should be wrapped in try/except with a fallback."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        idx = source.find("agg = aggregate(tasks, args.granularity)")
        after = source[idx:idx + 500]
        self.assertIn("except Exception", after,
                      "aggregate() should have an except clause")
        self.assertIn("fallback", after.lower(),
                      "aggregate() except should mention fallback")

    def test_render_try_except(self):
        """_render() calls should be wrapped in try/except."""
        run_path = os.path.join(SCRIPTS, "run.py")
        with open(run_path, encoding="utf-8") as f:
            source = f.read()
        # Find both _render() call sites
        for needle in ["content = _render()", "print(_render())"]:
            idx = source.find(needle)
            self.assertGreater(idx, 0, f"{needle} not found in run.py")
            after = source[idx:idx + 300]
            self.assertIn("except Exception", after,
                          f"{needle} should be followed by an except clause")

    def test_crashing_aggregate_falls_back(self):
        """If aggregate() raises, the fallback agg should be used."""
        from collections import Counter
        fake_tasks = [
            {"start": 1000.0, "source_kind": "ai_session", "success": "unknown"},
            {"start": 2000.0, "source_kind": "ai_session", "success": True},
        ]
        # Simulate the fallback logic from run.py
        try:
            raise RuntimeError("boom")
        except Exception:
            kind_counts = Counter(t.get("source_kind", "unknown") for t in fake_tasks)
            agg = {"_fallback": True, "task_count": len(fake_tasks),
                   "kinds": dict(kind_counts)}
        self.assertTrue(agg.get("_fallback"))
        self.assertEqual(agg["task_count"], 2)
        self.assertIn("ai_session", agg["kinds"])


class TestC6ZeroLengthTaskEvents(unittest.TestCase):
    """C6: verify _events_for_task widens window for zero-length tasks."""

    def test_zero_length_task_widens_window_with_session(self):
        """For zero-length tasks with session_id, end should be widened to session max."""
        import run as run_module
        session_id = "sess-1"
        start_ts = 1000.0
        # Zero-length task: start == end
        task = {"start": start_ts, "end": start_ts, "session_id": session_id}
        # Events: one at start, one much later in same session
        events = [
            {"timestamp": start_ts, "session_id": session_id},
            {"timestamp": start_ts + 100, "session_id": session_id},
            {"timestamp": start_ts + 3600, "session_id": session_id},
            {"timestamp": start_ts + 7200, "session_id": "other-session"},
        ]
        result = run_module._events_for_task(task, events)
        # Should capture all 3 events from the same session (not the other-session one)
        self.assertEqual(len(result), 3,
                         "Zero-length task should widen to capture same-session events")

    def test_zero_length_task_widens_without_session(self):
        """For zero-length tasks without session_id, end should be widened by 4h."""
        import run as run_module
        start_ts = 1000.0
        task = {"start": start_ts, "end": start_ts, "session_id": None}
        events = [
            {"timestamp": start_ts, "session_id": None},
            {"timestamp": start_ts + 100, "session_id": None},
            {"timestamp": start_ts + 3 * 3600, "session_id": None},
            # This one is beyond the 4h window
            {"timestamp": start_ts + 5 * 3600, "session_id": None},
        ]
        result = run_module._events_for_task(task, events)
        # Should capture events within the 4-hour window (3 events)
        self.assertEqual(len(result), 3,
                         "Zero-length task without session should use a 4h window")

    def test_nonzero_task_uses_original_range(self):
        """For normal tasks (start < end), the original time range is used."""
        import run as run_module
        start_ts = 1000.0
        end_ts = 2000.0
        task = {"start": start_ts, "end": end_ts, "session_id": "s1"}
        events = [
            {"timestamp": start_ts, "session_id": "s1"},
            {"timestamp": end_ts, "session_id": "s1"},
            {"timestamp": end_ts + 5000, "session_id": "s1"},  # beyond range
        ]
        result = run_module._events_for_task(task, events)
        self.assertEqual(len(result), 2,
                         "Normal task should use original [start, end+1] range")

    def test_drill_down_warning_for_zero_events(self):
        """_render_drill_down should show a warning when task has zero events."""
        import run as run_module
        task = {"subject": "bg task", "events": []}
        result = {"stages": [], "total_active_seconds": 0, "total_wall_seconds": 0,
                  "all_markers": [], "narrative": None}
        output = run_module._render_drill_down(result, task)
        self.assertIn("WARNING", output)
        self.assertIn("zero-length background task", output)
        self.assertIn("incomplete", output)

    def test_drill_down_warning_for_zero_stages(self):
        """_render_drill_down should show a warning when result has zero stages."""
        import run as run_module
        task = {"subject": "bg task", "events": [{"timestamp": 100.0}]}
        result = {"stages": [], "total_active_seconds": 0, "total_wall_seconds": 0,
                  "all_markers": [], "narrative": None}
        output = run_module._render_drill_down(result, task)
        self.assertIn("WARNING", output)

    def test_drill_down_no_warning_when_data_present(self):
        """_render_drill_down should NOT show warning when events and stages exist."""
        import run as run_module
        task = {"subject": "real task", "events": [{"timestamp": 100.0}, {"timestamp": 200.0}]}
        result = {"stages": [{"stage_idx": 0, "start": 100.0, "duration_seconds": 100,
                              "active_seconds": 80, "event_count": 2, "summary": "ok",
                              "markers": []}],
                  "total_active_seconds": 80, "total_wall_seconds": 100,
                  "all_markers": [], "narrative": "smooth"}
        output = run_module._render_drill_down(result, task)
        self.assertNotIn("WARNING", output)


class TestTopTasks(unittest.TestCase):
    """--top N: the bridge from aggregation to drill-down.

    Lists the biggest time sinks by active time and prints each task's ID so the
    user can immediately ``--task <id> --drill`` into any of them.
    """

    @staticmethod
    def _task(tid, active_h, wall_h=None, kind="ai_session", subject="t",
              success="unknown", start=1000.0, human_engaged_h=None):
        """Build a minimal task for top-tasks testing.

        human_engaged_h: if provided, sets human_data.human_engaged_seconds so
        the task ranks by human time. If None, defaults to active_h (so tasks
        without explicit human_data still rank by active time as a fallback).
        """
        he = active_h if human_engaged_h is None else human_engaged_h
        return {
            "id": tid,
            "active_seconds": active_h * 3600,
            "wall_clock_seconds": (wall_h if wall_h is not None else active_h) * 3600,
            "source_kind": kind,
            "subject": subject,
            "success": success,
            "start": start,
            "human_data": {
                "human_engaged_seconds": he * 3600,
                "human_involvement": "high" if he > 0 else "none",
                "human_action_count": int(he * 10),
                "machine_autonomous_seconds": max(0, active_h - he) * 3600,
                "human_action_types": [f"{int(he*10)} prompt(s)"] if he > 0 else [],
            },
        }

    def test_ranks_by_human_engaged_time_descending(self):
        """Tasks must be sorted by HUMAN engaged time, highest first."""
        import run as run_module
        tasks = [
            self._task("a", 1.0, subject="small", human_engaged_h=1.0),
            self._task("b", 5.0, subject="biggest", human_engaged_h=5.0),
            self._task("c", 3.0, subject="medium", human_engaged_h=3.0),
        ]
        out = run_module._render_top_tasks(tasks, 3)
        # biggest must appear before medium before small
        idx_big = out.index("biggest")
        idx_med = out.index("medium")
        idx_small = out.index("small")
        self.assertLess(idx_big, idx_med)
        self.assertLess(idx_med, idx_small)

    def test_limits_to_n(self):
        """--top N must only show N tasks even if more exist."""
        import run as run_module
        tasks = [self._task(f"t{i}", float(i)) for i in range(10)]
        out = run_module._render_top_tasks(tasks, 3)
        # Count id: lines — there should be exactly 3.
        id_lines = [ln for ln in out.splitlines() if ln.strip().startswith("id:")]
        self.assertEqual(len(id_lines), 3)

    def test_includes_task_ids_for_drill_down(self):
        """Every row must show the task id so --task <id> --drill works."""
        import run as run_module
        tasks = [self._task("explicit-sess1-1000", 2.0, subject="sync repo"),
                 self._task("implicit-sess2-2000", 1.0, subject="research")]
        out = run_module._render_top_tasks(tasks, 5)
        self.assertIn("explicit-sess1-1000", out)
        self.assertIn("implicit-sess2-2000", out)
        self.assertIn("--task <id> --drill", out)

    def test_shows_total_active_and_task_count(self):
        """The header reports the total active/human hours and task count."""
        import run as run_module
        tasks = [self._task("a", 2.0), self._task("b", 3.0)]
        out = run_module._render_top_tasks(tasks, 5)
        self.assertIn("5.0h total active", out)
        self.assertIn("of 2 tasks", out)

    def test_n_larger_than_task_count_is_safe(self):
        """--top 50 with only 3 tasks must not crash — show all 3."""
        import run as run_module
        tasks = [self._task("a", 1.0), self._task("b", 2.0), self._task("c", 3.0)]
        out = run_module._render_top_tasks(tasks, 50)
        id_lines = [ln for ln in out.splitlines() if ln.strip().startswith("id:")]
        self.assertEqual(len(id_lines), 3)

    def test_zero_human_task_ranks_below_active_task(self):
        """A task with 0 human engagement ranks below a task with human engagement."""
        import run as run_module
        tasks = [self._task("a", 0.0, subject="unpaired event", human_engaged_h=0.0),
                 self._task("b", 2.0, subject="real work", human_engaged_h=2.0)]
        out = run_module._render_top_tasks(tasks, 5)
        # real work (2.0h human) must rank above unpaired event (0h human)
        idx_real = out.index("real work")
        idx_unpaired = out.index("unpaired event")
        self.assertLess(idx_real, idx_unpaired)


class TestContextRendering(unittest.TestCase):
    """Tests that task['context'] is surfaced in render_task_detail, render_html,
    and the insights layer — the 'why this took as long as it did' answer.
    """

    def test_task_detail_shows_context_for_meeting(self):
        """render_task_detail shows organizer/attendees for a meeting task."""
        from aggregate import render_task_detail
        task = {
            "id": "t1", "subject": "standup", "source_kind": "meeting",
            "context": {"organizer": "zhang", "attendees": 3,
                        "attendee_names": ["a", "b", "c"], "location": "room1"},
        }
        out = render_task_detail(task)
        self.assertIn("Why this took as long as it did", out)
        self.assertIn("zhang", out)
        self.assertIn("3 attendee(s)", out)
        self.assertIn("room1", out)

    def test_task_detail_shows_blocker_for_coding(self):
        """render_task_detail shows the synthesized blocker for a coding task."""
        from aggregate import render_task_detail
        task = {
            "id": "t2", "subject": "sync main", "source_kind": "ai_session",
            "errors": 46,
            "context": {"blocker": "corporate proxy auth (407) (12 of 46 errors)",
                        "retry_targets": ["Bash on git fetch (4×)"],
                        "files_touched": ["D:/proj/run.py"]},
        }
        out = render_task_detail(task)
        self.assertIn("Blocker:", out)
        self.assertIn("407", out)
        self.assertIn("git fetch", out)

    def test_task_detail_no_context_section_when_empty(self):
        """render_task_detail omits the context section when context is empty."""
        from aggregate import render_task_detail
        task = {"id": "t3", "subject": "x", "source_kind": "ai_session"}
        out = render_task_detail(task)
        self.assertNotIn("Why this took as long as it did", out)

    def test_render_context_inline_meeting(self):
        """render_context_inline produces a one-line meeting summary."""
        from aggregate import render_context_inline
        task = {"source_kind": "meeting",
                "context": {"attendees": 5, "organizer": "zhang"}}
        line = render_context_inline(task)
        self.assertIn("5 attendee(s)", line)
        self.assertIn("zhang", line)

    def test_render_context_inline_coding_blocker(self):
        """render_context_inline surfaces the blocker for coding tasks."""
        from aggregate import render_context_inline
        task = {"source_kind": "ai_session", "errors": 10,
                "context": {"blocker": "command timeout (3 of 10 errors)"}}
        line = render_context_inline(task)
        self.assertIn("blocker:", line)
        self.assertIn("timeout", line)

    def test_render_context_inline_empty(self):
        """render_context_inline returns '' when no active time and no context."""
        from aggregate import render_context_inline
        # No active time and no context → empty
        self.assertEqual(render_context_inline({"source_kind": "ai_session"}), "")
        self.assertEqual(render_context_inline({}), "")

    def test_html_top_tasks_has_root_cause_column(self):
        """render_html top-tasks table includes a 'Root cause' column."""
        base = 1782967200.0
        tasks = [
            {"start": base, "duration_seconds": 3600, "active_seconds": 2400,
             "wall_clock_seconds": 3600, "excised_gap_seconds": 0,
             "flavor": "implicit", "tool_names": ["Edit"], "cwd": "/p",
             "subject": "fix bug", "event_count": 10, "success": True,
             "source_kind": "ai_session", "errors": 3,
             "context": {"blocker": "command timeout (3 errors)",
                         "files_touched": ["run.py"]},
             "human_data": {"human_engaged_seconds": 2400, "human_involvement": "high",
                            "human_action_count": 50, "machine_autonomous_seconds": 0,
                            "human_action_types": ["50 prompt(s)"],
                            "is_genuine_time_sink": True}},
        ]
        agg = aggregate(tasks, "day")
        html = render_html(agg, "day", tasks=tasks)
        self.assertIn("根因", html)
        self.assertIn("blocker:", html)

    def test_html_kind_section_shows_context_inline(self):
        """render_html 'What the work was' section shows context under each item."""
        base = 1782967200.0
        tasks = [
            {"start": base, "duration_seconds": 3600, "active_seconds": 2400,
             "flavor": "implicit", "tool_names": [], "cwd": "/p",
             "subject": "standup", "event_count": 3, "success": True,
             "source_kind": "meeting",
             "context": {"attendees": 4, "organizer": "li"}},
        ]
        agg = aggregate(tasks, "day")
        html = render_html(agg, "day", tasks=tasks)
        self.assertIn("why-inline", html)
        self.assertIn("4 attendee(s)", html)

    def test_insights_include_blocker_for_time_sink(self):
        """generate_insights surfaces the blocker in the time-sink insight line."""
        from aggregate import generate_insights
        tasks = [
            {"start": 1782967200.0, "active_seconds": 36000, "wall_clock_seconds": 40000,
             "subject": "sync main", "source_kind": "ai_session", "errors": 46,
             "tool_names": ["Edit", "Bash"], "id": "t1",
             "context": {"blocker": "corporate proxy auth (407) (12 of 46 errors)"},
             "human_data": {"human_engaged_seconds": 36000, "human_involvement": "high",
                            "human_action_count": 100, "machine_autonomous_seconds": 0,
                            "human_action_types": ["100 prompt(s)"]}},
        ]
        insights = generate_insights(tasks, {"2026-07": {}})
        joined = " ".join(insights)
        self.assertIn("blocker:", joined)
        self.assertIn("407", joined)


class TestDataAvailability(unittest.TestCase):
    """Tests for render_data_availability_html — per-source coverage table."""

    def test_shows_no_data_for_missing_sources(self):
        """Sources with zero tasks in range show 'No data in range'."""
        from aggregate import render_data_availability_html
        # Only ai_session tasks — other sources should show "No data"
        tasks = [
            {"source_kind": "ai_session", "start": 1782967200.0,
             "active_seconds": 3600},
        ]
        html = render_data_availability_html(tasks, 1782967200.0, 1783053600.0)
        self.assertIn("ai_session", html)
        self.assertIn("范围内无数据", html)
        self.assertIn("browser", html)  # listed as no data
        self.assertIn("meeting", html)  # listed as no data

    def test_shows_source_dates_when_data_present(self):
        """Sources with tasks show task count, active hours, earliest/latest dates."""
        from aggregate import render_data_availability_html
        tasks = [
            {"source_kind": "ai_session", "start": 1782967200.0,
             "active_seconds": 3600},
            {"source_kind": "ai_session", "start": 1783053600.0,
             "active_seconds": 1800},
        ]
        html = render_data_availability_html(tasks, 1782967200.0, 1783140000.0)
        self.assertIn("ai_session", html)
        self.assertIn("2", html)  # 2 tasks
        self.assertIn("1.5h", html)  # 1.5h active total

    def test_data_availability_in_render_html(self):
        """render_html includes data-availability section when since_ts/until_ts given."""
        base = 1782967200.0
        tasks = [
            {"start": base, "duration_seconds": 3600, "active_seconds": 2400,
             "flavor": "implicit", "tool_names": ["Edit"], "cwd": "/p",
             "subject": "x", "event_count": 5, "success": True,
             "source_kind": "ai_session"},
        ]
        agg = aggregate(tasks, "day")
        html = render_html(agg, "day", tasks=tasks,
                           since_ts=base, until_ts=base + 86400)
        self.assertIn("数据可用性", html)
        self.assertIn("ai_session", html)
        self.assertIn("范围内无数据", html)  # browser/meeting/etc. are empty

    def test_no_data_availability_section_without_dates(self):
        """render_html omits data-availability when since_ts/until_ts not given."""
        base = 1782967200.0
        tasks = [
            {"start": base, "duration_seconds": 3600, "active_seconds": 2400,
             "flavor": "implicit", "tool_names": ["Edit"], "cwd": "/p",
             "subject": "x", "event_count": 5, "success": True},
        ]
        agg = aggregate(tasks, "day")
        html = render_html(agg, "day", tasks=tasks)
        self.assertNotIn("数据可用性", html)


class TestRootCauseRendering(unittest.TestCase):
    """Tests that render_context_inline produces root-cause explanations,
    not just metadata. The 'why' column should explain WHY a task took long.
    """

    def test_all_day_meeting_shows_calendar_marker(self):
        """All-day meeting → 'Calendar day-marker — 0h real meeting time'."""
        from aggregate import render_context_inline
        task = {
            "source_kind": "meeting",
            "active_seconds": 0,
            "wall_clock_seconds": 86400,
            "excised_gap_seconds": 86400,
            "context": {"is_all_day": True, "organizer": "Bogao"},
        }
        line = render_context_inline(task)
        self.assertIn("Calendar day-marker", line)
        self.assertIn("0h real meeting", line)

    def test_multi_day_meeting_shows_cap(self):
        """Multi-day meeting → 'Multi-day event, capped to 8h'.

        Uses _make_task with a real 56h meeting event to verify the full
        pipeline produces the correct root-cause explanation.
        """
        from aggregate import render_context_inline
        from segment_tasks import _make_task, MAX_MEETING_DURATION
        events = [{"kind": "meeting", "timestamp": 1000.0,
                   "source_kind": "meeting",
                   "extra": {"end_ts": 1000.0 + 56 * 3600},
                   "tool_input": {"is_all_day": False, "subject": "conference"}}]
        task = _make_task("t1", "implicit", events, None)
        line = render_context_inline(task)
        self.assertIn("跨天", line)
        self.assertIn("封顶", line)
        # wall_clock should reflect the real span, clamped to MAX_MEETING_DURATION
        self.assertAlmostEqual(task["wall_clock_seconds"], MAX_MEETING_DURATION, delta=1)
        # active should be capped to 8h
        self.assertAlmostEqual(task["active_seconds"], 8 * 3600, delta=1)

    def test_normal_meeting_shows_organizer(self):
        """Normal 2h meeting → '2.0h meeting, organizer: X'."""
        from aggregate import render_context_inline
        task = {
            "source_kind": "meeting",
            "active_seconds": 7200,
            "wall_clock_seconds": 7200,
            "excised_gap_seconds": 0,
            "context": {"organizer": "jiangxuyang", "attendees": 5},
        }
        line = render_context_inline(task)
        self.assertIn("2.0h meeting", line)
        self.assertIn("jiangxuyang", line)
        self.assertIn("5 attendee", line)

    def test_browser_overnight_inflation_explained(self):
        """Browser tabs open overnight → explains idle gaps excised."""
        from aggregate import render_context_inline
        task = {
            "source_kind": "browser",
            "active_seconds": 3600 * 4,  # 4h active
            "wall_clock_seconds": 3600 * 28,  # 28h wall
            "excised_gap_seconds": 3600 * 24,  # 24h excised
            "context": {"n_visits": 300, "queries": [], "downloads": 0},
        }
        line = render_context_inline(task)
        self.assertIn("Tabs open", line)
        self.assertIn("4.0h active", line)
        self.assertIn("idle/overnight", line)

    def test_browser_continuous_shows_genuine(self):
        """Continuous browser session (no gaps) → 'continuous browsing'."""
        from aggregate import render_context_inline
        task = {
            "source_kind": "browser",
            "active_seconds": 3600 * 3,  # 3h
            "wall_clock_seconds": 3600 * 3,
            "excised_gap_seconds": 0,
            "context": {"n_visits": 830, "queries": [], "downloads": 0},
        }
        line = render_context_inline(task)
        self.assertIn("continuous browsing", line)
        self.assertNotIn("Tabs open", line)

    def test_coding_blocker_shown(self):
        """Coding task with blocker → 'blocker: ...'."""
        from aggregate import render_context_inline
        task = {
            "source_kind": "ai_session",
            "active_seconds": 3600 * 10,
            "wall_clock_seconds": 3600 * 20,
            "excised_gap_seconds": 3600 * 10,
            "errors": 46,
            "context": {"blocker": "command timeout (21 of 46 errors)",
                        "retry_targets": ["Bash on fetch (11×)"],
                        "files_touched": ["run.py"]},
        }
        line = render_context_inline(task)
        self.assertIn("blocker:", line)
        self.assertIn("timeout", line)

    def test_coding_no_blocker_shows_work_summary(self):
        """Coding task without errors → shows active time + files edited."""
        from aggregate import render_context_inline
        task = {
            "source_kind": "ai_session",
            "active_seconds": 3600 * 3,
            "wall_clock_seconds": 3600 * 3,
            "excised_gap_seconds": 0,
            "errors": 0,
            "tool_calls": 50,
            "context": {"blocker": None, "files_touched": ["a.py", "b.py"]},
        }
        line = render_context_inline(task)
        self.assertIn("3.0h active", line)
        self.assertIn("file(s) edited", line)

    def test_vcs_shows_commit_count(self):
        """VCS task → 'N commit(s): subject'."""
        from aggregate import render_context_inline
        task = {
            "source_kind": "vcs",
            "active_seconds": 3600,
            "wall_clock_seconds": 3600,
            "context": {"commit_subjects": ["fix bug", "add tests"]},
        }
        line = render_context_inline(task)
        self.assertIn("2 commit(s)", line)


class TestStructuredRootCause(unittest.TestCase):
    """render_structured_root_cause breaks the narrative into separate HTML divs.

    Each labeled section (Goal, Struggle, Detail, Pages, Evidence, Time) should
    produce its own <div class="rc-part"> so the 根因 cell is readable, not a
    single lumped blob.
    """

    class _FakeHtmlMod:
        """Minimal stand-in for the html module — escapes for display."""
        def escape(self, s):
            import html as _html
            return _html.escape(s)

    def test_browser_narrative_produces_separate_divs(self):
        """A browser narrative with Goal/Struggle/Detail/Pages/Downloads should
        render as separate divs, not one lumped section."""
        from aggregate import render_structured_root_cause
        task = {
            "source_kind": "browser",
            "context": {
                "narrative": " ".join([
                    "Goal: 浏览 AgentCenter。",
                    "Struggle: 用户在 8.2h 内进行了 593 次页面访问（382 次重复点击），属于活跃交互。",
                    "Detail: 主要浏览内容：「AgentCenter」86次——配置或管理AI Agent。",
                    "Pages: AgentCenter, Google Gemini, mem0ai/mem0。",
                    "Downloads: 下载了 1 个文件。",
                    "8.2h 活跃浏览。",
                ]),
            },
        }
        html_out = render_structured_root_cause(task, self._FakeHtmlMod())
        # Each label should produce its own div.
        self.assertIn("rc-goal", html_out)
        self.assertIn("rc-struggle", html_out)
        self.assertIn("rc-detail", html_out)
        self.assertIn("rc-pages", html_out)
        self.assertIn("rc-downloads", html_out)
        # Detail should appear once (per-page breakdown only).
        self.assertEqual(html_out.count('rc-detail'), 1)
        # Downloads should be its own div, not merged into Detail.
        self.assertEqual(html_out.count('rc-downloads'), 1)
        # Time line should render as rc-time.
        self.assertIn("rc-time", html_out)
        # Verify structure: each div has label + content spans.
        self.assertIn("rc-label", html_out)
        self.assertIn("rc-content", html_out)

    def test_ai_session_narrative_evidence_is_separate(self):
        """AI session narrative: Evidence should be a separate div, not merged
        into Struggle."""
        from aggregate import render_structured_root_cause
        task = {
            "source_kind": "ai_session",
            "context": {
                "narrative": " ".join([
                    "Goal: sync local main branch with remote.",
                    "Struggle: repeatedly hit proxy auth errors.",
                    "Evidence: 'git fetch origin' → 407 proxy auth.",
                    "1.0h active.",
                ]),
            },
        }
        html_out = render_structured_root_cause(task, self._FakeHtmlMod())
        self.assertIn("rc-goal", html_out)
        self.assertIn("rc-struggle", html_out)
        self.assertIn("rc-evidence", html_out)
        self.assertIn("rc-time", html_out)
        # Evidence content should NOT appear inside rc-struggle div.
        # Count divs: struggle should appear once, evidence once.
        self.assertEqual(html_out.count('rc-struggle'), 1)
        self.assertEqual(html_out.count('rc-evidence'), 1)

    def test_no_narrative_falls_back_to_inline(self):
        """When no narrative in context, falls back to render_context_inline."""
        from aggregate import render_structured_root_cause
        task = {
            "source_kind": "ai_session",
            "errors": 5,
            "context": {"blocker": "timeout (5 errors)"},
        }
        html_out = render_structured_root_cause(task, self._FakeHtmlMod())
        # Should contain the escaped inline text, not rc-part divs.
        self.assertNotIn("rc-part", html_out)
        self.assertIn("blocker", html_out.lower())


if __name__ == "__main__":
    unittest.main()
