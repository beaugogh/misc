"""Coarse cross-source linking (MVP scaffolding — throwaway by design).

Links git commit events to AI-session tasks heuristically: same `cwd`, commit timestamp
within [task.start, task.end + 2h]. Attaches matched commits to the task's `outputs`.

THIS IS SCAFFOLDING ONLY. It is deliberately naive and will be replaced wholesale by the
Fellegi-Sunter / Leiden probabilistic linker in Phase 4.4. Do not invest in hardening it.
Its purpose is to surface fused output in the report early so we can eyeball the cross-source
data while building the real thing.

Limitations (to be solved by Phase 4):
  - No semantic matching (commit message vs task subject).
  - Fixed 2h collar — too loose for long sessions, too tight for slow commits.
  - cwd must match exactly (no path normalization, no submodule handling).
  - A commit with no matching session is dropped (not its own task).
"""

from __future__ import annotations

LINK_COLLAR_SECONDS = 2 * 3600  # 2 hours after task end


def link_commits_to_tasks(tasks: list[dict], commit_events: list[dict]) -> list[dict]:
    """Attach git commits to matching tasks. Returns the tasks list (mutated in place).

    A commit matches a task if:
      - the commit's cwd matches the task's cwd (after normalization), AND
      - the commit timestamp is within [task.start, task.end + LINK_COLLAR_SECONDS].

    Matched commits are appended to the task's `outputs` list as "commit: <hash> <subject>".
    """
    # Index tasks by normalized cwd for quick lookup.
    by_cwd: dict[str, list[dict]] = {}
    for t in tasks:
        c = _norm_cwd(t.get("cwd"))
        if c:
            by_cwd.setdefault(c, []).append(t)

    for commit in commit_events:
        c = _norm_cwd(commit.get("cwd"))
        if not c or c not in by_cwd:
            continue
        ct = commit.get("timestamp")
        if ct is None:
            continue
        ti = commit.get("tool_input") or {}
        hash_short = (ti.get("hash") or "")[:8]
        subject = ti.get("subject") or commit.get("text") or ""
        link_str = f"commit: {hash_short} {subject[:60]}"
        ins = ti.get("insertions", 0)
        dl = ti.get("deletions", 0)
        if ins or dl:
            link_str += f" (+{ins}/-{dl})"

        for t in by_cwd[c]:
            start = t.get("start") or 0
            end = t.get("end") or 0
            if start <= ct <= end + LINK_COLLAR_SECONDS:
                if "git_commits" not in t:
                    t["git_commits"] = []
                t["git_commits"].append({"hash": ti.get("hash"), "subject": subject,
                                         "insertions": ins, "deletions": dl,
                                         "timestamp": ct})
                if link_str not in t.get("outputs", []):
                    t.setdefault("outputs", []).append(link_str)
                break  # a commit links to at most one task per the naive rule

    return tasks


def _norm_cwd(cwd: str | None) -> str:
    """Normalize a cwd for matching: lowercase, forward slashes, no trailing slash."""
    if not cwd:
        return ""
    import os
    return os.path.normpath(cwd).replace("\\", "/").lower().rstrip("/")


def tag_agent_file_edits(events: list[dict]) -> list[dict]:
    """Tag filesystem file_edit events that were likely made by an AI agent.

    VSCode Local History records every edit in the editor — including edits made
    by AI agents (Claude Code, Copilot, etc.) through Edit/Write/NotebookEdit tool
    calls. Without this tagging, files the user never touched personally (e.g. an
    agent-edited .ps1 script) appear in the report as "frequently edited by the
    user." (rubric 68)

    Approach: collect (file_path, timestamp) pairs from AI-session tool_use events
    for Edit/Write/NotebookEdit. Then mark any filesystem file_edit event whose
    file matches and whose timestamp is within ±WINDOW seconds of an agent edit
    as ``agent_edited = True``.

    Must run BEFORE segmentation so the summarizer sees the tags during
    ``_make_task()``. Returns the events list (mutated in place).
    """
    import os

    WINDOW = 120  # seconds — VSCode History timestamp vs tool_use timestamp

    # Build index of agent edits: (norm_path, timestamp) from ai_session tool_use.
    agent_edits: list[tuple[str, float]] = []
    for ev in events:
        if ev.get("source_kind") != "ai_session":
            continue
        if ev.get("kind") != "tool_use":
            continue
        name = ev.get("tool_name") or ""
        if name not in ("Edit", "Write", "NotebookEdit"):
            continue
        ti = ev.get("tool_input") or {}
        fp = ti.get("file_path") or ti.get("notebook_path")
        if not fp:
            continue
        ts = ev.get("timestamp")
        if ts is None:
            continue
        agent_edits.append((_norm_path(fp), float(ts)))

    if not agent_edits:
        return events  # nothing to tag

    # Sort by timestamp for efficient range lookup.
    agent_edits.sort(key=lambda x: x[1])
    agent_paths = {p for p, _ in agent_edits}
    agent_times = [t for _, t in agent_edits]

    tagged = 0
    import bisect
    for ev in events:
        if ev.get("source_kind") != "filesystem":
            continue
        if ev.get("kind") not in ("file_edit", "file_open"):
            continue
        # VSCode History stores the resource path in tool_input.resource,
        # the basename in text.
        ti = ev.get("tool_input") or {}
        resource = ti.get("resource", "")
        text = (ev.get("text") or "").strip()

        # Try to match by full path first, then by basename.
        if resource:
            for prefix in ("file:///", "file://"):
                if resource.startswith(prefix):
                    resource = resource[len(prefix):]
                    break
        ev_path = _norm_path(resource if resource else "")
        if not ev_path and text:
            ev_path = text  # basename-only fallback

        # Quick path filter: only check timestamps if the file was agent-edited.
        match_path = None
        if ev_path and ev_path in agent_paths:
            match_path = ev_path
        elif text:
            # Check if any agent edit path ends with this basename.
            for ap in agent_paths:
                if os.path.basename(ap).lower() == text.lower():
                    match_path = ap
                    break

        if not match_path:
            continue

        ts = ev.get("timestamp")
        if ts is None:
            continue
        ts = float(ts)

        # Binary search for agent edits within ±WINDOW of this event.
        lo = bisect.bisect_left(agent_times, ts - WINDOW)
        hi = bisect.bisect_right(agent_times, ts + WINDOW)
        for i in range(lo, hi):
            ap, at = agent_edits[i]
            if ap == match_path and abs(at - ts) <= WINDOW:
                ev["agent_edited"] = True
                tagged += 1
                break

    if tagged:
        import sys
        print(f"[cross_source] tagged {tagged} filesystem events as agent-edited", file=sys.stderr)
    return events


def _norm_path(path: str) -> str:
    """Normalize a file path for matching: lowercase, forward slashes."""
    if not path:
        return ""
    import os
    return os.path.normpath(path).replace("\\", "/").lower()


if __name__ == "__main__":
    # Quick smoke test against real data.
    import sys, os, json
    sys.path.insert(0, os.path.dirname(__file__))
    from sources import default_registry
    from segment_tasks import segment

    reg = default_registry()
    events, skipped = reg.collect_all()
    tasks = segment(events)
    commits = [e for e in events if e.get("kind") == "commit"]
    tasks = link_commits_to_tasks(tasks, commits)
    linked = [t for t in tasks if t.get("git_commits")]
    print(f"# {len(linked)} tasks linked to git commits (of {len(tasks)} tasks, {len(commits)} commits)", file=sys.stderr)
    for t in linked[:10]:
        print(json.dumps({"id": t["id"], "subject": (t.get("subject") or "")[:50],
                          "commits": len(t["git_commits"]),
                          "first_hash": t["git_commits"][0]["hash"][:8]}, ensure_ascii=False))
