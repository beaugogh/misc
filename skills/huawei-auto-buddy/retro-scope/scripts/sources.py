"""Unified event schema + adapter registry.

Defines:
  - `Event` — the normalized event contract all adapters emit. A typed dict (kept as a
    plain dict for JSON-serializability) with a documented set of fields.
  - `SourceAdapter` — the interface every source implements: `detect() -> bool` and
    `collect() -> Iterator[Event]`. Optional `collect_since(watermark) -> Iterator[Event]`
    for incremental collection (Phase 2).
  - `SourceRegistry` — holds all adapters; `collect_all()` runs them and merges events.

`source_kind` discriminates the source category:
  ai_session | vcs | browser | filesystem | meeting | comm | doc_authoring

The registry is the seam every later source (git, browser, vscode, etc.) plugs into.
Pattern reference: Memacs (per-source modules) + Plaso (normalized µs-epoch + dedup).
"""

from __future__ import annotations

from typing import Iterator, Protocol, runtime_checkable


# Discriminator for the source category. Drives classifier + fusion behavior.
SOURCE_KINDS = {
    "ai_session",    # Claude Code, codeagent, codex, etc. — JSONL transcripts with task model
    "vcs",           # git / CodeHub — commits, branch checkouts
    "browser",       # Chrome/Edge history — visits, downloads, searches
    "filesystem",    # Windows Recent, VSCode Local History, Jump Lists
    "meeting",       # .ics, WeLink recordings, Outlook calendar
    "comm",          # welink-cli IM, email
    "doc_authoring", # 3ms, CloudDevOps Wiki, W3
    "auxiliary",     # daemon.log, tasks/jobs, shell-snapshots — weak time signal
}


def make_event(
    *,
    source: str,            # adapter name, e.g. "claude_code"
    source_kind: str,       # one of SOURCE_KINDS
    session_id: str | None,
    cwd: str | None,
    git_branch: str | None,
    timestamp: float,       # epoch seconds, normalized
    timestamp_raw: str | None = None,
    kind: str = "event",    # event type within the source
    role: str | None = None,
    text: str | None = None,
    tool_name: str | None = None,
    tool_input: dict | None = None,
    tool_is_error: bool | None = None,
    tool_use_id: str | None = None,
    usage: dict | None = None,
    stop_reason: str | None = None,
    extra: dict | None = None,
) -> dict:
    """Construct a normalized event dict.

    All events share this shape. Adapters may add source-specific fields via `extra`,
    but the core fields above are the contract the fusion/segmentation layers rely on.
    """
    ev = {
        "source": source,
        "source_kind": source_kind,
        "session_id": session_id,
        "cwd": cwd,
        "git_branch": git_branch,
        "timestamp": timestamp,
        "timestamp_raw": timestamp_raw,
        "kind": kind,
        "role": role,
        "text": text,
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_is_error": tool_is_error,
        "tool_use_id": tool_use_id,
        "usage": usage,
        "stop_reason": stop_reason,
    }
    if extra:
        ev["extra"] = extra
    return ev


@runtime_checkable
class SourceAdapter(Protocol):
    """Interface every source adapter implements.

    `name` — short identifier, e.g. "claude_code".
    `source_kind` — one of SOURCE_KINDS.
    `detect()` — return True if this source is present in the current environment.
    `collect()` — yield normalized events (full history).
    `collect_since(watermark)` — optional: yield only events after the watermark (epoch
        seconds). Adapters that don't support incremental collection should leave this
        as-is (defaults to full collect).
    """

    name: str
    source_kind: str

    def detect(self) -> bool: ...

    def collect(self) -> Iterator[dict]: ...

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        """Default: ignore watermark, do full collect. Override for incremental."""
        yield from self.collect()


class SourceRegistry:
    """Holds all registered adapters and runs collection across them."""

    def __init__(self):
        self._adapters: list[SourceAdapter] = []

    def register(self, adapter: SourceAdapter) -> "SourceRegistry":
        self._adapters.append(adapter)
        return self

    def detected(self) -> list[SourceAdapter]:
        """Return only adapters whose detect() is True."""
        return [a for a in self._adapters if a.detect()]

    def collect_all(self, watermark: float | None = None) -> tuple[list[dict], list[dict]]:
        """Run all detected adapters. Returns (events, skipped).

        `events` — flat sorted list of normalized events from all detected adapters.
        `skipped` — list of {name, reason} for adapters that didn't detect or errored.

        After collecting from each adapter, calls ``adapter.close()`` if the
        method exists — this releases COM objects (Outlook adapter) and other
        resources to prevent MAPI session exhaustion.
        """
        events: list[dict] = []
        skipped: list[dict] = []
        max_events_per_source = 100_000
        for adapter in self._adapters:
            if not adapter.detect():
                skipped.append({"name": adapter.name, "reason": "not detected"})
                continue
            try:
                if watermark is not None:
                    evs = adapter.collect_since(watermark)
                else:
                    evs = adapter.collect()
                for index, event in enumerate(evs):
                    if index >= max_events_per_source:
                        skipped.append({"name": adapter.name,
                                        "reason": "partial: 100000-event safety limit reached"})
                        break
                    events.append(event)
            except Exception as e:
                skipped.append({"name": adapter.name, "reason": f"error: {e}"})
            finally:
                # Release resources (COM objects, file handles, etc.) after
                # each adapter finishes. Critical for the Outlook COM adapter —
                # unreleased MAPI sessions cause "shared resources exhausted" popups.
                close_fn = getattr(adapter, "close", None)
                if close_fn is not None:
                    try:
                        close_fn()
                    except Exception:
                        pass
        events.sort(key=lambda e: (e.get("timestamp") is None, e.get("timestamp") or 0.0))
        return events, skipped


def default_registry(session_cwds: list[str] | None = None) -> SourceRegistry:
    """Build a registry with all currently-implemented adapters.

    As more adapters are implemented (git, browser, vscode, etc.), register them here.
    Adapters that don't detect simply skip — the registry's collect_all handles it.

    `session_cwds` — optional list of cwd values from AI-session events, used by the git
    adapter to discover project roots. If None, the git adapter falls back to its own
    discovery (walk-up from the script dir). To wire the full discovery loop, collect
    AI-session events first, extract cwds, then pass them here. For the simple case
    (no session cwds), git still works on the repo the script lives in.
    """
    from claude_code_adapter import ClaudeCodeAdapter, CodeagentAdapter
    from git_adapter import GitAdapter, discover_git_roots
    from browser_adapter import ChromeHistoryAdapter, EdgeHistoryAdapter
    from more_adapters import (
        VSCodeHistoryAdapter, ICalendarAdapter, WindowsRecentAdapter,
        WeLinkRecordingsAdapter, JumpListAdapter, ThreeMsAdapter,
    )
    from welink_cli_adapter import WeLinkCLIAdapter
    from legacy_codeagent_adapter import LegacyCodeagentAdapter
    from outlook_adapter import OutlookAdapter

    reg = SourceRegistry()
    reg.register(ClaudeCodeAdapter())
    reg.register(CodeagentAdapter())
    roots = discover_git_roots(session_cwds) if session_cwds else None
    reg.register(GitAdapter(roots=roots))
    reg.register(ChromeHistoryAdapter())
    reg.register(EdgeHistoryAdapter())
    reg.register(VSCodeHistoryAdapter())
    reg.register(ICalendarAdapter())
    reg.register(WindowsRecentAdapter())
    reg.register(JumpListAdapter())
    reg.register(WeLinkRecordingsAdapter())
    reg.register(WeLinkCLIAdapter(enable_im=True))
    reg.register(LegacyCodeagentAdapter())
    reg.register(OutlookAdapter())
    reg.register(ThreeMsAdapter())

    # Phase 6.10: unverified-source adapters. Each detect() returns False when
    # the tool isn't present, so they silently skip on machines without them.
    from unverified_adapters import register_unverified_adapters
    register_unverified_adapters(reg)

    return reg
