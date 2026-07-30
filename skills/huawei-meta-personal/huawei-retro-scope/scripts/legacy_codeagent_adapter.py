"""Legacy codeagent (nga) adapter — reads ngagent.db SQLite.

Reads the SQLite database used by the legacy codeagent (`nga` cmd) and emits normalized
events matching the same schema as the Claude Code JSONL adapter. This is the first SQL
adapter in the registry — it validates the incremental `collect_since(watermark)` path
with efficient `WHERE time_created > ?` filtering instead of in-memory timestamp checks.

Schema (verified against a live ngagent.db on 2026-07-29):
  - `session` table: id, project_id, directory (cwd), title, slug, time_created (millis),
    time_updated, version, share_url, summary_*, etc.
  - `message` table: id, session_id, time_created (millis), time_updated, data (JSON).
    The `data` JSON has: role ("user"/"assistant"), path.cwd, tokens (total/input/output/
    cache), finish (stop reason), modelID, providerID, agent, mode, etc.
  - `part` table: id, message_id, session_id, time_created (millis), data (JSON).
    The `data` JSON type field: "text", "tool", "step-start", "step-finish", "reasoning".
    Tool parts carry: tool (name), callID, state.status ("completed"/"error"),
    state.input, state.output.
  - `project` table: id, worktree, vcs, name, time_created.
  - `metrics` table: per-request token counts, model_id, provider_id, durations.

Timestamps are millis-epoch INTEGERs, normalized to seconds (ts_ms / 1000.0).

Events emitted:
  - user_message: from a message with role="user" whose parts are all text (no tool results).
  - assistant_message: from a message with role="assistant" — one event per message.
  - tool_use: from a part with type="tool" — carries tool_name, tool_input, tool_use_id.
  - tool_result: from a part with type="tool" and state.status — carries tool_is_error,
    tool_use_id, and output text. (The legacy DB stores tool call+result in one part, so
    we emit both a tool_use and a tool_result event from each tool part.)
  - reasoning: from a part with type="reasoning" — emitted as kind="reasoning".

Implements the `SourceAdapter` protocol (see sources.py).
"""

from __future__ import annotations

import json
import os
import sqlite3
import shutil
import tempfile
from typing import Iterator

from sources import make_event
import platform_paths


# Default path for ngagent.db (set in platform_paths.py).
DEFAULT_DB_PATH = platform_paths.LEGACY_CODEAGENT_DB

# Alternative search locations.
_SEARCH_PATHS = [
    DEFAULT_DB_PATH,
    os.path.expanduser("~/.cac/ngagent.db"),
    os.path.expanduser("~/.ngagent/ngagent.db"),
    os.path.join(os.path.expanduser("~"), "AppData", "Local", "ngagent", "ngagent.db"),
    os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "ngagent", "ngagent.db"),
]

# Truncation limits (match claude_code_adapter.py).
MAX_TEXT_LEN = 2000
MAX_TOOL_INPUT_REPR = 1000


def _find_db() -> str | None:
    """Search common locations for ngagent.db. Return the first existing path, or None."""
    for p in _SEARCH_PATHS:
        if os.path.exists(p):
            return p
    return None


def _copy_then_read(db_path: str) -> str:
    """Copy a (possibly locked) SQLite DB to a temp file and return the temp path.

    Same pattern as browser_adapter.py — the legacy codeagent process may hold a write
    lock on ngagent.db while running.
    """
    fd, tmp = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    shutil.copy2(db_path, tmp)
    return tmp


def _table_columns(c: sqlite3.Cursor, table: str) -> set[str]:
    """Return the set of column names for a table, or empty set if table is missing."""
    try:
        return {row[1] for row in c.execute(f"PRAGMA table_info({table})")}
    except sqlite3.OperationalError:
        return set()


def _millis_to_seconds(ms: int | None) -> float | None:
    """Convert millis-epoch INTEGER to seconds. Returns None if input is None."""
    if ms is None:
        return None
    return ms / 1000.0


def _truncate(text: str | None) -> str | None:
    """Truncate text to MAX_TEXT_LEN."""
    if text is None:
        return None
    return text[:MAX_TEXT_LEN]


def _truncate_tool_input(ti: dict | None) -> dict | None:
    """Truncate large tool inputs to avoid memory blowup (matches Claude Code adapter)."""
    if ti is None:
        return None
    if isinstance(ti, dict) and len(str(ti)) > MAX_TOOL_INPUT_REPR:
        ti = {k: (str(v)[:200] if isinstance(v, str) else v) for k, v in ti.items()}
        ti["_truncated"] = True
    return ti


def _extract_usage(msg_data: dict) -> dict | None:
    """Extract token usage from message.data JSON.

    The legacy DB stores tokens in message.data.tokens:
    {"total": N, "input": N, "output": N, "reasoning": N, "cache": {"read": N, "write": N}}

    Normalize to the Claude Code usage dict shape for consistency.
    """
    tokens = msg_data.get("tokens")
    if not isinstance(tokens, dict):
        return None
    usage = {}
    if "input" in tokens:
        usage["input_tokens"] = tokens["input"]
    if "output" in tokens:
        usage["output_tokens"] = tokens["output"]
    if "total" in tokens:
        usage["total_tokens"] = tokens["total"]
    if "reasoning" in tokens:
        usage["reasoning_tokens"] = tokens["reasoning"]
    cache = tokens.get("cache")
    if isinstance(cache, dict):
        if "read" in cache:
            usage["cache_read_input_tokens"] = cache["read"]
        if "write" in cache:
            usage["cache_creation_input_tokens"] = cache["write"]
    return usage if usage else None


def _extract_cwd(msg_data: dict, session_dir: str | None) -> str | None:
    """Extract cwd from message.data.path.cwd, falling back to session.directory."""
    path = msg_data.get("path")
    if isinstance(path, dict) and path.get("cwd"):
        return path["cwd"]
    return session_dir


def _extract_stop_reason(msg_data: dict) -> str | None:
    """Extract stop reason from message.data.finish."""
    return msg_data.get("finish")


def _parse_tool_part(part_data: dict) -> tuple[str | None, dict | None, str | None, bool | None, str | None]:
    """Parse a tool part's data JSON.

    Returns (tool_name, tool_input, tool_use_id, is_error, output_text).
    The legacy DB stores both the call and result in one part, so we get all of these
    from a single row.
    """
    tool_name = part_data.get("tool")
    call_id = part_data.get("callID")
    state = part_data.get("state")
    if not isinstance(state, dict):
        return tool_name, None, call_id, None, None

    tool_input = state.get("input")
    if isinstance(tool_input, dict):
        tool_input = _truncate_tool_input(tool_input)

    status = state.get("status")
    is_error = (status == "error") if status else None

    output = state.get("output")
    output_text = None
    if isinstance(output, str):
        output_text = _truncate(output)
    elif isinstance(output, dict):
        # Some outputs may be structured; try to extract text
        output_text = _truncate(json.dumps(output, ensure_ascii=False))

    return tool_name, tool_input, call_id, is_error, output_text


def _parse_text_part(part_data: dict) -> str | None:
    """Extract text from a text-type part."""
    text = part_data.get("text")
    return _truncate(text) if isinstance(text, str) else None


def iter_db_events(db_path: str, watermark_ms: int | None = None) -> Iterator[dict]:
    """Yield normalized events from ngagent.db.

    If watermark_ms is given (millis-epoch), C7 fix: yield ALL messages from
    sessions that have ANY message with time_created > watermark_ms. This ensures
    segment() sees the full session context to detect task boundaries (TaskCreate
    before the watermark, TaskUpdate after). Previously this only yielded
    post-watermark messages, which broke boundary detection.
    """
    if not os.path.exists(db_path):
        return

    tmp = _copy_then_read(db_path)
    try:
        conn = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        c = conn.cursor()

        # Discover which tables exist.
        msg_cols = _table_columns(c, "message")
        if not msg_cols:
            return  # no message table — nothing to do

        part_cols = _table_columns(c, "part")
        session_cols = _table_columns(c, "session")
        project_cols = _table_columns(c, "project")

        # Build session info lookup: session_id -> (directory, project_id)
        session_info: dict[str, tuple[str | None, str | None]] = {}
        if session_cols and "id" in session_cols and "directory" in session_cols:
            try:
                for sid, directory, pid in c.execute(
                    "SELECT id, directory, project_id FROM session"
                ):
                    session_info[sid] = (directory, pid)
            except sqlite3.OperationalError:
                pass

        # Build project info lookup: project_id -> (worktree, vcs)
        project_info: dict[str, tuple[str | None, str | None]] = {}
        if project_cols and "id" in project_cols:
            try:
                worktree_col = "worktree" if "worktree" in project_cols else None
                vcs_col = "vcs" if "vcs" in project_cols else None
                if worktree_col or vcs_col:
                    cols = "id"
                    if worktree_col:
                        cols += f", {worktree_col}"
                    else:
                        cols += ", NULL"
                    if vcs_col:
                        cols += f", {vcs_col}"
                    else:
                        cols += ", NULL"
                    for pid, wt, vcs in c.execute(f"SELECT {cols} FROM project"):
                        project_info[pid] = (wt, vcs)
            except sqlite3.OperationalError:
                pass

        # Query messages, optionally filtered by watermark.
        has_time_created = "time_created" in msg_cols
        has_data = "data" in msg_cols
        has_session_id = "session_id" in msg_cols

        if not has_data:
            return  # can't do anything without the data JSON column

        # Build the SELECT and WHERE clause.
        select_cols = ["id"]
        if has_session_id:
            select_cols.append("session_id")
        if has_time_created:
            select_cols.append("time_created")
        select_cols.append("data")

        select_sql = f"SELECT {', '.join(select_cols)} FROM message"
        params: list = []

        if has_time_created and watermark_ms is not None and has_session_id:
            # C7 fix: find sessions that have ANY message after the watermark,
            # then yield ALL messages from those sessions. This ensures segment()
            # sees full session context for boundary detection.
            # Step 1: find session_ids with at least one post-watermark message.
            active_session_ids = set()
            try:
                for (sid,) in c.execute(
                    "SELECT DISTINCT session_id FROM message WHERE time_created > ?",
                    (watermark_ms,),
                ):
                    if sid:
                        active_session_ids.add(sid)
            except sqlite3.OperationalError:
                pass
            if not active_session_ids:
                return  # no sessions with new messages
            # Step 2: select ALL messages from those sessions.
            placeholders = ",".join("?" * len(active_session_ids))
            select_sql += f" WHERE session_id IN ({placeholders})"
            params.extend(active_session_ids)
            select_sql += " ORDER BY time_created" if has_time_created else ""
        elif has_time_created and watermark_ms is not None:
            # Fallback: no session_id column — use the old per-message filter.
            select_sql += " WHERE time_created > ?"
            params.append(watermark_ms)
            select_sql += " ORDER BY time_created" if has_time_created else ""
        else:
            select_sql += " ORDER BY time_created" if has_time_created else ""

        # Collect parts per message for richer event extraction.
        # We do a separate query per message to avoid a giant join result.
        has_parts = bool(part_cols) and "message_id" in part_cols and "data" in part_cols

        try:
            msg_rows = list(c.execute(select_sql, params))
        except sqlite3.OperationalError:
            return

        for row in msg_rows:
            msg_id = row[0]
            offset = 1
            session_id = None
            if has_session_id:
                session_id = row[offset]
                offset += 1
            time_created_ms = None
            if has_time_created:
                time_created_ms = row[offset]
                offset += 1
            data_json = row[offset]

            # Parse message data JSON.
            try:
                msg_data = json.loads(data_json) if isinstance(data_json, str) else {}
            except (json.JSONDecodeError, TypeError):
                msg_data = {}

            role = msg_data.get("role")
            ts_sec = _millis_to_seconds(time_created_ms)

            # Resolve cwd and git_branch from session/project.
            session_dir = None
            project_id = None
            if session_id and session_id in session_info:
                session_dir, project_id = session_info[session_id]

            cwd = _extract_cwd(msg_data, session_dir)
            git_branch = None
            if project_id and project_id in project_info:
                _, git_branch = project_info[project_id]

            usage = _extract_usage(msg_data)
            stop_reason = _extract_stop_reason(msg_data)

            def base(kind: str, ts: float | None = ts_sec) -> dict:
                return make_event(
                    source="legacy_codeagent",
                    source_kind="ai_session",
                    session_id=session_id,
                    cwd=cwd,
                    git_branch=git_branch,
                    timestamp=ts if ts is not None else 0.0,
                    timestamp_raw=str(time_created_ms) if time_created_ms is not None else None,
                    kind=kind,
                    role=role,
                    usage=usage,
                    stop_reason=stop_reason,
                )

            # Emit the message-level event.
            if role == "user":
                # User message — check if it's actually a tool result wrapper.
                # In the legacy DB, tool results come as parts with type="tool" on
                # assistant messages, not user messages. So a user message is always
                # a user_message.
                ev = base("user_message")
                # Try to get text from parts.
                if has_parts:
                    parts = _get_parts_for_message(c, msg_id)
                    texts = []
                    for pdata in parts:
                        if pdata.get("type") == "text":
                            t = _parse_text_part(pdata)
                            if t:
                                texts.append(t)
                    if texts:
                        ev["text"] = "\n".join(texts)
                yield ev

            elif role == "assistant":
                # Assistant message — emit the message event, then expand parts.
                ev = base("assistant_message")
                if has_parts:
                    parts = _get_parts_for_message(c, msg_id)
                    texts = []
                    for pdata in parts:
                        ptype = pdata.get("type")
                        if ptype == "text":
                            t = _parse_text_part(pdata)
                            if t:
                                texts.append(t)
                    if texts:
                        ev["text"] = "\n".join(texts)
                yield ev

                # Emit part-level events (tool_use, tool_result, reasoning).
                if has_parts:
                    parts = _get_parts_for_message(c, msg_id)
                    for pdata in parts:
                        ptype = pdata.get("type")

                        if ptype == "tool":
                            tool_name, tool_input, call_id, is_error, output_text = _parse_tool_part(pdata)
                            # Emit tool_use event.
                            tev = base("tool_use")
                            tev["tool_name"] = tool_name
                            tev["tool_use_id"] = call_id
                            tev["tool_input"] = tool_input
                            yield tev

                            # Emit tool_result event (legacy DB bundles call+result).
                            rev = base("tool_result")
                            rev["tool_name"] = tool_name
                            rev["tool_use_id"] = call_id
                            rev["tool_is_error"] = is_error
                            rev["text"] = output_text
                            yield rev

                        elif ptype == "reasoning":
                            rev = base("reasoning")
                            rev["text"] = _parse_text_part(pdata)
                            yield rev

            else:
                # Unknown role — yield a lightweight marker.
                ev = base(role or "unknown")
                yield ev

        conn.close()
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def _get_parts_for_message(c: sqlite3.Cursor, msg_id: str) -> list[dict]:
    """Fetch and parse all parts for a message, returning their data JSON dicts."""
    parts = []
    try:
        for (data_json,) in c.execute(
            "SELECT data FROM part WHERE message_id = ? ORDER BY time_created",
            (msg_id,),
        ):
            try:
                parts.append(json.loads(data_json) if isinstance(data_json, str) else {})
            except (json.JSONDecodeError, TypeError):
                pass
    except sqlite3.OperationalError:
        pass
    return parts


class LegacyCodeagentAdapter:
    """Adapter for the legacy codeagent (`nga` cmd) SQLite database (ngagent.db).

    Implements the SourceAdapter protocol (see sources.py). The first SQL-based adapter
    in the registry — validates that the incremental collection path works with
    `WHERE time_created > ?` filtering instead of in-memory timestamp checks.
    """

    name = "legacy_codeagent"
    source_kind = "ai_session"

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or _find_db() or DEFAULT_DB_PATH

    def detect(self) -> bool:
        return os.path.exists(self.db_path)

    def collect(self) -> Iterator[dict]:
        yield from iter_db_events(self.db_path)

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        """Incremental collection via efficient SQL WHERE clause.

        `watermark` is in epoch seconds (the unified event timestamp format).
        We convert to millis for the SQL comparison since ngagent.db stores millis.

        C7 fix: yields ALL messages from sessions that have ANY message after the
        watermark, not just the post-watermark messages. This ensures segment()
        sees full session context for boundary detection.

        This is the first adapter with real SQL-level incremental filtering — the
        plan (9.5) calls this out as validating the registry handles non-JSONL sources.
        """
        if watermark is None:
            yield from self.collect()
            return
        watermark_ms = int(watermark * 1000)
        yield from iter_db_events(self.db_path, watermark_ms=watermark_ms)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Emit normalized events from legacy codeagent ngagent.db.")
    ap.add_argument("--db-path", default=None, help="path to ngagent.db (auto-detected if omitted)")
    ap.add_argument("--limit", type=int, default=0, help="limit number of events (0 = all)")
    args = ap.parse_args()

    adapter = LegacyCodeagentAdapter(db_path=args.db_path)
    if not adapter.detect():
        print(f"ngagent.db not found at {adapter.db_path}", file=__import__("sys").stderr)
        raise SystemExit(1)

    count = 0
    for ev in adapter.collect():
        print(json.dumps(ev, ensure_ascii=False))
        count += 1
        if args.limit and count >= args.limit:
            break
