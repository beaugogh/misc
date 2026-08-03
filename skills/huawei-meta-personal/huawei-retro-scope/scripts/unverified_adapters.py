"""Unverified-source adapters (Phase 6.10).

Adapters for AI coding agents and doc-authoring platforms that are NOT on the
author's machine but may be on a colleague's. Each adapter follows the standard
detect()/collect() pattern:

  - `detect()` returns True only when the expected data path exists.
  - `collect()` parses defensively — if the real layout differs from what's
    documented, it skips bad records rather than crashing.
  - The registry skips any adapter whose detect() returns False, with a clear
    reason in the per-run discovery report.

Sources:
  - Codex (OpenAI CLI)         → `~/.codex/sessions/` (JSONL expected)
  - Openclaw                   → `~/.openclaw/` or `~/.open-claw/` (JSONL/SQLite)
  - Hermes-agent               → `~/.hermes-agent/` or `~/.hermes/` (JSONL/SQLite)
  - CloudDevOps Wiki           → via `opencli` if a wiki plugin exists
  - W3                         → via `opencli` if a w3 plugin exists

These are [unverified] in SKILL.md — the expected paths are documented from
public tool docs / community knowledge. The adapter verifies itself on first
real encounter: if the layout differs, the defensive parser yields what it
can and logs unparseable records to stderr.
"""

from __future__ import annotations

import os
import json
import glob
import shutil
import sqlite3
import subprocess
from typing import Iterator
from datetime import datetime, timezone
from pathlib import Path

from sources import make_event


# ---------------------------------------------------------------------------
# Codex (OpenAI CLI)
# ---------------------------------------------------------------------------

CODEX_DIR = os.path.join(os.path.expanduser("~"), ".codex")
CODEX_SESSIONS_DIR = os.path.join(CODEX_DIR, "sessions")
CODEX_HISTORY_FILE = os.path.join(CODEX_DIR, "history.jsonl")


class CodexAdapter:
    """Adapter for OpenAI Codex CLI session transcripts.

    Expected layout (from public Codex docs):
      ~/.codex/sessions/<session_id>.jsonl  — per-session transcripts
      ~/.codex/history.jsonl                — prompt log

    The JSONL schema is expected to be similar to Claude Code (role/content
    messages with timestamps). This adapter parses defensively — if the schema
    differs, it yields what it can and skips unparseable lines.
    """

    name = "codex"
    source_kind = "ai_session"

    def __init__(self, codex_dir: str | None = None):
        self._codex_dir = codex_dir or CODEX_DIR

    def detect(self) -> bool:
        return os.path.isdir(self._codex_dir) and (
            os.path.isdir(os.path.join(self._codex_dir, "sessions"))
            or os.path.isfile(os.path.join(self._codex_dir, "history.jsonl"))
        )

    def _parse_iso8601(self, ts: str | None) -> float | None:
        if not ts:
            return None
        try:
            s = ts.replace("Z", "+00:00")
            return datetime.fromisoformat(s).timestamp()
        except (ValueError, TypeError):
            return None

    def _parse_jsonl_file(self, path: str) -> Iterator[dict]:
        """Parse a JSONL session file, yielding normalized events.

        Defensive: skips lines that aren't valid JSON or don't have a timestamp.
        Handles both Claude-Code-style (type/message/timestamp) and Codex-style
        (role/content/created_at) schemas.
        """
        session_id = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Timestamp: try common field names.
                ts_raw = obj.get("timestamp") or obj.get("created_at") or obj.get("time")
                ts = self._parse_iso8601(ts_raw) if isinstance(ts_raw, str) else None
                if ts is None:
                    # Try millis epoch.
                    if isinstance(ts_raw, (int, float)):
                        ts = float(ts_raw) / 1000 if ts_raw > 1e12 else float(ts_raw)
                if ts is None:
                    continue

                cwd = obj.get("cwd") or obj.get("directory")
                git_branch = obj.get("gitBranch") or obj.get("git_branch")
                typ = obj.get("type", "?")
                message = obj.get("message") if isinstance(obj.get("message"), dict) else None
                # Role can be at top level (Codex style) or inside message (Claude style).
                role = None
                if message:
                    role = message.get("role")
                elif obj.get("role"):
                    role = obj.get("role")

                # Determine event kind.
                if typ == "user" or role == "user":
                    # Extract content from message or top-level.
                    content = None
                    if message:
                        content = message.get("content")
                    elif obj.get("content"):
                        content = obj.get("content")
                    ev = make_event(
                        source="codex", source_kind="ai_session",
                        session_id=session_id, cwd=cwd, git_branch=git_branch,
                        timestamp=ts, timestamp_raw=str(ts_raw),
                        kind="user_message",
                        role="user",
                    )
                    ev["text"] = str(content)[:2000] if content else None
                    yield ev
                elif typ == "assistant" or role == "assistant":
                    # Extract content from message or top-level.
                    content = None
                    if message:
                        content = message.get("content")
                    elif obj.get("content"):
                        content = obj.get("content")
                    ev = make_event(
                        source="codex", source_kind="ai_session",
                        session_id=session_id, cwd=cwd, git_branch=git_branch,
                        timestamp=ts, timestamp_raw=str(ts_raw),
                        kind="assistant_message",
                        role="assistant",
                        usage=message.get("usage") if message else (obj.get("usage") if isinstance(obj.get("usage"), dict) else None),
                        stop_reason=message.get("stop_reason") if message else obj.get("stop_reason"),
                    )
                    ev["text"] = str(content)[:2000] if content else None
                    yield ev
                else:
                    # Other line types — yield as lightweight markers.
                    yield make_event(
                        source="codex", source_kind="ai_session",
                        session_id=session_id, cwd=cwd, git_branch=git_branch,
                        timestamp=ts, timestamp_raw=str(ts_raw),
                        kind=typ,
                    )

    def collect(self) -> Iterator[dict]:
        sessions_dir = os.path.join(self._codex_dir, "sessions")
        if os.path.isdir(sessions_dir):
            for path in glob.glob(os.path.join(sessions_dir, "**", "*.jsonl"), recursive=True):
                try:
                    yield from self._parse_jsonl_file(path)
                except OSError:
                    continue

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# Openclaw
# ---------------------------------------------------------------------------

OPENCLAW_DIRS = [
    os.path.join(os.path.expanduser("~"), ".openclaw"),
    os.path.join(os.path.expanduser("~"), ".open-claw"),
]


class OpenclawAdapter:
    """Adapter for Openclaw session transcripts.

    Layout is unknown — the adapter searches ~/.openclaw/ and ~/.open-claw/
    for JSONL files (*.jsonl) and SQLite databases (*.db, *.sqlite).
    Parses JSONL defensively (same as CodexAdapter); for SQLite, tries
    common session/message table schemas.
    """

    name = "openclaw"
    source_kind = "ai_session"

    def __init__(self, openclaw_dir: str | None = None):
        self._dirs = [openclaw_dir] if openclaw_dir else OPENCLAW_DIRS

    def detect(self) -> bool:
        return any(os.path.isdir(d) for d in self._dirs)

    def _find_data_files(self) -> Iterator[str]:
        for d in self._dirs:
            if not os.path.isdir(d):
                continue
            # JSONL files.
            yield from glob.glob(os.path.join(d, "**", "*.jsonl"), recursive=True)
            # SQLite files.
            yield from glob.glob(os.path.join(d, "**", "*.db"), recursive=True)
            yield from glob.glob(os.path.join(d, "**", "*.sqlite"), recursive=True)

    def _parse_sqlite(self, path: str) -> Iterator[dict]:
        """Try to parse a SQLite DB with session/message tables.

        Defensive: tries common table names and column names. If the schema
        doesn't match, yields nothing.
        """
        try:
            conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        except sqlite3.Error:
            return
        try:
            cur = conn.cursor()
            # Discover tables.
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0].lower() for row in cur.fetchall()}
            # Look for a message-like table.
            msg_table = None
            for candidate in ("messages", "message", "events", "chat", "turns", "parts"):
                if candidate in tables:
                    msg_table = candidate
                    break
            if not msg_table:
                return
            # Get column names.
            cur.execute(f"PRAGMA table_info({msg_table})")
            cols = {row[1].lower(): row[1] for row in cur.fetchall()}
            # Find timestamp column.
            ts_col = None
            for candidate in ("timestamp", "time", "created_at", "time_created",
                              "created", "date", "sendtime"):
                if candidate in cols:
                    ts_col = cols[candidate]
                    break
            if not ts_col:
                return
            # Find role/content columns.
            role_col = cols.get("role") or cols.get("sender") or cols.get("type")
            content_col = cols.get("content") or cols.get("text") or cols.get("message") or cols.get("body")
            session_col = cols.get("session_id") or cols.get("sessionid")

            cur.execute(f"SELECT * FROM {msg_table} ORDER BY {ts_col}")
            for row in cur.fetchall():
                col_names = [desc[0] for desc in cur.description]
                row_dict = dict(zip(col_names, row))
                ts_val = row_dict.get(ts_col)
                if isinstance(ts_val, (int, float)):
                    ts = float(ts_val) / 1000 if ts_val > 1e12 else float(ts_val)
                elif isinstance(ts_val, str):
                    try:
                        ts = datetime.fromisoformat(ts_val.replace("Z", "+00:00")).timestamp()
                    except (ValueError, TypeError):
                        continue
                else:
                    continue
                kind = "user_message"
                if role_col:
                    role = str(row_dict.get(role_col, "")).lower()
                    if "assistant" in role or "ai" in role:
                        kind = "assistant_message"
                yield make_event(
                    source="openclaw", source_kind="ai_session",
                    session_id=str(row_dict.get(session_col, "")) if session_col else None,
                    cwd=None, git_branch=None,
                    timestamp=ts, kind=kind,
                    text=str(row_dict.get(content_col, ""))[:2000] if content_col else None,
                )
        except sqlite3.Error:
            pass
        finally:
            conn.close()

    def collect(self) -> Iterator[dict]:
        codex_parser = CodexAdapter()  # reuse the JSONL parser
        for path in self._find_data_files():
            try:
                if path.endswith((".db", ".sqlite")):
                    yield from self._parse_sqlite(path)
                elif path.endswith(".jsonl"):
                    yield from codex_parser._parse_jsonl_file(path)
            except (OSError, sqlite3.Error):
                continue

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# Hermes-agent
# ---------------------------------------------------------------------------

HERMES_DIRS = [
    os.path.join(os.path.expanduser("~"), ".hermes-agent"),
    os.path.join(os.path.expanduser("~"), ".hermes"),
]


class HermesAgentAdapter:
    """Adapter for Hermes-agent session transcripts.

    Layout is unknown — searches ~/.hermes-agent/ and ~/.hermes/ for JSONL
    and SQLite files. Same defensive parsing as OpenclawAdapter.
    """

    name = "hermes_agent"
    source_kind = "ai_session"

    def __init__(self, hermes_dir: str | None = None):
        self._dirs = [hermes_dir] if hermes_dir else HERMES_DIRS

    def detect(self) -> bool:
        return any(os.path.isdir(d) for d in self._dirs)

    def collect(self) -> Iterator[dict]:
        # Reuse OpenclawAdapter's parsing logic with hermes dirs.
        parser = OpenclawAdapter.__new__(OpenclawAdapter)
        parser._dirs = self._dirs
        for ev in parser.collect():
            # Relabel events as hermes_agent source.
            ev["source"] = "hermes_agent"
            yield ev

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# CloudDevOps Wiki (via opencli plugin)
# ---------------------------------------------------------------------------

class CloudDevOpsWikiAdapter:
    """Adapter for CloudDevOps Wiki authoring activity.

    CloudDevOps Wiki is a Huawei-internal web platform. There's no local
    session store — activity must be fetched via an API or CLI plugin.

    Detection: checks for `opencli` in PATH (the Huawei internal CLI bridge).
    If a `clouddevops-wiki` plugin is available via opencli, this adapter
    will use it to fetch wiki edit/publish timestamps.

    Currently detector-only: the opencli plugin for CloudDevOps Wiki doesn't
    expose structured timestamps yet. When it does, collect() will yield
    doc_authoring events. The adapter is registered so that a colleague with
    the plugin gets automatic detection.
    """

    name = "clouddevops_wiki"
    source_kind = "doc_authoring"

    def detect(self) -> bool:
        # Check if opencli is available AND has a clouddevops/wiki command.
        if not shutil.which("opencli"):
            return False
        try:
            result = subprocess.run(
                ["opencli", "list"], capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=15,
            )
            if result.returncode != 0:
                return False
            # Check for clouddevops or wiki commands in the output.
            output = result.stdout.lower()
            return "clouddevops" in output or "wiki" in output
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def collect(self) -> Iterator[dict]:
        # Placeholder: the opencli clouddevops-wiki plugin doesn't yet expose
        # structured publish/edit timestamps. When it does, this will yield
        # doc_authoring events with title, url, author, publish_time, edit_time.
        return
        yield  # make it a generator

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        yield from self.collect()


# ---------------------------------------------------------------------------
# W3 (Huawei internal portal, via opencli plugin)
# ---------------------------------------------------------------------------

class W3Adapter:
    """Adapter for W3 (Huawei internal portal) activity.

    W3 is Huawei's internal web portal. Like CloudDevOps Wiki, there's no
    local session store — activity would come via an API or CLI plugin.

    Detection: checks for `opencli` with a w3 command.
    Currently detector-only (same as CloudDevOpsWikiAdapter).
    """

    name = "w3"
    source_kind = "doc_authoring"

    def detect(self) -> bool:
        if not shutil.which("opencli"):
            return False
        try:
            result = subprocess.run(
                ["opencli", "list"], capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=15,
            )
            if result.returncode != 0:
                return False
            # Check for w3 commands (but not huawei-3ms which is a different source).
            output = result.stdout.lower()
            # Look for a standalone w3 command, not w3 within another command name.
            lines = output.split("\n")
            for line in lines:
                if line.strip().startswith("w3") or "w3 " in line.lower():
                    return True
            return False
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def collect(self) -> Iterator[dict]:
        # Placeholder: the W3 access path is not yet defined. When an opencli
        # w3 plugin exposes structured timestamps, this will yield doc_authoring
        # events.
        return
        yield  # make it a generator

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        yield from self.collect()


# ---------------------------------------------------------------------------
# Registration helper
# ---------------------------------------------------------------------------

def register_unverified_adapters(registry) -> None:
    """Register all unverified-source adapters on the given registry.

    Each adapter's detect() returns False when the source isn't present,
    so they silently skip on machines without them.
    """
    registry.register(CodexAdapter())
    registry.register(OpenclawAdapter())
    registry.register(HermesAgentAdapter())
    registry.register(CloudDevOpsWikiAdapter())
    registry.register(W3Adapter())
