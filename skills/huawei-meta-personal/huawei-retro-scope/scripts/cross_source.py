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
