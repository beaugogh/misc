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
import os
from collections import defaultdict
from datetime import datetime, timezone


def classify_task(task: dict) -> str:
    """Classify a task into a kind for aggregation.

    Rules use source_kind (the originating adapter) first, then tool names and
    subject. Categories are chosen so each is self-explanatory and the opaque
    "other" bucket shrinks to near-zero:
      - coding       — AI-session task that edits/builds (Edit/Write/Read/Bash)
      - planning     — AI-session task with task-management tools only (TaskCreate,
                       TaskUpdate, EnterPlanMode) or short no-tool turns (chat/review)
      - research     — browser visits/searches, or WebSearch/WebFetch tool use
      - vcs          — git commits/checkouts
      - meeting      — calendar events, meeting recordings
      - communication — email, IM
      - file-edit    — manual file activity (VSCode Local History, Windows Recent)
    """
    tools = set(task.get("tool_names") or [])
    cwd = (task.get("cwd") or "").lower()
    subject = (task.get("subject") or "").lower()
    source_kind = task.get("source_kind", "")

    # Source-kind shortcuts (strongest signal).
    if source_kind == "browser":
        return "research"
    if source_kind == "vcs":
        return "vcs"
    if source_kind == "meeting":
        return "meeting"
    if source_kind == "comm":
        return "communication"

    # Filesystem-sourced tasks (VSCode history, Windows Recent, Jump Lists).
    if source_kind == "filesystem":
        return "file-edit"

    # AI-session tasks: classify by tool usage.
    edit_tools = tools & {"Edit", "Write", "Read", "Bash", "NotebookEdit"}
    if edit_tools:
        return "coding"
    if tools & {"WebSearch", "WebFetch"}:
        return "research"
    # Task-management tools only (TaskCreate/TaskUpdate/EnterPlanMode) or no tools
    # at all (short chat turns) → planning. This replaces the old "conversation" +
    # "other" buckets that were opaque and overlapped with "communication".
    return "planning"


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


def generate_insights(tasks: list[dict], agg: dict) -> list[str]:
    """Surface actionable findings from the reconstructed tasks.

    This is the layer that turns "coding 161h" into "you spent 10.6h retrying a
    git sync — that's an automation candidate." Each insight is a plain-text
    string, rendered in all report formats. Returns a list so the caller can
    format each as a bullet/card.

    Insight types (constitution point #4 — informative toward automation):
      1. Time sinks: the top tasks by active time, with their subject and a
         pain-point hint if the task has errors/retries (from task fields).
      2. Meeting load: total hours, daily average, and all-day-event warnings.
      3. Recurring pain: tasks sharing a retry/error pattern across the period.
      4. Success gaps: categories that are 100% unknown (measurement gap, not failure).
      5. Parallelism: how much time overlapped (coordination) vs exclusive.
    """
    from datetime import datetime, timezone
    insights: list[str] = []

    if not tasks:
        return ["No tasks in range."]

    # --- 1. Time sinks (top 3 by active time) ---
    ranked = sorted(tasks, key=lambda t: t.get("active_seconds") or 0, reverse=True)
    top_sinks = [t for t in ranked[:3] if (t.get("active_seconds") or 0) > 0]
    for t in top_sinks:
        act_h = (t.get("active_seconds") or 0) / 3600
        subj = t.get("subject") or "(no subject)"
        kind = classify_task(t)
        hint = ""
        if t.get("errors"):
            hint = f" — {t['errors']} error(s)"
        # Check for retry signals in the subject/text
        text = (t.get("subject") or "").lower()
        if any(k in text for k in ("retry", "again", "still", "sync", "fetch", "debug")):
            hint += ", possible retry/debug loop"
        # Surface the context (blocker/attendees/queries) so the insight line
        # explains WHY the task was a time sink, not just that it was one.
        context_inline = render_context_inline(t)
        if context_inline:
            hint += f". {context_inline}"
        insights.append(
            f"Time sink: {act_h:.1f}h on '{subj[:60]}' ({kind}{hint}). "
            f"Drill: --task {t.get('id', '?')} --drill"
        )

    # --- 2. Meeting load ---
    meeting_tasks = [t for t in tasks if classify_task(t) == "meeting"]
    if meeting_tasks:
        meeting_h = sum(t.get("active_seconds") or 0 for t in meeting_tasks) / 3600
        # Count all-day events (24h duration = calendar artifact, not real meeting)
        all_day = [t for t in meeting_tasks
                    if (t.get("active_seconds") or 0) >= 24 * 3600 - 1]
        # Date span for daily average
        starts = [t.get("start") or 0 for t in meeting_tasks]
        if starts:
            span_days = max(1, (max(starts) - min(starts)) / 86400)
            daily_avg = meeting_h / span_days
            line = (f"Meeting load: {meeting_h:.0f}h across {len(meeting_tasks)} meetings "
                    f"(~{daily_avg:.1f}h/day)")
            if all_day:
                line += (f" — {len(all_day)} all-day calendar entry(ies) counted as 24h; "
                         f"these are likely day-markers, not real meetings")
            insights.append(line)

    # --- 3. Recurring pain patterns ---
    pain_tasks = [t for t in tasks if t.get("errors") and t.get("errors") >= 2]
    if len(pain_tasks) >= 2:
        # Group by subject keyword to find recurrence
        from collections import Counter
        keywords = Counter()
        for t in pain_tasks:
            subj = (t.get("subject") or "").lower()
            for trigger in ("sync", "fetch", "git", "build", "install", "deploy", "debug"):
                if trigger in subj:
                    keywords[trigger] += 1
        recurring = [(k, n) for k, n in keywords.most_common(3) if n >= 2]
        if recurring:
            parts = [f"'{k}' failed across {n} tasks" for k, n in recurring]
            insights.append(
                f"Recurring pain: {', '.join(parts)} — these repeat the same error "
                f"pattern and are automation candidates."
            )
        else:
            insights.append(
                f"{len(pain_tasks)} tasks had 2+ errors — review for retry patterns "
                f"(use --top N to find them, then --task <id> --drill)."
            )

    # --- 4. Success measurement gaps ---
    from collections import defaultdict
    kind_success = defaultdict(lambda: {"succ": 0, "fail": 0, "unk": 0})
    for t in tasks:
        k = classify_task(t)
        s = t.get("success")
        if s == "succeeded":
            kind_success[k]["succ"] += 1
        elif s == "failed":
            kind_success[k]["fail"] += 1
        else:
            kind_success[k]["unk"] += 1
    all_unknown = [k for k, v in kind_success.items()
                   if v["unk"] > 0 and v["succ"] == 0 and v["fail"] == 0]
    if all_unknown:
        insights.append(
            f"Success not yet measured for: {', '.join(sorted(all_unknown))} — "
            f"these aren't failures, just categories with no success signal detected yet."
        )

    # --- 5. Parallelism / overlap ---
    # Use excised_gap_seconds as a proxy for idle, and count tasks with wall >> active
    high_wall = [t for t in tasks
                 if (t.get("wall_clock_seconds") or 0) > 2 * max(t.get("active_seconds") or 0, 1)
                 and (t.get("wall_clock_seconds") or 0) > 3600]
    if len(high_wall) >= 3:
        insights.append(
            f"{len(high_wall)} tasks have wall-clock 2×+ their active time — "
            f"long idle/overlap periods. Use --top to find them and --drill to see why."
        )

    return insights


def render_report(agg: dict, granularity: str, tasks: list[dict] | None = None) -> str:
    """Render an aggregation as a human-readable text report.

    When ``tasks`` is provided, an insights section is appended at the end.
    """
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

    # Insights section (pain points + automation candidates).
    if tasks is not None:
        insights = generate_insights(tasks, agg)
        if insights:
            lines.append("## Insights & pain points")
            for ins in insights:
                lines.append(f"  • {ins}")
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


def render_markdown(agg: dict, granularity: str, tasks: list[dict] | None = None) -> str:
    """Render an aggregation as a Markdown document.

    Mirrors the structure of render_report() but as proper Markdown:
    ``##`` headers for periods, Markdown tables for the per-kind breakdown,
    and a summary line per period. When ``tasks`` is provided, an insights
    section is appended.
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

    if tasks is not None:
        insights = generate_insights(tasks, agg)
        if insights:
            lines.append("## Insights & pain points")
            for ins in insights:
                lines.append(f"- {ins}")
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


def render_data_availability_html(tasks: list[dict], since_ts: float | None,
                                  until_ts: float | None) -> str:
    """Render a per-source data-availability table for the requested time range.

    Shows, for each source_kind present in the tasks: the number of tasks, the
    earliest and latest task timestamps, and the active hours. For source_kinds
    with zero tasks in range, shows "No data in range" so the reader knows the
    horizon is sparse, not empty-by-design.

    This directly addresses the "if you cannot find data for a time range, state
    that it is not available" requirement: each source is listed with its actual
    coverage, and missing sources are called out plainly.
    """
    import html as html_mod
    from datetime import datetime as _dt, timezone as _tz

    # Group tasks by source_kind.
    from collections import defaultdict
    by_kind: dict[str, list[dict]] = defaultdict(list)
    for t in tasks:
        sk = t.get("source_kind") or "unknown"
        by_kind[sk].append(t)

    # All source_kinds we know about (so we can show "No data" for missing ones).
    all_source_kinds = ["ai_session", "browser", "meeting", "comm", "vcs", "filesystem"]

    # Format the requested range label.
    if since_ts and until_ts:
        s_dt = _dt.fromtimestamp(since_ts, tz=_tz.utc).strftime("%Y-%m-%d")
        e_dt = _dt.fromtimestamp(until_ts, tz=_tz.utc).strftime("%Y-%m-%d")
        range_label = f"{s_dt} → {e_dt}"
    elif since_ts:
        s_dt = _dt.fromtimestamp(since_ts, tz=_tz.utc).strftime("%Y-%m-%d")
        range_label = f"{s_dt} → now"
    else:
        range_label = "all available data"

    rows = []
    for sk in all_source_kinds:
        sk_tasks = by_kind.get(sk, [])
        if not sk_tasks:
            rows.append(
                f'      <tr class="no-data">'
                f'<td>{html_mod.escape(sk)}</td>'
                f'<td class="num">0</td>'
                f'<td colspan="3" class="no-data-msg">No data in range — source not active or lookback exceeded</td>'
                f'</tr>'
            )
            continue
        starts = [t.get("start") or 0 for t in sk_tasks]
        earliest = min(starts)
        latest = max(starts)
        active_h = sum(t.get("active_seconds") or 0 for t in sk_tasks) / 3600
        e_str = _dt.fromtimestamp(earliest, tz=_tz.utc).strftime("%Y-%m-%d")
        l_str = _dt.fromtimestamp(latest, tz=_tz.utc).strftime("%Y-%m-%d")
        rows.append(
            f'      <tr>'
            f'<td>{html_mod.escape(sk)}</td>'
            f'<td class="num">{len(sk_tasks)}</td>'
            f'<td class="num">{active_h:.1f}h</td>'
            f'<td>{e_str}</td>'
            f'<td>{l_str}</td>'
            f'</tr>'
        )

    rows_html = "\n".join(rows)
    return f"""<h2>Data availability</h2>
<p class="hint">Requested range: {html_mod.escape(range_label)}. Each row shows what data this source actually provided in that range.</p>
<table class="data-avail">
  <thead><tr><th>Source</th><th>Tasks</th><th>Active</th><th>Earliest</th><th>Latest</th></tr></thead>
  <tbody>
{rows_html}
  </tbody>
</table>"""


def render_html(agg: dict, granularity: str, tasks: list[dict] | None = None,
                since_ts: float | None = None, until_ts: float | None = None) -> str:
    """Render an aggregation as a self-contained, readable HTML dashboard.

    Single file with inline CSS, no external resources, no JS dependencies.
    Layout: header + summary stats, data-availability table, insights callout
    cards, active-time bar chart, per-period breakdown table with color-coded
    success, top tasks list, and per-kind subject breakdown so the reader sees
    WHAT the work was.

    When ``since_ts``/``until_ts`` are provided, a data-availability section is
    included showing per-source coverage (and "No data" for sources with zero
    tasks in the requested range).
    """
    import html as html_mod
    from datetime import datetime as _dt

    periods = sorted(agg.keys())
    total_wall = sum(r["total_seconds"] for r in agg.values()) / 3600
    total_active = sum(r.get("active_seconds", 0.0) for r in agg.values()) / 3600
    total_tasks = sum(r["task_count"] for r in agg.values())

    # --- Palette for kinds (consistent across chart + table) ---
    all_kinds = sorted({k for r in agg.values() for k in r["by_kind"]})
    palette = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f",
               "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac"]
    kind_colors = {k: palette[i % len(palette)] for i, k in enumerate(all_kinds)}

    # --- Table rows (per-period × kind breakdown) ---
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
            sr_class = "sr-good" if k_known and ksr >= 80 else ("sr-bad" if k_known and ksr < 50 else "sr-na")
            period_label = html_mod.escape(period) if j == 0 else ""
            color = kind_colors.get(kind, "#888")
            table_rows.append(
                f'      <tr>'
                f'<td>{period_label}</td>'
                f'<td><span class="kind-dot" style="background:{color}"></span>{html_mod.escape(kind)}</td>'
                f'<td class="num">{h:.1f}</td>'
                f'<td class="num">{ah:.1f}</td>'
                f'<td class="num">{pct:.1f}</td>'
                f'<td class="num">{stats["count"]}</td>'
                f'<td class="num {sr_class}">{sr_str}</td>'
                f'<td class="num">{kup:.0f}%</td>'
                f'</tr>'
            )
    table_rows_html = "\n".join(table_rows)

    # --- Active-time bar chart (active, not wall — wall is misleading) ---
    chart_bars = []
    chart_labels = []
    chart_legend = []
    bar_width = 24
    bar_gap = 4
    group_gap = 32
    chart_left_margin = 40
    chart_bottom_margin = 40
    chart_top_margin = 20
    chart_height = 260
    bar_area_h = chart_height - chart_top_margin - chart_bottom_margin

    max_h = 0.0
    for period in periods:
        for kind, stats in agg[period]["by_kind"].items():
            max_h = max(max_h, stats.get("active_seconds", 0.0) / 3600)
    if max_h == 0:
        max_h = 1.0

    x = chart_left_margin
    for period in periods:
        row = agg[period]
        kinds_in_period = sorted(row["by_kind"].items(),
                                 key=lambda kv: -kv[1].get("active_seconds", 0.0))
        for kind, stats in kinds_in_period:
            h = stats.get("active_seconds", 0.0) / 3600
            bar_h = (h / max_h) * bar_area_h if h > 0 else 0
            y_top = chart_height - chart_bottom_margin - bar_h
            color = kind_colors.get(kind, "#888")
            chart_bars.append(
                f'    <rect x="{x}" y="{y_top:.1f}" width="{bar_width}" height="{bar_h:.1f}" '
                f'fill="{color}" rx="2"><title>{html_mod.escape(kind)}: {h:.1f}h active</title></rect>'
            )
            x += bar_width + bar_gap
        label_x = x - (bar_width + bar_gap) * len(kinds_in_period) / 2 if kinds_in_period else x
        chart_labels.append(
            f'    <text x="{label_x:.0f}" y="{chart_height - chart_bottom_margin + 18}" '
            f'text-anchor="middle" font-size="11" fill="#555">{html_mod.escape(period)}</text>'
        )
        x += group_gap

    chart_width = max(x + 20, 400)

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

    for kind in all_kinds:
        color = kind_colors[kind]
        chart_legend.append(
            f'    <span class="legend-item"><span class="legend-swatch" '
            f'style="background:{color}"></span>{html_mod.escape(kind)}</span>'
        )

    svg_content = "\n".join(gridlines + chart_bars + chart_labels)
    legend_html = "\n".join(chart_legend)

    # --- Data availability table (per-source coverage in the requested range) ---
    data_avail_html = ""
    if tasks is not None and (since_ts is not None or until_ts is not None):
        data_avail_html = render_data_availability_html(tasks, since_ts, until_ts)

    # --- Insights cards ---
    insights_html = ""
    if tasks is not None:
        insights = generate_insights(tasks, agg)
        if insights:
            cards = "\n".join(
                f'  <div class="insight-card">{html_mod.escape(ins)}</div>'
                for ins in insights
            )
            insights_html = f"""<h2>Insights &amp; pain points</h2>
<div class="insights-grid">
{cards}
</div>"""

    # --- Top tasks list (what the biggest time sinks were) ---
    top_tasks_html = ""
    if tasks:
        ranked = sorted(tasks, key=lambda t: t.get("active_seconds") or 0, reverse=True)
        top5 = [t for t in ranked[:5] if (t.get("active_seconds") or 0) > 0]
        if top5:
            rows = []
            for i, t in enumerate(top5, 1):
                act_h = (t.get("active_seconds") or 0) / 3600
                wall_h = (t.get("wall_clock_seconds") or 0) / 3600
                kind = html_mod.escape(classify_task(t))
                subj = html_mod.escape((t.get("subject") or "(no subject)")[:55])
                start_str = _dt.fromtimestamp(t.get("start") or 0).strftime("%m-%d %H:%M")
                tid = html_mod.escape(t.get("id", "?"))
                color = kind_colors.get(classify_task(t), "#888")
                why = html_mod.escape(render_context_inline(t))
                rows.append(
                    f'      <tr>'
                    f'<td class="num">{i}</td>'
                    f'<td class="num">{act_h:.1f}h</td>'
                    f'<td class="num">{wall_h:.1f}h</td>'
                    f'<td><span class="kind-dot" style="background:{color}"></span>{kind}</td>'
                    f'<td>{start_str}</td>'
                    f'<td>{subj}</td>'
                    f'<td class="why">{why}</td>'
                    f'<td class="task-id">{tid}</td>'
                    f'</tr>'
                )
            top_tasks_html = f"""<h2>Top 5 time sinks</h2>
<p class="hint">Drill into any: <code>python run.py --task &lt;id&gt; --drill</code></p>
<table class="top-tasks">
  <thead><tr><th>#</th><th>Active</th><th>Wall</th><th>Kind</th><th>Start</th><th>Subject</th><th>Root cause</th><th>Task ID</th></tr></thead>
  <tbody>
{chr(10).join(rows)}
  </tbody>
</table>"""

    # --- Per-kind subject breakdown (WHAT was the work, not just hours) ---
    kind_subjects_html = ""
    if tasks:
        from collections import defaultdict
        by_kind_tasks = defaultdict(list)
        for t in tasks:
            by_kind_tasks[classify_task(t)].append(t)
        kind_sections = []
        for kind in sorted(by_kind_tasks.keys(),
                           key=lambda k: -sum(t.get("active_seconds", 0) for t in by_kind_tasks[k])):
            kind_tasks = sorted(by_kind_tasks[kind],
                                key=lambda t: t.get("active_seconds") or 0, reverse=True)[:3]
            kind_active = sum(t.get("active_seconds", 0) for t in by_kind_tasks[kind]) / 3600
            color = kind_colors.get(kind, "#888")
            items = []
            for t in kind_tasks:
                act_h = (t.get("active_seconds") or 0) / 3600
                subj = html_mod.escape((t.get("subject") or "(no subject)")[:50])
                why = html_mod.escape(render_context_inline(t))
                why_html = f'<div class="why-inline">{why}</div>' if why else ''
                items.append(f"<li><span class='num'>{act_h:.1f}h</span> {subj}{why_html}</li>")
            kind_sections.append(
                f'  <div class="kind-section">'
                f'<h3><span class="kind-dot" style="background:{color}"></span>'
                f'{html_mod.escape(kind)} <span class="kind-total">({kind_active:.1f}h, {len(by_kind_tasks[kind])} tasks)</span></h3>'
                f'<ul>{"".join(items)}</ul>'
                f'</div>'
            )
        if kind_sections:
            kind_subjects_html = '<h2>What the work was — by kind</h2>\n' + \
                                 '<div class="kind-grid">\n' + \
                                 "\n".join(kind_sections) + '\n</div>'

    range_str = f"{periods[0]} — {periods[-1]}" if len(periods) > 1 else (periods[0] if periods else "n/a")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Time report (by {html_mod.escape(granularity)})</title>
<style>
  body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; margin: 2em; color: #2c2c2c; max-width: 1200px; }}
  h1 {{ font-size: 1.6em; border-bottom: 3px solid #4e79a7; padding-bottom: 0.3em; }}
  h2 {{ font-size: 1.25em; margin-top: 2em; color: #333; }}
  h3 {{ font-size: 1.05em; margin: 0.5em 0; }}
  .summary {{ background: #f8f9fa; padding: 1em 1.5em; border-radius: 8px; margin: 1em 0; font-size: 1em; }}
  .summary strong {{ color: #4e79a7; }}
  .hint {{ font-size: 0.85em; color: #777; margin: 0.3em 0; }}
  code {{ background: #eef; padding: 1px 5px; border-radius: 3px; font-size: 0.85em; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em; }}
  th, td {{ border: 1px solid #e0e0e0; padding: 7px 10px; text-align: left; }}
  th {{ background: #f5f5f5; font-weight: 600; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  tr:nth-child(even) {{ background: #fafbfc; }}
  .kind-dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }}
  .sr-good {{ color: #2e7d32; font-weight: 600; }}
  .sr-bad {{ color: #c62828; font-weight: 600; }}
  .sr-na {{ color: #999; }}
  .insights-grid {{ display: grid; grid-template-columns: 1fr; gap: 10px; margin: 1em 0; }}
  .insight-card {{ background: #fff3e0; border-left: 4px solid #f28e2b; padding: 10px 14px; border-radius: 4px; font-size: 0.92em; line-height: 1.5; }}
  .chart-container {{ margin: 1.5em 0; overflow-x: auto; }}
  .legend {{ margin-top: 0.5em; display: flex; flex-wrap: wrap; gap: 12px; font-size: 0.85em; }}
  .legend-item {{ display: inline-flex; align-items: center; gap: 4px; }}
  .legend-swatch {{ display: inline-block; width: 12px; height: 12px; border-radius: 2px; }}
  .top-tasks .task-id {{ font-family: monospace; font-size: 0.8em; color: #667; }}
  .kind-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; margin: 1em 0; }}
  .kind-section {{ background: #fafbfc; border: 1px solid #e8e8e8; border-radius: 6px; padding: 12px 16px; }}
  .kind-section ul {{ list-style: none; padding-left: 0; margin: 0.3em 0; }}
  .kind-section li {{ padding: 3px 0; font-size: 0.88em; }}
  .kind-section .num {{ font-weight: 600; color: #4e79a7; display: inline-block; width: 50px; }}
  .kind-total {{ font-size: 0.85em; color: #888; font-weight: normal; }}
  .top-tasks td.why {{ font-size: 0.82em; color: #666; max-width: 320px; }}
  .why-inline {{ font-size: 0.85em; color: #888; margin-left: 56px; margin-top: 2px; }}
  .data-avail {{ font-size: 0.88em; }}
  .data-avail .no-data {{ background: #fff8f8; }}
  .data-avail .no-data-msg {{ color: #c62828; font-style: italic; }}
</style>
</head>
<body>
<h1>Time report (by {html_mod.escape(granularity)})</h1>
<div class="summary">
  <strong>Range:</strong> {html_mod.escape(range_str)} &nbsp;|&nbsp;
  <strong>Active:</strong> {total_active:.1f}h &nbsp;|&nbsp;
  <strong>Wall:</strong> {total_wall:.1f}h &nbsp;|&nbsp;
  <strong>Tasks:</strong> {total_tasks}
</div>

{data_avail_html}

{insights_html}

<h2>Active time by kind</h2>
<div class="chart-container">
<svg width="{chart_width:.0f}" height="{chart_height}" xmlns="http://www.w3.org/2000/svg">
{svg_content}
</svg>
<div class="legend">
{legend_html}
</div>
</div>

<h2>Breakdown by period</h2>
<table>
  <thead>
    <tr><th>Period</th><th>Kind</th><th>Wall(h)</th><th>Active(h)</th><th>%</th><th>Tasks</th><th>Success</th><th>Unknown%</th></tr>
  </thead>
  <tbody>
{table_rows_html}
  </tbody>
</table>

{top_tasks_html}

{kind_subjects_html}

</body>
</html>"""
    return html


def render_context_text(task: dict) -> str:
    """Render task['context'] as a human-readable 'why this took as long as it did' block.

    Returns a multi-line string (without a header), or '' if no context is available.
    Used by render_task_detail(), the drill-down lead-off, and the insight lines.
    """
    ctx = task.get("context") or {}
    if not ctx:
        return ""
    lines: list[str] = []
    source_kind = task.get("source_kind", "")

    if source_kind == "meeting":
        org = ctx.get("organizer")
        n_att = ctx.get("attendees")
        names = ctx.get("attendee_names") or []
        loc = ctx.get("location")
        is_all_day = ctx.get("is_all_day")
        if org:
            lines.append(f"Organizer: {org}")
        if n_att is not None:
            label = f"{n_att} attendee(s)"
            if names:
                label += f" ({', '.join(names)})"
            lines.append(label)
        if loc:
            lines.append(f"Location: {loc}")
        if is_all_day:
            lines.append("All-day event (calendar marker, likely not a real meeting)")

    elif source_kind == "browser":
        queries = ctx.get("queries") or []
        titles = ctx.get("top_titles") or []
        downloads = ctx.get("downloads") or 0
        n_visits = ctx.get("n_visits") or 0
        if queries:
            lines.append(f"Searched for: {', '.join(repr(q) for q in queries)}")
        if titles:
            lines.append(f"Visited: {', '.join(titles[:3])}")
        if downloads:
            lines.append(f"Downloaded {downloads} file(s) — artifact(s) produced")
        elif n_visits > 5:
            lines.append(f"{n_visits} visits, no downloads — research may be incomplete")
        if n_visits and not queries and not titles:
            lines.append(f"{n_visits} visits")

    elif source_kind == "comm":
        senders = ctx.get("senders") or []
        subjects = ctx.get("subjects") or []
        has_reply = ctx.get("has_reply")
        if subjects:
            lines.append(f"Threads: {', '.join(subjects[:3])}")
        if senders:
            lines.append(f"From: {', '.join(senders[:3])}")
        if has_reply:
            lines.append("Reply sent in thread")
        else:
            lines.append("No reply detected")

    elif source_kind == "ai_session":
        blocker = ctx.get("blocker")
        error_samples = ctx.get("error_samples") or []
        retry_targets = ctx.get("retry_targets") or []
        files = ctx.get("files_touched") or []
        tools = ctx.get("dominant_tools") or []
        if blocker:
            lines.append(f"Blocker: {blocker}")
        if retry_targets:
            lines.append(f"Retried: {', '.join(retry_targets[:3])}")
        if error_samples and not blocker:
            lines.append(f"Errors: {error_samples[0][:80]}")
        if files:
            lines.append(f"Files touched: {', '.join(os.path.basename(f) for f in files[:5])}")
        if tools:
            lines.append(f"Dominant tools: {', '.join(tools)}")

    elif source_kind == "vcs":
        subjects = ctx.get("commit_subjects") or []
        if subjects:
            lines.append(f"Commits: {', '.join(subjects)}")

    elif source_kind == "filesystem":
        files = ctx.get("files") or []
        if files:
            lines.append(f"Files: {', '.join(os.path.basename(f) for f in files)}")

    return "\n".join(lines)


def render_context_inline(task: dict) -> str:
    """One-line root-cause explanation for the 'why' column and insight lines.

    Diagnoses WHY the task took as long as it did by comparing active vs wall
    time and identifying the inflation pattern. Returns a single string, or ''.

    The principle: if active ≈ wall, it's genuine work — show what the work was.
    If active << wall, explain where the time went (idle gaps, overnight tabs,
    all-day marker, multi-day cap).
    """
    ctx = task.get("context") or {}
    source_kind = task.get("source_kind", "")
    active = task.get("active_seconds") or 0
    wall = task.get("wall_clock_seconds") or 0
    excised = task.get("excised_gap_seconds") or 0
    active_h = active / 3600
    wall_h = wall / 3600
    excised_h = excised / 3600

    # No active time and no context → nothing to explain.
    if active <= 0 and not ctx:
        return ""

    # --- Meeting: diagnose calendar inflation ---
    if source_kind == "meeting":
        if ctx.get("is_all_day"):
            return "Calendar day-marker — 0h real meeting time"
        # Multi-day: either wall_h > 8 (correct wall) or excised > 0 (capped)
        if wall_h > 8 or (excised_h > 0 and active_h >= 8):
            return f"Multi-day event, capped to {active_h:.0f}h (actual attendance unknown)"
        # Normal meeting — show organizer if available
        org = ctx.get("organizer")
        n_att = ctx.get("attendees")
        parts = [f"{active_h:.1f}h meeting"]
        if org:
            parts.append(f"organizer: {org}")
        if n_att is not None and n_att > 0:
            parts.append(f"{n_att} attendee(s)")
        return ", ".join(parts)

    # --- Browser: diagnose overnight-tab inflation ---
    if source_kind == "browser":
        n_visits = ctx.get("n_visits") or 0
        queries = ctx.get("queries") or []
        downloads = ctx.get("downloads") or 0
        if active < 60:  # <1 min active
            return f"Tabs open {wall_h:.1f}h but no measurable activity (idle/overnight)"
        if excised_h > 0.5 and excised_h > active_h:
            # Significant idle time — tabs were left open
            return (f"Tabs open {wall_h:.1f}h, only {active_h:.1f}h active browsing "
                    f"— {excised_h:.1f}h idle/overnight gaps excised")
        # Genuine browsing session
        parts = [f"{active_h:.1f}h continuous browsing"]
        if queries:
            parts.append(f"searched '{queries[0][:30]}'")
        elif n_visits > 10:
            parts.append(f"{n_visits} visits")
        if downloads:
            parts.append(f"{downloads} download(s)")
        return ", ".join(parts)

    # --- Coding (ai_session): show blocker or work summary ---
    if source_kind == "ai_session":
        blocker = ctx.get("blocker")
        retries = ctx.get("retry_targets") or []
        files = ctx.get("files_touched") or []
        errors = task.get("errors", 0)
        if blocker:
            parts = [f"blocker: {blocker}"]
            if retries:
                parts.append(retries[0])
            return ", ".join(parts)
        if errors > 0:
            parts = [f"{errors} error(s)"]
            if retries:
                parts.append(retries[0])
            return ", ".join(parts)
        # No errors — was it genuine work or idle session?
        if excised_h > 1 and excised_h > active_h:
            return (f"{active_h:.1f}h active in {wall_h:.1f}h wall "
                    f"— {excised_h:.1f}h idle gaps, {len(files)} file(s) edited")
        parts = [f"{active_h:.1f}h active"]
        if files:
            parts.append(f"{len(files)} file(s) edited")
        tool_calls = task.get("tool_calls", 0)
        if tool_calls > 20:
            parts.append(f"{tool_calls} tool calls")
        return ", ".join(parts)

    # --- VCS ---
    if source_kind == "vcs":
        subjects = ctx.get("commit_subjects") or []
        if subjects:
            return f"{len(subjects)} commit(s): {subjects[0][:40]}"
        return f"{active_h:.1f}h VCS activity"

    # --- Communication ---
    if source_kind == "comm":
        has_reply = ctx.get("has_reply")
        subjects = ctx.get("subjects") or []
        if subjects:
            return f"'{subjects[0][:30]}' — {'replied' if has_reply else 'no reply'}"
        return "replied" if has_reply else "no reply"

    # --- Filesystem ---
    if source_kind == "filesystem":
        files = ctx.get("files") or []
        if files:
            return f"{len(files)} file(s): {os.path.basename(files[0])}"
        return ""

    # --- Fallback: active vs wall comparison ---
    if active > 0:
        if excised_h > active_h:
            return f"{active_h:.1f}h active in {wall_h:.1f}h wall — {excised_h:.1f}h idle"
        return f"{active_h:.1f}h active"
    return ""


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

    # Why this took as long as it did — the key context section.
    context_text = render_context_text(task)
    if context_text:
        lines.append(f"\n## Why this took as long as it did")
        lines.append(context_text)

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
