"""Browser history adapter (Chrome / Edge).

Reads the `History` SQLite database from Chrome and/or Edge and emits normalized events:
  - kind=visit: a page was visited. Carries url, title.
  - kind=download: a file was downloaded. Carries target_path, start/end time.
  - kind=search: a search query was entered. Carries the query text.

Chrome/Edge lock the History DB while running, so we copy-then-read.

Timestamps in Chrome's DB are microseconds since 1601-01-01 (Windows epoch). We normalize
to Unix epoch seconds.

This is the first non-AI, non-VCS source — validates the classifier handling `browser`
source_kind.
"""

from __future__ import annotations

import os
import sqlite3
import shutil
import tempfile
from typing import Iterator

from sources import make_event
from platform_paths import CHROME_HISTORY as DEFAULT_CHROME_HISTORY
from platform_paths import EDGE_HISTORY as DEFAULT_EDGE_HISTORY


# Chrome/Edge epoch: 1601-01-01 00:00:00 UTC, in microseconds.
# Unix epoch: 1970-01-01. The difference is 11644473600 seconds.
CHROME_EPOCH_OFFSET_US = 11644473600 * 1_000_000


def _chrome_ts_to_epoch(ts_us: int) -> float:
    """Convert Chrome microseconds-since-1601 to Unix epoch seconds."""
    return (ts_us - CHROME_EPOCH_OFFSET_US) / 1_000_000


def _copy_then_read(db_path: str) -> str:
    """Copy a (possibly locked) SQLite DB to a temp file and return the temp path."""
    fd, tmp = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    shutil.copy2(db_path, tmp)
    return tmp


def iter_history_events(db_path: str, browser_name: str = "chrome") -> Iterator[dict]:
    """Yield visit/download/search events from a Chrome/Edge History DB."""
    if not os.path.exists(db_path):
        return

    tmp = _copy_then_read(db_path)
    try:
        conn = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        c = conn.cursor()

        # Visits (joined with urls for url+title)
        try:
            for url, title, visit_time_us, visit_count in c.execute(
                "SELECT u.url, u.title, v.visit_time, u.visit_count "
                "FROM urls u JOIN visits v ON u.id = v.url "
                "ORDER BY v.visit_time"
            ):
                ts = _chrome_ts_to_epoch(visit_time_us)
                yield make_event(
                    source=browser_name,
                    source_kind="browser",
                    session_id=None,
                    cwd=None,
                    git_branch=None,
                    timestamp=ts,
                    timestamp_raw=str(visit_time_us),
                    kind="visit",
                    text=title,
                    tool_input={"url": url, "title": title, "visit_count": visit_count},
                )
        except sqlite3.OperationalError:
            pass  # table missing or locked

        # Downloads
        try:
            for row in c.execute(
                "SELECT target_path, start_time, end_time, total_bytes, mime_type "
                "FROM downloads ORDER BY start_time"
            ):
                target, start_us, end_us, total_bytes, mime = row
                ts = _chrome_ts_to_epoch(start_us)
                yield make_event(
                    source=browser_name,
                    source_kind="browser",
                    session_id=None,
                    cwd=None,
                    git_branch=None,
                    timestamp=ts,
                    timestamp_raw=str(start_us),
                    kind="download",
                    text=os.path.basename(target or ""),
                    tool_input={"target_path": target, "total_bytes": total_bytes,
                                "mime_type": mime,
                                "end_time": _chrome_ts_to_epoch(end_us) if end_us else None},
                )
        except sqlite3.OperationalError:
            pass

        # Search queries
        try:
            for row in c.execute(
                "SELECT kst.url_id, kst.search_terms, u.url, v.visit_time "
                "FROM keyword_search_terms kst "
                "JOIN urls u ON kst.url_id = u.id "
                "JOIN visits v ON kst.url_id = v.url "
                "ORDER BY v.visit_time"
            ):
                url_id, query, url, visit_time_us = row
                ts = _chrome_ts_to_epoch(visit_time_us)
                yield make_event(
                    source=browser_name,
                    source_kind="browser",
                    session_id=None,
                    cwd=None,
                    git_branch=None,
                    timestamp=ts,
                    timestamp_raw=str(visit_time_us),
                    kind="search",
                    text=query,
                    tool_input={"query": query, "url": url},
                )
        except sqlite3.OperationalError:
            pass

        conn.close()
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


class ChromeHistoryAdapter:
    """Adapter for Chrome browser history."""

    name = "chrome"
    source_kind = "browser"

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or DEFAULT_CHROME_HISTORY

    def detect(self) -> bool:
        return os.path.exists(self.db_path)

    def collect(self) -> Iterator[dict]:
        yield from iter_history_events(self.db_path, "chrome")

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            ts = ev.get("timestamp")
            if ts is not None and ts > watermark:
                yield ev


class EdgeHistoryAdapter(ChromeHistoryAdapter):
    """Adapter for Edge browser history (same schema as Chrome)."""

    name = "edge"

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or DEFAULT_EDGE_HISTORY

    def collect(self) -> Iterator[dict]:
        yield from iter_history_events(self.db_path, "edge")
