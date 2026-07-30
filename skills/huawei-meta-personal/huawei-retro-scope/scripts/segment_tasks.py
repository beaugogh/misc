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

import re
from typing import Iterator

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
    if len(text) > MAX_SUBJECT_LEN:
        return text[:MAX_SUBJECT_LEN] + "…"
    return text


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
    """Pull input artifacts: user messages that started the task, files Read, URLs fetched."""
    inputs = []
    for ev in events:
        if ev.get("kind") == "user_message" and ev.get("text"):
            inputs.append(f"prompt: {ev['text'][:100]}")
        elif ev.get("kind") == "tool_use":
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
    # dedupe
    seen = set()
    deduped = []
    for i in inputs:
        if i not in seen:
            seen.add(i)
            deduped.append(i)
    return deduped[:15]


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
    for e in events:
        ti = e.get("tool_input") or {}
        # Meeting/email subject from tool_input
        if isinstance(ti, dict) and ti.get("subject"):
            s = str(ti["subject"]).strip().strip('"')
            if s:
                return s[:MAX_SUBJECT_LEN]
        # Text field (meeting title, commit message, email subject, page title)
        text = (e.get("text") or "").strip().strip('"')
        if text and text != "(no text)":
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
    # For meetings with a real end_ts, the active time IS the real duration and
    # may exceed the task's wall_clock (which was computed from event timestamps
    # that may not include the meeting's actual end). Use the real duration for
    # both — it's the grounded number.
    if active > wall_clock:
        wall_clock = active
    source_kind = first.get("source_kind", "ai_session")
    success, success_evidence = _determine_success(flavor, events, task_status, source_kind)
    return {
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
    }


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
