"""Recurring time-consumption detection across time windows within a single horizon.

The second thing huawei-retro-scope reports (after absolute time sinks): time
consumption patterns that keep coming back across time windows. A 30d report is split
into 4 weekly windows; if the same task subject is a top-5 time sink in 3 of those 4
weeks, that's a recurring time consumption — worth examining, not necessarily painful.

IMPORTANT: high or recurring human time investment does NOT imply the user was
suffering. A 3h deep coding session might be flow state; a weekly code review might
be valuable routine. This module surfaces observable time-consumption patterns and
lets the user decide what to do about them. The "automation candidate" label is a
suggestion based on recurrence + errors, not a conclusion that the work was painful.

This module is a pure function of the already-collected task list. No persistence, no
state across runs — every ``python run.py`` recomputes from current data. (Retro-scope's
sources are persistent: JSONL sessions, git history, browser DB, OST. A 30d report
already holds 30 days of tasks; splitting them into windows is trivially cheap.)

Window splitting by horizon:
    90d → 3 monthly windows  (month-over-month)
    30d → 4 weekly windows   (week-over-week)
    7d  → 7 daily windows     (day-over-day)
    1d  → single window       (no comparison possible — returns [])

Insight types:
    1. Persistent: same subject in top 5 of ≥2 windows (not necessarily consecutive)
    2. Declining: top sink in earlier windows, gone from the latest
    3. Increasing: human hours on a kind increased ≥50% earliest→latest
    4. Automation candidate: recurrent (≥2 windows) + high error count (≥3 avg)
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from collections import defaultdict


def split_into_windows(tasks: list[dict], end_ts: float,
                       horizon_days: int) -> list[tuple[str, list[dict]]]:
    """Split tasks into time windows for recurring time-consumption comparison.

    Returns a list of (window_label, window_tasks) pairs, oldest first.
    Returns [] if the horizon is too short to split (1d) or if there are
    fewer than 2 windows with data.
    """
    if horizon_days <= 1:
        return []

    # Choose window size: daily for 7d, weekly for 30d, monthly for 90d+.
    if horizon_days <= 7:
        window_days = 1
        label_fmt = "%m-%d"
    elif horizon_days <= 30:
        window_days = 7
        label_fmt = "%m-%d"
    else:
        window_days = 30
        label_fmt = "%Y-%m"

    n_windows = horizon_days // window_days
    if n_windows < 2:
        return []

    windows: list[tuple[str, list[dict]]] = []
    for i in range(n_windows):
        w_end = end_ts - i * window_days * 86400
        w_start = w_end - window_days * 86400
        w_tasks = [t for t in tasks
                   if w_start < (t.get("start") or 0) <= w_end]
        label = datetime.fromtimestamp(w_start, tz=timezone.utc).strftime(label_fmt)
        windows.append((label, w_tasks))

    # Reverse to oldest-first for natural comparison.
    windows.reverse()
    # Drop empty windows from the ends only — interior gaps are kept (a gap
    # in the middle is itself information).
    while windows and not windows[0][1]:
        windows.pop(0)
    while windows and not windows[-1][1]:
        windows.pop()

    if len(windows) < 2:
        return []
    return windows


def _human_engaged_h(task: dict) -> float:
    """Human engaged hours for a task (0 if no human_data)."""
    hd = task.get("human_data") or {}
    return (hd.get("human_engaged_seconds") or 0) / 3600


def _normalize_subject(subject: str | None) -> str:
    """Normalize a task subject for cross-window matching.

    Strips timestamps, session IDs, truncation markers, and whitespace so that
    the same task in different windows can be recognized.
    """
    if not subject:
        return ""
    s = subject.strip()
    # Strip leading/trailing punctuation that varies by truncation.
    s = s.strip("—-:|…")
    # Remove timestamps like "2026-07-30 14:32" or "07-30 14:32".
    s = re.sub(r'\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}(:\d{2})?', '', s)
    s = re.sub(r'\d{2}-\d{2}\s+\d{2}:\d{2}', '', s)
    # Remove hex/uuid-like tokens (session IDs in subjects).
    s = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '', s)
    s = re.sub(r'\b[0-9a-f]{12,}\b', '', s)
    # Remove trailing task IDs like "explicit-123" or "implicit-456".
    s = re.sub(r'\b(explicit|implicit|background|browser)-\d+\b', '', s)
    # Collapse whitespace and lowercase.
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s


def _window_summary(tasks: list[dict]) -> dict:
    """Compute top-5 sinks + totals for one window.

    Only tasks with genuine HUMAN engagement qualify as time-consumption
    candidates — a 10h autonomous agent run with 2 prompts did NOT meaningfully
    consume the user's time (rubrics 5, 54-60). The minimum threshold is 10 minutes
    of human engaged time; below that the task didn't meaningfully
    cost the user effort.

    Returns:
        top_sinks: list of {subject, norm_subject, kind, human_h, errors}
        total_human_h: float
    """
    # Rank by human engaged time (consistent with the main report's ranking).
    # Exclude tasks below the human-engagement minimum — they didn't consume real human time.
    MIN_HUMAN_H = 10 / 60  # 10 minutes
    ranked = sorted(tasks, key=_human_engaged_h, reverse=True)
    top_sinks = []
    for t in ranked[:5]:
        if _human_engaged_h(t) < MIN_HUMAN_H:
            continue
        subj = t.get("subject") or "(no subject)"
        kind = t.get("source_kind") or "unknown"
        top_sinks.append({
            "subject": subj,
            "norm_subject": _normalize_subject(subj),
            "kind": kind,
            "human_h": _human_engaged_h(t),
            "errors": t.get("errors") or 0,
        })

    total_human_h = sum(_human_engaged_h(t) for t in tasks)

    return {
        "top_sinks": top_sinks,
        "total_human_h": total_human_h,
    }


def generate_recurring_painpoints(tasks: list[dict], end_ts: float,
                                  horizon_days: int) -> list[str]:
    """Compare time windows within the current horizon.

    Returns a list of insight strings (Chinese per rubric 38).
    Empty list if <2 windows, too few tasks, or no recurring time consumption found.
    """
    windows = split_into_windows(tasks, end_ts, horizon_days)
    if not windows:
        return []

    total_tasks = sum(len(wt) for _, wt in windows)
    if total_tasks < 4:
        return []

    summaries = [(label, _window_summary(wt)) for label, wt in windows]
    window_labels = [label for label, _ in summaries]
    insights: list[str] = []

    # --- 1. Persistent time consumption ---
    # A normalized subject appearing in top-5 of ≥2 windows.
    subject_windows: dict[str, list[int]] = defaultdict(list)
    subject_info: dict[str, dict] = {}  # latest display info per norm_subject

    for i, (_, summ) in enumerate(summaries):
        for sink in summ["top_sinks"]:
            ns = sink["norm_subject"]
            if not ns or ns == "(no subject)":
                continue
            subject_windows[ns].append(i)
            subject_info[ns] = sink

    persistent_sinks = []
    for ns, w_indices in subject_windows.items():
        if len(w_indices) >= 2:
            # Sum human hours and errors across all windows where this subject appeared.
            total_human = 0.0
            total_errors = 0
            for idx in w_indices:
                for sink in summaries[idx][1]["top_sinks"]:
                    if sink["norm_subject"] == ns:
                        total_human += sink["human_h"]
                        total_errors += sink["errors"]
            persistent_sinks.append({
                "subject": subject_info[ns]["subject"],
                "kind": subject_info[ns]["kind"],
                "windows_count": len(w_indices),
                "total_human_h": total_human,
                "total_errors": total_errors,
                "window_labels": [window_labels[idx] for idx in w_indices],
            })

    persistent_sinks.sort(key=lambda c: c["total_human_h"], reverse=True)
    for c in persistent_sinks[:3]:
        windows_str = "、".join(c["window_labels"])
        insight = (f"⏰ 持续性时间消耗：'{c['subject'][:50]}' 在 {c['windows_count']} 个时间窗口"
                   f"（{windows_str}）中均位居时间消耗前列，累计 {c['total_human_h']:.1f}h 人工时间")
        if c["total_errors"] > 0:
            insight += f"，共 {c['total_errors']} 个错误"
        insight += "——这是反复出现的时间消耗，建议审视是否可自动化。"
        insights.append(insight)

    # --- 2. Declining time consumption ---
    # Top sink in ≥2 earlier windows that's absent from the latest window's top 5.
    if len(summaries) >= 3:
        latest_top_norms = {s["norm_subject"]
                           for s in summaries[-1][1]["top_sinks"]}
        for ns, info in subject_info.items():
            if ns in latest_top_norms:
                continue
            earlier_count = sum(
                1 for i in range(len(summaries) - 1)
                if any(s["norm_subject"] == ns for s in summaries[i][1]["top_sinks"])
            )
            if earlier_count >= 2:
                insights.append(
                    f"✅ 时间消耗已下降：'{info['subject'][:50]}' 在前 {earlier_count} 个窗口中排名靠前，"
                    f"最近一个窗口（{summaries[-1][0]}）未进入前 5——该工作的时间投入可能已减少。"
                )
                if len(insights) > 6:  # cap total insights
                    break

    # --- 3. Increasing time consumption ---
    # Human hours on a kind increased ≥50% from earliest to latest window
    # where that kind appeared. Track labels alongside hours so the insight
    # references the correct first/last window for each kind — a kind may
    # be absent from some interior windows, so its hours list is shorter
    # than the global window_labels list.
    kind_data_by_window: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for label, summ in summaries:
        kind_hours: dict[str, float] = defaultdict(float)
        for sink in summ["top_sinks"]:
            kind_hours[sink["kind"]] += sink["human_h"]
        for kind, hours in kind_hours.items():
            kind_data_by_window[kind].append((label, hours))

    for kind, data_list in kind_data_by_window.items():
        if len(data_list) >= 2 and data_list[0][1] > 0:
            earliest_label, earliest = data_list[0]
            latest_label, latest = data_list[-1]
            pct_change = (latest - earliest) / earliest * 100
            if pct_change >= 50:
                insights.append(
                    f"📈 时间消耗上升：{kind} 人工时间从 {earliest_label} 的 {earliest:.1f}h "
                    f"增至 {latest_label} 的 {latest:.1f}h（+{pct_change:.0f}%）。"
                )

    # --- 4. Automation candidates ---
    # Persistent sinks (≥2 windows) with high error count (≥3 total).
    # Recurrence + errors is the strongest signal for "worth examining for
    # elimination" — but it's a suggestion, not a conclusion that the work
    # was painful.
    for c in persistent_sinks:
        if c["windows_count"] >= 2 and c["total_errors"] >= 3:
            avg_errors = c["total_errors"] / c["windows_count"]
            insights.append(
                f"🔧 自动化候选：'{c['subject'][:50]}' 在 {c['windows_count']} 个窗口中反复出现，"
                f"每次平均 {avg_errors:.1f} 个错误——适合审视是否可自动化。"
            )

    return insights
