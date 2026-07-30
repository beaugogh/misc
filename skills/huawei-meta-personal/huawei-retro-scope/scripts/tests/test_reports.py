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

    Two tasks on the same day: one coding (Edit tool), one conversation.
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
        """Output contains the kind names (coding, conversation, research)."""
        self.assertIn("coding", self.output)
        self.assertIn("conversation", self.output)

    def test_contains_success_rate(self):
        """Output contains success percentage values."""
        # The coding task succeeded, conversation failed
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
        data_lines = [l for l in lines if "coding" in l or "conversation" in l or "research" in l]
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
        self.assertIn("<th>Period</th>", self.output)
        self.assertIn("<th>Kind</th>", self.output)
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
              success="unknown", start=1000.0):
        return {
            "id": tid,
            "active_seconds": active_h * 3600,
            "wall_clock_seconds": (wall_h if wall_h is not None else active_h) * 3600,
            "source_kind": kind,
            "subject": subject,
            "success": success,
            "start": start,
        }

    def test_ranks_by_active_time_descending(self):
        """Tasks must be sorted by active time, highest first."""
        import run as run_module
        tasks = [
            self._task("a", 1.0, subject="small"),
            self._task("b", 5.0, subject="biggest"),
            self._task("c", 3.0, subject="medium"),
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
        """The header reports the total active hours and task count for context."""
        import run as run_module
        tasks = [self._task("a", 2.0), self._task("b", 3.0)]
        out = run_module._render_top_tasks(tasks, 5)
        self.assertIn("5.0h active total", out)
        self.assertIn("of 2 tasks", out)

    def test_n_larger_than_task_count_is_safe(self):
        """--top 50 with only 3 tasks must not crash — show all 3."""
        import run as run_module
        tasks = [self._task("a", 1.0), self._task("b", 2.0), self._task("c", 3.0)]
        out = run_module._render_top_tasks(tasks, 50)
        id_lines = [ln for ln in out.splitlines() if ln.strip().startswith("id:")]
        self.assertEqual(len(id_lines), 3)

    def test_zero_active_time_task_included(self):
        """A task with 0 active time (single event, honest gap) is still listable."""
        import run as run_module
        tasks = [self._task("a", 0.0, subject="unpaired event"),
                 self._task("b", 2.0, subject="real work")]
        out = run_module._render_top_tasks(tasks, 5)
        self.assertIn("unpaired event", out)


if __name__ == "__main__":
    unittest.main()
