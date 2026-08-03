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


def _summarize_ai_session(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for an AI coding session.

    Structure: Goal → Struggle (merged: what failed + why it was hard) → Time.
    """
    # 1. Goal: first real user message, cleaned of conversational prefixes.
    # Only the user's prompt — never the assistant's response.
    user_msgs = [e for e in events if e.get("kind") == "user_message" and e.get("text")]
    goal = _clean_user_goal(user_msgs[0].get("text")) if user_msgs else ""
    goal = _strip_conversational_prefix(goal)

    # 2. Error-command pairs + diagnostics (the struggle).
    error_pairs = _pair_errors_with_commands(events)
    asst_texts = [(e.get("text") or "") for e in events if e.get("kind") == "assistant_message"]
    diagnostics = _extract_diagnostic_sentences(asst_texts)

    ctx = task.get("context") or {}
    retry_targets = ctx.get("retry_targets") or []

    active_h = (task.get("active_seconds") or 0) / 3600
    wall_h = (task.get("wall_clock_seconds") or 0) / 3600
    excised_h = (task.get("excised_gap_seconds") or 0) / 3600
    n_errors = task.get("errors", 0)
    n_tool_calls = task.get("tool_calls", 0)

    parts: list[str] = []

    # Goal — just the user's intent, not the assistant's response.
    if goal and not _CONTINUATION_RE.match(goal):
        parts.append(f"Goal: {goal}.")

    # Struggle — merged section: what went wrong + why it was hard.
    # Reframed as a struggle description, not a mundane error log.
    struggle = _synthesize_struggle(n_errors, error_pairs, diagnostics, retry_targets, ctx)
    if struggle:
        parts.append(f"Struggle: {struggle}")

    # Time explanation.
    if excised_h > 1 and excised_h > active_h:
        parts.append(
            f"{active_h:.1f}h active（Wall {wall_h:.1f}h）——{excised_h:.1f}h 空闲/隔夜间隔。"
        )
    elif n_errors >= 5 or (retry_targets and active_h > 1):
        parts.append(
            f"{active_h:.1f}h，{n_errors} 个错误，{n_tool_calls} 次工具调用。"
        )
    elif active_h > 0.5:
        files = ctx.get("files_touched") or []
        if files:
            parts.append(
                f"{active_h:.1f}h，编辑了 {len(files)} 个文件："
                f"{', '.join(os.path.basename(f) for f in files[:3])}。"
            )
        else:
            parts.append(f"{active_h:.1f}h active。")

    return " ".join(parts) if parts else ""


def _synthesize_struggle(n_errors: int, error_pairs: list[tuple[str, str]],
                         diagnostics: list[str], retry_targets: list[str],
                         ctx: dict) -> str:
    """Synthesize a single struggle description that explains WHY it was hard.

    Merges the old "Struggle" (what failed) and "Difficulty" (why it was hard)
    into one coherent description. Reframes mundane error logs as struggle
    narratives — e.g. instead of "'edit README.md' → File has not been read
    yet", says "repeatedly hit file-read-before-edit errors — the workflow
    kept skipping the Read step before attempting edits."
    """
    if not error_pairs and not diagnostics and n_errors == 0:
        return ""

    # Classify the error pattern.
    error_texts = [err.lower() for _, err in error_pairs]
    all_text = " ".join(error_texts)

    patterns: list[str] = []
    if "407" in all_text or ("proxy" in all_text and "tunnel" in all_text):
        patterns.append("企业代理认证阻止 git/网络访问")
    if "timeout" in all_text or "timed out" in all_text:
        patterns.append("命令超时（网络慢或进程挂起）")
    if "not found" in all_text or "no such file" in all_text:
        patterns.append("文件或路径缺失——环境配置不正确")
    if "permission denied" in all_text or "access is denied" in all_text:
        patterns.append("权限不足——拒绝访问")
    if "doesn't want to proceed" in all_text or "rejected" in all_text:
        patterns.append("用户拒绝工具调用——agent 反复提出不需要的操作")
    if "exit code 128" in all_text or "merge conflict" in all_text:
        patterns.append("git 失败（合并冲突、推送被拒）")
    if "modulenotfounderror" in all_text or "importerror" in all_text:
        patterns.append("Python 依赖缺失——环境搭建不完整")
    if "syntaxerror" in all_text or "indentationerror" in all_text:
        patterns.append("Python 语法/缩进错误——编辑时反复破坏代码")
    if "file has not been read" in all_text:
        patterns.append("编辑前未读取文件——工作流反复跳过 Read 步骤")

    # Count retries.
    retry_count = 0
    if retry_targets:
        for rt in retry_targets:
            m = re.search(r'\((\d+)×\)', rt)
            if m:
                retry_count += int(m.group(1))

    # Build the struggle description.
    bits: list[str] = []

    if patterns:
        pattern_str = "；".join(patterns[:2])
        if retry_count >= 5:
            bits.append(f"{pattern_str}，尽管重试 {retry_count} 次仍反复出现——根本原因未被解决")
        elif n_errors >= 10:
            bits.append(f"{pattern_str}，导致 {n_errors} 个错误——尝试了多种方法均未解决根本问题")
        else:
            bits.append(f"{pattern_str}（{n_errors} 个错误）")
    elif n_errors > 0:
        if error_pairs:
            cmd, err = error_pairs[0]
            bits.append(f"反复遇到 '{cmd}' 失败（共 {n_errors} 次）——{err}")
        else:
            bits.append(f"执行过程中出现 {n_errors} 个错误")
    elif diagnostics:
        bits.append(diagnostics[0])

    if not bits and n_errors == 0:
        return ""

    return "。".join(bits) + "。"


def _summarize_browser(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a browser/research session."""
    ctx = task.get("context") or {}
    titles = ctx.get("top_titles") or []
    queries = ctx.get("queries") or []
    downloads = ctx.get("downloads") or 0
    n_visits = ctx.get("n_visits") or 0

    active_h = (task.get("active_seconds") or 0) / 3600
    wall_h = (task.get("wall_clock_seconds") or 0) / 3600
    excised_h = (task.get("excised_gap_seconds") or 0) / 3600

    parts: list[str] = []

    # Goal: what was the user researching?
    if queries:
        parts.append(f"Goal: 搜索 '{queries[0][:50]}'。")
    elif titles:
        parts.append(f"Goal: 浏览 {titles[0][:40]}。")

    # Struggle: what made this session take as long as it did?
    if active_h < 0.05 and wall_h > 1:
        first_page = titles[0][:40] if titles else "browsing"
        parts.append(f"Struggle: 标签页在 {first_page} 上停留 {wall_h:.1f}h 但无可测量活动——被遗忘，非活跃使用。")
    elif excised_h > 0.5 and excised_h > active_h:
        parts.append(f"Struggle: Wall {wall_h:.1f}h 中仅 {active_h:.1f}h 活跃浏览——{excised_h:.1f}h 空闲/隔夜标签页未关闭。")
    elif n_visits > 50 and active_h > 2:
        parts.append(f"Struggle: 大量浏览（{n_visits} 次访问）——在多个页面中搜索难以找到的信息。")

    # What was visited.
    if titles:
        key_pages = _dedupe(titles)[:3]
        parts.append(f"访问：{', '.join(key_pages)}。")
    if downloads:
        parts.append(f"下载了 {downloads} 个文件。")

    # Time.
    if active_h > 0.1 and excised_h <= 0.5:
        parts.append(f"{active_h:.1f}h 活跃浏览。")

    return " ".join(parts) if parts else ""


def _summarize_meeting(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a meeting."""
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
        return f"Goal: 日历全天标记 '{subject[:60]}'。Struggle: 非真实会议——0h 人工时间，用户未参加任何活动。"

    parts: list[str] = []

    # Goal: what was the meeting about?
    if subject:
        parts.append(f"Goal: 参加 '{subject[:60]}'。")
    else:
        parts.append("Goal: 参加会议。")

    # Context: who, where.
    context_bits: list[str] = []
    if organizer:
        context_bits.append(f"组织者 {organizer}")
    if location:
        context_bits.append(f"地点 {location}")
    if context_bits:
        parts.append(f"（{'，'.join(context_bits)}）。")

    # Struggle: what made this meeting take as long as it did?
    if wall_h > 24 or (excised_h > 0 and active_h >= 8):
        real_span_h = active_h + excised_h
        days = real_span_h / 24
        parts.append(f"Struggle: 跨天会议（{days:.1f} 天），封顶为 {active_h:.0f}h——实际出勤未知，日历数据无法显示参与情况。")
    elif active_h == 0 and wall_h > 0:
        parts.append(f"Struggle: Wall {wall_h:.1f}h 但 0h active——未检测到人工交互，可能是会议窗口未关闭。")
    elif active_h > 4:
        parts.append(f"Struggle: 会议时长 {active_h:.1f}h——日历数据无法显示实际参与程度。")

    # Time.
    if active_h > 0:
        parts.append(f"{active_h:.1f}h 会议。")

    return " ".join(parts) if parts else ""


def _summarize_comm(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for an email/communication task."""
    ctx = task.get("context") or {}
    subjects = ctx.get("subjects") or []
    senders = ctx.get("senders") or []
    has_reply = ctx.get("has_reply")
    im_count = ctx.get("im_message_count") or 0
    im_conversations = ctx.get("im_conversations") or []
    im_senders = ctx.get("im_senders") or []

    parts: list[str] = []

    # Email.
    if subjects:
        parts.append(f"Goal: 处理邮件 '{subjects[0][:60]}'。")
        if senders:
            parts.append(f"来自 {senders[0]}。")
        if has_reply:
            parts.append("Struggle: 活跃的往来邮件——已回复，表明该事项需要响应。")
        else:
            parts.append("Struggle: 未检测到回复——可能是仅查阅或该事项不需要回复。")

    # IM.
    if im_count:
        active_h = (task.get("active_seconds") or 0) / 3600
        conv = im_conversations[0][:40] if im_conversations else "一段对话"
        parts.append(f"Goal: 参与 IM 聊天（{conv}）。")
        if im_count > 50:
            parts.append(f"Struggle: 大量消息（{im_count} 条，{len(im_senders)} 位参与者）——长时间讨论，需要大量人工参与。")
        elif im_count > 10:
            parts.append(f"Struggle: 中等量消息（{im_count} 条）——来回讨论。")
        else:
            parts.append(f"交换了 {im_count} 条消息。")
        if active_h > 0.1:
            parts.append(f"{active_h:.1f}h 消息交流。")

    return " ".join(parts) if parts else ""


def _summarize_vcs(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a VCS/commit task."""
    ctx = task.get("context") or {}
    subjects = ctx.get("commit_subjects") or []
    if subjects:
        active_h = (task.get("active_seconds") or 0) / 3600
        parts = [f"Goal: 提交代码——'{subjects[0][:60]}'。"]
        if len(subjects) > 3:
            parts.append(f"Struggle: 本次会话 {len(subjects)} 次提交——迭代开发，多个检查点。")
        elif active_h > 1:
            parts.append(f"Struggle: 版本控制耗时 {active_h:.1f}h——大量 git 操作（变基、合并或解决冲突）。")
        if active_h > 0.1:
            parts.append(f"{active_h:.1f}h VCS 活动。")
        return " ".join(parts)
    return ""


def _summarize_filesystem(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a filesystem task."""
    ctx = task.get("context") or {}
    files = ctx.get("files") or []
    if files:
        active_h = (task.get("active_seconds") or 0) / 3600
        names = [os.path.basename(f) for f in files[:3]]
        parts = [f"Goal: 编辑文件。触碰了 {len(files)} 个文件：{', '.join(names)}。"]
        if active_h > 0.1:
            parts.append(f"{active_h:.1f}h。")
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
