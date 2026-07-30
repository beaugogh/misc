"""Aggregation layer.

Consumes task objects (from segment_tasks.segment) and produces time/effort
distribution reports by day / week / month, broken down by task kind.

For the MVP, task "kind" is a crude classification derived from the dominant tool
names and cwd. This is the placeholder for the deeper categorization work
(domain detection from file paths, LLM labeling, etc.) — see SKILL.md open
questions.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone


def classify_task(task: dict) -> str:
    """Crude task-kind classifier for the MVP.

    This will be replaced by the deeper categorization (domain detection, LLM
    labeling, RIPPER rules) — see SKILL.md. For now, a few rules on tool names,
    source_kind, and cwd give a usable first cut.
    """
    tools = set(task.get("tool_names") or [])
    cwd = (task.get("cwd") or "").lower()
    subject = (task.get("subject") or "").lower()
    source_kind = task.get("source_kind", "")

    # Browser-sourced tasks: visits/downloads/searches
    if source_kind == "browser":
        # if the task has search events, it's research; otherwise browsing
        return "research"

    # VCS-sourced tasks (git commits/checkouts without an AI session)
    if source_kind == "vcs":
        return "vcs"

    # Meeting-sourced tasks (welink-cli meetings, calendar events, .ics, recordings)
    if source_kind == "meeting":
        return "meeting"

    # Communication-sourced tasks (welink-cli mail, IM)
    if source_kind == "comm":
        return "communication"

    if any(t in tools for t in ("TaskCreate", "TaskUpdate", "ExitPlanMode", "EnterPlanMode")):
        pass
    if "Bash" in tools and any(k in cwd for k in ("workspace", "repo", "project")):
        return "coding"
    if tools & {"Edit", "Write", "Read"}:
        return "coding"
    if tools & {"WebSearch", "WebFetch"}:
        return "research"
    if any(k in subject for k in ("commit", "push", "rebase", "merge")):
        return "vcs"
    if not tools and task.get("event_count", 0) <= 3:
        return "conversation"
    return "other"


def _period_key(ts: float, granularity: str) -> str:
    """Return a period key for grouping. granularity: 'day' | 'week' | 'month'."""
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    if granularity == "day":
        return dt.strftime("%Y-%m-%d")
    if granularity == "week":
        # ISO week
        iso = dt.isocalendar()
        return f"{iso[0]}-W{iso[1]:02d}"
    if granularity == "month":
        return dt.strftime("%Y-%m")
    raise ValueError(f"unknown granularity: {granularity}")


def aggregate(tasks: list[dict], granularity: str = "day") -> dict:
    """Aggregate tasks by period and kind. Returns a nested dict.

    Structure:
        {
          "<period_key>": {
            "total_seconds": float,
            "active_seconds": float,
            "task_count": int,
            "success_count": int,
            "failure_count": int,
            "unknown_count": int,
            "by_kind": { "<kind>": {"seconds": float, "active_seconds": float, "count": int,
                                     "successes": int, "failures": int, "unknowns": int}, ... }
          },
          ...
        }
    """
    out: dict[str, dict] = {}
    for t in tasks:
        start = t.get("start") or 0.0
        if not start:
            continue
        kind = classify_task(t)
        dur = t.get("duration_seconds") or t.get("wall_clock_seconds") or 0.0
        active = t.get("active_seconds") or 0.0
        success = t.get("success")
        # A "gap" is a task with 0 active time — a single event (or burst at one
        # timestamp) that couldn't be paired into a measurable duration. We know
        # it happened but not how long it took. Surface these so the report
        # doesn't silently swallow activity it can't duration-ize.
        is_gap = active <= 0.0
        key = _period_key(start, granularity)
        if key not in out:
            out[key] = {"total_seconds": 0.0, "active_seconds": 0.0,
                        "excised_gap_seconds": 0.0,
                        "task_count": 0, "success_count": 0, "failure_count": 0,
                        "unknown_count": 0, "gap_count": 0, "by_kind": {}}
        out[key]["total_seconds"] += dur
        out[key]["active_seconds"] += active
        out[key]["excised_gap_seconds"] += t.get("excised_gap_seconds") or 0.0
        out[key]["task_count"] += 1
        if is_gap:
            out[key]["gap_count"] += 1
        if success == "succeeded":
            out[key]["success_count"] += 1
        elif success == "failed":
            out[key]["failure_count"] += 1
        else:
            out[key]["unknown_count"] += 1
        bk = out[key]["by_kind"]
        if kind not in bk:
            bk[kind] = {"seconds": 0.0, "active_seconds": 0.0,
                        "excised_gap_seconds": 0.0,
                        "count": 0,
                        "successes": 0, "failures": 0, "unknowns": 0, "gaps": 0}
        bk[kind]["seconds"] += dur
        bk[kind]["active_seconds"] += active
        bk[kind]["excised_gap_seconds"] += t.get("excised_gap_seconds") or 0.0
        bk[kind]["count"] += 1
        if is_gap:
            bk[kind]["gaps"] += 1
        if success == "succeeded":
            bk[kind]["successes"] += 1
        elif success == "failed":
            bk[kind]["failures"] += 1
        else:
            bk[kind]["unknowns"] += 1
    return out


def render_report(agg: dict, granularity: str) -> str:
    """Render an aggregation as a human-readable text report."""
    lines = [f"# Time report (by {granularity})\n"]
    for period in sorted(agg.keys()):
        row = agg[period]
        total_h = row["total_seconds"] / 3600
        active_h = row.get("active_seconds", 0.0) / 3600
        sc = row.get("success_count", 0)
        fc = row.get("failure_count", 0)
        uc = row.get("unknown_count", 0)
        gc = row.get("gap_count", 0)
        known = sc + fc
        sr = (sc / known * 100) if known else 0
        up = (uc / row["task_count"] * 100) if row["task_count"] else 0
        gap_str = f", {gc} gaps" if gc else ""
        if known:
            lines.append(f"## {period}  -  {total_h:.1f}h wall / {active_h:.1f}h active, "
                         f"{row['task_count']} tasks{gap_str}, {sr:.0f}% success, {up:.0f}% unknown")
        else:
            lines.append(f"## {period}  -  {total_h:.1f}h wall / {active_h:.1f}h active, "
                         f"{row['task_count']} tasks{gap_str}, success: n/a (all unknown)")
        kinds = sorted(row["by_kind"].items(), key=lambda kv: -kv[1]["seconds"])
        for kind, stats in kinds:
            h = stats["seconds"] / 3600
            ah = stats.get("active_seconds", 0.0) / 3600
            pct = (stats["seconds"] / row["total_seconds"] * 100) if row["total_seconds"] else 0
            ksc = stats.get("successes", 0)
            kfc = stats.get("failures", 0)
            kuc = stats.get("unknowns", 0)
            kgaps = stats.get("gaps", 0)
            k_excised = stats.get("excised_gap_seconds", 0.0) / 3600
            k_known = ksc + kfc
            ksr = (ksc / k_known * 100) if k_known else 0
            kup = (kuc / stats["count"] * 100) if stats["count"] else 0
            kgap_str = f", {kgaps} gaps" if kgaps else ""
            kexcised_str = f" ({k_excised:.1f}h excised)" if k_excised > 0.01 else ""
            if k_known:
                lines.append(f"  - {kind:12s} {h:5.1f}h wall / {ah:4.1f}h active{kexcised_str}  "
                             f"({pct:4.1f}%, {stats['count']} tasks{kgap_str}, {ksr:.0f}% success, {kup:.0f}% unknown)")
            else:
                lines.append(f"  - {kind:12s} {h:5.1f}h wall / {ah:4.1f}h active{kexcised_str}  "
                             f"({pct:4.1f}%, {stats['count']} tasks{kgap_str}, success: n/a (all unknown))")
        lines.append("")
    return "\n".join(lines)


def _period_summary(row: dict) -> str:
    """One-line summary string for a period (used by text + markdown)."""
    total_h = row["total_seconds"] / 3600
    active_h = row.get("active_seconds", 0.0) / 3600
    sc = row.get("success_count", 0)
    fc = row.get("failure_count", 0)
    uc = row.get("unknown_count", 0)
    known = sc + fc
    sr = (sc / known * 100) if known else 0
    up = (uc / row["task_count"] * 100) if row["task_count"] else 0
    if known:
        return (f"{total_h:.1f}h wall / {active_h:.1f}h active, "
                f"{row['task_count']} tasks, {sr:.0f}% success, {up:.0f}% unknown")
    return (f"{total_h:.1f}h wall / {active_h:.1f}h active, "
            f"{row['task_count']} tasks, success: n/a (all unknown)")


def render_markdown(agg: dict, granularity: str) -> str:
    """Render an aggregation as a Markdown document.

    Mirrors the structure of render_report() but as proper Markdown:
    ``##`` headers for periods, Markdown tables for the per-kind breakdown,
    and a summary line per period.
    """
    lines = [f"# Time report (by {granularity})\n"]
    for period in sorted(agg.keys()):
        row = agg[period]
        lines.append(f"## {period}")
        lines.append(f"_{_period_summary(row)}_\n")
        # Table header
        lines.append("| Kind | Wall(h) | Active(h) | % | Tasks | Success% | Unknown% |")
        lines.append("|------|---------|-----------|---|-------|----------|----------|")
        kinds = sorted(row["by_kind"].items(), key=lambda kv: -kv[1]["seconds"])
        for kind, stats in kinds:
            h = stats["seconds"] / 3600
            ah = stats.get("active_seconds", 0.0) / 3600
            pct = (stats["seconds"] / row["total_seconds"] * 100) if row["total_seconds"] else 0
            ksc = stats.get("successes", 0)
            kfc = stats.get("failures", 0)
            kuc = stats.get("unknowns", 0)
            k_known = ksc + kfc
            ksr = (ksc / k_known * 100) if k_known else 0
            kup = (kuc / stats["count"] * 100) if stats["count"] else 0
            sr_str = f"{ksr:.0f}%" if k_known else "n/a"
            lines.append(f"| {kind} | {h:.1f} | {ah:.1f} | {pct:.1f} | {stats['count']} | {sr_str} | {kup:.0f}% |")
        lines.append("")
    return "\n".join(lines)


def render_table(agg: dict, granularity: str) -> str:
    """Render an aggregation as a fixed-width ASCII table (stdlib only).

    Columns: Period, Kind, Wall(h), Active(h), %, Tasks, Success%, Unknown%.
    One row per kind per period, with a separator between periods.
    """
    # Column widths
    w_period = 12
    w_kind = 14
    w_wall = 8
    w_active = 9
    w_pct = 7
    w_tasks = 6
    w_sr = 10
    w_unk = 9

    header = (f"{'Period':<{w_period}}  "
              f"{'Kind':<{w_kind}}  "
              f"{'Wall(h)':>{w_wall}}  "
              f"{'Active(h)':>{w_active}}  "
              f"{'%':>{w_pct}}  "
              f"{'Tasks':>{w_tasks}}  "
              f"{'Success%':>{w_sr}}  "
              f"{'Unknown%':>{w_unk}}")
    sep = "-" * len(header)
    lines = [f"# Time report (by {granularity})", "", header, sep]

    for i, period in enumerate(sorted(agg.keys())):
        if i > 0:
            lines.append(sep)
        row = agg[period]
        kinds = sorted(row["by_kind"].items(), key=lambda kv: -kv[1]["seconds"])
        for j, (kind, stats) in enumerate(kinds):
            h = stats["seconds"] / 3600
            ah = stats.get("active_seconds", 0.0) / 3600
            pct = (stats["seconds"] / row["total_seconds"] * 100) if row["total_seconds"] else 0
            ksc = stats.get("successes", 0)
            kfc = stats.get("failures", 0)
            kuc = stats.get("unknowns", 0)
            k_known = ksc + kfc
            ksr = (ksc / k_known * 100) if k_known else 0
            kup = (kuc / stats["count"] * 100) if stats["count"] else 0
            sr_str = f"{ksr:.0f}%" if k_known else "n/a"
            period_label = period if j == 0 else ""
            lines.append(
                f"{period_label:<{w_period}}  "
                f"{kind:<{w_kind}}  "
                f"{h:>{w_wall}.1f}  "
                f"{ah:>{w_active}.1f}  "
                f"{pct:>{w_pct}.1f}  "
                f"{stats['count']:>{w_tasks}}  "
                f"{sr_str:>{w_sr}}  "
                f"{kup:>{w_unk:.0f}}%"
            )
    lines.append("")
    return "\n".join(lines)


def render_html(agg: dict, granularity: str, tasks: list[dict] | None = None) -> str:
    """Render an aggregation as a self-contained HTML file.

    Single file with inline CSS, no external resources, no JS dependencies.
    Includes a header, summary table, and a simple bar chart via inline SVG.
    """
    import html as html_mod

    periods = sorted(agg.keys())
    total_wall = sum(r["total_seconds"] for r in agg.values()) / 3600
    total_active = sum(r.get("active_seconds", 0.0) for r in agg.values()) / 3600
    total_tasks = sum(r["task_count"] for r in agg.values())

    # Build table rows
    table_rows = []
    for period in periods:
        row = agg[period]
        kinds = sorted(row["by_kind"].items(), key=lambda kv: -kv[1]["seconds"])
        for j, (kind, stats) in enumerate(kinds):
            h = stats["seconds"] / 3600
            ah = stats.get("active_seconds", 0.0) / 3600
            pct = (stats["seconds"] / row["total_seconds"] * 100) if row["total_seconds"] else 0
            ksc = stats.get("successes", 0)
            kfc = stats.get("failures", 0)
            kuc = stats.get("unknowns", 0)
            k_known = ksc + kfc
            ksr = (ksc / k_known * 100) if k_known else 0
            kup = (kuc / stats["count"] * 100) if stats["count"] else 0
            sr_str = f"{ksr:.0f}%" if k_known else "n/a"
            period_label = html_mod.escape(period) if j == 0 else ""
            table_rows.append(
                f"      <tr>"
                f"<td>{period_label}</td>"
                f"<td>{html_mod.escape(kind)}</td>"
                f"<td class=\"num\">{h:.1f}</td>"
                f"<td class=\"num\">{ah:.1f}</td>"
                f"<td class=\"num\">{pct:.1f}</td>"
                f"<td class=\"num\">{stats['count']}</td>"
                f"<td class=\"num\">{sr_str}</td>"
                f"<td class=\"num\">{kup:.0f}%</td>"
                f"</tr>"
            )
    table_rows_html = "\n".join(table_rows)

    # SVG bar chart: wall-time per kind per period, grouped by period.
    # Collect all kinds across all periods for the legend.
    all_kinds = sorted({k for r in agg.values() for k in r["by_kind"]})
    # Palette (no external dep, just CSS colors)
    palette = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
               "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]
    kind_colors = {k: palette[i % len(palette)] for i, k in enumerate(all_kinds)}

    # Build grouped bar chart
    chart_bars = []
    chart_labels = []
    chart_legend = []
    bar_width = 24
    bar_gap = 4
    group_gap = 32
    chart_left_margin = 40
    chart_bottom_margin = 40
    chart_top_margin = 20
    chart_height = 260  # tall enough for bars + labels + gridline labels

    # Calculate max wall time across all kinds/periods for scaling
    max_h = 0.0
    for period in periods:
        for kind, stats in agg[period]["by_kind"].items():
            max_h = max(max_h, stats["seconds"] / 3600)
    if max_h == 0:
        max_h = 1.0  # avoid div-by-zero

    # Usable bar area height (from top_margin to chart_height - bottom_margin)
    bar_area_h = chart_height - chart_top_margin - chart_bottom_margin

    x = chart_left_margin
    for pi, period in enumerate(periods):
        row = agg[period]
        kinds_in_period = sorted(row["by_kind"].items(), key=lambda kv: -kv[1]["seconds"])
        for kind, stats in kinds_in_period:
            h = stats["seconds"] / 3600
            bar_h = (h / max_h) * bar_area_h if h > 0 else 0
            y_top = chart_height - chart_bottom_margin - bar_h
            color = kind_colors.get(kind, "#888")
            chart_bars.append(
                f'    <rect x="{x}" y="{y_top:.1f}" width="{bar_width}" height="{bar_h:.1f}" '
                f'fill="{color}" rx="2"><title>{html_mod.escape(kind)}: {h:.1f}h</title></rect>'
            )
            x += bar_width + bar_gap
        # Period label below the bar group
        label_x = x - (bar_width + bar_gap) * len(kinds_in_period) / 2 if kinds_in_period else x
        chart_labels.append(
            f'    <text x="{label_x:.0f}" y="{chart_height - chart_bottom_margin + 18}" '
            f'text-anchor="middle" font-size="11" fill="#555">{html_mod.escape(period)}</text>'
        )
        x += group_gap

    chart_width = max(x + 20, 400)

    # Y-axis gridlines
    gridlines = []
    for frac in (0.25, 0.5, 0.75, 1.0):
        gy = chart_height - chart_bottom_margin - frac * bar_area_h
        gv = frac * max_h
        gridlines.append(
            f'    <line x1="{chart_left_margin}" y1="{gy:.1f}" x2="{chart_width - 10}" '
            f'y2="{gy:.1f}" stroke="#e0e0e0" stroke-width="1"/>'
            f'<text x="{chart_left_margin - 5}" y="{gy + 3:.1f}" text-anchor="end" '
            f'font-size="9" fill="#999">{gv:.1f}h</text>'
        )

    # Legend
    for kind in all_kinds:
        color = kind_colors[kind]
        chart_legend.append(
            f'    <span class="legend-item"><span class="legend-swatch" '
            f'style="background:{color}"></span>{html_mod.escape(kind)}</span>'
        )

    svg_content = "\n".join(gridlines + chart_bars + chart_labels)
    legend_html = "\n".join(chart_legend)

    range_str = f"{periods[0]} — {periods[-1]}" if len(periods) > 1 else (periods[0] if periods else "n/a")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Time report (by {html_mod.escape(granularity)})</title>
<style>
  body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; margin: 2em; color: #333; }}
  h1 {{ font-size: 1.5em; }}
  h2 {{ font-size: 1.2em; margin-top: 1.5em; }}
  .summary {{ margin: 1em 0; font-size: 0.95em; color: #555; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
  th {{ background: #f5f5f5; font-weight: 600; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  tr:nth-child(even) {{ background: #fafafa; }}
  .chart-container {{ margin: 1.5em 0; overflow-x: auto; }}
  .legend {{ margin-top: 0.5em; display: flex; flex-wrap: wrap; gap: 12px; font-size: 0.85em; }}
  .legend-item {{ display: inline-flex; align-items: center; gap: 4px; }}
  .legend-swatch {{ display: inline-block; width: 12px; height: 12px; border-radius: 2px; }}
</style>
</head>
<body>
<h1>Time report (by {html_mod.escape(granularity)})</h1>
<p class="summary">
  <strong>Range:</strong> {html_mod.escape(range_str)} &nbsp;|&nbsp;
  <strong>Total:</strong> {total_wall:.1f}h wall / {total_active:.1f}h active &nbsp;|&nbsp;
  <strong>Tasks:</strong> {total_tasks}
</p>

<h2>Summary table</h2>
<table>
  <thead>
    <tr><th>Period</th><th>Kind</th><th>Wall(h)</th><th>Active(h)</th><th>%</th><th>Tasks</th><th>Success%</th><th>Unknown%</th></tr>
  </thead>
  <tbody>
{table_rows_html}
  </tbody>
</table>

<h2>Wall-time by kind</h2>
<div class="chart-container">
<svg width="{chart_width:.0f}" height="{chart_height}" xmlns="http://www.w3.org/2000/svg">
{svg_content}
</svg>
<div class="legend">
{legend_html}
</div>
</div>

</body>
</html>"""
    return html


def render_task_detail(task: dict) -> str:
    """Render a single task's full detail for the --task drill-down."""
    from datetime import datetime, timezone
    lines = [f"# Task {task.get('id', '?')}\n"]
    subject = task.get("subject") or "(no subject)"
    lines.append(f"**Subject:** {subject}")
    lines.append(f"**Flavor:** {task.get('flavor', '?')}")
    lines.append(f"**Status:** {task.get('task_status', '?')}")
    lines.append(f"**Success:** {task.get('success')} — {task.get('success_evidence', '')}")
    start = task.get("start")
    end = task.get("end")
    if start:
        s_dt = datetime.fromtimestamp(start, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        e_dt = datetime.fromtimestamp(end, tz=timezone.utc).strftime("%H:%M") if end else "?"
        lines.append(f"**Time:** {s_dt} - {e_dt} UTC")
    wall = task.get("wall_clock_seconds", task.get("duration_seconds", 0))
    active = task.get("active_seconds", 0)
    lines.append(f"**Duration:** {wall:.0f}s wall / {active:.0f}s active")
    lines.append(f"**Effort:** {task.get('output_tokens', 0)} output tokens, "
                 f"{task.get('input_tokens', 0)} input tokens")
    lines.append(f"**Errors:** {task.get('errors', 0)}")
    lines.append(f"**CWD:** {task.get('cwd', '?')}")
    lines.append(f"**Session:** {task.get('session_id', '?')}")
    lines.append(f"**Tools:** {', '.join(task.get('tool_names', []))} ({task.get('tool_calls', 0)} calls)")
    lines.append(f"**Events:** {task.get('event_count', 0)}")

    inputs = task.get("inputs", [])
    if inputs:
        lines.append(f"\n## Inputs ({len(inputs)})")
        for i in inputs:
            lines.append(f"  - {i}")

    outputs = task.get("outputs", [])
    if outputs:
        lines.append(f"\n## Outputs ({len(outputs)})")
        for o in outputs:
            lines.append(f"  - {o}")

    commits = task.get("git_commits", [])
    if commits:
        lines.append(f"\n## Linked git commits ({len(commits)})")
        for c in commits:
            lines.append(f"  - {c.get('hash', '?')[:8]} {c.get('subject', '')[:60]} "
                         f"(+{c.get('insertions', 0)}/-{c.get('deletions', 0)})")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from claude_code_adapter import collect_events
    from segment_tasks import segment

    import argparse
    ap = argparse.ArgumentParser(description="Aggregate reconstructed tasks into a time report.")
    ap.add_argument("--granularity", choices=["day", "week", "month"], default="week")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of text report")
    args = ap.parse_args()

    events = collect_events()
    tasks = segment(events)
    agg = aggregate(tasks, args.granularity)
    if args.json:
        print(json.dumps(agg, ensure_ascii=False, indent=2))
    else:
        print(render_report(agg, args.granularity))
