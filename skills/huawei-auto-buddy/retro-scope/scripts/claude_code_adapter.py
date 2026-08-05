"""Claude Code session adapter.

Reads ~/.claude/projects/<slug>/<uuid>.jsonl session transcripts and emits a normalized
list of events — the raw material for task reconstruction.

Implements the `SourceAdapter` protocol (see `sources.py`): `detect()`, `collect()`,
`collect_since(watermark)`. Registered in `default_registry()`.

Events are constructed via `sources.make_event(...)` so they carry the unified schema
(source, source_kind, timestamp, kind, tool_name, tool_use_id, usage, ...). The legacy
module-level functions (`parse_session`, `collect_events`) are retained for backwards
compatibility and tests; they delegate to the adapter class.
"""

from __future__ import annotations

import json
import os
import glob
from datetime import datetime, timezone
from typing import Iterator

from sources import make_event


CLAUDE_PROJECTS_DIR = os.path.expanduser("~/.claude/projects")

# Fields truncated to avoid blowing up memory on large transcripts.
MAX_TEXT_LEN = 2000
MAX_TOOL_INPUT_REPR = 1000


def _parse_iso8601(ts: str) -> float:
    """Parse an ISO 8601 timestamp (e.g. '2026-07-23T08:57:07.631Z') to epoch seconds."""
    # Python 3.11+ datetime.fromisoformat handles 'Z' suffix; 3.12 does. Keep a fallback.
    s = ts.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    return dt.timestamp()


def _extract_text(message: dict) -> str | None:
    """Extract readable text from a message's content (str or list of blocks)."""
    content = message.get("content")
    if isinstance(content, str):
        return content[:MAX_TEXT_LEN]
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        if parts:
            joined = "\n".join(parts)
            return joined[:MAX_TEXT_LEN]
    return None


def _extract_tool_uses(message: dict) -> list[dict]:
    """Extract tool_use blocks from an assistant message's content."""
    content = message.get("content")
    if not isinstance(content, list):
        return []
    out = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            out.append({
                "tool_name": block.get("name", "?"),
                "tool_input": block.get("input", {}),
                "tool_use_id": block.get("id"),
            })
    return out


def _extract_tool_result(message: dict) -> tuple[str | None, bool | None, str | None]:
    """From a user message containing a tool_result block, return (text, is_error, tool_use_id).

    The tool_use_id links the result back to the tool_use block that produced it, enabling
    call↔result pairing for success attribution. A user message may contain multiple tool_result
    blocks (one per parallel tool call); we return the first's id and merge their text.
    """
    content = message.get("content")
    if not isinstance(content, list):
        return None, None, None
    text_parts = []
    is_error = None
    tool_use_id = None
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_result":
            if block.get("is_error"):
                is_error = True
            if tool_use_id is None:
                tool_use_id = block.get("tool_use_id")
            c = block.get("content")
            if isinstance(c, str):
                text_parts.append(c)
            elif isinstance(c, list):
                for sub in c:
                    if isinstance(sub, dict) and sub.get("type") == "text":
                        text_parts.append(sub.get("text", ""))
    text = "\n".join(text_parts) if text_parts else None
    if text:
        text = text[:MAX_TEXT_LEN]
    return text, is_error, tool_use_id


def iter_session_files(projects_dir: str = CLAUDE_PROJECTS_DIR) -> Iterator[str]:
    """Yield paths to all *.jsonl session transcripts under the projects dir."""
    pattern = os.path.join(projects_dir, "*", "*.jsonl")
    for path in glob.glob(pattern):
        yield path


def parse_session(path: str) -> Iterator[dict]:
    """Parse one session JSONL file, yielding normalized events in order.

    Each line is one JSON object. We emit one event per line, but assistant
    messages containing multiple tool_use blocks are expanded into separate
    tool_use events (one per block) so the pipeline can treat each tool call
    as its own time-stamped unit.
    """
    session_id = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts_raw = obj.get("timestamp")
            try:
                ts = _parse_iso8601(ts_raw) if isinstance(ts_raw, str) and ts_raw else None
            except (TypeError, ValueError, OverflowError):
                # Reject only the malformed record; one bad timestamp must not
                # truncate the rest of a session file.
                continue
            typ = obj.get("type", "?")
            message = obj.get("message") if isinstance(obj.get("message"), dict) else None
            cwd = obj.get("cwd")
            git_branch = obj.get("gitBranch")

            # Common base event — uses the unified schema from sources.make_event.
            def base(kind: str) -> dict:
                return make_event(
                    source="claude_code",
                    source_kind="ai_session",
                    session_id=session_id,
                    cwd=cwd,
                    git_branch=git_branch,
                    timestamp=ts if ts is not None else 0.0,
                    timestamp_raw=ts_raw,
                    kind=kind,
                    role=message.get("role") if message else None,
                    usage=message.get("usage") if message else None,
                    stop_reason=message.get("stop_reason") if message else None,
                )

            if typ == "user" and message:
                # Could be a user prompt OR a tool_result wrapper.
                text, is_error, tuid = _extract_tool_result(message)
                if is_error is not None or text is not None:
                    ev = base("tool_result")
                    ev["text"] = text
                    ev["tool_is_error"] = is_error
                    ev["tool_use_id"] = tuid
                    yield ev
                else:
                    ev = base("user_message")
                    ev["text"] = _extract_text(message)
                    yield ev
            elif typ == "assistant" and message:
                # Emit one assistant_message event, then expand tool_use blocks.
                ev = base("assistant_message")
                ev["text"] = _extract_text(message)
                yield ev
                for tu in _extract_tool_uses(message):
                    tev = base("tool_use")
                    tev["tool_name"] = tu["tool_name"]
                    tev["tool_use_id"] = tu.get("tool_use_id")
                    # Truncate large inputs (e.g. Write/Edit file contents).
                    ti = tu["tool_input"]
                    if isinstance(ti, dict) and len(str(ti)) > MAX_TOOL_INPUT_REPR:
                        ti = {k: (str(v)[:200] if isinstance(v, str) else v) for k, v in ti.items()}
                        ti["_truncated"] = True
                    tev["tool_input"] = ti
                    yield tev
            else:
                # Other line types (mode, permission-mode, file-history-snapshot,
                # custom-title, ai-title, agent-name, etc.) — yield a lightweight
                # marker so the pipeline can use titles if it wants.
                ev = base(typ)
                yield ev


def collect_events(projects_dir: str = CLAUDE_PROJECTS_DIR) -> list[dict]:
    """Convenience: read all sessions, return a flat sorted event list.

    Legacy entry point — equivalent to `ClaudeCodeAdapter().collect()` but accepts a
    custom projects_dir (used by tests). New code should use the adapter class via the
    registry.
    """
    events = []
    for path in iter_session_files(projects_dir):
        events.extend(parse_session(path))
    # Sort by timestamp; events without a timestamp sink to the end.
    events.sort(key=lambda e: (e.get("timestamp") is None, e.get("timestamp") or 0.0))
    return events


class ClaudeCodeAdapter:
    """Adapter for Claude Code session transcripts (~/.claude/projects/<slug>/*.jsonl).

    Implements the SourceAdapter protocol (see sources.py). The richest source —
    JSONL transcripts with per-message timestamps, tool calls, task model, and usage.
    """

    name = "claude_code"
    source_kind = "ai_session"

    def __init__(self, projects_dir: str | None = None):
        self.projects_dir = projects_dir or CLAUDE_PROJECTS_DIR

    def detect(self) -> bool:
        return os.path.isdir(self.projects_dir) and any(iter_session_files(self.projects_dir))

    def collect(self) -> Iterator[dict]:
        yield from collect_events(self.projects_dir)

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        """Incremental collection: yield ALL events from sessions that have any
        event after the watermark.

        C7 fix: Previously this yielded only events with timestamp > watermark.
        But segment() needs the full session context to detect task boundaries
        (TaskCreate, gaps, cwd shifts). A task whose TaskCreate is before the
        watermark but whose TaskUpdate(completed) is after would have no start
        boundary detected. Implicit segmentation's gap heuristic also breaks
        because the first post-watermark event has no prior event to compare
        against.

        Fix: yield ALL events from any session file that contains at least one
        event with timestamp > watermark. Deduplication of already-processed
        tasks happens at the persistence layer (save_tasks merge by task ID).
        """
        if watermark is None:
            yield from self.collect()
            return
        for path in iter_session_files(self.projects_dir):
            # First pass: check if this session has any event after the watermark.
            # We parse all events, check if any qualifies, and if so yield all.
            session_events = list(parse_session(path))
            has_new = any(
                ev.get("timestamp") is not None and ev["timestamp"] > watermark
                for ev in session_events
            )
            if has_new:
                yield from session_events


class CodeagentAdapter(ClaudeCodeAdapter):
    """Adapter for the new codeagent (`codeagent` cmd) session transcripts.

    Same JSONL schema as Claude Code (~/.cac/projects/<slug>/<uuid>.jsonl) — reuses the
    parent's parser. The only difference is the path and the `source` field name so the
    fusion layer can distinguish which tool produced which session.
    """

    name = "codeagent"

    def __init__(self, projects_dir: str | None = None):
        default = os.path.expanduser("~/.cac/projects")
        self.projects_dir = projects_dir or default

    def collect(self) -> Iterator[dict]:
        # Reuse the parent's collection, but relabel events with source="codeagent".
        for ev in collect_events(self.projects_dir):
            ev["source"] = "codeagent"
            yield ev

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        """Incremental collection — C7 fix: yield ALL events from sessions that
        have any event after the watermark (same logic as ClaudeCodeAdapter).
        """
        if watermark is None:
            yield from self.collect()
            return
        for path in iter_session_files(self.projects_dir):
            session_events = list(parse_session(path))
            has_new = any(
                ev.get("timestamp") is not None and ev["timestamp"] > watermark
                for ev in session_events
            )
            if has_new:
                for ev in session_events:
                    ev["source"] = "codeagent"
                    yield ev


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Emit normalized events from Claude Code sessions.")
    ap.add_argument("--projects-dir", default=CLAUDE_PROJECTS_DIR)
    ap.add_argument("--limit", type=int, default=0, help="limit number of events (0 = all)")
    args = ap.parse_args()

    evs = collect_events(args.projects_dir)
    if args.limit:
        evs = evs[:args.limit]
    for ev in evs:
        print(json.dumps(ev, ensure_ascii=False))
