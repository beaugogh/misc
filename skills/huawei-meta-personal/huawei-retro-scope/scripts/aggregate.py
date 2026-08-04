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
import re
from collections import defaultdict
from datetime import datetime, timezone

# A working day is 8 hours. Used to express active time as an intuitive
# percentage ("680h active = 85 working days") rather than a raw hour count.
WORKING_DAY_HOURS = 8.0


def _as_working_days(active_hours: float, working_day_hours: float = WORKING_DAY_HOURS) -> str:
    """Format active hours as a human-readable working-day count.

    By default uses 8h/day. When actual working hours are available, pass the
    per-day average for a more accurate conversion.

    Returns e.g. "85.0 working days" for 680h, "0.5 working days" for 4h.
    Returns "" for zero/negative.
    """
    if active_hours <= 0 or working_day_hours <= 0:
        return ""
    days = active_hours / working_day_hours
    return f"{days:.1f} working days"


def _working_day_pct(active_hours: float, working_day_hours: float = WORKING_DAY_HOURS) -> str:
    """Format active hours as a percentage of a working day.

    By default uses 8h. When actual working hours are computed from the data
    (via human_involvement.compute_actual_working_hours), pass that as the
    denominator for a more accurate percentage.

    Returns e.g. "133%" for 10.6h (more than a full day), "48%" for 3.8h.
    Capped at 999% to avoid absurd numbers from corrupt data. Returns ""
    for zero/negative.
    """
    if active_hours <= 0 or working_day_hours <= 0:
        return ""
    pct = active_hours / working_day_hours * 100
    if pct > 999:
        return "999%+"
    return f"{pct:.0f}%"


def classify_task(task: dict) -> str:
    """Classify a task into a kind for aggregation.

    Rules use source_kind (the originating adapter) first, then tool names and
    subject. Tool-name matching is case-insensitive (Claude Code yields
    "Edit"/"Read"/"Bash"; the legacy codeagent adapter yields "edit"/"read"/
    "bash"). Categories are chosen so each is self-explanatory and the opaque
    "other" bucket shrinks to near-zero:
      - coding       — AI-session task that edits/builds (Edit/Write/Read/Bash)
      - planning     — AI-session task that explicitly entered plan mode
                       (EnterPlanMode tool). Genuine planning phase, not chat.
      - research     — web browser visits/searches, or WebSearch/WebFetch tool use
      - git          — git commits/checkouts
      - meeting      — calendar events, meeting recordings
      - welink       — email, WeLink IM chats
      - file-edit    — manual file activity (VSCode Local History, Windows Recent)
      - doc-edit     — document authoring (3ms, CloudDevOps Wiki, W3)
      - other        — honest catch-all: AI sessions with no hands-on tools
                       (chat/review/task-management), auxiliary sources
                       (daemon.log, shell-snapshots), anything unclassified
    """
    tools = set(task.get("tool_names") or [])
    # Adapter casing is inconsistent: Claude Code yields capitalized names
    # (Edit, Read, Bash), the legacy codeagent adapter yields lowercase
    # (edit, read, bash). Normalize once so every comparison below is
    # case-insensitive.
    tools_lc = {t.lower() for t in tools}
    cwd = (task.get("cwd") or "").lower()
    subject = (task.get("subject") or "").lower()
    source_kind = task.get("source_kind", "")

    # Source-kind shortcuts (strongest signal).
    if source_kind == "browser":
        return "research"
    if source_kind == "vcs":
        return "git"
    if source_kind == "meeting":
        return "meeting"
    if source_kind == "comm":
        return "WeLink"
    if source_kind == "filesystem":
        return "file-edit"
    if source_kind == "doc_authoring":
        return "doc-edit"
    if source_kind == "auxiliary":
        return "other"

    # AI-session tasks: classify by tool usage (case-insensitive — see above).
    if tools_lc & {"edit", "write", "read", "bash", "notebookedit"}:
        return "coding"
    if tools_lc & {"websearch", "webfetch"}:
        return "research"
    # Genuine plan mode (EnterPlanMode tool used) → planning. Everything else
    # (TaskCreate/TaskUpdate, short chat, review with no tools) → other.
    if "enterplanmode" in tools_lc:
        return "planning"
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
        human = ((t.get("human_data") or {}).get("human_engaged_seconds") or 0)
        success = t.get("success")
        # A "gap" is a task with 0 active time — a single event (or burst at one
        # timestamp) that couldn't be paired into a measurable duration. We know
        # it happened but not how long it took. Surface these so the report
        # doesn't silently swallow activity it can't duration-ize.
        is_gap = active <= 0.0
        key = _period_key(start, granularity)
        if key not in out:
            out[key] = {"total_seconds": 0.0, "active_seconds": 0.0,
                        "human_seconds": 0.0,
                        "excised_gap_seconds": 0.0,
                        "task_count": 0, "success_count": 0, "failure_count": 0,
                        "unknown_count": 0, "gap_count": 0, "by_kind": {}}
        out[key]["total_seconds"] += dur
        out[key]["active_seconds"] += active
        out[key]["human_seconds"] += human
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
                        "human_seconds": 0.0,
                        "excised_gap_seconds": 0.0,
                        "count": 0,
                        "successes": 0, "failures": 0, "unknowns": 0, "gaps": 0}
        bk[kind]["seconds"] += dur
        bk[kind]["active_seconds"] += active
        bk[kind]["human_seconds"] += human
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

    # --- 1. Time sinks (top 3 by HUMAN engaged time, not raw active time) ---
    # The principle: we're looking for tasks that cost HUMAN time, not machine
    # time. A 10h autonomous agent run with 2 prompts is NOT a time sink. Rank
    # by human_engaged_seconds — the time the human was actively interacting.
    def _human_engaged(t: dict) -> float:
        hd = t.get("human_data") or {}
        return hd.get("human_engaged_seconds", 0) or 0

    ranked_human = sorted(tasks, key=_human_engaged, reverse=True)
    top_sinks = [t for t in ranked_human[:3] if _human_engaged(t) > 0]
    for t in top_sinks:
        act_h = (t.get("active_seconds") or 0) / 3600
        eng_h = _human_engaged(t) / 3600
        subj = t.get("subject") or "(no subject)"
        kind = classify_task(t)
        hd = t.get("human_data") or {}
        inv = hd.get("human_involvement", "?")
        hint = ""
        if t.get("errors"):
            hint = f" — {t['errors']} error(s)"
        # Surface the context (narrative/queries) so the insight explains WHY.
        context_inline = render_context_inline(t)
        if context_inline:
            hint += f". {context_inline}"
        insights.append(
            f"人工时间消耗：{eng_h:.1f}h 人工参与"
            f"（共 {act_h:.1f}h active，{inv}）——'{subj[:60]}'（{kind}{hint}）。"
        )

    # Also flag tasks with high active time but LOW human involvement — these
    # look like time sinks but are actually autonomous machine work.
    autonomous_lookalikes = [t for t in tasks
                              if (t.get("active_seconds") or 0) > 2 * 3600
                              and (t.get("human_data") or {}).get("human_involvement") == "low"]
    if autonomous_lookalikes:
        names = [(t.get("subject") or "(no subject)")[:40] for t in autonomous_lookalikes[:3]]
        insights.append(
            f"{len(autonomous_lookalikes)} 个任务 active 时间较长但人工参与度低——"
            f"主要为 agent 自主工作，非人工时间消耗：{', '.join(names)}。"
        )

    # --- 2. Meeting load ---
    meeting_tasks = [t for t in tasks if classify_task(t) == "meeting"]
    if meeting_tasks:
        meeting_h = sum(t.get("active_seconds") or 0 for t in meeting_tasks) / 3600
        all_day = [t for t in meeting_tasks
                    if (t.get("active_seconds") or 0) >= 24 * 3600 - 1]
        starts = [t.get("start") or 0 for t in meeting_tasks]
        if starts:
            span_days = max(1, (max(starts) - min(starts)) / 86400)
            daily_avg = meeting_h / span_days
            line = (f"会议负荷：{meeting_h:.0f}h，共 {len(meeting_tasks)} 个会议"
                    f"（日均 {daily_avg:.1f}h/天）")
            if all_day:
                line += (f"——{len(all_day)} 个全天日历条目被计为 24h；"
                         f"这些可能是日期标记，非真实会议")
            insights.append(line)

    # --- 3. Recurring pain patterns ---
    pain_tasks = [t for t in tasks if t.get("errors") and t.get("errors") >= 2]
    if len(pain_tasks) >= 2:
        from collections import Counter
        keywords = Counter()
        for t in pain_tasks:
            subj = (t.get("subject") or "").lower()
            for trigger in ("sync", "fetch", "git", "build", "install", "deploy", "debug"):
                if trigger in subj:
                    keywords[trigger] += 1
        recurring = [(k, n) for k, n in keywords.most_common(3) if n >= 2]
        if recurring:
            parts = [f"'{k}' 在 {n} 个任务中失败" for k, n in recurring]
            insights.append(
                f"反复出现的痛点：{', '.join(parts)}——这些重复相同的错误模式，"
                f"是自动化候选对象。"
            )
        else:
            insights.append(
                f"{len(pain_tasks)} 个任务出现 2+ 个错误——检查重试模式"
                f"（用 --top N 查找，再 --task <id> --drill 下钻）。"
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
            f"尚未度量成功率的类别：{', '.join(sorted(all_unknown))}——"
            f"这些不是失败，只是尚未检测到成功信号的类别。"
        )

    # --- 5. Parallelism / overlap ---
    high_wall = [t for t in tasks
                 if (t.get("wall_clock_seconds") or 0) > 2 * max(t.get("active_seconds") or 0, 1)
                 and (t.get("wall_clock_seconds") or 0) > 3600]
    if len(high_wall) >= 3:
        insights.append(
            f"{len(high_wall)} 个任务的 Wall 时间是 Active 的 2 倍以上——"
            f"存在长时间空闲/重叠。用 --top 查找，--drill 查看原因。"
        )

    return insights


def render_report(agg: dict, granularity: str, tasks: list[dict] | None = None) -> str:
    """Render an aggregation as a human-readable text report.

    When ``tasks`` is provided, an insights section is appended at the end.
    """
    lines = [f"# Time report (by {granularity})\n"]
    # Overall working-day total for the whole report.
    total_active_all = sum(r.get("active_seconds", 0.0) for r in agg.values()) / 3600
    wd_all = _as_working_days(total_active_all)
    if wd_all:
        lines.append(f"Total active: {total_active_all:.1f}h ({wd_all}, 1 day = 8h)\n")
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
    total_active_all = sum(r.get("active_seconds", 0.0) for r in agg.values()) / 3600
    wd_all = _as_working_days(total_active_all)
    if wd_all:
        lines.append(f"_Total active: {total_active_all:.1f}h ({wd_all}, 1 day = 8h)_\n")
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


def render_recurring_painpoints_section(tasks: list[dict], since_ts: float | None,
                                        until_ts: float | None, html_mod) -> str:
    """Render the recurring-painpoints section for the HTML report.

    Splits the current horizon into time windows and compares them to surface
    pain points that keep coming back. Returns "" if no recurring painpoints
    found or the horizon is too short to split.
    """
    if not tasks or since_ts is None or until_ts is None:
        return ""
    horizon_days = int((until_ts - since_ts) / 86400)
    if horizon_days <= 1:
        return ""
    try:
        from recurring_painpoints import generate_recurring_painpoints
        insights = generate_recurring_painpoints(tasks, until_ts, horizon_days)
    except Exception:
        return ""
    if not insights:
        return ""
    cards = "\n".join(
        f'  <div class="painpoint-card">{html_mod.escape(ins)}</div>'
        for ins in insights
    )
    return f"""<h2>反复出现的痛点</h2>
<p class="hint">将本周期按时间窗口划分后对比，识别反复出现的时间消耗与问题。90d→月度对比，30d→周度对比，7d→日度对比。</p>
<div class="painpoints-grid">
{cards}
</div>"""


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
                f'<td colspan="3" class="no-data-msg">范围内无数据 — 数据源未激活或超出回溯范围</td>'
                f'</tr>'
            )
            continue
        starts = [t.get("start") or 0 for t in sk_tasks]
        earliest = min(starts)
        latest = max(starts)
        active_h = sum(t.get("active_seconds") or 0 for t in sk_tasks) / 3600
        wd = _as_working_days(active_h)
        e_str = _dt.fromtimestamp(earliest, tz=_tz.utc).strftime("%Y-%m-%d")
        l_str = _dt.fromtimestamp(latest, tz=_tz.utc).strftime("%Y-%m-%d")
        active_str = f"{active_h:.1f}h"
        if wd:
            active_str += f" ({wd})"
        rows.append(
            f'      <tr>'
            f'<td>{html_mod.escape(sk)}</td>'
            f'<td class="num">{len(sk_tasks)}</td>'
            f'<td class="num">{active_str}</td>'
            f'<td>{e_str}</td>'
            f'<td>{l_str}</td>'
            f'</tr>'
        )

    rows_html = "\n".join(rows)
    return f"""<h2>数据可用性</h2>
<p class="hint">请求范围：{html_mod.escape(range_label)}。Active 时间同时显示为工作日（1 天 = 8h）。每行显示该数据源在范围内的实际覆盖情况。</p>
<table class="data-avail">
  <thead><tr><th>数据源</th><th>任务数</th><th>Active</th><th>最早</th><th>最晚</th></tr></thead>
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

    # Compute actual working hours from human activity (not flat 8h/day).
    actual_working_hours = 0.0
    if tasks:
        try:
            from human_involvement import compute_actual_working_hours
            actual_working_hours = compute_actual_working_hours(tasks)
        except ImportError:
            pass

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
            hh = stats.get("human_seconds", 0.0) / 3600
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
                f'<td class="num">{hh:.1f}</td>'
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

    # --- Recurring painpoints section (cross-window comparison) ---
    recurring_painpoints_html = ""
    if tasks is not None and since_ts is not None and until_ts is not None:
        recurring_painpoints_html = render_recurring_painpoints_section(
            tasks, since_ts, until_ts, html_mod)

    # --- Insights cards ---
    insights_html = ""
    if tasks is not None:
        insights = generate_insights(tasks, agg)
        if insights:
            cards = "\n".join(
                f'  <div class="insight-card">{html_mod.escape(ins)}</div>'
                for ins in insights
            )
            insights_html = f"""<h2>洞察与痛点</h2>
<div class="insights-grid">
{cards}
</div>"""

    # --- Top tasks list (ranked by HUMAN engaged time, not raw active time) ---
    top_tasks_html = ""
    if tasks:
        def _human_engaged_h(t: dict) -> float:
            return (t.get("human_data") or {}).get("human_engaged_seconds", 0) or 0
        ranked = sorted(tasks, key=_human_engaged_h, reverse=True)
        # Filter to genuine time sinks only (rubric 54-60: forgotten/abandoned
        # sessions are NOT time sinks). Tasks without human_data are excluded.
        top10 = [t for t in ranked[:10]
                 if _human_engaged_h(t) > 0
                 and (t.get("human_data") or {}).get("is_genuine_time_sink", False)]
        if top10:
            # Compute per-type totals for percentage denominators (rubric 36):
            # h/H, a/A, w/W — each type's percentage is relative to its own total.
            total_human_h = sum(_human_engaged_h(t) for t in tasks) / 3600
            total_active_h = sum(t.get("active_seconds") or 0 for t in tasks) / 3600
            total_wall_h = sum(t.get("wall_clock_seconds") or 0 for t in tasks) / 3600
            rows = []
            for i, t in enumerate(top10, 1):
                act_h = (t.get("active_seconds") or 0) / 3600
                eng_h = _human_engaged_h(t) / 3600
                wall_h = (t.get("wall_clock_seconds") or 0) / 3600
                hd = t.get("human_data") or {}
                inv = hd.get("human_involvement", "?")
                kind = html_mod.escape(classify_task(t))
                subj = html_mod.escape((t.get("subject") or "(no subject)")[:55])
                start_str = _dt.fromtimestamp(t.get("start") or 0).strftime("%m-%d %H:%M")
                tid = html_mod.escape(t.get("id", "?"))
                color = kind_colors.get(classify_task(t), "#888")
                inv_class = f"inv-{inv}"
                why_html = render_structured_root_cause(t, html_mod)
                # Per-type percentages: h/H, a/A, w/W (rubric 36).
                h_pct = (eng_h / total_human_h * 100) if total_human_h > 0 else 0
                a_pct = (act_h / total_active_h * 100) if total_active_h > 0 else 0
                w_pct = (wall_h / total_wall_h * 100) if total_wall_h > 0 else 0
                rows.append(
                    f'      <tr>'
                    f'<td class="num">{i}</td>'
                    f'<td class="num">{eng_h:.1f}h</td>'
                    f'<td class="num">{h_pct:.1f}%</td>'
                    f'<td class="num">{act_h:.1f}h</td>'
                    f'<td class="num">{a_pct:.1f}%</td>'
                    f'<td class="num">{wall_h:.1f}h</td>'
                    f'<td class="num">{w_pct:.1f}%</td>'
                    f'<td class="num {inv_class}">{inv}</td>'
                    f'<td><span class="kind-dot" style="background:{color}"></span>{kind}</td>'
                    f'<td>{start_str}</td>'
                    f'<td>{subj}</td>'
                    f'<td class="why">{why_html}</td>'
                    f'<td class="task-id">{tid}</td>'
                    f'</tr>'
                )
            top_tasks_html = f"""<h2>Top 10 人工时间消耗</h2>
<p class="hint">三类时间：<strong>Wall</strong>（总时钟跨度）→ <strong>Active</strong>（检测到的工作）→ <strong>Human</strong>（用户参与）。百分比按类型计算：h/H, a/A, w/W。按 Human 时间排序。下钻：<code>python run.py --task &lt;id&gt; --drill</code></p>
<table class="top-tasks">
  <thead><tr><th>#</th><th>Human</th><th>%H</th><th>Active</th><th>%A</th><th>Wall</th><th>%W</th><th>参与度</th><th>类型</th><th>开始</th><th>主题</th><th>根因</th><th>Task ID</th></tr></thead>
  <tbody>
{chr(10).join(rows)}
  </tbody>
</table>"""

        # Low-engagement tasks: active time but NOT genuine time sinks.
        # These are likely forgotten tabs / abandoned sessions (rubric 54-60).
        low_eng = [t for t in tasks
                   if (t.get("human_data") or {}).get("is_genuine_time_sink") is False
                   and (t.get("active_seconds") or 0) > 3600]
        if low_eng:
            low_eng.sort(key=lambda t: t.get("active_seconds", 0), reverse=True)
            low_items = []
            for t in low_eng[:10]:
                act_h = (t.get("active_seconds") or 0) / 3600
                eng_h = _human_engaged_h(t) / 3600
                subj = html_mod.escape((t.get("subject") or "(no subject)")[:40])
                kind = html_mod.escape(classify_task(t))
                low_items.append(
                    f"<li><span class='num'>{act_h:.1f}h active</span> "
                    f"（Human {eng_h:.1f}h）{subj} [{kind}]</li>"
                )
            top_tasks_html += f"""
<h2>低参与度任务（非人工时间消耗）</h2>
<p class="hint">以下任务 active 时间较长但人工参与度低（<5次操作或<5分钟），可能为遗忘的标签页/会话，不属于真正的人工时间消耗。</p>
<ul class="kind-section ul">
{chr(10).join(low_items)}
</ul>"""

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
            kind_human = sum(
                (t.get("human_data") or {}).get("human_engaged_seconds", 0) or 0
                for t in by_kind_tasks[kind]
            ) / 3600
            kind_wd = _as_working_days(kind_active)
            color = kind_colors.get(kind, "#888")
            items = []
            for t in kind_tasks:
                act_h = (t.get("active_seconds") or 0) / 3600
                eng_h = ((t.get("human_data") or {}).get("human_engaged_seconds", 0) or 0) / 3600
                subj = html_mod.escape((t.get("subject") or "(no subject)")[:50])
                llm_label = t.get("llm_label")
                label_html = f' <span class="llm-label">{html_mod.escape(llm_label)}</span>' if llm_label else ''
                why_html = render_structured_root_cause(t, html_mod)
                why_div = f'<div class="why-inline">{why_html}</div>' if why_html else ''
                items.append(
                    f"<li><span class='num'>{eng_h:.1f}h Human</span> / "
                    f"<span class='num-act'>{act_h:.1f}h Active</span> {subj}{label_html}{why_div}</li>"
                )
            # For WeLink kind: append email items (0-duration but still work).
            # Emails are instantaneous events — they have no active time so they
            # never appear in the top-3-by-active list. Show them by count here
            # so the user sees their email activity in context.
            if kind == "WeLink":
                # Emails are 0-duration instantaneous events — show by count.
                # Include both Outlook and welink-cli emails (both source_kind=comm).
                email_tasks = [t for t in by_kind_tasks[kind]
                               if (t.get("context") or {}).get("comm_directions")
                               and not (t.get("context") or {}).get("im_message_count")]
                if email_tasks:
                    sent_count = 0
                    recv_count = 0
                    email_items = []
                    for t in email_tasks:
                        ctx = t.get("context") or {}
                        dirs = ctx.get("comm_directions", [])
                        subj = (t.get("subject") or "(no subject)")[:60]
                        if "sent" in dirs:
                            sent_count += 1
                            email_items.append(f"<li>📤 {html_mod.escape(subj)}</li>")
                        else:
                            recv_count += 1
                            email_items.append(f"<li>📥 {html_mod.escape(subj)}</li>")
                    more = (f'<li class="hint">…共 {len(email_tasks)} 封邮件</li>'
                            if len(email_items) > 15 else "")
                    items.append(
                        f'<li class="hint">邮件往来：收件 {recv_count} 封，'
                        f'发件 {sent_count} 封（瞬时事件，无持续时间）</li>'
                    )
                    items.extend(email_items[:15])
                    if more:
                        items.append(more)
            kind_total_str = f"Human {kind_human:.1f}h / Active {kind_active:.1f}h"
            if kind_wd:
                kind_total_str += f" · {kind_wd}"
            kind_sections.append(
                f'  <div class="kind-section">'
                f'<h3><span class="kind-dot" style="background:{color}"></span>'
                f'{html_mod.escape(kind)} <span class="kind-total">({kind_total_str}, {len(by_kind_tasks[kind])} tasks)</span></h3>'
                f'<ul>{"".join(items)}</ul>'
                f'</div>'
            )
        if kind_sections:
            kind_subjects_html = '<h2>各类工作内容</h2>\n' + \
                                 '<p class="hint">类型说明：coding=AI编程，planning=AI计划模式（EnterPlanMode），research=网页浏览/搜索，git=代码提交，meeting=会议，WeLink=邮件/聊天，file-edit=本地文件编辑，doc-edit=文档编辑（3ms/Wiki/W3），other=其他（AI讨论/任务管理/辅助日志等未分类活动）</p>\n' + \
                                 '<div class="kind-grid">\n' + \
                                 "\n".join(kind_sections) + '\n</div>'

    range_str = f"{periods[0]} — {periods[-1]}" if len(periods) > 1 else (periods[0] if periods else "n/a")

    # Working-day conversion for the summary header.
    # Use actual working hours (from human activity) if available, else 8h/day.
    wd_total = _as_working_days(total_active)
    human_engaged_total = sum(
        (t.get("human_data") or {}).get("human_engaged_seconds", 0) or 0
        for t in (tasks or [])
    ) / 3600
    working_basis = f"8h/day" if actual_working_hours <= 0 else f"{actual_working_hours:.0f}h actual"

    # Three-way time breakdown: wall → active → human, with percentages.
    # Per-type: human is % of active (nested), active is % of wall (rubric 36).
    human_pct_of_active = (human_engaged_total / total_active * 100) if total_active > 0 else 0
    active_pct_of_wall = (total_active / total_wall * 100) if total_wall > 0 else 0
    human_pct_of_wall = (human_engaged_total / total_wall * 100) if total_wall > 0 else 0

    # Chinese labels for the summary (rubric 38: output in Chinese, English where clear).
    wd_str = f"（{wd_total}）" if wd_total else ""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>时间报告（{html_mod.escape(granularity)}）</title>
<style>
  body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; margin: 2em; color: #2c2c2c; max-width: 1600px; }}
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
  .kind-section .num {{ font-weight: 600; color: #4e79a7; display: inline-block; width: 75px; }}
  .kind-section .num-act {{ font-weight: 600; color: #76b7b2; }}
  .kind-total {{ font-size: 0.85em; color: #888; font-weight: normal; }}
  .top-tasks td.why {{ font-size: 0.82em; color: #666; max-width: 560px; min-width: 300px; }}
  .why-inline {{ font-size: 0.85em; color: #888; margin-left: 56px; margin-top: 2px; }}
  .rc-part {{ margin: 2px 0; line-height: 1.4; }}
  .rc-label {{ font-weight: 600; color: #555; }}
  .rc-goal .rc-label {{ color: #4e79a7; }}
  .rc-struggle .rc-label {{ color: #c62828; }}
  .rc-detail .rc-label {{ color: #6a6a6a; }}
  .rc-pages .rc-label {{ color: #59a14f; }}
  .rc-evidence .rc-label {{ color: #b0791b; }}
  .rc-downloads .rc-label {{ color: #9c755f; }}
  .rc-time .rc-label {{ color: #76b7b2; }}
  .rc-content {{ color: #666; }}
  .llm-label {{ font-size: 0.8em; color: #7b57c7; background: #f3edf9; padding: 1px 6px; border-radius: 3px; margin-left: 4px; }}
  .wd-pct {{ font-size: 0.8em; color: #999; margin-left: 2px; }}
  .inv-high {{ color: #c62828; font-weight: 600; }}
  .inv-moderate {{ color: #e65100; font-weight: 600; }}
  .inv-low {{ color: #888; }}
  .inv-none {{ color: #bbb; font-style: italic; }}
  .data-avail {{ font-size: 0.88em; }}
  .data-avail .no-data {{ background: #fff8f8; }}
  .data-avail .no-data-msg {{ color: #c62828; font-style: italic; }}
  .section-divider {{ border: none; border-top: 2px solid #e0e0e0; margin: 2em 0; }}
  .painpoints-grid {{ display: grid; grid-template-columns: 1fr; gap: 10px; margin: 1em 0; }}
  .painpoint-card {{ background: #fff3e0; border-left: 4px solid #e15759; padding: 10px 14px; border-radius: 4px; font-size: 0.92em; line-height: 1.5; }}
</style>
</head>
<body>
<h1>时间报告（{html_mod.escape(granularity)}）</h1>
<div class="summary">
  <strong>范围：</strong>{html_mod.escape(range_str)} &nbsp;|&nbsp;
  <strong>Wall：</strong>{total_wall:.1f}h &nbsp;|&nbsp;
  <strong>Active：</strong>{total_active:.1f}h（占 Wall {active_pct_of_wall:.0f}%）{f" · {wd_total}" if wd_total else ""} &nbsp;|&nbsp;
  <strong>Human：</strong>{human_engaged_total:.1f}h（占 Active {human_pct_of_active:.0f}%，占 Wall {human_pct_of_wall:.0f}%） &nbsp;|&nbsp;
  <strong>任务数：</strong>{total_tasks}
</div>
<p class="hint">三类时间：<strong>Wall</strong>（总时钟跨度）→ <strong>Active</strong>（检测到的工作，占 Wall {active_pct_of_wall:.0f}%）→ <strong>Human</strong>（用户参与，占 Active {human_pct_of_active:.0f}%）。工作日基准：{working_basis}。时间消耗按 Human 时间排序。</p>

<hr class="section-divider">

{recurring_painpoints_html}

{top_tasks_html}

<hr class="section-divider">

{kind_subjects_html}

<hr class="section-divider">

<h2>按周期明细</h2>
<table>
  <thead>
    <tr><th>周期</th><th>类型</th><th>Wall(h)</th><th>Active(h)</th><th>Human(h)</th><th>%</th><th>任务数</th><th>成功率</th><th>未知%</th></tr>
  </thead>
  <tbody>
{table_rows_html}
  </tbody>
</table>

<h2>各类型 Active 时间</h2>
<div class="chart-container">
<svg width="{chart_width:.0f}" height="{chart_height}" xmlns="http://www.w3.org/2000/svg">
{svg_content}
</svg>
<div class="legend">
{legend_html}
</div>
</div>

<hr class="section-divider">

{insights_html}

<hr class="section-divider">

{data_avail_html}

</body>
</html>"""
    return html


def render_context_text(task: dict) -> str:
    """Render task['context'] as a human-readable 'why this took as long as it did' block.

    Returns a multi-line string (without a header), or '' if no context is available.
    Used by render_task_detail(), the drill-down lead-off, and the insight lines.

    When a content-driven ``narrative`` is available, it leads the section —
    followed by the structured signals (organizer, files, queries, etc.) as
    supporting detail.
    """
    ctx = task.get("context") or {}
    if not ctx:
        return ""
    lines: list[str] = []

    # Lead with the content-driven narrative (the grounded root-cause story).
    narrative = ctx.get("narrative")
    if narrative:
        lines.append(narrative)
        lines.append("")  # blank line before structured detail

    # Human involvement — is this a real human time sink or autonomous machine work?
    human_data = task.get("human_data")
    if human_data:
        from human_involvement import describe_human_involvement
        human_desc = describe_human_involvement(human_data, task)
        if human_desc:
            lines.append(f"Human involvement: {human_desc}")
            lines.append("")

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
        im_count = ctx.get("im_message_count") or 0
        im_conversations = ctx.get("im_conversations") or []
        im_senders = ctx.get("im_senders") or []
        if subjects:
            lines.append(f"Threads: {', '.join(subjects[:3])}")
        if senders:
            lines.append(f"From: {', '.join(senders[:3])}")
        if has_reply:
            lines.append("Reply sent in thread")
        else:
            if not im_count:
                lines.append("No reply detected")
        if im_count:
            lines.append(f"IM: {im_count} message(s) in {len(im_conversations)} conversation(s)")
            if im_conversations:
                lines.append(f"  Conversations: {', '.join(im_conversations[:3])}")
            if im_senders:
                lines.append(f"  Senders: {', '.join(im_senders[:3])}")

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


def render_structured_root_cause(task: dict, html_mod) -> str:
    """Render the root cause as structured HTML with labeled sections.

    Breaks the narrative into:
      - Goal: what the user was trying to do
      - Struggle: what went wrong and why it was hard (merged)
      - Detail: supporting content (per-page breakdown, downloads, etc.)
      - Pages: list of visited pages
      - Evidence: verbatim command/error/message evidence
      - Downloads: files downloaded during browsing
      - Time: where the time went (active vs wall vs idle)

    Falls back to render_context_inline (escaped) when no structured parts
    can be extracted.
    """
    ctx = task.get("context") or {}
    narrative = ctx.get("narrative")
    if not narrative:
        line = render_context_inline(task)
        return html_mod.escape(line) if line else ""

    # The narrative uses labeled sentences: "Goal: ...", "Struggle: ...", "Time: ..."
    # Split on both English (.!?) and Chinese (。！？) sentence boundaries.
    parts: list[tuple[str, str]] = []  # (label, content)

    sentences = re.split(r'(?<=[.!?。！？])\s+', narrative)

    current_label = ""
    current_content: list[str] = []

    def _flush():
        nonlocal current_label, current_content
        if current_label and current_content:
            parts.append((current_label, " ".join(current_content)))
        elif current_content:
            if parts:
                label, prev = parts[-1]
                parts[-1] = (label, prev + " " + " ".join(current_content))
            else:
                parts.append(("Summary", " ".join(current_content)))
        current_label = ""
        current_content = []

    for sent in sentences:
        s = sent.strip()
        if not s:
            continue
        # Detect labeled sentences.
        if s.startswith("Goal:"):
            _flush()
            current_label = "Goal"
            current_content = [s[len("Goal:"):].strip().rstrip(".。")]
        elif s.startswith("Struggle:"):
            _flush()
            current_label = "Struggle"
            current_content = [s[len("Struggle:"):].strip().rstrip(".。")]
        elif s.startswith("Key failure:"):
            _flush()
            current_label = "Struggle"
            current_content = [s[len("Key failure:"):].strip().rstrip(".。")]
        elif s.startswith("Failed:"):
            _flush()
            current_label = "Struggle"
            current_content = [s[len("Failed:"):].strip().rstrip(".。")]
        elif s.startswith("Difficulty:"):
            _flush()
            current_label = "Struggle"
            current_content = [s[len("Difficulty:"):].strip().rstrip(".。")]
        elif s.startswith("Blocker:"):
            _flush()
            current_label = "Struggle"
            current_content = [s[len("Blocker:"):].strip().rstrip(".。")]
        elif s.startswith("Detail:"):
            _flush()
            current_label = "Detail"
            current_content = [s[len("Detail:"):].strip().rstrip(".。")]
        elif s.startswith("Pages:"):
            _flush()
            current_label = "Pages"
            current_content = [s[len("Pages:"):].strip().rstrip(".。")]
        elif s.startswith("Evidence:"):
            _flush()
            current_label = "Evidence"
            current_content = [s[len("Evidence:"):].strip().rstrip(".。")]
        elif s.startswith("Downloads:"):
            _flush()
            current_label = "Downloads"
            current_content = [s[len("Downloads:"):].strip().rstrip(".。")]
        elif s.startswith("Also:"):
            current_content.append(s[len("Also:"):].strip().rstrip(".。"))
        elif s.startswith("Retried"):
            current_content.append(s.rstrip(".。"))
        elif re.match(r'^[\d.]+h[\s，。]', s):
            _flush()
            current_label = "Time"
            current_content = [s.rstrip(".。")]
        else:
            current_content.append(s.rstrip(".。"))
    _flush()

    if not parts:
        return html_mod.escape(narrative)

    # Render as structured HTML divs.
    label_icons = {
        "Goal": "🎯",
        "Struggle": "⚠️",
        "Detail": "📝",
        "Pages": "🌐",
        "Evidence": "🔍",
        "Downloads": "📥",
        "Time": "⏱️",
        "Summary": "📋",
    }
    # Chinese labels (rubric 38: output in Chinese, English where clear).
    label_cn = {
        "Goal": "目标",
        "Struggle": "困难",
        "Detail": "详情",
        "Pages": "页面",
        "Evidence": "证据",
        "Downloads": "下载",
        "Time": "时间",
        "Summary": "概要",
    }
    divs = []
    for label, content in parts:
        icon = label_icons.get(label, "•")
        cn = label_cn.get(label, label)
        divs.append(
            f'<div class="rc-part rc-{label.lower()}">'
            f'<span class="rc-label">{icon} {html_mod.escape(cn)}:</span> '
            f'<span class="rc-content">{html_mod.escape(content)}</span>'
            f'</div>'
        )
    return "".join(divs)


def render_context_inline(task: dict) -> str:
    """One-line root-cause explanation for the 'why' column and insight lines.

    Diagnoses WHY the task took as long as it did by comparing active vs wall
    time and identifying the inflation pattern. Returns a single string, or ''.

    The principle: if active ≈ wall, it's genuine work — show what the work was.
    If active << wall, explain where the time went (idle gaps, overnight tabs,
    all-day marker, multi-day cap).

    When a content-driven ``narrative`` is available (from summarize.py), that
    is used directly — it is grounded in the actual event text (prompts,
    assistant diagnostics, errors, page titles) and far more informative than
    a pattern-bucket label.
    """
    ctx = task.get("context") or {}
    # Prefer the content-driven narrative when available.
    narrative = ctx.get("narrative")
    if narrative:
        return narrative
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
