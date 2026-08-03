"""Task segmentation.

Consumes normalized events (from claude_code_adapter.collect_events) and reconstructs
task objects. Two flavors, per the SKILL.md task model:

  - EXPLICIT tasks: bounded by TaskCreate / TaskUpdate tool calls.
  - IMPLICIT tasks: inferred from user-message turns when no TaskCreate is present.

For the MVP spine, implicit-task boundary detection uses simple heuristics:
  - Each user message that introduces a new goal starts a task.
  - A user message that is a correction/continuation extends the current task.
  - Long gaps (> GAP_THRESHOLD_SECONDS) suggest a task boundary.
  - A shift in cwd suggests a task boundary.

This is deliberately naive — the deep research candidates (PELT, GMM on inter-arrival
times) are for later. The point of this version is to get an end-to-end pipeline working
against real data, so the output can be eyeballed for sanity before adding sophistication.

Output: a list of task dicts:
    {
        "id": str,                  # synthetic, e.g. "explicit-<n>" or "implicit-<n>"
        "flavor": "explicit" | "implicit",
        "source": "claude_code",
        "session_id": str,
        "cwd": str | None,
        "git_branch": str | None,
        "subject": str | None,      # explicit: TaskCreate.subject; implicit: first user message
        "start": float,             # epoch seconds
        "end": float,               # epoch seconds
        "duration_seconds": float,
        "event_count": int,
        "tool_calls": int,          # count of tool_use events
        "tool_names": list[str],    # distinct tool names used
        "output_tokens": int,       # sum of assistant usage.output_tokens (effort signal)
        "input_tokens": int,        # sum of assistant usage.input_tokens
        "errors": int,              # count of tool_result.is_error == True
        "outputs": list[str],       # Write/Edit target paths + commit hashes (truncated)
        "task_status": str | None,  # explicit: from TaskUpdate; implicit: None
    }
"""

from __future__ import annotations

import os
import re
from typing import Iterator

# Content-driven root-cause summarizer — produces human-interpretable narratives
# from the actual event text (prompts, assistant diagnostics, errors, page titles).
# Imported lazily inside _make_task to avoid a circular import (summarize.py
# imports from segment_tasks for its self-test only, guarded by __main__).
def _get_summarizer():
    try:
        from summarize import summarize_root_cause
        return summarize_root_cause
    except ImportError:
        return None

# Human-involvement detector — distinguishes HUMAN time (the user typing,
# clicking, interrupting) from MACHINE time (the agent running autonomously).
# This is the key to identifying real time sinks: a 10h autonomous agent run
# with 2 prompts is NOT a human time sink, even though active_seconds=10h.
def _get_human_involvement_fn():
    try:
        from human_involvement import compute_human_involvement
        return compute_human_involvement
    except ImportError:
        return None

# Heuristic thresholds for implicit segmentation.
GAP_THRESHOLD_SECONDS = 30 * 60  # 30 min gap => likely a new task
MAX_SUBJECT_LEN = 120

# Maximum plausible meeting duration — used to clamp corrupt end_ts values.
MAX_MEETING_DURATION = 24 * 3600  # 24 hours

# User-correction signal keywords (English + Chinese).
# Curated to exclude ambiguous bare words that are common in non-correction
# contexts (e.g. "fix" in task instructions, "wait" in patience phrases,
# "actually" in confirmations). Continuation words like 再/另外/还有/改 are
# NOT corrections — they extend the task, not redirect it.
_CORRECTION_SIGNALS = [
    # English — strong correction signals only
    "no,", "wrong", "not right", "incorrect", "didn't", "did not",
    "instead", "not what i asked",
    # Chinese — true corrections only (removed continuation words 再/另外/还有/改/重新/不是)
    "不对", "错了", "又错", "不要",
]


def _summarize_message(text: str | None) -> str:
    if not text:
        return "(no text)"
    text = text.strip().replace("\n", " ")
    # Clean system-reminder wrappers and command metadata from the subject.
    text = _clean_subject_text(text)
    if not text:
        return "(no text)"
    if len(text) > MAX_SUBJECT_LEN:
        return text[:MAX_SUBJECT_LEN] + "…"
    return text


# Conversational prefixes that make a prompt read as a question/chat rather
# than a task description. Stripping these yields a cleaner subject.
# E.g. "what do you mean by install skill-creator" → "install skill-creator"
#      "i cannot do this, help me debug: git clone..." → "git clone..."
_CONVERSATION_PREFIXES = [
    "what do you mean by ", "what is ", "what are ", "what does ",
    "i cannot do this, help me debug: ", "help me debug: ",
    "i see you are struggling, maybe there are some skills that help you: ",
    "can you ", "could you ", "please ", "i want to ", "i need to ",
    "i need you to ", "let's ", "lets ", "how about ", "how do i ",
    "how to ", "why is ", "why does ", "why did ",
    "wait, you should have already set up the ",
    "yes, continue", "make sure the skill ",
]
# System-reminder patterns — extract the useful bit, discard the wrapper.
_SYSTEM_REMINDER_RE = re.compile(
    r'<system-reminder>.*?The user named this session "([^"]+)".*?</system-reminder>',
    re.DOTALL
)


def _clean_subject_text(text: str) -> str:
    """Clean a raw user prompt into a descriptive task subject.

    Strips system-reminder wrappers, command metadata, and conversational
    prefixes so the subject reads as a task description, not a chat message.
    """
    t = text.strip()
    # Extract session name from system-reminder wrappers.
    m = _SYSTEM_REMINDER_RE.search(t)
    if m:
        session_name = m.group(1).strip()
        # Use the session name as the subject — it's the user's own title.
        rest = _SYSTEM_REMINDER_RE.sub("", t).strip()
        if rest and len(rest) > 10:
            # There's content after the reminder — use it.
            t = rest
        else:
            return f'"{session_name}" session'
    # Strip command-wrapper lines entirely.
    for wrapper in ("<command-name>", "<local-command-stdout>",
                    "<command-message>", "<command-args>", "<system-reminder>"):
        if wrapper in t:
            # If there's a /goal command-args, extract it.
            if "<command-args>" in t:
                m = re.search(r'<command-args>(.*?)</command-args>', t, re.DOTALL)
                if m:
                    t = m.group(1).strip()
                    break
            # Otherwise, strip lines containing command metadata.
            lines = [ln for ln in t.split("\n")
                     if not any(w in ln for w in
                                ("<command-name>", "<local-command-stdout>",
                                 "<command-message>", "<command-args>",
                                 "<system-reminder>", "</system-reminder>"))]
            t = " ".join(ln.strip() for ln in lines if ln.strip()).strip()
            break
    # Strip conversational prefixes (case-insensitive).
    t_lower = t.lower()
    for prefix in _CONVERSATION_PREFIXES:
        if t_lower.startswith(prefix):
            t = t[len(prefix):].strip()
            break
    # Capitalize first letter for readability.
    if t:
        t = t[0].upper() + t[1:]
    return t


def _is_correction(text: str | None) -> bool:
    """Heuristic: does this user message look like a correction?

    Uses word-boundary matching to avoid false positives from bare substrings
    (e.g. "fix" in "fix the typo", "wait" in "please wait"). Additionally
    requires the correction keyword to appear near the START of the message
    (first 5 words) — real corrections lead with the signal
    ("no, do X instead", "wrong, that's not right").
    """
    if not text:
        return False
    t = text.strip().lower()

    # Extract the lead portion: first 5 words of the first sentence, so we
    # only match correction signals at the start.
    first_sentence = re.split(r'[.!?]\s', t, maxsplit=1)[0].strip()
    first_words = first_sentence.split()[:5]
    lead = ' '.join(first_words)

    # For Chinese text (no spaces), use the first ~20 chars of the first sentence.
    lead_chinese = first_sentence[:20]

    for sig in _CORRECTION_SIGNALS:
        # Word-boundary matching for English keywords.
        # For signals ending in non-word chars (e.g. "no,"), skip the trailing \b
        # since there's no word boundary after a comma.
        prefix = r'\b'
        suffix = r'\b' if sig[-1].isalnum() else ''
        if re.search(prefix + re.escape(sig) + suffix, lead):
            return True
        # Chinese: substring check in the lead portion (no word boundaries).
        if sig in lead_chinese:
            return True
    return False


def _extract_output_artifacts(events: list[dict]) -> list[str]:
    """Pull output artifacts from tool_use events: Write/Edit target paths, Bash commits, etc."""
    out = []
    for ev in events:
        if ev.get("kind") != "tool_use":
            continue
        name = ev.get("tool_name")
        ti = ev.get("tool_input") or {}
        if name in ("Write", "Edit") and ti.get("file_path"):
            out.append(ti["file_path"])
        elif name == "Bash":
            cmd = str(ti.get("command", ""))
            if "git commit" in cmd.lower():
                out.append(f"git commit: {cmd[:80]}")
            elif any(k in cmd.lower() for k in ("mkdir", "curl", "wget", "touch", "cp ", "mv ")):
                out.append(f"bash: {cmd[:80]}")
        elif name == "NotebookEdit" and ti.get("notebook_path"):
            out.append(ti["notebook_path"])
    # dedupe preserving order
    seen = set()
    deduped = []
    for o in out:
        if o not in seen:
            seen.add(o)
            deduped.append(o)
    return deduped[:20]  # cap


def _extract_inputs(events: list[dict]) -> list[str]:
    """Pull input artifacts: user messages, files Read, URLs fetched, and non-tool events.

    Handles both AI-session tool_use events AND non-AI events (browser visits, searches,
    meetings, emails, commits) so the ``inputs`` list is useful for every source_kind,
    not just ai_session. Each entry is prefixed with its type for readability.
    """
    inputs = []
    for ev in events:
        kind = ev.get("kind")
        if kind == "user_message" and ev.get("text"):
            inputs.append(f"prompt: {ev['text'][:100]}")
        elif kind == "tool_use":
            name = ev.get("tool_name")
            ti = ev.get("tool_input") or {}
            if name == "Read" and ti.get("file_path"):
                inputs.append(f"read: {ti['file_path']}")
            elif name == "WebFetch" and ti.get("url"):
                inputs.append(f"url: {ti['url']}")
            elif name == "WebSearch" and ti.get("query"):
                inputs.append(f"search: {ti['query']}")
            elif name == "Grep" and ti.get("pattern"):
                inputs.append(f"grep: {ti['pattern']}")
        elif kind == "visit":
            ti = ev.get("tool_input") or {}
            title = (ti.get("title") or ev.get("text") or "")[:60]
            url = (ti.get("url") or "")[:80]
            inputs.append(f"visit: {title}" + (f" ({url})" if url else ""))
        elif kind == "search":
            q = (ev.get("text") or (ev.get("tool_input") or {}).get("query") or "")[:80]
            inputs.append(f"search: {q}")
        elif kind == "download":
            ti = ev.get("tool_input") or {}
            fname = (ti.get("target_path") or ev.get("text") or "")[:80]
            inputs.append(f"download: {os.path.basename(fname) if fname else '?'}")
        elif kind == "meeting":
            ti = ev.get("tool_input") or {}
            subj = (ti.get("subject") or ev.get("text") or "(no subject)")[:60]
            org = ti.get("organizer")
            atts = _attendee_count(ti.get("attendees"))
            inputs.append(f"meeting: {subj}" + (f" ({org}, {atts} attendees)" if org or atts else ""))
        elif kind == "email":
            ti = ev.get("tool_input") or {}
            subj = (ti.get("subject") or ev.get("text") or "(no subject)")[:60]
            sender = ti.get("from") or ti.get("from_email")
            inputs.append(f"email: {subj}" + (f" (from {sender})" if sender else ""))
        elif kind == "commit":
            ti = ev.get("tool_input") or {}
            subj = (ti.get("subject") or ev.get("text") or "")[:80]
            inputs.append(f"commit: {subj}")
    # dedupe
    seen = set()
    deduped = []
    for i in inputs:
        if i not in seen:
            seen.add(i)
            deduped.append(i)
    return deduped[:15]


def _attendee_count(attendees: object) -> int | None:
    """Count attendees from the various shapes adapters produce (list/str/int)."""
    if attendees is None:
        return None
    if isinstance(attendees, list):
        return len(attendees)
    if isinstance(attendees, (int, float)):
        return int(attendees)
    s = str(attendees).strip()
    if s.isdigit():
        return int(s)
    # Some adapters stringify a list — count separators as a rough estimate.
    if "," in s or ";" in s:
        return s.count(",") + s.count(";") + 1
    return None


def _attendee_names(attendees: object, cap: int = 5) -> list[str]:
    """Extract readable attendee names from the various shapes adapters produce."""
    if not attendees:
        return []
    names: list[str] = []
    if isinstance(attendees, list):
        for a in attendees[:cap * 2]:
            if isinstance(a, dict):
                name = a.get("name") or a.get("staff_name") or a.get("account") or a.get("email")
                if name:
                    names.append(str(name)[:40])
            elif isinstance(a, str):
                names.append(a[:40])
    elif isinstance(attendees, str):
        # Stringified list — split on delimiters.
        for part in attendees.replace(";", ",").split(","):
            part = part.strip().strip('"').strip("'")
            if part and len(part) < 60:
                names.append(part)
    return names[:cap]


def _extract_context(events: list[dict], source_kind: str) -> dict:
    """Pull the most diagnostic signals from events for the report/drill-down.

    Returns a structured dict (possibly empty) that lets the report answer
    "why did this task take as long as it did?" inline, without requiring the
    user to run a separate ``--task <id> --drill``. The data is already in the
    events — this function just surfaces it per source_kind:

      - meeting  → organizer, attendee count + names, location, is_all_day
      - browser  → search queries, top URLs/titles, downloads, visit count
      - comm     → senders, subjects, whether a reply was sent
      - ai_session → error samples + synthesized blocker, retry targets,
                     dominant tools, files touched
      - vcs      → commit subjects (if not already in git_commits)
      - filesystem → files touched

    All lists are capped (5 items, 120 chars each) to keep the task dict compact.
    """
    ctx: dict = {}
    if source_kind == "meeting":
        for ev in events:
            if ev.get("kind") != "meeting":
                continue
            ti = ev.get("tool_input") or {}
            organizer = ti.get("organizer")
            attendees = ti.get("attendees")
            location = ti.get("location")
            is_all_day = ti.get("is_all_day")
            ctx.setdefault("organizer", organizer)
            ctx.setdefault("attendees", _attendee_count(attendees))
            ctx.setdefault("attendee_names", _attendee_names(attendees))
            ctx.setdefault("location", location)
            if is_all_day is not None:
                ctx.setdefault("is_all_day", bool(is_all_day))
            ctx.setdefault("subject", ti.get("subject") or ev.get("text"))
            break  # one meeting event is enough; a task = one meeting
        return ctx

    if source_kind == "browser":
        queries, urls, titles, downloads = [], [], [], 0
        for ev in events:
            kind = ev.get("kind")
            ti = ev.get("tool_input") or {}
            if kind == "search":
                q = (ev.get("text") or ti.get("query") or "").strip()
                if q:
                    queries.append(q[:120])
            elif kind == "visit":
                title = (ti.get("title") or ev.get("text") or "").strip()
                url = (ti.get("url") or "").strip()
                if title:
                    titles.append(title[:120])
                if url:
                    urls.append(url[:120])
            elif kind == "download":
                downloads += 1
        # dedupe preserving order
        ctx["queries"] = _dedupe(queries)[:5]
        ctx["top_titles"] = _dedupe(titles)[:5]
        ctx["top_urls"] = _dedupe(urls)[:5]
        ctx["downloads"] = downloads
        ctx["n_visits"] = sum(1 for e in events if e.get("kind") == "visit")
        return ctx

    if source_kind == "comm":
        senders, subjects = [], []
        directions = set()
        im_conversations: list[str] = []
        im_senders: list[str] = []
        im_message_count = 0
        for ev in events:
            kind = ev.get("kind")
            ti = ev.get("tool_input") or {}
            if kind == "email":
                sender = ti.get("from") or ti.get("from_email")
                if sender:
                    senders.append(str(sender)[:60])
                subj = ti.get("subject") or ev.get("text")
                if subj:
                    subjects.append(str(subj)[:80])
                d = ti.get("direction")
                if d:
                    directions.add(d)
            elif kind == "chat_message":
                im_message_count += 1
                conv_name = ti.get("conversation_name")
                if conv_name:
                    im_conversations.append(str(conv_name)[:60])
                sender = ti.get("sender")
                if sender:
                    im_senders.append(str(sender)[:60])
        ctx["senders"] = _dedupe(senders)[:5]
        ctx["subjects"] = _dedupe(subjects)[:5]
        ctx["has_reply"] = "sent" in directions and "received" in directions
        if im_message_count:
            ctx["im_message_count"] = im_message_count
            ctx["im_conversations"] = _dedupe(im_conversations)[:5]
            ctx["im_senders"] = _dedupe(im_senders)[:5]
        return ctx

    if source_kind == "ai_session":
        # Error samples + synthesized blocker — the key signal for coding pain.
        error_texts, retry_targets = [], []
        files_touched = set()
        tool_counter: dict[str, int] = {}
        # Track tool_use calls by (tool, target) for retry detection.
        call_counts: dict[str, int] = {}
        for ev in events:
            kind = ev.get("kind")
            if kind == "tool_result" and ev.get("tool_is_error") is True:
                text = (ev.get("text") or "").strip()
                if text:
                    error_texts.append(text[:120])
            elif kind == "tool_use":
                name = ev.get("tool_name") or ""
                ti = ev.get("tool_input") or {}
                if name in ("Edit", "Write", "NotebookEdit") and ti.get("file_path"):
                    files_touched.add(str(ti["file_path"]))
                tool_counter[name] = tool_counter.get(name, 0) + 1
                # Retry target — same tool on same file/command.
                target = _retry_target_key(name, ti)
                if target:
                    key = f"{name}:{target}"
                    call_counts[key] = call_counts.get(key, 0) + 1
        # Synthesize a one-line blocker from the error texts.
        ctx["error_samples"] = _dedupe(error_texts)[:5]
        ctx["blocker"] = _synthesize_blocker(error_texts)
        # Retry targets: tools called 2+× on the same target.
        retries = [(k.split(":", 1)[0], k.split(":", 1)[1], v)
                   for k, v in call_counts.items() if v >= 2]
        retries.sort(key=lambda x: -x[2])
        ctx["retry_targets"] = [f"{t} on {_short_target(tg)} ({n}×)"
                                for t, tg, n in retries[:5]]
        ctx["dominant_tools"] = [t for t, _ in sorted(tool_counter.items(),
                                                      key=lambda x: -x[1])[:5]]
        ctx["files_touched"] = sorted(files_touched)[:5]
        # User prompts: top 3 distinct user messages (evidence of what the user was instructing).
        user_prompts = []
        for ev in events:
            if ev.get("kind") == "user_message" and ev.get("text"):
                text = ev["text"].strip().replace("\n", " ")
                # Skip system-reminders and command wrappers.
                if text and not text.startswith("<") and not text.startswith("[Request"):
                    prompt = text[:80]
                    if prompt not in user_prompts:
                        user_prompts.append(prompt)
        ctx["user_prompts"] = user_prompts[:3]
        return ctx

    if source_kind == "vcs":
        subjects = []
        for ev in events:
            if ev.get("kind") == "commit":
                ti = ev.get("tool_input") or {}
                subj = ti.get("subject") or ev.get("text")
                if subj:
                    subjects.append(str(subj)[:80])
        if subjects:
            ctx["commit_subjects"] = _dedupe(subjects)[:5]
        return ctx

    if source_kind == "filesystem":
        files = set()
        for ev in events:
            ti = ev.get("tool_input") or {}
            f = ti.get("path") or ti.get("file_path") or ev.get("text")
            if f:
                files.add(str(f)[:120])
        if files:
            ctx["files"] = sorted(files)[:5]
        return ctx

    return ctx


def _is_truthy(val: object) -> bool:
    """Check truthiness for values from external APIs that may return strings.

    Handles: True, "true", "True", "TRUE", 1, "1", "yes" → True.
    Handles: False, "false", "False", 0, "0", "", None → False.
    """
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, str):
        return val.strip().lower() in ("true", "1", "yes", "y")
    return bool(val)


def _dedupe(items: list[str]) -> list[str]:
    """Deduplicate a list preserving order."""
    seen = set()
    out = []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _retry_target_key(tool_name: str, ti: dict) -> str | None:
    """Return a target key for retry grouping (mirrors drill_down._extract_retry_target
    but simplified — we only need grouping, not hash precision)."""
    if tool_name in ("Edit", "Write", "NotebookEdit"):
        fp = ti.get("file_path") or ti.get("notebook_path")
        return str(fp) if fp else None
    if tool_name == "Bash":
        return str(ti.get("command", ""))[:80]
    if tool_name == "WebSearch":
        return str(ti.get("query", ""))
    if tool_name == "WebFetch":
        return str(ti.get("url", ""))
    if tool_name == "Grep":
        return str(ti.get("pattern", ""))
    return None


def _short_target(target: str) -> str:
    """Shorten a retry target for display (basename for paths)."""
    if "/" in target or "\\" in target:
        return os.path.basename(target.rstrip("/\\"))
    if len(target) > 50:
        return target[:50] + "..."
    return target


def _synthesize_blocker(error_texts: list[str]) -> str | None:
    """Synthesize a one-line 'blocker' description from error text samples.

    Groups similar errors by pattern and returns the most common pattern as a
    human-readable string. Returns None if no errors. This is deterministic
    pattern matching — not an LLM summary.
    """
    if not error_texts:
        return None
    from collections import Counter
    # Classify each error into a pattern bucket.
    patterns: list[str] = []
    for text in error_texts:
        t = text.lower()
        if "407" in t or ("proxy" in t and "tunnel" in t):
            patterns.append("corporate proxy auth (407)")
        elif "timeout" in t or "timed out" in t:
            patterns.append("command timeout")
        elif "rejected" in t or "doesn't want to proceed" in t:
            patterns.append("user rejected tool use")
        elif "not found" in t or "no such file" in t or "does not exist" in t:
            patterns.append("file/path not found")
        elif "permission denied" in t or "access is denied" in t:
            patterns.append("permission denied")
        elif "exit code 128" in t or "merge conflict" in t:
            patterns.append("git failure (exit 128)")
        elif "exit code 1" in t:
            patterns.append("command failed (exit 1)")
        elif "syntaxerror" in t or "indentationerror" in t:
            patterns.append("Python syntax/indent error")
        elif "modulenotfounderror" in t or "importerror" in t:
            patterns.append("module import error")
        elif "connection" in t and ("refused" in t or "reset" in t or "closed" in t):
            patterns.append("network connection error")
        else:
            patterns.append("other error")
    counts = Counter(patterns)
    top_pattern, top_n = counts.most_common(1)[0]
    if top_pattern == "other error":
        # Don't synthesize a vague "other error" — show the first raw snippet instead.
        return error_texts[0][:100]
    return f"{top_pattern} ({top_n} of {len(error_texts)} errors)"


def _compute_active_seconds(events: list[dict], gap_threshold: float = GAP_THRESHOLD_SECONDS) -> tuple[float, float]:
    """Compute active work time from actual event timestamps — no guessing.

    Two grounded sources of duration:

    1. **Real duration (meetings):** if any event carries ``extra.end_ts``, the task
       has a real start+end. Use the latest ``end_ts`` minus the earliest timestamp.
       This is the actual meeting length from welink-cli / calendar — not inferred.

    2. **Inter-event span (everything else):** for point-in-time events (commits,
       messages, browser visits, emails), the only grounded measure is the span
       between consecutive events. We sum the inter-event intervals that are below
       the gap threshold (continuous activity) and exclude gaps above it (idle).
       A session open 4h with 3 messages in 15min → 15min active, not 4h.

    What we do NOT do: fabricate a per-event "collar" (e.g. 5 min around each
    event). That was a guess with no basis in the data. A single event at one
    timestamp has 0 active time — we know it happened, not how long it took.

    Returns ``(active_seconds, excised_gap_seconds)`` where ``excised_gap_seconds``
    is the sum of inter-event intervals that exceeded the gap threshold (mid-task
    idle gaps that were excluded from the active total).
    """
    ts_list = sorted(e["timestamp"] for e in events if e.get("timestamp") is not None)
    if not ts_list:
        return 0.0, 0.0

    # 1. Real duration: meeting events carry extra.end_ts (from welink-cli/calendar).
    end_ts_values = [e["extra"]["end_ts"] for e in events
                     if (e.get("extra") or {}).get("end_ts") is not None]
    if end_ts_values:
        real_end = max(end_ts_values)

        # All-day calendar entries (holiday markers, "月末周六工作日") have
        # start=midnight, end=midnight+86400. These are day-markers, not real
        # meetings — the user didn't spend 24h in a meeting. Return 0 active.
        # The is_all_day flag is on the event's tool_input (set by welink_cli/
        # outlook adapters).
        is_all_day = any(
            _is_truthy((e.get("tool_input") or {}).get("is_all_day"))
            for e in events
        )
        if is_all_day:
            return 0.0, max(0.0, real_end - ts_list[0])

        # Multi-day events (e.g. "下一代智能运维平台集中研讨" spanning 2 days at a
        # location): nobody attends a 48h meeting non-stop. Cap at 8h (a working
        # day) and flag the rest as excised. The actual attendance is unknown.
        raw_duration = real_end - ts_list[0]
        if raw_duration > 8 * 3600:
            capped = 8 * 3600
            return float(capped), max(0.0, raw_duration - capped)

        # C2 fix: clamp real_end to MAX_MEETING_DURATION from the task start.
        # A corrupt millis value, year-2099 calendar entry, or all-day event
        # can produce active_seconds of hours/days/years. No real meeting is
        # longer than 24h — clamp to prevent one bad timestamp from poisoning
        # the period total.
        if real_end - ts_list[0] > MAX_MEETING_DURATION:
            real_end = ts_list[0] + MAX_MEETING_DURATION
        return max(0.0, real_end - ts_list[0]), 0.0

    # 2. Inter-event span: sum intervals between consecutive events that are
    # below the gap threshold. Gaps > threshold = idle (excluded).
    if len(ts_list) < 2:
        # Single event — we know it happened, not how long it took.
        return 0.0, 0.0
    active = 0.0
    excised = 0.0
    MAX_EXCISED_GAP = 24 * 3600  # cap each gap at 24h — longer = corrupt timestamp, not idle
    for i in range(1, len(ts_list)):
        delta = ts_list[i] - ts_list[i - 1]
        if delta <= gap_threshold:
            active += delta
        else:
            # Cap the excised gap — a delta of years means a corrupt timestamp
            # or mixed-session data, not real idle time within a task.
            excised += min(delta, MAX_EXCISED_GAP)
    return active, excised


# Three-valued success constants.
SUCCESS_SUCCEEDED = "succeeded"
SUCCESS_FAILED = "failed"
SUCCESS_UNKNOWN = "unknown"


def _determine_success(flavor: str, events: list[dict], task_status: str | None,
                       source_kind: str = "ai_session") -> tuple[str, str]:
    """Determine task success from signals. Returns (success, evidence).

    Three-valued: "succeeded" / "failed" / "unknown".
    "unknown" means no signal exists — NOT failure.

    Per-type signals:
      - AI coding (explicit): TaskUpdate(completed) + no errors → succeeded;
        TaskUpdate(deleted) → failed; no terminal update → unknown.
      - AI coding (implicit): end_turn + no errors + no corrections → succeeded;
        errors + corrections → failed; otherwise → unknown.
      - VCS: commit landed → succeeded; commit reverted → failed; no commit → unknown.
      - Research (browser): artifact produced (Write/Edit) → succeeded; browsing only → unknown.
      - Meeting: no in-task signal → unknown (refined by refine_success()).
      - Email (comm): reply sent in thread → succeeded; no reply → unknown.
    """
    # Per-type signals for non-ai_session sources
    if source_kind == "vcs":
        return _determine_vcs_success(events)
    if source_kind == "browser":
        return _determine_research_success(events)
    if source_kind == "meeting":
        return SUCCESS_UNKNOWN, "no in-task signal (follow-up checked in refine_success)"
    if source_kind == "comm":
        return _determine_email_success(events)
    if source_kind != "ai_session":
        # filesystem, doc_authoring, auxiliary — no success signal
        return SUCCESS_UNKNOWN, f"no success signal for source_kind={source_kind}"

    # AI-coding signals (existing logic, mapped to three-valued strings)
    errors = sum(1 for e in events if e.get("tool_is_error") is True)
    if flavor == "explicit":
        if task_status == "completed" and errors == 0:
            return SUCCESS_SUCCEEDED, "TaskUpdate(completed) with no tool errors"
        elif task_status == "completed" and errors > 0:
            return SUCCESS_SUCCEEDED, f"TaskUpdate(completed) but {errors} tool error(s) during execution"
        elif task_status in ("deleted",):
            return SUCCESS_FAILED, f"TaskUpdate({task_status})"
        else:
            return SUCCESS_UNKNOWN, f"no terminal TaskUpdate (status={task_status})"
    else:  # implicit
        # Find the last assistant message's stop_reason
        last_stop = None
        for e in reversed(events):
            if e.get("kind") == "assistant_message":
                last_stop = e.get("stop_reason")
                break
        # Check if the next user message (after the task) is a correction
        # (heuristic: if the task's last user message is a correction, it likely failed)
        has_correction = any(
            e.get("kind") == "user_message" and _is_correction(e.get("text"))
            for e in events
        )
        if errors > 0 and has_correction:
            return SUCCESS_FAILED, f"{errors} tool error(s) + user correction"
        elif last_stop == "end_turn" and errors == 0 and not has_correction:
            return SUCCESS_SUCCEEDED, "assistant end_turn, no errors, no corrections"
        elif last_stop == "end_turn" and errors > 0:
            return SUCCESS_UNKNOWN, f"assistant end_turn but {errors} tool error(s)"
        else:
            return SUCCESS_UNKNOWN, f"stop_reason={last_stop}, errors={errors}"


def _determine_vcs_success(events: list[dict]) -> tuple[str, str]:
    """VCS task success: commit landed → succeeded; reverted → failed; no commit → unknown."""
    has_commit = any(e.get("kind") == "commit" for e in events)
    has_revert = any(
        "revert" in str((e.get("tool_input") or {}).get("subject", "")).lower()
        or "revert" in str(e.get("text", "")).lower()
        for e in events
    )
    if has_revert:
        return SUCCESS_FAILED, "commit reverted"
    if has_commit:
        return SUCCESS_SUCCEEDED, "commit landed"
    return SUCCESS_UNKNOWN, "no commit detected"


def _determine_research_success(events: list[dict]) -> tuple[str, str]:
    """Research task success: artifact produced (Write/Edit) → succeeded; browsing only → unknown."""
    has_artifact = any(
        e.get("kind") == "tool_use" and e.get("tool_name") in ("Write", "Edit", "NotebookEdit")
        for e in events
    )
    if has_artifact:
        return SUCCESS_SUCCEEDED, "research produced an artifact (Write/Edit)"
    return SUCCESS_UNKNOWN, "browsing with no follow-up artifact"


def _determine_email_success(events: list[dict]) -> tuple[str, str]:
    """Email task success: reply sent in thread → succeeded; no reply → unknown."""
    directions = []
    for e in events:
        if e.get("kind") == "email":
            ti = e.get("tool_input") or {}
            d = ti.get("direction")
            if d:
                directions.append(d)
    has_received = "received" in directions
    has_sent = "sent" in directions
    if has_received and has_sent:
        recv_idx = directions.index("received")
        sent_idx = directions.index("sent")
        if sent_idx > recv_idx:
            return SUCCESS_SUCCEEDED, "reply sent in thread"
    return SUCCESS_UNKNOWN, "no reply detected"


# C3 fix: commits whose subjects match this pattern are not success signals.
_NON_SUCCESS_COMMIT_RE = re.compile(r'revert|wip|tmp|fixup|squash', re.IGNORECASE)

# C3 fix: stopwords excluded from token-overlap matching.
_TOKEN_STOPWORDS = frozenset({
    "the", "a", "an", "is", "it", "to", "of", "in", "on", "for", "and", "or",
    "but", "not", "with", "by", "at", "from", "as", "be", "was", "are", "this",
    "that", "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "should", "may", "might", "must", "shall", "if", "then", "else",
    "when", "where", "why", "how", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "too", "very", "just", "so",
})


def _significant_tokens(text: str | None) -> set[str]:
    """Extract significant tokens (length >= 3, not stopwords) from text."""
    if not text:
        return set()
    tokens = re.split(r'[^a-zA-Z0-9]+', text.lower())
    return {t for t in tokens if len(t) >= 3 and t not in _TOKEN_STOPWORDS}


def _commit_is_meaningful(commit: dict) -> bool:
    """Check if a commit subject represents real work (not revert/wip/tmp/fixup/squash)."""
    subject = commit.get("subject") or ""
    return not _NON_SUCCESS_COMMIT_RE.search(subject)


def _has_semantic_overlap(task_subject: str | None, commit: dict) -> bool:
    """Check if a commit subject shares at least one significant token with the task subject.

    If the task has no subject, skip this check (allow the commit).
    """
    if not task_subject or not task_subject.strip():
        return True  # no subject to compare — allow the commit
    task_tokens = _significant_tokens(task_subject)
    if not task_tokens:
        return True  # no significant tokens to match — allow the commit
    commit_tokens = _significant_tokens(commit.get("subject") or "")
    return bool(task_tokens & commit_tokens)


def refine_success(tasks: list[dict]) -> list[dict]:
    """Refine task success based on cross-task and post-linking signals.

    Called after cross-source linking has attached git_commits and after
    all tasks are segmented. Upgrades 'unknown' to 'succeeded' or 'failed'
    based on per-type signals that require cross-task context:

      - git_commits attached → succeeded (commit linked to this task), but
        only if the commit is meaningful (not revert/wip/tmp/fixup/squash),
        shares semantic overlap with the task subject, and the task has no
        in-task error signal (C3 fix).
      - Research (browser) followed by coding task within 1h → succeeded.
      - Meeting with follow-up referencing subject keywords within 24h → succeeded.
      - Conversation followed by coding task within 1h → succeeded.

    After all upgrades, a cross-task revert pass (M7 fix) scans later tasks
    for revert commits that downgrade a previously-upgraded task.

    Be conservative: when in doubt, leave as 'unknown'.
    """
    sorted_tasks = sorted(tasks, key=lambda t: t.get("start") or 0.0)
    n = len(sorted_tasks)

    for i, t in enumerate(sorted_tasks):
        if t.get("success") != SUCCESS_UNKNOWN:
            continue

        source_kind = t.get("source_kind", "ai_session")
        end_ts = t.get("end") or t.get("start") or 0.0

        # Signal 1: git_commits attached by cross_source.py
        # C3 fix: don't blindly upgrade — filter non-success commits, require
        # semantic overlap, and respect in-task error signals.
        if t.get("git_commits"):
            commits = t["git_commits"]
            # Exclude commits whose subject matches revert/wip/tmp/fixup/squash.
            meaningful_commits = [c for c in commits if _commit_is_meaningful(c)]
            if not meaningful_commits:
                # All commits are non-success signals (e.g. all WIP/revert) — don't upgrade.
                continue
            # If the task has in-task errors, don't upgrade based on commit alone.
            if t.get("errors", 0) > 0:
                continue
            # Require semantic overlap between task subject and at least one commit.
            task_subject = t.get("subject")
            has_overlap = any(
                _has_semantic_overlap(task_subject, c) for c in meaningful_commits
            )
            if not has_overlap:
                continue
            hash_short = (meaningful_commits[0].get("hash") or "?")[:8]
            t["success"] = SUCCESS_SUCCEEDED
            t["success_evidence"] = f"git commit linked: {hash_short}"
            continue

        # Signal 2: Research (browser) followed by coding task within 1h
        if source_kind == "browser":
            for j in range(i + 1, n):
                next_t = sorted_tasks[j]
                next_start = next_t.get("start") or 0.0
                if next_start > end_ts + 3600:
                    break
                if next_start >= end_ts:
                    next_tools = set(next_t.get("tool_names") or [])
                    if next_tools & {"Write", "Edit", "NotebookEdit"}:
                        t["success"] = SUCCESS_SUCCEEDED
                        t["success_evidence"] = "research followed by coding task within 1h"
                        break
            continue

        # Signal 3: Meeting with follow-up referencing subject keywords within 24h
        if source_kind == "meeting":
            subject = (t.get("subject") or "").lower()
            keywords = [w for w in subject.split() if len(w) > 2]
            if keywords:
                for j in range(i + 1, n):
                    next_t = sorted_tasks[j]
                    next_start = next_t.get("start") or 0.0
                    if next_start > end_ts + 86400:
                        break
                    if next_start >= end_ts:
                        next_subject = (next_t.get("subject") or "").lower()
                        next_commits = next_t.get("git_commits") or []
                        commit_text = " ".join(
                            (c.get("subject") or "").lower() for c in next_commits
                        )
                        check_text = next_subject + " " + commit_text
                        if any(kw in check_text for kw in keywords):
                            t["success"] = SUCCESS_SUCCEEDED
                            t["success_evidence"] = "follow-up within 24h references meeting subject"
                            break
            continue

        # Signal 4: Conversation (ai_session, no tools, few events) followed by coding
        if source_kind == "ai_session":
            tools = set(t.get("tool_names") or [])
            event_count = t.get("event_count", 0)
            if not tools and event_count <= 3:
                for j in range(i + 1, n):
                    next_t = sorted_tasks[j]
                    next_start = next_t.get("start") or 0.0
                    if next_start > end_ts + 3600:
                        break
                    if next_start >= end_ts:
                        next_tools = set(next_t.get("tool_names") or [])
                        if next_tools & {"Write", "Edit", "Bash"}:
                            t["success"] = SUCCESS_SUCCEEDED
                            t["success_evidence"] = "conversation followed by coding task"
                            break

    # M7 fix: Cross-task revert detection.
    # A revert almost always lands as a SEPARATE task in a later session.
    # For each task upgraded to 'succeeded' via a linked commit, scan later
    # tasks (within 7 days, same cwd) for a commit whose subject contains
    # "revert". If found, downgrade the original task.
    #
    # Limitation: force-push/reset reverts are structurally undetectable
    # (no commit record exists to scan). This pass only catches explicit
    # "Revert ..." commits.
    REVERT_WINDOW_SECONDS = 7 * 24 * 3600  # 7 days
    for i, t in enumerate(sorted_tasks):
        if t.get("success") != SUCCESS_SUCCEEDED:
            continue
        if not t.get("git_commits"):
            continue
        # Only check tasks upgraded via commit-link evidence.
        evidence = t.get("success_evidence") or ""
        if "git commit linked" not in evidence:
            continue
        t_cwd = t.get("cwd")
        t_end = t.get("end") or t.get("start") or 0.0
        for j in range(i + 1, n):
            next_t = sorted_tasks[j]
            next_start = next_t.get("start") or 0.0
            if next_start > t_end + REVERT_WINDOW_SECONDS:
                break
            # Same cwd check (normalized).
            if t_cwd and next_t.get("cwd") and t_cwd != next_t.get("cwd"):
                continue
            next_commits = next_t.get("git_commits") or []
            for c in next_commits:
                if "revert" in (c.get("subject") or "").lower():
                    t["success"] = SUCCESS_FAILED
                    t["success_evidence"] = (
                        f"downgraded: revert commit found in later task "
                        f"({(c.get('hash') or '?')[:8]})"
                    )
                    break
            if t["success"] == SUCCESS_FAILED:
                break

    return tasks


def _derive_subject_from_events(events: list[dict]) -> str | None:
    """Derive a human-readable subject from event data when no user message exists.

    Meetings, git commits, emails, and browser visits don't carry a user_message
    event, so segment_implicit leaves ``current_subject`` as None. The actual title
    is in ``event["text"]`` (meeting subject, commit message, email subject, page
    title) or ``event["tool_input"]["subject"]``. This picks the most informative
    one so the report shows "【会议通知】 AI4W 站会" instead of "(no subject)".
    """
    # Two-pass: first look for the most informative structured field (subject,
    # conversation_name) across ALL events. Only then fall back to text.
    # This prevents a message-text field from shadowing a conversation_name
    # that appears on a later event.
    for e in events:
        ti = e.get("tool_input") or {}
        if isinstance(ti, dict) and ti.get("subject"):
            s = str(ti["subject"]).strip().strip('"')
            if s:
                return s[:MAX_SUBJECT_LEN]
    # IM conversation name (second priority — identifies who the chat was with).
    for e in events:
        ti = e.get("tool_input") or {}
        if isinstance(ti, dict) and ti.get("conversation_name"):
            s = str(ti["conversation_name"]).strip().strip('"')
            if s:
                return s[:MAX_SUBJECT_LEN]
    # Text field (meeting title, commit message, email subject, page title).
    # Skip non-informative text like "(CARD_MSG)" or "(message)".
    for e in events:
        text = (e.get("text") or "").strip().strip('"')
        if text and text != "(no text)" and not re.match(r'^\([A-Z_]+\)$', text):
            return text[:MAX_SUBJECT_LEN]
    return None


def _make_task(tid: str, flavor: str, events: list[dict], subject: str | None,
               task_status: str | None = None) -> dict:
    ts = [e["timestamp"] for e in events if e.get("timestamp")]
    start = min(ts) if ts else 0.0
    end = max(ts) if ts else 0.0
    tool_uses = [e for e in events if e.get("kind") == "tool_use"]
    output_tokens = 0
    input_tokens = 0
    for e in events:
        u = e.get("usage")
        if isinstance(u, dict):
            output_tokens += int(u.get("output_tokens") or 0)
            input_tokens += int(u.get("input_tokens") or 0)
    errors = sum(1 for e in events if e.get("tool_is_error") is True)
    first = events[0] if events else {}
    wall_clock = round(end - start, 1) if end >= start else 0.0
    active_raw, excised_raw = _compute_active_seconds(events)
    active = round(active_raw, 1)
    excised_gap = round(excised_raw, 1)
    # Subject fallback: meetings/commits/emails have no user_message — derive from
    # event text so the report shows the real title instead of "(no subject)".
    if not subject or subject == "(no subject)":
        subject = _derive_subject_from_events(events)
    # For meetings with a real end_ts, the wall_clock should reflect the full
    # meeting span (real_end - start), not the event-timestamp span (which for
    # single-event meetings is 0). The active time may be less than wall_clock
    # (all-day → 0h, multi-day → capped 8h) — that's the honest picture.
    end_ts_values = [e["extra"]["end_ts"] for e in events
                     if (e.get("extra") or {}).get("end_ts") is not None]
    if end_ts_values:
        real_end = max(end_ts_values)
        if MAX_MEETING_DURATION and real_end - start > MAX_MEETING_DURATION:
            real_end = start + MAX_MEETING_DURATION
        wall_clock = round(real_end - start, 1) if real_end > start else 0.0
    elif active > wall_clock:
        wall_clock = active
    source_kind = first.get("source_kind", "ai_session")
    success, success_evidence = _determine_success(flavor, events, task_status, source_kind)
    context = _extract_context(events, source_kind)

    # Build the task dict first (the summarizer reads task["context"], time fields).
    task = {
        "id": tid,
        "flavor": flavor,
        "source": first.get("source", "claude_code"),
        "source_kind": source_kind,
        "session_id": first.get("session_id"),
        "cwd": first.get("cwd"),
        "git_branch": first.get("git_branch"),
        "subject": subject,
        "start": start,
        "end": end,
        "duration_seconds": wall_clock,        # wall-clock span (kept for backwards compat)
        "wall_clock_seconds": wall_clock,      # explicit name
        "active_seconds": active,              # active work time (gaps excised)
        "excised_gap_seconds": excised_gap,    # sum of mid-task gaps > threshold (excluded from active)
        "event_count": len(events),
        "tool_calls": len(tool_uses),
        "tool_names": sorted({e.get("tool_name") for e in tool_uses if e.get("tool_name")}),
        "output_tokens": output_tokens,
        "input_tokens": input_tokens,
        "errors": errors,
        "inputs": _extract_inputs(events),
        "outputs": _extract_output_artifacts(events),
        "success": success,
        "success_evidence": success_evidence,
        "task_status": task_status,
        "context": context,
    }

    # Content-driven root-cause narrative — grounded in the actual event text.
    # Stored in context["narrative"] so the render layer can display it inline.
    _summarize_fn = _get_summarizer()
    if _summarize_fn is not None:
        narrative = _summarize_fn(task, events)
        if narrative:
            context["narrative"] = narrative

    # Human-involvement metrics — distinguish HUMAN time (the user typing,
    # clicking, interrupting) from MACHINE time (agent working autonomously).
    # This drives the re-ranking of time sinks by human cost, not raw active time.
    _human_fn = _get_human_involvement_fn()
    if _human_fn is not None:
        task["human_data"] = _human_fn(events, task)

    return task


def segment_explicit(events: list[dict]) -> tuple[list[dict], list[dict]]:
    """Find explicit tasks (TaskCreate / TaskUpdate bounded). Returns (tasks, remaining_events).

    An explicit task starts at a TaskCreate tool_use. Its scope extends until the first
    terminal TaskUpdate (status=completed/deleted) AFTER it — tracking across the WHOLE
    session, not just to the next TaskCreate. If no terminal update arrives, the task
    extends to session end with status="unknown" (previously under-bounded to the next
    TaskCreate, yielding 0-5s tasks). Multiple tasks may be open in parallel.

    Events not inside any explicit task are returned as 'remaining' for implicit segmentation.
    """
    tasks: list[dict] = []
    claimed = set()  # indices of events claimed by an explicit task
    n = len(events)

    # First pass: find all TaskCreate boundaries with their subject as identity key.
    creates: list[tuple[int, str, str]] = []  # (idx, taskId, subject)
    for i, ev in enumerate(events):
        if ev.get("kind") == "tool_use" and ev.get("tool_name") == "TaskCreate":
            ti = ev.get("tool_input") or {}
            subject = ti.get("subject") or "(no subject)"
            tid = subject[:40] or f"create-{i}"
            creates.append((i, tid, subject))

    # For each create, find its end: the FIRST terminal TaskUpdate after it. We do NOT
    # stop at the next TaskCreate — parallel tasks are allowed. If none found, extend
    # to session end with status="unknown".
    for ci, (start_idx, tid, subject) in enumerate(creates):
        end_idx = n - 1  # default: session end
        status = "unknown"
        for j in range(start_idx + 1, n):
            ev = events[j]
            if ev.get("kind") == "tool_use" and ev.get("tool_name") == "TaskUpdate":
                ti = ev.get("tool_input") or {}
                if ti.get("status") in ("completed", "deleted"):
                    end_idx = j
                    status = ti.get("status")
                    break
        # Claim events from start to end. Ranges may overlap for parallel tasks —
        # both tasks share the overlapped events. Implicit pass gets only unclaimed.
        for k in range(start_idx, end_idx + 1):
            claimed.add(k)
        task_events = events[start_idx:end_idx + 1]
        tasks.append(_make_task(f"explicit-{ci+1}", "explicit", task_events, subject, status))

    remaining = [ev for i, ev in enumerate(events) if i not in claimed]
    return tasks, remaining


def segment_implicit(events: list[dict], counter: list[int]) -> list[dict]:
    """Segment a stream of events (those not in explicit tasks) into implicit tasks.

    `counter` is a one-element list used to keep implicit task IDs globally unique.
    """
    if not events:
        return []
    tasks: list[dict] = []
    current: list[dict] = []
    current_subject: str | None = None
    last_ts: float | None = None
    current_cwd: str | None = events[0].get("cwd")

    def flush():
        nonlocal current, current_subject
        if current:
            counter[0] += 1
            tasks.append(_make_task(f"implicit-{counter[0]}", "implicit", current, current_subject))
            current = []
            current_subject = None

    for ev in events:
        ts = ev.get("timestamp")
        # Boundary heuristics
        is_user_msg = ev.get("kind") == "user_message"
        boundary = False
        if current:
            # Split on any large gap between consecutive events — a session left open
            # for hours/days between messages produces a single nonsense task spanning
            # the whole gap. This is the "session open but idle" problem.
            if ts and last_ts and (ts - last_ts) > GAP_THRESHOLD_SECONDS:
                boundary = True
            elif is_user_msg and ev.get("cwd") != current_cwd:
                boundary = True
            elif is_user_msg and not _is_correction(ev.get("text")) and current_subject is not None:
                # New non-correction user message => new task
                boundary = True
        if boundary:
            flush()
        if is_user_msg:
            if not current or current_subject is None:
                current_subject = _summarize_message(ev.get("text"))
            current_cwd = ev.get("cwd")
        current.append(ev)
        if ts:
            last_ts = ts
    flush()
    return tasks


def segment(events: list[dict], use_advanced: bool = True) -> list[dict]:
    """Full segmentation: explicit first, then implicit over the remainder.

    Events without a timestamp are dropped — they are session metadata lines
    (mode, permission-mode, file-history-snapshot, etc.) that carry no time signal
    and would otherwise create phantom zero-duration tasks.

    When `use_advanced` is True and the optional libraries (ruptures, sklearn) are
    available, implicit segmentation uses PELT change-point detection + GMM gap
    threshold (Phase 4). Otherwise it falls back to the naive gap+cwd heuristics.
    """
    events = [e for e in events if e.get("timestamp") is not None]
    explicit_tasks, remaining = segment_explicit(events)
    # Group remaining by session for implicit segmentation (don't cross sessions).
    remaining.sort(key=lambda e: (e.get("session_id") or "", e.get("timestamp") or 0.0))
    implicit_tasks: list[dict] = []
    counter = [0]
    # split remaining into per-session runs
    by_session: dict[str, list[dict]] = {}
    for ev in remaining:
        sid = ev.get("session_id") or "none"
        by_session.setdefault(sid, []).append(ev)

    # Try advanced segmentation (Phase 4); fall back to naive if unavailable.
    advanced_ok = False
    if use_advanced:
        try:
            from advanced_segment import segment_implicit_advanced
            advanced_ok = True
        except ImportError:
            pass

    for sid, evs in by_session.items():
        evs.sort(key=lambda e: e.get("timestamp") or 0.0)
        if advanced_ok:
            implicit_tasks.extend(segment_implicit_advanced(evs, counter))
        else:
            implicit_tasks.extend(segment_implicit(evs, counter))
    all_tasks = explicit_tasks + implicit_tasks
    all_tasks.sort(key=lambda t: t.get("start") or 0.0)
    return all_tasks


if __name__ == "__main__":
    import sys, os, json
    sys.path.insert(0, os.path.dirname(__file__))
    from claude_code_adapter import collect_events

    events = collect_events()
    tasks = segment(events)
    print(f"# {len(tasks)} tasks from {len(events)} events", file=sys.stderr)
    for t in tasks:
        print(json.dumps(t, ensure_ascii=False))
