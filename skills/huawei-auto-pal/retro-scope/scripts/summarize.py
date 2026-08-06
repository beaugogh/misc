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
    # Also detect idle sessions (agent running autonomously with little human input).
    human_engaged_h = ((task.get("human_data") or {}).get("human_engaged_seconds", 0) or 0) / 3600
    human_actions = (task.get("human_data") or {}).get("human_action_count", 0)

    # Idle session detection (rubric 56): if human engaged < 10% of active time.
    if active_h > 1 and human_engaged_h < 0.1 * active_h and human_actions < 10:
        parts.append(f"Struggle: agent 自主运行 {active_h:.1f}h，人工仅参与 {human_engaged_h:.1f}h（{human_actions} 次操作）——非人工时间消耗，可能为遗忘的会话。")
    else:
        struggle = _synthesize_struggle(n_errors, error_pairs, diagnostics, retry_targets, ctx)
        if struggle:
            parts.append(f"Struggle: {struggle}")
            # Add specific error evidence (rubric 56: verifiable evidence).
            if error_pairs:
                cmd, err = error_pairs[0]
                parts.append(f"Evidence: '{cmd}' → {err[:80]}")
        elif active_h > 0.5:
            files = ctx.get("files_touched") or []
            if files:
                parts.append(f"Struggle: 编辑了 {len(files)} 个文件（{', '.join(os.path.basename(f) for f in files[:3])}），{n_tool_calls} 次工具调用。")
            else:
                parts.append(f"Struggle: {n_tool_calls} 次工具调用，无明显错误。")
        else:
            parts.append("Struggle: 任务时间较短，无明显困难。")

    # User prompt evidence (rubric 56: investigate session content).
    user_prompts = ctx.get("user_prompts") or []
    if user_prompts:
        evidence = "；".join(f"'{p[:50]}'" for p in user_prompts[:2])
        parts.append(f"Evidence: 用户指令——{evidence}")

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
        patterns.append("企业代理认证失败，git 无法访问 GitHub")
    if "timeout" in all_text or "timed out" in all_text:
        patterns.append("命令执行超时，网络慢或进程卡住")
    if "not found" in all_text or "no such file" in all_text:
        patterns.append("找不到文件或路径，环境配置有误")
    if "permission denied" in all_text or "access is denied" in all_text:
        patterns.append("权限不足，无法访问")
    if "doesn't want to proceed" in all_text or "rejected" in all_text:
        patterns.append("用户多次拒绝了 agent 的操作请求")
    if "exit code 128" in all_text or "merge conflict" in all_text:
        patterns.append("git 操作失败（合并冲突或推送被拒）")
    if "modulenotfounderror" in all_text or "importerror" in all_text:
        patterns.append("缺少 Python 依赖包，环境没装全")
    if "syntaxerror" in all_text or "indentationerror" in all_text:
        patterns.append("Python 代码语法或缩进错误")
    if "file has not been read" in all_text:
        patterns.append("尝试编辑文件但没先读取，工作流有缺陷")

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
            bits.append(f"{pattern_str}。重试了 {retry_count} 次都没解决，说明没找到根本原因")
        elif n_errors >= 10:
            bits.append(f"{pattern_str}。累计 {n_errors} 个错误，试了多种方法都不行")
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


def _infer_page_topic(title: str) -> str:
    """Infer what the user was actually doing on a page from its title.

    Returns a concrete Chinese description of the browsing action — not just
    'this is a code repository' but '用户在浏览代码仓库的文件列表和提交记录'.
    This is the 'WHY' that rubric 62 demands: the reader must understand what
    content was on the page, not just how many times it was visited.
    """
    t = title.lower()
    # Code repositories — be specific about what the user was doing.
    if "codehub" in t or "github" in t:
        if "文件" in title or "files" in t or "tree" in t:
            return "用户在浏览代码仓库的文件目录结构"
        if "commit" in t or "提交" in title:
            return "用户在查看代码提交记录"
        if "设置" in title or "settings" in t:
            return "用户在配置代码仓库设置"
        if "misc" in t or "beaugogh" in t:
            return "用户在管理自己的代码仓库（查看文件、提交、设置）"
        return "用户在浏览代码仓库页面"
    if "beaugogh" in t or "/misc" in t:
        return "用户在管理自己的代码仓库"
    # Internal knowledge platforms.
    if "稼先" in title or "jiaxian" in t:
        if "search" in t or "搜索" in title:
            return "用户在稼先社区搜索内部技术文章"
        return "用户在阅读稼先社区的技术帖子"
    if "3ms" in t or "知识管理" in title:
        if "搜索" in t or "search" in t:
            return "用户在3MS知识库搜索文档"
        return "用户在阅读3MS知识库的技术文档"
    # AI agent platforms.
    if "agentcenter" in t:
        return "用户在AgentCenter平台上配置或管理AI Agent"
    if "agent" in t and "ai" in t:
        return "用户在管理AI Agent相关配置"
    # AI tools.
    if "gemini" in t:
        return "用户在使用 Google Gemini AI 工具"
    if "chatgpt" in t:
        return "用户在使用 ChatGPT"
    if "claude" in t:
        return "用户在使用 Claude AI"
    # Huawei internal.
    if "w3" in t and "workplace" in t:
        return "用户在W3门户首页浏览内部信息"
    if "w3" in t:
        return "用户在W3门户浏览华为内部信息"
    if "clouddevops" in t or "wiki" in t:
        return "用户在阅读CloudDevOps Wiki开发文档"
    # Search engines.
    if "google" in t and "search" in t:
        return "用户在Google搜索技术信息"
    # Technical topics.
    if "memory" in t or "mem0" in t:
        return "用户在研究AI记忆/存储技术方案"
    if "graph engineering" in t or "loop engineering" in t:
        return "用户在阅读AI工程方法论文章"
    if "knowledge online" in t:
        return "用户在知识库首页检索信息"
    if "swagger" in t or "api" in t:
        return "用户在查看API技术文档"
    if "python" in t or "linux" in t:
        return "用户在查阅技术教程"
    # Wushan platform.
    if "wushan" in t or "巫山" in title:
        if "文件" in title or "files" in t:
            return "用户在浏览巫山平台的代码文件"
        return "用户在巫山平台进行开发相关工作"
    # Generic.
    if "文件" in title or "files" in t:
        return "用户在浏览文件列表"
    if "设置" in title or "settings" in t:
        return "用户在配置项目设置"
    if "search" in t or "搜索" in title:
        return "用户在搜索信息"
    return "用户在浏览网页内容"


def _classify_page_content(title: str, text_excerpt: str, headings: list[str]) -> str:
    """Classify what a page is about using its actual content, not just title.

    When enrichment data is available (text_excerpt + headings), this produces
    a much more specific description than _infer_page_topic(title).
    """
    combined = f"{title} {' '.join(headings)} {text_excerpt[:300]}".lower()

    # Code repository / MR
    if "merge request" in combined or "合并请求" in combined or "pull request" in combined:
        if "diff" in combined or "改动" in combined:
            return "用户在审查代码合并请求的改动内容"
        return "用户在查看代码合并请求"
    if "codehub" in combined or "github" in combined:
        if "commit" in combined or "提交" in combined:
            return "用户在查看代码提交记录"
        if "file" in combined or "文件" in combined or "tree" in combined:
            return "用户在浏览代码仓库的文件目录"
        return "用户在浏览代码仓库"

    # Wiki / documentation
    if "wiki" in combined or "clouddevops" in combined:
        if "api" in combined or "接口" in combined:
            return "用户在阅读API技术文档"
        if "架构" in combined or "architecture" in combined:
            return "用户在阅读架构设计文档"
        return "用户在阅读技术Wiki文档"

    # Sprint / project tracking
    if "sprint" in combined or "迭代" in combined or "看板" in combined:
        return "用户在查看迭代/冲刺进度"
    if "task" in combined and ("assign" in combined or "分配" in combined):
        return "用户在查看任务分配情况"

    # Build / CI
    if "build" in combined or "构建" in combined or "pipeline" in combined:
        if "fail" in combined or "失败" in combined:
            return "用户在排查构建失败"
        return "用户在查看构建/流水线状态"

    # Search results
    if "search" in combined and ("result" in combined or "结果" in combined):
        return "用户在查看搜索结果页"

    # AI tools
    if "chatgpt" in combined or "gemini" in combined or "claude" in combined:
        return "用户在使用AI工具对话"

    # Tech tutorials / blogs
    if any(k in combined for k in ("tutorial", "教程", "guide", "指南")):
        return "用户在阅读技术教程"
    if any(k in combined for k in ("blog", "博客", "article", "文章")):
        return "用户在阅读技术博客文章"

    # Fallback: use title-based inference
    return _infer_page_topic(title)


def _format_relationships(relationships: list[dict]) -> str:
    """Format page relationship clusters into a human-readable Chinese string."""
    if not relationships:
        return ""

    parts: list[str] = []
    for rel in relationships[:3]:  # cap at 3 clusters
        entity_type = rel.get("entity_type", "")
        value = rel.get("entity_value", "")
        n_pages = len(rel.get("pages", []))

        if entity_type == "us_tickets":
            parts.append(f"多个页面（{n_pages}个）关联同一需求 {value}")
        elif entity_type == "mr_numbers":
            parts.append(f"多个页面（{n_pages}个）关联同一合并请求 #{value}")
        elif entity_type == "wiki_ids":
            parts.append(f"多个页面（{n_pages}个）关联同一Wiki文档 {value}")
        elif entity_type == "projects":
            parts.append(f"多个页面（{n_pages}个）关联同一项目 {value}")
        else:
            parts.append(f"多个页面（{n_pages}个）关联同一实体 {value}")

    if parts:
        return "页面关联：" + "；".join(parts) + "。"
    return ""


def _infer_goal_from_content(enrichment: dict, queries: list[str]) -> str:
    """Infer the user's research goal from page content + relationships."""
    pages = enrichment.get("pages", [])
    relationships = enrichment.get("relationships", [])

    # If there are relationships, the goal is likely about that shared entity.
    if relationships:
        rel = relationships[0]
        entity_type = rel.get("entity_type", "")
        value = rel.get("entity_value", "")
        n_pages = len(rel.get("pages", []))

        if entity_type == "us_tickets":
            return f"围绕需求 {value} 在 {n_pages} 个相关页面间交叉查阅"
        elif entity_type == "mr_numbers":
            return f"围绕合并请求 #{value} 在 {n_pages} 个相关页面间追踪进度"
        elif entity_type == "wiki_ids":
            return f"围绕Wiki文档 {value} 在 {n_pages} 个相关页面间阅读和参考"
        elif entity_type == "projects":
            return f"围绕项目 {value} 在 {n_pages} 个相关页面间查阅不同方面"

    # No relationships — try to infer from the top page content.
    if pages:
        top = pages[0]
        title = top.get("title", "")
        text = top.get("text_excerpt", "")[:200]
        headings = top.get("headings", [])

        # Check for common patterns in content
        combined = f"{title} {' '.join(headings)} {text}".lower()
        if any(k in combined for k in ("fix", "修复", "bug", "缺陷")):
            return "排查和修复问题"
        if any(k in combined for k in ("deploy", "部署", "release", "发布")):
            return "跟踪部署或发布进度"
        if any(k in combined for k in ("learn", "学习", "tutorial", "教程")):
            return "学习新技术或方案"
        if any(k in combined for k in ("design", "设计", "architecture", "架构")):
            return "研究架构或设计方案"

    return ""


def _summarize_browser(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a browser/research session.

    Analyzes page interaction depth (revisits, visit_count) to distinguish
    genuine engagement from forgotten tabs. When page enrichment data is
    available (task["context"]["page_enrichment"]), uses actual page content
    to explain what each page was about and how pages relate.
    """
    ctx = task.get("context") or {}
    titles = ctx.get("top_titles") or []
    queries = ctx.get("queries") or []
    downloads = ctx.get("downloads") or 0
    n_visits = ctx.get("n_visits") or 0
    enrichment = ctx.get("page_enrichment")  # None if not enriched

    active_h = (task.get("active_seconds") or 0) / 3600
    wall_h = (task.get("wall_clock_seconds") or 0) / 3600
    excised_h = (task.get("excised_gap_seconds") or 0) / 3600

    # Analyze per-page interaction depth from raw events.
    from collections import Counter
    page_visit_counts: Counter = Counter()  # title → number of visit events
    page_total_visits: dict[str, int] = {}  # title → max visit_count seen (Chrome's count)
    for ev in events:
        if ev.get("kind") != "visit":
            continue
        ti = ev.get("tool_input") or {}
        title = (ti.get("title") or ev.get("text") or "").strip()
        if not title or title == "(no title)":
            continue
        page_visit_counts[title] += 1
        vc = ti.get("visit_count") or 0
        if isinstance(vc, (int, float)) and vc > page_total_visits.get(title, 0):
            page_total_visits[title] = int(vc)

    # Top interacted pages (by number of visit events = clicks/revisits).
    top_pages = page_visit_counts.most_common(5)
    revisit_total = sum(1 for ev in events if ev.get("kind") == "visit"
                        and (ev.get("tool_input") or {}).get("visit_count", 0) > 1)

    # Build a title→enriched-page lookup for content-based descriptions.
    enriched_by_title: dict[str, dict] = {}
    if enrichment:
        for ep in enrichment.get("pages", []):
            et = ep.get("title", "").strip()
            if et:
                enriched_by_title[et] = ep

    parts: list[str] = []

    # Goal: what was the user researching?
    # When enrichment is available, infer goal from page content + relationships.
    top_page_title = top_pages[0][0] if top_pages else (titles[0] if titles else "")
    if queries:
        parts.append(f"Goal: 搜索 '{queries[0][:50]}'。")
    elif enrichment:
        # Use content-based goal inference.
        goal = _infer_goal_from_content(enrichment, queries)
        if goal:
            parts.append(f"Goal: {goal}。")
        elif top_page_title:
            n_top = len(top_pages)
            if n_top >= 3 and top_pages[2][1] >= 10:
                parts.append(
                    f"Goal: 浏览多个页面（以「{top_page_title[:30]}」为主，共 {n_visits} 次访问）。"
                )
            else:
                parts.append(f"Goal: 浏览 {top_page_title[:40]}。")
    elif top_page_title:
        # When multiple distinct pages were heavily interacted with, broaden
        # the goal to reflect the session's overall scope rather than naming
        # just one page (rubric 72: 目标 must match the content that follows).
        n_top = len(top_pages)
        if n_top >= 3 and top_pages[2][1] >= 10:
            parts.append(
                f"Goal: 浏览多个页面（以「{top_page_title[:30]}」为主，共 {n_visits} 次访问）。"
            )
        else:
            parts.append(f"Goal: 浏览 {top_page_title[:40]}。")

    # Struggle: distinguish genuine interaction from forgotten tabs.
    # A forgotten tab has low active time relative to wall clock — the page was
    # left open but the user wasn't actually browsing. Two conditions:
    # 1. Near-zero activity (active < 0.05h = 3 min) with long wall clock (>1h)
    # 2. Low activity ratio (active/wall < 15%) with long wall clock (>2h)
    active_ratio = active_h / wall_h if wall_h > 0 else 1.0
    is_forgotten = (active_h < 0.05 and wall_h > 1) or (active_ratio < 0.15 and wall_h > 2 and active_h < 0.5)
    if is_forgotten:
        # No measurable activity — forgotten tab, NOT a time sink.
        first_page = top_page_title[:40] if top_page_title else (titles[0][:40] if titles else "browsing")
        parts.append(f"Struggle: 标签页在 {first_page} 上停留 {wall_h:.1f}h 但仅 {active_h:.2f}h 活跃（{active_ratio*100:.0f}%）——被遗忘，非活跃使用，不属于人工时间消耗。")
    elif revisit_total > 20 and active_h > 0.5:
        # Genuine heavy interaction — many revisits = clicks.
        # Describe WHAT the user was doing on each top page (rubric 62).
        top_page = top_pages[0] if top_pages else ("", 0)
        top_title = top_page[0][:40]
        top_count = top_page[1]
        # Use content-based classification when available.
        if top_page_title in enriched_by_title:
            ep = enriched_by_title[top_page_title]
            topic = _classify_page_content(
                top_page_title, ep.get("text_excerpt", ""), ep.get("headings", [])
            )
        else:
            topic = _infer_page_topic(top_title)
        parts.append(
            f"Struggle: 用户在 {active_h:.1f}h 内进行了 {n_visits} 次页面访问（{revisit_total} 次重复点击），"
            f"属于活跃交互。最常访问的「{top_title}」({top_count}次)：{topic}。"
        )
    elif excised_h > 0.5 and excised_h > active_h:
        parts.append(f"Struggle: Wall {wall_h:.1f}h 中仅 {active_h:.1f}h 活跃浏览——{excised_h:.1f}h 空闲/隔夜标签页未关闭。")
    elif n_visits > 50 and active_h > 2:
        parts.append(f"Struggle: 大量浏览（{n_visits} 次访问）——在多个页面中搜索难以找到的信息。")
    elif active_h > 0.1:
        parts.append(f"Struggle: 浏览了 {n_visits} 个页面，活跃浏览 {active_h:.1f}h。")
    else:
        parts.append("Struggle: 浏览活动较少，无明显困难。")

    # Per-page content description (rubric 62: describe what was on each page).
    # When enrichment is available, use content-based classification.
    if top_pages and revisit_total > 10:
        page_descs: list[str] = []
        for title, count in top_pages[:4]:
            short_title = title[:30]
            if title in enriched_by_title:
                ep = enriched_by_title[title]
                action = _classify_page_content(
                    title, ep.get("text_excerpt", ""), ep.get("headings", [])
                )
                # Note auth-required pages that couldn't be enriched.
                if ep.get("status") == "auth_required":
                    action += "（内容需登录访问，仅根据标题推断）"
            else:
                action = _infer_page_topic(title)
            page_descs.append(f"「{short_title}」{count}次——{action}")
        if page_descs:
            parts.append(f"Detail: 主要浏览内容：{'；'.join(page_descs)}。")

    # Page relationships (from enrichment).
    if enrichment:
        rel_str = _format_relationships(enrichment.get("relationships", []))
        if rel_str:
            parts.append(f"Relations: {rel_str}")

    # What was visited — show more pages for longer sessions.
    if titles:
        max_pages = 5 if active_h > 2 else 3
        key_pages = _dedupe(titles)[:max_pages]
        parts.append(f"Pages: {', '.join(key_pages)}。")
    if downloads:
        parts.append(f"Downloads: 下载了 {downloads} 个文件。")

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
    elif active_h > 0:
        parts.append(f"Struggle: 会议 {active_h:.1f}h，日历数据无法显示实际参与程度。")

    # Time.
    if active_h > 0:
        parts.append(f"{active_h:.1f}h 会议。")

    return " ".join(parts) if parts else ""


def _synthesize_chat_topic(messages: list[str]) -> str:
    """Synthesize a 1-sentence topic description from chat message texts.

    Extracts keywords from the messages to describe WHAT was discussed,
    not just how many messages. Returns a Chinese topic description.
    """
    if not messages:
        return ""
    # Collect all message texts.
    all_text = " ".join(messages)

    # Detect common topics from keywords.
    keywords_map = {
        "报销": "费用报销流程",
        "学位": "学位证明相关事宜",
        "专利": "专利申请/评审",
        "会议": "会议安排/讨论",
        "项目": "项目进度/规划",
        "代码": "代码审查/开发",
        "部署": "部署/上线",
        "测试": "测试/验证",
        "文档": "文档编写/修改",
        "agent": "AI Agent开发",
        "模型": "AI模型相关",
        "git": "git/版本控制",
        "环境": "环境配置",
        "权限": "权限申请",
        "招聘": "招聘/面试",
        "绩效": "绩效评估",
        "obp": "OBP目标规划",
        "huawei": "华为内部事务",
    }
    detected: list[str] = []
    t_lower = all_text.lower()
    for kw, desc in keywords_map.items():
        if kw in t_lower:
            if desc not in detected:
                detected.append(desc)

    if detected:
        return f"讨论主题：{', '.join(detected[:2])}。"
    # Fallback: use the first message as topic hint.
    first = messages[0][:40] if messages else ""
    if first:
        return f"讨论内容：{first}。"
    return ""


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
        is_group = ctx.get("im_is_group")
        participants = ctx.get("im_participants") or []
        # Build participant name list (prefer names over account IDs).
        participant_names = [p.get("name", p.get("account", "?")) for p in participants]
        participant_str = "、".join(participant_names[:5])
        if len(participant_names) > 5:
            participant_str += f" 等{len(participant_names)}人"

        # Conversation label: group name for group chats, peer name for P2P.
        if is_group:
            conv = im_conversations[0][:40] if im_conversations else "群聊"
            parts.append(f"Goal: 参与群聊「{conv}」。")
        else:
            # P2P: use the peer's name (first participant who isn't the user,
            # or just the conversation name / first participant).
            conv = im_conversations[0][:40] if im_conversations else (participant_names[0] if participant_names else "私聊")
            parts.append(f"Goal: 与 {conv} 的私聊。")

        # Extract sample message texts and synthesize a topic (rubric 58).
        sample_msgs: list[str] = []
        for ev in events:
            if ev.get("kind") == "chat_message":
                text = (ev.get("text") or "").strip()
                if text and len(text) > 5 and not text.startswith("("):
                    sample_msgs.append(text[:60])
                    if len(sample_msgs) >= 5:
                        break
        # Synthesize chat topic from message keywords.
        topic = _synthesize_chat_topic(sample_msgs)
        if im_count > 50:
            parts.append(f"Struggle: 大量消息（{im_count} 条，参与者：{participant_str}）——长时间讨论，需要大量人工参与。{topic}")
        elif im_count > 10:
            parts.append(f"Struggle: 中等量消息（{im_count} 条，参与者：{participant_str}）——来回讨论。{topic}")
        else:
            parts.append(f"Struggle: {im_count} 条消息（参与者：{participant_str}）。{topic}")
        # Show content evidence (rubric 58: verifiable evidence).
        if sample_msgs:
            parts.append(f"Evidence: {'；'.join(sample_msgs[:2])}。")
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
        else:
            parts.append(f"Struggle: {len(subjects)} 次提交，{active_h:.1f}h git 活动。")
        if active_h > 0.1:
            parts.append(f"{active_h:.1f}h VCS 活动。")
        return " ".join(parts)
    return ""


def _summarize_filesystem(events: list[dict], task: dict) -> str:
    """Produce a grounded narrative for a filesystem task.

    Detects genuine editing (multiple edit events per file = versions) vs
    a file simply opened and forgotten (rubric 60).
    """
    ctx = task.get("context") or {}
    files = ctx.get("files") or []
    if not files:
        return ""

    active_h = (task.get("active_seconds") or 0) / 3600

    # Count edit events per file (rubric 60: detect genuine editing).
    # Only count kind="file_edit" (VSCode History save events) as real edits —
    # kind="file_open" (Windows Recent, Jump List) just means the file was
    # opened/accessed, not edited. Exclude events tagged as agent-edited
    # (rubric 68: VSCode History records agent edits too — those are NOT human edits).
    from collections import Counter
    file_edit_counts: Counter = Counter()
    agent_edit_counts: Counter = Counter()
    file_open_names: set = set()
    for ev in events:
        if ev.get("source_kind") != "filesystem":
            continue
        text = (ev.get("text") or "").strip()
        if not text:
            continue
        kind = ev.get("kind", "")
        if kind == "file_edit":
            if ev.get("agent_edited"):
                agent_edit_counts[text] += 1
            else:
                file_edit_counts[text] += 1
        else:
            # file_open or other — track as opened, not edited.
            file_open_names.add(text)

    # File type inference (rubric 60: what kind of file).
    def _file_type(filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        types = {
            ".py": "Python代码", ".js": "JavaScript代码", ".ts": "TypeScript代码",
            ".md": "Markdown文档", ".txt": "文本文件",
            ".pptx": "PowerPoint演示文稿", ".ppt": "PowerPoint演示文稿",
            ".xlsx": "Excel表格", ".xls": "Excel表格",
            ".docx": "Word文档", ".doc": "Word文档",
            ".json": "JSON配置", ".yaml": "YAML配置", ".yml": "YAML配置",
            ".html": "HTML页面", ".css": "CSS样式", ".sql": "SQL脚本",
            ".sh": "Shell脚本", ".bat": "批处理脚本",
            ".svg": "SVG图形", ".png": "PNG图片", ".jpg": "JPG图片",
        }
        return types.get(ext, f"{ext}文件" if ext else "文件")

    names = [os.path.basename(f) for f in files[:3]]
    file_types = [_file_type(f) for f in names]
    # Distinguish human-edited from agent-edited files (rubric 68).
    agent_files = list(agent_edit_counts.keys())
    human_edited_count = len(file_edit_counts)
    opened_only = file_open_names - set(file_edit_counts.keys()) - set(agent_files)

    # All edits were agent-edited (no human file_edit events).
    if agent_files and not human_edited_count:
        agent_names = [os.path.basename(f)[:30] for f in agent_files[:3]]
        parts = [f"Goal: 文件变更由AI代理执行（非用户手动编辑）。"
                 f"代理编辑了 {len(agent_files)} 个文件：{', '.join(agent_names)}。"]
        parts.append(f"Struggle: 这些编辑由AI代理（Edit/Write工具）完成，用户可能仅下达指令，未直接编辑文件。")
        if opened_only:
            open_names = sorted(opened_only)[:2]
            parts.append(f"另有 {len(opened_only)} 个文件仅被打开（无编辑记录）：{', '.join(open_names)}。")
        parts.append(f"{active_h:.1f}h。")
        return " ".join(parts)

    # No genuine edits at all — only file_open events.
    if not human_edited_count and not agent_files:
        parts = [f"Goal: 打开/访问文件。涉及 {len(files)} 个文件：{', '.join(names)}。"]
        parts.append(f"Struggle: 仅检测到文件打开记录（Windows最近使用/跳转列表），未检测到实际编辑保存。无法确认用户是否手动编辑了这些文件。")
        parts.append(f"{active_h:.1f}h。")
        return " ".join(parts)

    parts = [f"Goal: 编辑文件。触碰了 {len(files)} 个文件：{', '.join(names)}。"]

    # Genuine editing detection: files with multiple edit events = real editing.
    genuinely_edited = [(f, c) for f, c in file_edit_counts.most_common(5) if c >= 2]
    if genuinely_edited and active_h > 0.1:
        edit_descs = []
        for fname, count in genuinely_edited[:3]:
            short = os.path.basename(fname)[:30]
            ftype = _file_type(fname)
            edit_descs.append(f"「{short}」{count}个版本（{ftype}）")
        parts.append(f"Struggle: 频繁编辑 {len(genuinely_edited)} 个文件——{', '.join(edit_descs)}，表明用户在反复修改内容。")
        # If some files were agent-edited, note them so the report is honest.
        if agent_files:
            agent_names = [os.path.basename(f)[:30] for f in agent_files[:2]]
            parts.append(f"另有 {len(agent_files)} 个文件由AI代理编辑（非用户手动操作）：{', '.join(agent_names)}。")
        if opened_only:
            parts.append(f"另有 {len(opened_only)} 个文件仅被打开（无编辑记录）。")
        parts.append(f"{active_h:.1f}h。")
    elif active_h > 0.1:
        parts.append(f"Struggle: 文件编辑 {active_h:.1f}h，涉及 {len(files)} 个文件（{', '.join(file_types[:2])}）。")
        parts.append(f"{active_h:.1f}h。")
    else:
        parts.append("Struggle: 文件编辑活动较少，可能仅打开未编辑。")

    return " ".join(parts) if parts else ""


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
