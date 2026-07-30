#!/usr/bin/env python3
"""huawei-retro-scope — single CLI entrypoint for the full pipeline.

Runs: collect (via registry) → segment → aggregate → report.

Usage:
    python run.py --granularity week
    python run.py --granularity day --json
    python run.py --granularity month --since 2026-07-01 --until 2026-07-31
    python run.py --granularity week --format table
    python run.py --granularity week --format markdown --output report.md
    python run.py --granularity week --output report.html   # format inferred from .html
    python run.py --sources          # list detected + skipped sources
    python run.py --check            # verify environment + adapters, no analysis
    python run.py --task <id> --drill  # root-cause drill-down on one task (Phase 10.2)

Flags:
    --granularity {day,week,month,year}   aggregation period (default: week)
    --format {text,table,markdown,html,json}  output format (default: text)
    --json                                emit raw JSON (equivalent to --format json; takes precedence)
    --output <path>                       write report to file instead of stdout (format inferred from extension if --format not given)
    --since YYYY-MM-DD                    only include tasks starting on/after this date
    --until YYYY-MM-DD                    only include tasks starting on/before this date
    --sources                             report which sources were found/used/skipped, then exit
    --check                               environment + adapter check, then exit
    --rebuild                             ignore any watermark, do full reparse (Phase 2 placeholder)
    --eval                                run segmentation evaluation against the labeled benchmark (Phase 9.8)
    --task <id>                           show full detail for a single task
    --drill                               with --task: stage-by-stage root-cause analysis (Phase 10.2)
"""

from __future__ import annotations

import sys
import os
import json
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sources import default_registry
from segment_tasks import segment
from aggregate import aggregate, render_report, render_markdown, render_table, render_html


def _parse_date(s: str) -> float:
    """Parse YYYY-MM-DD to epoch seconds (UTC start of day)."""
    dt = datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.timestamp()


def _remap_task_ids(tasks: list[dict]) -> list[dict]:
    """Assign stable task IDs that survive across incremental runs.

    C7 fix: segment_tasks.py generates IDs like ``explicit-N`` and ``implicit-N``
    where N is re-numbered from 1 on each run. In incremental mode this causes
    ID collisions — an unrelated task in run 2 gets the same ID as a task in run 1,
    silently overwriting it in ``save_tasks(mode='merge')``.

    New format: ``{flavor}-{session_id}-{start_timestamp}``.
    For tasks without a session_id: ``{flavor}-nosession-{start_timestamp}``.
    Tasks created by parallel_tasks.py (background, browser_research) and other
    flavors already have unique-ish IDs; we only remap explicit/implicit ones.
    """
    for t in tasks:
        flavor = t.get("flavor", "")
        if flavor in ("explicit", "implicit"):
            sid = t.get("session_id") or "nosession"
            start = int(t.get("start") or 0)
            t["id"] = f"{flavor}-{sid}-{start}"
    return tasks


def _filter_tasks_by_watermark(tasks: list[dict], watermark: float) -> list[dict]:
    """Keep only tasks that have at least one event with timestamp > watermark.

    C7 fix: in incremental mode, collect_since() now yields ALL events from sessions
    that have any post-watermark event. This means segment() may produce tasks that
    are entirely before the watermark (already processed in a prior run). Filter
    them out here so they aren't re-persisted or double-counted.
    """
    result = []
    for t in tasks:
        start = t.get("start") or 0
        end = t.get("end") or start
        # A task overlaps the post-watermark window if its end > watermark.
        # (start <= watermark is fine — the task spans the boundary.)
        if end > watermark:
            result.append(t)
    return result


def _events_for_task(task: dict, all_events: list[dict]) -> list[dict]:
    """Reconstruct the events belonging to a task.

    segment() doesn't attach events to task dicts — it only stores aggregates.
    For drill-down we need the raw events. Match by session_id + time range;
    if no session_id, match by time range alone (less precise but workable).

    For zero-length background tasks (start == end, from parallel_tasks.py),
    widen the window to the session's max timestamp so we capture the full
    event stream. If the session max can't be determined, fall back to a
    4-hour window after start as a reasonable bound.
    """
    start = task.get("start") or 0
    end = task.get("end") or (task.get("wall_clock_seconds") and start + task["wall_clock_seconds"]) or start
    session_id = task.get("session_id")
    source = task.get("source")

    # C6 fix: zero-length background tasks (start == end) get a widened window.
    zero_length = end <= start
    if zero_length:
        if session_id:
            # Scan all_events for the max timestamp in the same session.
            session_max = start
            for e in all_events:
                if e.get("session_id") == session_id:
                    ts = e.get("timestamp") or 0
                    if ts > session_max:
                        session_max = ts
            end = session_max
        else:
            # No session_id — fall back to a 4-hour window.
            end = start + 4 * 3600

    result = []
    for e in all_events:
        ts = e.get("timestamp") or 0
        if ts < start or ts > end + 1:
            continue
        if session_id and e.get("session_id") and e["session_id"] != session_id:
            continue
        if source and e.get("source") and e["source"] != source:
            # Allow cross-source events (e.g. git commits linked to a coding task)
            # but prefer same-source. Keep all for now — drill_down can filter.
            pass
        result.append(e)
    return result


def _render_drill_down(result: dict, task: dict) -> str:
    """Render a stage-by-stage root-cause drill-down (Phase 10.2)."""
    from datetime import datetime as _dt
    lines = []
    subj = task.get("subject") or "(no subject)"
    lines.append(f"# Drill-down: {subj}")
    lines.append("")
    act_h = (result.get("total_active_seconds") or 0) / 3600
    wall_h = (result.get("total_wall_seconds") or 0) / 3600
    lines.append(f"Active: {act_h:.1f}h | Wall: {wall_h:.1f}h | "
                 f"Stages: {len(result.get('stages', []))}")
    lines.append("")

    # C6 fix: warn when the task has zero events or zero stages so that "no data"
    # is distinguishable from "no problems."
    event_count = len(task.get("events") or [])
    stage_count = len(result.get("stages") or [])
    if event_count == 0 or stage_count == 0:
        lines.append("WARNING: this task has unknown duration (zero-length background task).")
        lines.append("Event reconstruction may be incomplete — the analysis below is based on limited data.")
        lines.append("")

    # Narrative
    narrative = result.get("narrative")
    if narrative:
        lines.append(f"> {narrative}")
        lines.append("")

    # Stage-by-stage timeline
    markers = result.get("all_markers", [])
    lines.append("## Stages")
    lines.append(f"{'#':>2} {'Start':<17} {'Wall':>7} {'Active':>7} {'Events':>7}  "
                 f"{'Summary'}")
    lines.append("-" * 80)
    for stage in result.get("stages", []):
        idx = stage.get("stage_idx", 0)
        start_ts = stage.get("start", 0)
        start_str = _dt.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M") if start_ts else "?"
        wall = (stage.get("duration_seconds") or 0) / 60
        act = (stage.get("active_seconds") or 0) / 60
        ev = stage.get("event_count", 0)
        summary = stage.get("summary", "")[:50]
        lines.append(f"{idx:>2} {start_str:<17} {wall:>6.0f}m {act:>6.0f}m {ev:>7}  {summary}")
        # Inline markers for this stage
        for m in stage.get("markers", []):
            mtype = m.get("type", "")
            msg = m.get("message", "")
            lines.append(f"     ↳ [{mtype}] {msg}")

    # All markers summary
    if markers:
        lines.append("")
        lines.append(f"## Root-cause markers ({len(markers)} total)")
        for m in markers:
            lines.append(f"  - [{m.get('type')}] {m.get('message')}")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        prog="run.py",
        description="huawei-retro-scope: retrospective task & time reconstruction.",
    )
    ap.add_argument("--granularity", choices=["day", "week", "month", "year"],
                    default="week")
    ap.add_argument("--json", action="store_true", help="emit raw JSON instead of text report (equivalent to --format json)")
    ap.add_argument("--format", choices=["text", "table", "markdown", "html", "json"],
                    default=None, help="output format (default: text; --json overrides to json)")
    ap.add_argument("--output", default=None,
                    help="write report to this file instead of stdout (format inferred from extension if --format not given)")
    ap.add_argument("--since", help="only include tasks starting on/after this date (YYYY-MM-DD)")
    ap.add_argument("--until", help="only include tasks starting on/before this date (YYYY-MM-DD)")
    ap.add_argument("--sources", action="store_true",
                    help="report which sources were found/used/skipped, then exit")
    ap.add_argument("--check", action="store_true",
                    help="verify environment + adapters, then exit (no analysis)")
    ap.add_argument("--rebuild", action="store_true",
                    help="ignore watermark, do full reparse (overrides incremental)")
    ap.add_argument("--persist", action="store_true",
                    help="save reconstructed tasks to data/tasks.jsonl (merged with prior)")
    ap.add_argument("--task", help="show full detail for a single task by id (e.g. explicit-<session_id>-<timestamp>)")
    ap.add_argument("--drill", action="store_true",
                    help="with --task: stage-by-stage root-cause analysis (Phase 10.2)")
    ap.add_argument("--eval", action="store_true",
                    help="run segmentation evaluation against the labeled benchmark (Phase 9.8)")
    args = ap.parse_args()

    # Two-pass collection: first collect AI-session events to discover project cwds,
    # then build the registry with those cwds so the git adapter finds the right repos.
    from claude_code_adapter import ClaudeCodeAdapter
    from git_adapter import GitAdapter, discover_git_roots

    ai_adapter = ClaudeCodeAdapter()
    session_cwds: list[str] = []
    if ai_adapter.detect():
        ai_events = list(ai_adapter.collect())
        session_cwds = sorted({e.get("cwd") for e in ai_events if e.get("cwd")})

    reg = default_registry(session_cwds=session_cwds)

    # --eval: run segmentation evaluation against the labeled benchmark, then exit.
    if args.eval:
        from eval_segmentation import run_eval, format_metrics_report
        metrics = run_eval()
        print(format_metrics_report(metrics))
        sys.exit(0)

    # --check: verify adapters detect, report status, exit.
    if args.check:
        print("# huawei-retro-scope environment check")
        for adapter in reg._adapters:
            try:
                ok = adapter.detect()
            except Exception as e:
                ok = False
                print(f"  {adapter.name:20s} ERROR: {e}")
                continue
            print(f"  {adapter.name:20s} {'OK' if ok else 'not detected'}")
        sys.exit(0)

    # Collect events — incremental if watermark exists and --rebuild not set.
    from persistence import read_watermark, write_watermark, save_tasks

    watermark = None if args.rebuild else read_watermark()
    if watermark:
        # Incremental: only events after the watermark.
        # For the two-pass git discovery, we still need session cwds — collect those
        # from the full AI history (cheap, just the cwd field) even in incremental mode.
        events, skipped = reg.collect_all(watermark=watermark)
        # Also include any git commits after the watermark.
        # (The registry already handles this via collect_since on each adapter.)
    else:
        events, skipped = reg.collect_all()

    # --sources: report found/used/skipped, then exit.
    if args.sources:
        detected = [a.name for a in reg.detected()]
        print("# Sources")
        print(f"  detected: {detected}")
        print(f"  skipped:  {skipped}")
        # IM-honesty: welink-cli is the only source of WeLink chat history; no local
        # store exists (verified: 52 WeLink Desktop .db files, zero message tables).
        # Surface this plainly rather than silently dropping the chat category.
        welink_detected = any(a.name == "welink_cli" for a in reg.detected())
        if not welink_detected:
            print("")
            print("  NOTE: welink-cli not detected.")
            print("    - IM/chat history is UNAVAILABLE. WeLink stores no messages locally;")
            print("      welink-cli is the only path to chat data. This category is skipped,")
            print("      not silently dropped.")
            print("    - Meetings/calendar/mail have backup routes (see SKILL.md")
            print("      'Data sources without welink-cli'). Recordings, .ics export, and")
            print("      Outlook OST provide partial-to-full coverage of those domains.")
        sys.exit(0)

    # Segment into tasks.
    try:
        tasks = segment(events)
    except Exception as e:
        print(f"[segment] stage failed: {e}", file=sys.stderr)
        print("[segment] continuing with empty task list.", file=sys.stderr)
        tasks = []

    # C7 fix: assign stable task IDs that survive across incremental runs.
    # The segment() function generates ephemeral IDs (explicit-N/implicit-N) that
    # are re-numbered from 1 each run, causing merge collisions. Remap to stable
    # IDs based on session_id + start timestamp.
    tasks = _remap_task_ids(tasks)

    # C7 fix: in incremental mode, collect_since() now yields ALL events from
    # sessions with any post-watermark event. Filter out tasks that are entirely
    # before the watermark (already processed in a prior run).
    if watermark:
        tasks = _filter_tasks_by_watermark(tasks, watermark)

    # Cross-source linking: naive commit attachment (Phase 1.4) + entity resolution (Phase 4.4).
    from cross_source import link_commits_to_tasks
    commit_events = [e for e in events if e.get("kind") == "commit"]
    try:
        tasks = link_commits_to_tasks(tasks, commit_events)
    except Exception as e:
        print(f"[cross_source] stage failed: {e}", file=sys.stderr)
        print("[cross_source] continuing with unlinked tasks.", file=sys.stderr)
    # Phase 4.4: probabilistic cross-source identity via Leiden graph clustering.
    try:
        from entity_resolution import resolve_cross_source_tasks
        tasks = resolve_cross_source_tasks(tasks)
    except ImportError:
        pass  # igraph unavailable — skip, naive linking stands
    except Exception as e:
        print(f"[entity_resolution] stage failed: {e}", file=sys.stderr)
        print("[entity_resolution] continuing with pre-resolution tasks.", file=sys.stderr)

    # Phase 10.1: detect parallel tasks (background sub-agents, concurrent sessions,
    # browser-during-coding) and compute exclusive time (non-overlapping union).
    exclusive = None
    try:
        from parallel_tasks import detect_parallel_tasks, compute_exclusive_time
        tasks = detect_parallel_tasks(tasks, events)
        exclusive = compute_exclusive_time(tasks)
    except ImportError:
        exclusive = None
    except Exception as e:
        print(f"[parallel_tasks] stage failed: {e}", file=sys.stderr)
        print("[parallel_tasks] continuing with pre-parallel tasks.", file=sys.stderr)

    # Phase 10.3: refine three-valued success using cross-task context (commit landed,
    # research followed by artifact, meeting followed by action, etc.).
    # Runs AFTER detect_parallel_tasks so that new background/browser tasks (which
    # have success=None) also get refined. Normalize None -> SUCCESS_UNKNOWN first
    # so refine_success's guard processes them.
    from segment_tasks import refine_success, SUCCESS_UNKNOWN
    for t in tasks:
        if t.get("success") is None:
            t["success"] = SUCCESS_UNKNOWN
    try:
        tasks = refine_success(tasks)
    except Exception as e:
        print(f"[refine_success] stage failed: {e}", file=sys.stderr)
        print("[refine_success] continuing with pre-refined success values.", file=sys.stderr)

    # Filter by --since / --until.
    if args.since:
        since_ts = _parse_date(args.since)
        tasks = [t for t in tasks if (t.get("start") or 0) >= since_ts]
    if args.until:
        until_ts = _parse_date(args.until) + 86400  # end of day
        tasks = [t for t in tasks if (t.get("start") or 0) <= until_ts]

    # --task: show single task detail, then exit.
    if args.task:
        from aggregate import render_task_detail
        match = [t for t in tasks if t.get("id") == args.task]
        if not match:
            # also try partial match
            match = [t for t in tasks if args.task in (t.get("id") or "")]
        if match:
            task = match[0]
            if args.drill:
                # Phase 10.2: stage-by-stage root-cause analysis.
                # segment() doesn't attach the events list to task dicts, so we
                # reconstruct it from the raw events by matching session + time range.
                from drill_down import drill_down
                task_events = _events_for_task(task, events)
                task_with_events = {**task, "events": task_events}
                result = drill_down(task_with_events)
                print(_render_drill_down(result, task_with_events))
            else:
                print(render_task_detail(task))
        else:
            print(f"No task found matching '{args.task}'. "
                  f"Try one of: {', '.join(t['id'] for t in tasks[:10])}...")
        sys.exit(0)

    # Aggregate.
    try:
        agg = aggregate(tasks, args.granularity)
    except Exception as e:
        print(f"[aggregate] stage failed: {e}", file=sys.stderr)
        print("[aggregate] falling back to trivial aggregate (task count by kind).", file=sys.stderr)
        from collections import Counter
        kind_counts = Counter(t.get("source_kind", "unknown") for t in tasks)
        agg = {"_fallback": True, "task_count": len(tasks),
               "kinds": dict(kind_counts)}

    # Persist tasks if requested.
    if args.persist:
        save_tasks(tasks, mode="merge")
        write_watermark()

    # Report.
    # Determine format: --json takes precedence (backwards compat), then --format,
    # then default "text".
    if args.json:
        fmt = "json"
    elif args.format:
        fmt = args.format
    else:
        fmt = "text"

    # If --output is given without --format, infer from extension.
    if args.output and not args.format and not args.json:
        ext = os.path.splitext(args.output)[1].lower()
        if ext == ".md":
            fmt = "markdown"
        elif ext == ".html" or ext == ".htm":
            fmt = "html"
        elif ext == ".json":
            fmt = "json"
        # else: fall through to "text"

    def _exclusive_footer() -> str:
        """Build a one-line footer summarising exclusive time, or '' if unavailable."""
        if not exclusive:
            return ""
        excl_h = exclusive["exclusive_seconds"] / 3600
        wall_h = exclusive["wall_span_seconds"] / 3600
        overlap_h = exclusive["overlap_seconds"] / 3600
        return (f"\n(exclusive time: {excl_h:.1f}h "
                f"(wall span {wall_h:.1f}h, overlap {overlap_h:.1f}h, "
                f"{exclusive['n_parallel_groups']} parallel group(s)))")

    def _render() -> str:
        """Produce the report string for the chosen format."""
        if fmt == "json":
            out = {"granularity": args.granularity, "aggregation": agg,
                   "source_count": len(reg.detected()), "skipped": skipped,
                   "task_count": len(tasks)}
            if exclusive:
                out["exclusive_time"] = exclusive
            return json.dumps(out, ensure_ascii=False, indent=2)
        elif fmt == "table":
            return render_table(agg, args.granularity)
        elif fmt == "markdown":
            text = render_markdown(agg, args.granularity)
            return text + _exclusive_footer()
        elif fmt == "html":
            text = render_html(agg, args.granularity, tasks=tasks)
            footer = _exclusive_footer().strip()
            if footer:
                # Insert before </body> if present, else append.
                if "</body>" in text:
                    text = text.replace("</body>", f"<p>{footer}</p>\n</body>")
                else:
                    text += f"\n<p>{footer}</p>"
            return text
        else:
            text = render_report(agg, args.granularity)
            if skipped:
                text += f"\n(skipped sources: {skipped})"
            text += _exclusive_footer()
            return text

    if args.output:
        try:
            content = _render()
        except Exception as e:
            print(f"[render] stage failed: {e}", file=sys.stderr)
            print("[render] falling back to raw JSON output.", file=sys.stderr)
            content = json.dumps(agg, ensure_ascii=False, indent=2)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
            if not content.endswith("\n"):
                f.write("\n")
    else:
        try:
            print(_render())
        except Exception as e:
            print(f"[render] stage failed: {e}", file=sys.stderr)
            print("[render] falling back to raw JSON output.", file=sys.stderr)
            print(json.dumps(agg, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
