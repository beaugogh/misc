"""Git / CodeHub adapter.

Reads commit history (`git log`) and branch-checkout history (`git reflog`) from git
repositories and emits normalized events. Implements the `SourceAdapter` protocol.

Events emitted:
  - kind=commit: a commit was made. Carries hash, message, files, insertions/deletions.
  - kind=branch_checkout: the user switched branches. Carries from/to branch. This is the
    finer "when you switched to working on X" signal borrowed from Hourgit (see
    research-findings.md).

Project directories are discovered from AI-session `cwd` fields (Phase 1.2) — the adapter
accepts an explicit list of git roots, or discovers them via `discover_git_roots()`.

Timestamps come from git's `%cI` (ISO 8601 strict) and are normalized to epoch seconds.

NOTE: `git log --author` filters by the current user. We detect the author from
`git config user.email` per-repo (commits by other people in the same repo are excluded).
"""

from __future__ import annotations

import os
import subprocess
import json
from typing import Iterator

from sources import make_event


def _run_git(args: list[str], cwd: str, timeout: int = 60) -> str:
    """Run a git command in cwd, return stdout. Raises on non-zero exit."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} in {cwd}: {result.stderr.strip()}")
    return result.stdout


def _parse_git_iso(ts: str) -> float:
    """Parse git's %cI ISO 8601 (e.g. '2026-07-29T12:34:56+08:00') to epoch seconds."""
    from datetime import datetime
    s = ts.strip()
    # Handle 'Z' suffix
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    return dt.timestamp()


def _repo_author_email(cwd: str) -> str | None:
    """Get the configured git user email for a repo (to filter --author)."""
    try:
        return _run_git(["config", "user.email"], cwd).strip() or None
    except Exception:
        return None


def iter_commits(cwd: str, since: str | None = None, until: str | None = None) -> Iterator[dict]:
    """Yield commit events from a git repo.

    Git's output interleaves header and numstat: for each commit, it emits
    `<hash>\x1f<ts>\x1f<subject>\x1f<body>\x1e` followed by numstat lines
    (`ins\tdel\tpath`). The numstat for commit N appears AFTER its \x1e terminator
    and BEFORE the next commit's header. So splitting on \x1e gives records where
    each record's numstat is at its START (before the header) — except the first
    record which has no preceding numstat.

    We handle this by splitting on \x1e, then for each record: the header is the
    LAST \x1f-delimited line, and the numstat lines are everything before it.
    """
    author = _repo_author_email(cwd)
    fmt = "%H%x1f%cI%x1f%s%x1f%b%x1e"  # hash \x1f timestamp \x1f subject \x1f body \x1e
    args = ["log", "--no-merges", f"--format={fmt}", "--numstat", "--no-color"]
    if author:
        args.append(f"--author={author}")
    if since:
        args.append(f"--since={since}")
    if until:
        args.append(f"--until={until}")

    try:
        out = _run_git(args, cwd, timeout=120)
    except (RuntimeError, subprocess.TimeoutExpired):
        return

    # Split into records on \x1e. Each record = [numstat lines...\n]<header>.
    # The first record has no numstat; subsequent records have numstat from the prior commit.
    records = out.split("\x1e")
    # We need to pair each header with the numstat that FOLLOWS it (in the next record).
    # Simpler: iterate records, extract header from each, and numstat from the start of
    # the NEXT record.
    headers: list[tuple[str, str, str, str]] = []  # (hash, ts, subject, body)
    numstats: list[list[tuple[int, int, str]]] = []  # per-commit numstat lines
    for i, record in enumerate(records):
        record = record.strip()
        if not record:
            continue
        lines = record.split("\n")
        # The header is the last line containing \x1f; numstat lines precede it.
        header_idx = None
        for j in range(len(lines) - 1, -1, -1):
            if "\x1f" in lines[j]:
                header_idx = j
                break
        if header_idx is None:
            continue
        header_parts = lines[header_idx].split("\x1f")
        if len(header_parts) < 3:
            continue
        commit_hash, ts_str, subject = header_parts[0], header_parts[1], header_parts[2]
        body = header_parts[3] if len(header_parts) > 3 else ""
        headers.append((commit_hash, ts_str, subject, body))

        # numstat lines are everything before the header in THIS record — these belong
        # to the PREVIOUS commit. But for the first record, there's no previous commit.
        # We'll collect numstat separately and pair by index offset.
        ns: list[tuple[int, int, str]] = []
        for line in lines[:header_idx]:
            line = line.strip()
            if not line:
                continue
            cols = line.split("\t")
            if len(cols) >= 3:
                ins_s, del_s, fpath = cols[0], cols[1], cols[2]
                ins = int(ins_s) if ins_s.isdigit() else 0
                dl = int(del_s) if del_s.isdigit() else 0
                ns.append((ins, dl, fpath))
        numstats.append(ns)

    # Now pair: commit[i]'s numstat is in numstats[i+1] (the numstat that followed its \x1e).
    for i, (commit_hash, ts_str, subject, body) in enumerate(headers):
        ts = _parse_git_iso(ts_str)
        ns = numstats[i + 1] if i + 1 < len(numstats) else []
        insertions = sum(n[0] for n in ns)
        deletions = sum(n[1] for n in ns)
        files_changed = [n[2] for n in ns]

        yield make_event(
            source="git",
            source_kind="vcs",
            session_id=None,
            cwd=cwd,
            git_branch=None,
            timestamp=ts,
            timestamp_raw=ts_str,
            kind="commit",
            text=subject,
            tool_name=None,
            tool_input={
                "hash": commit_hash,
                "subject": subject,
                "body": body[:500] if body else None,
                "files": files_changed[:50],
                "insertions": insertions,
                "deletions": deletions,
            },
            extra={"commit_hash": commit_hash, "insertions": insertions, "deletions": deletions},
        )


def iter_reflog(cwd: str) -> Iterator[dict]:
    """Yield branch-checkout events from the git reflog.

    `git reflog --format='%cI %gs'` gives lines like:
      '2026-07-29T12:34:56+08:00 checkout: moving from main to feature/x'
    We parse the 'moving from X to Y' to get from/to branches.
    """
    try:
        out = _run_git(["reflog", "--format=%cI%x1f%gs"], cwd)
    except RuntimeError:
        return

    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\x1f", 1)
        if len(parts) < 2:
            continue
        ts_str, msg = parts[0], parts[1]
        if "checkout: moving from" not in msg:
            continue
        # "checkout: moving from main to feature/x"
        import re
        m = re.search(r"moving from (\S+) to (\S+)", msg)
        if not m:
            continue
        from_branch, to_branch = m.group(1), m.group(2)
        ts = _parse_git_iso(ts_str)
        yield make_event(
            source="git",
            source_kind="vcs",
            session_id=None,
            cwd=cwd,
            git_branch=to_branch,
            timestamp=ts,
            timestamp_raw=ts_str,
            kind="branch_checkout",
            text=f"{from_branch} -> {to_branch}",
            tool_input={"from_branch": from_branch, "to_branch": to_branch},
        )


def discover_git_roots(session_cwds: list[str] | None = None) -> list[str]:
    """Discover candidate git repository roots.

    Phase 1.2: collects git roots from distinct cwd values in AI-session events. A directory
    is a git root if it contains a `.git` entry. Non-existent / non-git dirs are skipped.

    De-duplicates nested roots: if `/a/b` and `/a` are both git roots, only `/a` is kept
    (the inner one is a submodule or nested repo already covered by the parent's log).
    This prevents scanning the same history twice — critical when 41 session cwds collapse
    to ~6 real repos instead of 14.
    """
    candidates: set[str] = set()
    if session_cwds:
        for c in session_cwds:
            if c:
                candidates.add(c)

    roots: list[str] = []
    for c in candidates:
        if not c or not os.path.isdir(c):
            continue
        git_dir = os.path.join(c, ".git")
        if os.path.exists(git_dir):
            roots.append(os.path.normpath(c))

    # De-duplicate: drop any root that is a subdirectory of another root.
    roots.sort()
    deduped: list[str] = []
    for r in roots:
        if not any(r != other and r.startswith(other + os.sep) for other in deduped):
            deduped.append(r)
    return deduped


class GitAdapter:
    """Adapter for git / CodeHub commit + reflog history.

    Requires a list of git repository roots (from discover_git_roots or explicit).
    By default limits history to the last 90 days to keep collection fast across many
    repos; pass `since=None` for full history.
    """

    name = "git"
    source_kind = "vcs"

    def __init__(self, roots: list[str] | None = None, since: str | None = "90 days ago"):
        self._roots = roots
        self._since = since

    def detect(self) -> bool:
        return len(self._effective_roots()) > 0

    def _effective_roots(self) -> list[str]:
        if self._roots is not None:
            return [r for r in self._roots if os.path.isdir(os.path.join(r, ".git"))]
        # Without explicit roots, try the repo this script lives in as a fallback.
        here = os.path.dirname(os.path.abspath(__file__))
        d = here
        for _ in range(5):
            if os.path.isdir(os.path.join(d, ".git")):
                return [d]
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
        return []

    def collect(self) -> Iterator[dict]:
        for root in self._effective_roots():
            yield from iter_commits(root, since=self._since)
            yield from iter_reflog(root)

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            ts = ev.get("timestamp")
            if ts is not None and ts > watermark:
                yield ev
