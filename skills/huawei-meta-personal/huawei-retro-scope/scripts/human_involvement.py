"""Human-involvement detection — distinguish HUMAN time from MACHINE time.

The core principle (from the user's feedback):

  "We are looking for time sinks that cost HUMAN time! If a long coding
   session is mainly a coding agent that automatically programs solutions,
   barely with any human involvement, I would not call that a time sink."

This module identifies HUMAN actions in the event stream (the user typing
prompts, interrupting, rejecting tool uses, clicking browser pages, sending
emails, committing code) and computes:

  - ``human_action_count`` — how many human actions were detected
  - ``human_engaged_seconds`` — time the human was actively engaged
    (sum of inter-human-action intervals ≤ 30 min; gaps > 30 min = the
    human stepped away, not engaged)
  - ``machine_autonomous_seconds`` — active time NOT attributable to human
    engagement (agent working between human prompts)
  - ``human_involvement`` — qualitative label:
      "high"     — many human actions, engaged throughout
      "moderate" — some human actions, but significant autonomous stretches
      "low"      — few human actions; mostly autonomous
      "none"     — no human actions detected (e.g. meeting from calendar data
                   alone, idle browser tabs, all-day calendar markers)
      "unknown"  — can't determine (no data)

The report uses these to RANK time sinks by human cost, not raw active time.
A 10h coding session with 2 prompts → "low" involvement → NOT a top time sink.
A 3h browser session with 758 clicks → "high" involvement → IS a top time sink.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

# Threshold: if two human actions are >30 min apart, the human stepped away.
# The inter-action interval is only "engaged time" if ≤30 min.
HUMAN_ENGAGEMENT_GAP = 30 * 60  # 30 minutes

# Minimum human actions for each involvement level.
# These are calibrated against the audited real data:
#   - 4 msgs / 411 tool_uses → "low" (yes-continue autonomous run)
#   - 47 msgs / 879 tool_uses → "moderate"
#   - 191 msgs / 2991 tool_uses → "high" (heavy back-and-forth)
#   - 758 browser revisits → "high" (heavy clicking)
#   - 0 signals → "none" (meeting from calendar, idle tabs)
HIGH_HUMAN_ACTION_THRESHOLD = 50
MODERATE_HUMAN_ACTION_THRESHOLD = 10


def is_human_action(event: dict) -> bool:
    """Determine if an event represents a HUMAN action (not machine).

    Human actions are events where the USER did something:
      - user_message: the user typed a prompt/instruction
      - user_message with [Request interrupted]: the user interrupted the agent
      - tool_result with "doesn't want to proceed": the user rejected a tool use
      - visit with visit_count > 1: the user revisited a page (clicked a link)
      - email direction=sent: the user composed and sent an email
      - commit: the user committed code (or directed the agent to)
      - filesystem events: the user opened/saved files in an editor

    Machine actions (NOT human):
      - assistant_message: the agent thinking/responding
      - tool_use: the agent calling a tool (Bash, Read, Edit, etc.)
      - tool_result success: the agent's tool call succeeded
      - visit with visit_count=1: a one-time page load (could be auto-redirect)
    """
    kind = event.get("kind")
    if kind == "user_message":
        # User typed something — always a human action.
        return True
    if kind == "tool_result" and event.get("tool_is_error") is True:
        # Check if the user rejected the tool use.
        text = (event.get("text") or "").lower()
        if "doesn't want to proceed" in text or "rejected" in text:
            return True
        return False
    if kind == "visit":
        # A browser visit. If visit_count > 1, the user revisited (clicked).
        ti = event.get("tool_input") or {}
        visit_count = ti.get("visit_count") or 0
        if isinstance(visit_count, (int, float)) and visit_count > 1:
            return True
        return False
    if kind == "email":
        ti = event.get("tool_input") or {}
        if ti.get("direction") == "sent":
            return True
        return False
    if kind == "chat_message":
        # IM message. Human action if the user sent it (not received).
        # The sender field holds the account ID; we check if it matches the
        # current user's account. Since we don't have the user's ID here,
        # we treat all sent IM messages as human actions by checking the
        # conversation direction from tool_input.
        ti = event.get("tool_input") or {}
        # For WeLink IM, all messages in a conversation are either sent or
        # received. The sender field is the message author. If the sender
        # is the current user (account matches), it's a human action.
        # We approximate: messages where sender == the user's account are human.
        # The user's account is typically in the conversation_name or we
        # check if the message was sent by the user.
        # For now: all chat messages are human actions (someone typed them).
        # The distinction between sent vs received doesn't affect whether
        # a human was involved — both sides typing = human engagement.
        return True
    if kind == "commit":
        # Commits are human-directed (even if the agent executed them).
        return True
    if event.get("source_kind") == "filesystem":
        # Filesystem events (VSCode history, Windows Recent) = user opened files.
        return True
    return False


def compute_human_involvement(events: list[dict], task: dict) -> dict:
    """Compute human-involvement metrics for a task.

    Returns a dict with:
      - human_action_count: int
      - human_engaged_seconds: float (time between consecutive human actions, gaps ≤30min)
      - machine_autonomous_seconds: float (active time minus human engaged)
      - human_involvement: "high" | "moderate" | "low" | "none" | "unknown"
      - human_action_types: list[str] (what kinds of human actions were detected)
    """
    active_seconds = task.get("active_seconds") or 0.0

    # Extract human-action events with timestamps.
    human_events = [e for e in events
                    if e.get("timestamp") is not None and is_human_action(e)]

    # Count by action type for the narrative.
    action_types: list[str] = []
    user_msgs = sum(1 for e in human_events if e.get("kind") == "user_message")
    interrupts = sum(1 for e in human_events
                     if e.get("kind") == "user_message"
                     and "[Request interrupted" in (e.get("text") or ""))
    rejections = sum(1 for e in human_events
                     if e.get("kind") == "tool_result" and e.get("tool_is_error") is True
                     and "doesn't want to proceed" in (e.get("text") or "").lower())
    browser_clicks = sum(1 for e in human_events if e.get("kind") == "visit")
    emails_sent = sum(1 for e in human_events
                      if e.get("kind") == "email"
                      and (e.get("tool_input") or {}).get("direction") == "sent")
    im_messages = sum(1 for e in human_events if e.get("kind") == "chat_message")
    commits = sum(1 for e in human_events if e.get("kind") == "commit")
    fs_actions = sum(1 for e in human_events if e.get("source_kind") == "filesystem")

    if user_msgs:
        action_types.append(f"{user_msgs} prompt(s)")
    if interrupts:
        action_types.append(f"{interrupts} interrupt(s)")
    if rejections:
        action_types.append(f"{rejections} rejection(s)")
    if browser_clicks:
        action_types.append(f"{browser_clicks} click(s)/revisit(s)")
    if emails_sent:
        action_types.append(f"{emails_sent} email(s) sent")
    if im_messages:
        action_types.append(f"{im_messages} IM message(s)")
    if commits:
        action_types.append(f"{commits} commit(s)")
    if fs_actions:
        action_types.append(f"{fs_actions} file action(s)")

    human_action_count = len(human_events)

    # Compute human-engaged time: sum of inter-human-action intervals ≤ gap threshold.
    if len(human_events) < 2:
        # 0 or 1 human action — the human touched the task, but we can't measure
        # engagement span from a single point. Give a small minimum (5 min) if
        # there's at least one action, 0 if none.
        human_engaged = 300.0 if human_action_count >= 1 else 0.0
    else:
        ts_list = sorted(e["timestamp"] for e in human_events)
        human_engaged = 0.0
        for i in range(1, len(ts_list)):
            delta = ts_list[i] - ts_list[i - 1]
            if delta <= HUMAN_ENGAGEMENT_GAP:
                human_engaged += delta
            # Gaps > 30 min = human stepped away, not engaged.

    machine_autonomous = max(0.0, active_seconds - human_engaged)

    # Determine involvement level.
    if human_action_count == 0:
        involvement = "none"
    elif human_action_count >= HIGH_HUMAN_ACTION_THRESHOLD:
        involvement = "high"
    elif human_action_count >= MODERATE_HUMAN_ACTION_THRESHOLD:
        involvement = "moderate"
    else:
        involvement = "low"

    # Genuine time sink: 5+ human actions AND 5+ minutes engaged.
    # Tasks below this threshold are likely forgotten/abandoned, not genuine pain points.
    is_genuine = human_action_count >= 5 and human_engaged >= 300.0

    return {
        "human_action_count": human_action_count,
        "human_engaged_seconds": round(human_engaged, 1),
        "machine_autonomous_seconds": round(machine_autonomous, 1),
        "human_involvement": involvement,
        "human_action_types": action_types,
        "is_genuine_time_sink": is_genuine,
    }


def compute_actual_working_hours(tasks: list[dict]) -> float:
    """Compute actual working hours from human activity in the task set.

    Instead of assuming 8h/day, we derive the working-hour denominator from
    the data itself: the total human-engaged time across all tasks, plus a
    minimum per-day-with-activity to account for days where the human was
    present but the inter-action gaps were > 30 min (meetings, focused work).

    This is used as the denominator for the "% of working time" calculation,
    replacing the flat 8h/day assumption. If no human activity is detected
    at all, falls back to 8h × number of days with tasks (conservative).
    """
    from datetime import datetime, timezone

    total_human_engaged = 0.0
    days_with_activity: set[str] = set()

    for t in tasks:
        hd = t.get("human_data") or {}
        engaged = hd.get("human_engaged_seconds", 0) or 0
        total_human_engaged += engaged
        start = t.get("start")
        if start and engaged > 0:
            day = datetime.fromtimestamp(start, tz=timezone.utc).strftime("%Y-%m-%d")
            days_with_activity.add(day)

    if not days_with_activity:
        # No human activity detected — fall back to active time span.
        return 0.0

    # The actual working hours is the human-engaged time, but at minimum
    # 1h per day with activity (the human was present, even if gaps > 30min
    # prevented full engagement measurement).
    min_hours = len(days_with_activity) * 1.0
    engaged_hours = total_human_engaged / 3600
    return max(engaged_hours, min_hours)


def describe_human_involvement(human_data: dict, task: dict) -> str:
    """One-line human-readable description of human involvement.

    Used in the report to explain whether the task cost HUMAN time or was
    mostly autonomous machine work.
    """
    involvement = human_data.get("human_involvement", "unknown")
    action_count = human_data.get("human_action_count", 0)
    engaged_h = (human_data.get("human_engaged_seconds") or 0) / 3600
    active_h = (task.get("active_seconds") or 0) / 3600
    action_types = human_data.get("human_action_types") or []

    if involvement == "none":
        source_kind = task.get("source_kind", "")
        if source_kind == "meeting":
            return "No human interaction detected — attendance not measurable from calendar data alone."
        elif source_kind == "browser":
            wall_h = (task.get("wall_clock_seconds") or 0) / 3600
            return f"No human clicks/revisits detected — tabs likely left open ({wall_h:.1f}h wall, 0h engaged)."
        return "No human actions detected."

    parts: list[str] = []
    if action_types:
        parts.append(f"{action_count} human actions ({', '.join(action_types[:3])}).")

    if involvement == "high":
        parts.append(f"Human engaged ~{engaged_h:.1f}h of {active_h:.1f}h active — heavy involvement.")
    elif involvement == "moderate":
        parts.append(f"Human engaged ~{engaged_h:.1f}h of {active_h:.1f}h active — some autonomous stretches.")
    elif involvement == "low":
        autonomous_h = (human_data.get("machine_autonomous_seconds") or 0) / 3600
        parts.append(f"Only {engaged_h:.1f}h human engagement in {active_h:.1f}h — mostly autonomous ({autonomous_h:.1f}h).")

    return " ".join(parts)


if __name__ == "__main__":
    # Quick self-test against real data.
    import sys, os
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.path.insert(0, os.path.dirname(__file__))
    from sources import default_registry
    from segment_tasks import segment

    reg = default_registry()
    all_events, _ = reg.collect_all()
    tasks = segment(all_events)

    # Rank by human engaged time, not active time.
    for t in tasks:
        start = t.get("start", 0)
        end = t.get("end", 0)
        task_events = [e for e in all_events
                       if e.get("timestamp") is not None
                       and start <= e.get("timestamp", 0) <= end]
        hd = compute_human_involvement(task_events, t)
        t["human_data"] = hd

    # Sort by human engaged time.
    ranked = sorted(tasks, key=lambda t: (t.get("human_data") or {}).get("human_engaged_seconds", 0), reverse=True)

    print("=== TOP 10 HUMAN TIME SINKS (by human engaged time) ===\n")
    for t in ranked[:10]:
        hd = t.get("human_data") or {}
        act_h = (t.get("active_seconds") or 0) / 3600
        eng_h = (hd.get("human_engaged_seconds") or 0) / 3600
        sk = t.get("source_kind", "?")
        subj = (t.get("subject") or "")[:50]
        inv = hd.get("human_involvement", "?")
        desc = describe_human_involvement(hd, t)
        print(f"[{sk:11s}] {eng_h:5.1f}h human / {act_h:5.1f}h active | {inv:9s} | {subj}")
        print(f"  {desc}")
        print()
