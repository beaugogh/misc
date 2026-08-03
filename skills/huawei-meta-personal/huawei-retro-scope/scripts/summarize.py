"""Content-driven root-cause summarizer.

Reads the ACTUAL textual content of a task's events (user prompts, assistant
diagnostic messages, error texts, browser titles, meeting subjects, email
subjects, commit messages) and produces a human-interpretable narrative that
answers:

  - What was the user trying to do? (goal)
  - What exactly was done? (key actions)
  - What was struggled with? (errors, retries, blockers)
  - Why did it take as long as it did? (root cause of time spent)

This replaces the generic ``blocker: command timeout (21 of 46 errors)`` and
``Tabs open 29.6h`` messages with grounded, content-based narratives like:

  "Goal: sync local main with remote. Git fetch repeatedly failed with 407
   corporate-proxy auth errors and command timeouts (46 errors, 21 timeouts).
   Retried git fetch / proxy config ~8×. Root cause: corporate proxy auth
   not configured for git."

Deterministic — no LLM calls. Every clause is extracted from real event text.
"""

from __future__ import annotations

import os
import re

# Length cap for the narrative string (inline column + detail view).
MAX_DETAIL_LEN = 600
MAX_GOAL_LEN = 100

# Keywords that mark assistant messages as diagnostic (struggle narrative).
_DIAG_KEYWORDS = (
    "failed", "error", "let me", "cannot", "can't", "unable", "doesn't work",
    "not working", "proxy", "timeout", "timed out", "denied", "rejected",
    "missing", "not found", "doesn't exist", "wrong", "fix", "debug",
    "struggl", "issue", "problem", "blocker", "retry", "again",
)

# Command prefixes we strip from user messages to get the real goal.
_COMMAND_WRAPPERS = (
    "<command-name>", "<local-command-stdout>", "<command-message>",
    "<command-args>", "<system-reminder>",
)

# Continuation-only user messages (not real goals) — "yes", "ok", "continue", etc.
# Matched at the start of the message; if the first user message is one of these,
# we don't label it as the "Goal:".
_CONTINUATION_RE = re.compile(r'^(yes|ok|okay|continue|no|sure|thanks?|done)\b', re.I)

# Conversational prefixes to strip from goals (mirrors segment_tasks._CONVERSATION_PREFIXES).
_CONVERSATION_PREFIXES = [
    "what do you mean by ", "what is ", "what are ", "what does ",
    "i cannot do this, help me debug: ", "help me debug: ",
    "i see you are struggling, maybe there are some skills that help you: ",
    "can you ", "could you ", "please ", "i want to ", "i need to ",
    "i need you to ", "let's ", "lets ", "how about ", "how do i ",
    "how to ", "why is ", "why does ", "why did ",
    "wait, you should have already set up the ",
    "make sure the skill ",
]


def _strip_conversational_prefix(text: str) -> str:
    """Strip conversational prefixes like 'what do you mean by' from a goal."""
    if not text:
        return ""
    t_lower = text.lower()
    for prefix in _CONVERSATION_PREFIXES:
        if t_lower.startswith(prefix):
            return text[len(prefix):].strip()
    return text


def _clean_user_goal(text: str | None) -> str:
    """Extract a clean goal statement from the first user prompt.

    Strips Claude Code command wrappers (/goal, /skill, etc.), system-reminders,
    and local-command-stdout blocks. Returns the first meaningful sentence.
    """
    if not text:
        return ""
    t = text.strip()
    # Extract session name from system-reminder wrappers.
    m = re.search(r'<system-reminder>.*?The user named this session "([^"]+)".*?</system-reminder>',
                  t, re.DOTALL)
    if m:
        rest = re.sub(r'<system-reminder>.*?</system-reminder>', '', t, flags=re.DOTALL).strip()
        if rest and len(rest) > 10:
            t = rest
        else:
            return f'"{m.group(1)}" session'
    # Strip command-wrapper blocks entirely.
    for wrapper in _COMMAND_WRAPPERS:
        if wrapper in t:
            # If this is a /goal command, extract the args.
            if "<command-args>" in t:
                m = re.search(r'<command-args>(.*?)</command-args>', t, re.DOTALL)
                if m:
                    t = m.group(1).strip()
                    break
            else:
                # Skip lines that are command metadata.
                lines = [ln for ln in t.split("\n")
                         if not any(w in ln for w in _COMMAND_WRAPPERS)]
                t = " ".join(lines).strip()
                break
    # Take the first sentence.
    t = t.replace("\n", " ").strip()
    if not t:
        return ""
    # Split on sentence boundaries.
    first = re.split(r'[.!?]\s', t, maxsplit=1)[0].strip()
    if len(first) > 5:
        return first[:MAX_GOAL_LEN]
    return t[:MAX_GOAL_LEN]


def _extract_diagnostic_sentences(assistant_texts: list[str]) -> list[str]:
    """From assistant messages, pull sentences that describe a struggle/blocker.

    These are sentences containing diagnostic keywords — they narrate what went
    wrong and what was attempted. Returns deduplicated, ranked by informativeness.
    """
    candidates: list[str] = []
    for text in assistant_texts:
        if not text:
            continue
        # Split into sentences.
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for sent in sentences:
            s = sent.strip()
            if len(s) < 15 or len(s) > 200:
                continue
            sl = s.lower()
            if any(kw in sl for kw in _DIAG_KEYWORDS):
                candidates.append(s)
    # Dedupe and return top 3.
    seen: set[str] = set()
    out: list[str] = []
    for s in candidates:
        key = s.lower()[:80]
        if key not in seen:
            seen.add(key)
            out.append(s)
    return out[:3]


def _pair_errors_with_commands(events: list[dict]) -> list[tuple[str, str]]:
    """Pair each error with the command/tool that caused it.

    Returns a list of (command_description, error_snippet) tuples. This is the
    grounded "what failed and why" — far more informative than a pattern bucket.
    """
    pairs: list[tuple[str, str]] = []
    # Build a map from tool_use_id → command description.
    tool_lookup: dict[str, str] = {}
    for ev in events:
        if ev.get("kind") == "tool_use":
            tuid = ev.get("tool_use_id")
            if tuid:
                name = ev.get("tool_name", "?")
                ti = ev.get("tool_input") or {}
                desc = _describe_tool_call(name, ti)
                if desc:
                    tool_lookup[tuid] = desc
    # Match tool_result errors to their tool_use.
    for ev in events:
        if ev.get("kind") == "tool_result" and ev.get("tool_is_error") is True:
            tuid = ev.get("tool_use_id")
            err = (ev.get("text") or "").strip()
            if not err:
                continue
            # Clean the error text: strip "Exit code N\n" prefix and XML-like wrapper tags.
            err = re.sub(r'^Exit code \d+\n', '', err).strip()
            err = re.sub(r'</?tool_use_error>', '', err).strip()
            err = err[:120]
            cmd = tool_lookup.get(tuid)
            # Only pair when we know which command caused the error.
            # An unknown command ("?") is not informative.
            if cmd and err:
                pairs.append((cmd, err))
    return pairs[:5]


def _clean_retry_target(retry_str: str) -> str:
    """Clean up a retry-target string for display in the narrative.

    The retry_targets from _extract_context look like:
      "Bash on 20260723-0xcodez-x-art (11×)"
      "Edit on SKILL.md (44×)"
      "Bash on proxyuk.huawei.com:8080\" && export HTTP_PROXY=... (8×)"

    We extract the tool name, a short target description, and the count,
    producing: "git fetch (11×)" or "edit SKILL.md (44×)".
    """
    if not retry_str:
        return ""
    # Parse "Tool on target (N×)" format.
    m = re.match(r'(\w+)\s+on\s+(.*?)\s+\((\d+)×\)', retry_str)
    if not m:
        return retry_str[:60]
    tool, target, count = m.group(1), m.group(2), m.group(3)
    # Clean the target: for Bash, take the first command before &&/;/|.
    if tool == "Bash":
        target = target.replace("\n", " ").strip()
        target = re.split(r'[&;|]', target)[0].strip()
        # Strip prefixes.
        target = re.sub(r'^(timeout \d+ |sudo |export \S+\s+|cd \S+\s+)', '', target)
        # If it's a URL or hostname, keep it short.
        if len(target) > 40:
            target = target[:40] + "…"
    # For Edit/Write/Read, the target is already a basename.
    return f"{tool} {target} ({count}×)"


def _describe_tool_call(name: str, ti: dict) -> str:
    """One-line description of a tool call for the narrative."""
    if name == "Bash":
        cmd = str(ti.get("command", "")).strip()
        if not cmd:
            return ""
        # Collapse to single line, take the first meaningful command (before &&/;/|).
        cmd = cmd.replace("\n", " ").replace("\\", " ").strip()
        # Squash multiple spaces.
        cmd = re.sub(r'\s+', ' ', cmd)
        first_cmd = re.split(r'[&;|]', cmd)[0].strip()
        # Strip common prefixes (timeout, sudo, export, cd).
        first_cmd = re.sub(r'^(timeout \d+ |sudo |export \S+=\S+\s+)', '', first_cmd)
        # Strip "cd <path> && " prefix if the real command follows.
        first_cmd = re.sub(r'^cd \S+\s+', '', first_cmd)
        return first_cmd[:80]
    if name in ("Edit", "Write"):
        fp = ti.get("file_path") or ""
        return f"edit {os.path.basename(fp)}" if fp else ""
    if name == "Read":
        fp = ti.get("file_path") or ""
        return f"read {os.path.basename(fp)}" if fp else ""
    if name == "Grep":
        return f"grep '{(ti.get('pattern') or '')[:40]}'"
    if name == "WebSearch":
        return f"search '{(ti.get('query') or '')[:40]}'"
    if name == "WebFetch":
        return f"fetch {(ti.get('url') or '')[:50]}"
    if name == "TaskCreate":
        return f"create task '{(ti.get('subject') or '')[:40]}'"
    if name == "TaskUpdate":
        return f"update task to {ti.get('status', '?')}"
    return f"{name}"


def _explain_difficulty(n_errors: int, error_pairs: list[tuple[str, str]],
                        retry_targets: list[str]) -> str:
    """Synthesize a one-line explanation of WHY the problem was hard to solve.

    Looks at the error pattern (what types of errors, how many retries) and
    explains the difficulty in human terms — e.g. "same proxy auth failure
    kept recurring despite 11 retries" rather than just "46 errors".
    """
    if not error_pairs and not retry_targets:
        return ""

    # Classify the error pattern from the error texts.
    error_texts = [err.lower() for _, err in error_pairs]
    all_text = " ".join(error_texts)

    patterns: list[str] = []
    if "407" in all_text or ("proxy" in all_text and "tunnel" in all_text):
        patterns.append("corporate proxy authentication")
    if "timeout" in all_text or "timed out" in all_text:
        patterns.append("command timeouts")
    if "not found" in all_text or "no such file" in all_text:
        patterns.append("missing files/paths")
    if "permission denied" in all_text or "access is denied" in all_text:
        patterns.append("permission/access issues")
    if "doesn't want to proceed" in all_text or "rejected" in all_text:
        patterns.append("user rejecting tool uses")
    if "exit code 128" in all_text or "merge conflict" in all_text:
        patterns.append("git failures")
    if "modulenotfounderror" in all_text or "importerror" in all_text:
        patterns.append("missing Python dependencies")
    if "syntaxerror" in all_text or "indentationerror" in all_text:
        patterns.append("Python syntax errors")

    if not patterns:
        return f"{n_errors} errors total — repeated failures suggest the approach kept hitting walls."

    # Count retries for the difficulty assessment.
    retry_count = 0
    if retry_targets:
        for rt in retry_targets:
            m = re.search(r'\((\d+)×\)', rt)
            if m:
                retry_count += int(m.group(1))

    pattern_str = " + ".join(patterns[:2])
    if retry_count >= 5:
        return f"Difficulty: {pattern_str} kept recurring despite {retry_count} retries — the root cause was not addressed by the attempted fixes."
    elif n_errors >= 10:
        return f"Difficulty: {pattern_str} caused {n_errors} errors — multiple approaches tried without resolving the underlying issue."
    else:
        return f"Difficulty: {pattern_str} was the main blocker ({n_errors} errors)."


def _summarize_ai_session(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for an AI coding session.

    Structure: Goal → Key struggle (from assistant diagnostics + error-command
    pairs) → Retry pattern → Time explanation.
    """
    # 1. Goal: first real user message, cleaned of conversational prefixes.
    user_msgs = [e for e in events if e.get("kind") == "user_message" and e.get("text")]
    goal = _clean_user_goal(user_msgs[0].get("text")) if user_msgs else ""
    # Strip conversational prefixes from the goal too (e.g. "what do you mean by X" → "X").
    goal = _strip_conversational_prefix(goal)

    # 2. Assistant diagnostic sentences (the struggle narrative).
    asst_texts = [(e.get("text") or "") for e in events if e.get("kind") == "assistant_message"]
    diagnostics = _extract_diagnostic_sentences(asst_texts)

    # 3. Error-command pairs (grounded "what failed").
    error_pairs = _pair_errors_with_commands(events)

    # 4. Retry pattern: tools called 2+× on the same target.
    ctx = task.get("context") or {}
    retry_targets = ctx.get("retry_targets") or []

    # 5. Time context.
    active_h = (task.get("active_seconds") or 0) / 3600
    wall_h = (task.get("wall_clock_seconds") or 0) / 3600
    excised_h = (task.get("excised_gap_seconds") or 0) / 3600
    n_errors = task.get("errors", 0)
    n_tool_calls = task.get("tool_calls", 0)

    parts: list[str] = []

    # Goal line.
    if goal and not _CONTINUATION_RE.match(goal):
        parts.append(f"Goal: {goal}.")

    # Struggle narrative: synthesize WHY the problem was hard, not just WHAT failed.
    # The user's feedback: "after reading them, i still do not know why that
    # problem was hard to solve." So we need to explain the difficulty pattern.
    if diagnostics and error_pairs:
        # Lead with the assistant's diagnostic (it explains the struggle).
        parts.append(diagnostics[0])
        # Then the top error pair — what specifically failed.
        cmd, err = error_pairs[0]
        parts.append(f"Key failure: '{cmd}' → {err}.")
        # If there are many errors of the same type, explain the pattern.
        if n_errors >= 5:
            parts.append(_explain_difficulty(n_errors, error_pairs, retry_targets))
    elif diagnostics:
        parts.append(diagnostics[0])
        if len(diagnostics) > 1:
            parts.append(diagnostics[1])
        if n_errors >= 5:
            parts.append(_explain_difficulty(n_errors, error_pairs, retry_targets))
    elif error_pairs:
        cmd, err = error_pairs[0]
        parts.append(f"Failed: '{cmd}' → {err}.")
        if len(error_pairs) > 1:
            cmd2, err2 = error_pairs[1]
            parts.append(f"Also: '{cmd2}' → {err2}.")
        if n_errors >= 5:
            parts.append(_explain_difficulty(n_errors, error_pairs, retry_targets))
    elif n_errors > 0:
        # Errors exist but no paired text — use the blocker from context.
        blocker = ctx.get("blocker")
        if blocker:
            parts.append(f"Blocker: {blocker}.")

    # Retry pattern: clean up the retry target for display.
    if retry_targets:
        cleaned = _clean_retry_target(retry_targets[0])
        parts.append(f"Retried {cleaned}.")

    # Time explanation: why did it take this long?
    if excised_h > 1 and excised_h > active_h:
        # Significant idle/overnight.
        parts.append(
            f"{active_h:.1f}h active in {wall_h:.1f}h wall — {excised_h:.1f}h idle/overnight gaps."
        )
    elif n_errors >= 5 or (retry_targets and active_h > 1):
        # Time spent on errors/retries.
        parts.append(
            f"{active_h:.1f}h, {n_errors} error(s), {n_tool_calls} tool calls."
        )
    elif active_h > 0.5:
        files = ctx.get("files_touched") or []
        if files:
            parts.append(
                f"{active_h:.1f}h, edited {len(files)} file(s): "
                f"{', '.join(os.path.basename(f) for f in files[:3])}."
            )
        else:
            parts.append(f"{active_h:.1f}h active.")

    return " ".join(parts) if parts else ""


def _summarize_browser(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a browser/research session.

    The page titles + URLs reveal what was being researched. We list the key
    pages visited (the titles tell the story), note downloads, and explain
    whether the time was active browsing or idle tabs left open.
    """
    ctx = task.get("context") or {}
    titles = ctx.get("top_titles") or []
    urls = ctx.get("top_urls") or []
    queries = ctx.get("queries") or []
    downloads = ctx.get("downloads") or 0
    n_visits = ctx.get("n_visits") or 0

    active_h = (task.get("active_seconds") or 0) / 3600
    wall_h = (task.get("wall_clock_seconds") or 0) / 3600
    excised_h = (task.get("excised_gap_seconds") or 0) / 3600

    parts: list[str] = []

    # What was the user searching for? (the most direct goal signal)
    if queries:
        parts.append(f"Searched for '{queries[0][:50]}'.")

    # The visited page titles ARE the research story — list the key ones.
    if titles:
        key_pages = _dedupe(titles)[:3]
        parts.append(f"Visited: {', '.join(key_pages)}.")

    # Downloads = artifact produced (research outcome).
    if downloads:
        parts.append(f"Downloaded {downloads} file(s).")

    # Time explanation: active vs idle tabs.
    if active_h < 0.05 and wall_h > 1:
        # Tabs left open, no measurable activity.
        first_page = titles[0][:40] if titles else "browsing"
        parts.append(
            f"Tabs open {wall_h:.1f}h but no measurable activity — "
            f"left open on {first_page}."
        )
    elif excised_h > 0.5 and excised_h > active_h:
        parts.append(
            f"{active_h:.1f}h active browsing in {wall_h:.1f}h — "
            f"{excised_h:.1f}h idle/overnight tabs left open."
        )
    elif active_h > 0.1:
        if n_visits > 10:
            parts.append(f"{active_h:.1f}h, {n_visits} visits.")
        else:
            parts.append(f"{active_h:.1f}h browsing.")

    return " ".join(parts) if parts else ""


def _summarize_meeting(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a meeting.

    The subject, location, organizer, and time span tell the story. For
    multi-day events, we explain the cap. For all-day markers, we say so.
    """
    ctx = task.get("context") or {}
    subject = ctx.get("subject") or task.get("subject") or ""
    organizer = ctx.get("organizer")
    location = ctx.get("location")
    is_all_day = ctx.get("is_all_day")

    active_h = (task.get("active_seconds") or 0) / 3600
    wall_h = (task.get("wall_clock_seconds") or 0) / 3600
    excised_h = (task.get("excised_gap_seconds") or 0) / 3600

    # All-day calendar marker — not a real meeting.
    if is_all_day:
        return f"'{subject[:60]}' is an all-day calendar marker — 0h real meeting time."

    parts: list[str] = []

    # Subject is the content.
    if subject:
        parts.append(f"'{subject[:60]}'.")

    # Context: who, where.
    context_bits: list[str] = []
    if organizer:
        context_bits.append(f"organized by {organizer}")
    if location:
        context_bits.append(f"at {location}")
    if context_bits:
        parts.append(f"({', '.join(context_bits)}).")

    # Time explanation.
    # Multi-day detection: wall > 24h (a full calendar day) OR the active time
    # was capped (excised > 0 with active >= 8h means the raw duration exceeded
    # 8h and was capped). A 9h single-day workshop is NOT multi-day.
    if wall_h > 24 or (excised_h > 0 and active_h >= 8):
        # Multi-day event. Use (active + excised) for the real span — wall is
        # already capped to MAX_MEETING_DURATION (24h) so it understates the
        # true calendar span for events lasting several days.
        real_span_h = active_h + excised_h
        days = real_span_h / 24
        parts.append(
            f"Multi-day event ({days:.1f} days), capped to {active_h:.0f}h — "
            f"actual attendance unknown."
        )
    elif active_h > 0:
        parts.append(f"{active_h:.1f}h meeting.")
    elif wall_h > 0:
        parts.append(f"{wall_h:.1f}h wall-clock, 0h active.")

    return " ".join(parts) if parts else ""


def _summarize_comm(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for an email/communication task.

    Handles both email threads and WeLink IM chat sessions.
    """
    ctx = task.get("context") or {}
    subjects = ctx.get("subjects") or []
    senders = ctx.get("senders") or []
    has_reply = ctx.get("has_reply")
    im_count = ctx.get("im_message_count") or 0
    im_conversations = ctx.get("im_conversations") or []
    im_senders = ctx.get("im_senders") or []

    parts: list[str] = []

    # Email summary.
    if subjects:
        parts.append(f"Email '{subjects[0][:60]}'.")
        if senders:
            parts.append(f"From {senders[0]}.")
        if has_reply:
            parts.append("Reply sent.")
        else:
            parts.append("No reply detected.")

    # IM summary.
    if im_count:
        active_h = (task.get("active_seconds") or 0) / 3600
        conv = im_conversations[0][:40] if im_conversations else "a conversation"
        parts.append(f"{im_count} IM message(s) in {conv}.")
        if len(im_senders) > 1:
            parts.append(f"{len(im_senders)} participant(s).")
        if active_h > 0.1:
            parts.append(f"{active_h:.1f}h of messaging.")

    return " ".join(parts) if parts else ""


def _summarize_vcs(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a VCS/commit task."""
    ctx = task.get("context") or {}
    subjects = ctx.get("commit_subjects") or []
    if subjects:
        active_h = (task.get("active_seconds") or 0) / 3600
        parts = [f"{len(subjects)} commit(s): '{subjects[0][:60]}'."]
        if active_h > 0.1:
            parts.append(f"{active_h:.1f}h VCS activity.")
        return " ".join(parts)
    return ""


def _summarize_filesystem(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a filesystem task."""
    ctx = task.get("context") or {}
    files = ctx.get("files") or []
    if files:
        active_h = (task.get("active_seconds") or 0) / 3600
        names = [os.path.basename(f) for f in files[:3]]
        parts = [f"Touched {len(files)} file(s): {', '.join(names)}."]
        if active_h > 0.1:
            parts.append(f"{active_h:.1f}h.")
        return " ".join(parts)
    return ""


def _dedupe(items: list[str]) -> list[str]:
    """Deduplicate preserving order."""
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def summarize_root_cause(task: dict, events: list[dict]) -> str:
    """Produce a human-interpretable root-cause narrative for a task.

    Returns a 1-3 sentence string grounded in the actual event content, or ''
    if no content is available. The narrative explains WHAT was done, WHAT was
    struggled with, and WHY the task took as long as it did.

    Called at segmentation time (when events are available) and stored in
    ``task["context"]["narrative"]`` for the render layer.
    """
    source_kind = task.get("source_kind", "ai_session")
    if source_kind == "ai_session":
        narrative = _summarize_ai_session(events, task)
    elif source_kind == "browser":
        narrative = _summarize_browser(events, task)
    elif source_kind == "meeting":
        narrative = _summarize_meeting(events, task)
    elif source_kind == "comm":
        narrative = _summarize_comm(events, task)
    elif source_kind == "vcs":
        narrative = _summarize_vcs(events, task)
    elif source_kind == "filesystem":
        narrative = _summarize_filesystem(events, task)
    else:
        narrative = ""

    if not narrative:
        return ""

    # Cap length.
    if len(narrative) > MAX_DETAIL_LEN:
        narrative = narrative[:MAX_DETAIL_LEN - 3] + "…"
    return narrative


if __name__ == "__main__":
    # Quick self-test against real data.
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from claude_code_adapter import collect_events
    from segment_tasks import segment

    events = collect_events()
    tasks = segment(events)
    ranked = sorted(tasks, key=lambda t: t.get("active_seconds") or 0, reverse=True)

    print(f"# {len(tasks)} tasks\n")
    for t in ranked[:10]:
        tid = t.get("id", "?")
        act_h = (t.get("active_seconds") or 0) / 3600
        sk = t.get("source_kind", "?")
        # Re-find events for this task.
        sid = t.get("session_id")
        start = t.get("start", 0)
        end = t.get("end", 0)
        task_events = [e for e in events
                       if e.get("session_id") == sid
                       and e.get("timestamp") is not None
                       and start <= e.get("timestamp", 0) <= end]
        narrative = summarize_root_cause(t, task_events)
        print(f"=== {tid} [{sk}] {act_h:.1f}h ===")
        print(f"  {narrative}")
        print()
