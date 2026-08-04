"""Additional source adapters (Phase 6.4-6.8).

- VSCode Local History adapter: per-file edit timestamps from
  ~/AppData/Roaming/Code/User/History/**/entries.json
- iCalendar (.ics) adapter: user-exported calendar events (meetings with start/end).
- WeLink Meeting recordings adapter: .lnk files + recording files with timestamps.
- Windows Recent adapter: .lnk files in Recent/ + Jump Lists.
- 3ms adapter: via the existing huawei-3ms plugin (publish/edit timestamps).

Each implements the SourceAdapter protocol. All are optional — detect() returns False
if the source isn't present, and the registry skips them.
"""

from __future__ import annotations

import os
import re
import json
import glob
import struct
import shutil
import subprocess
from typing import Iterator
from datetime import datetime, timezone, timedelta

from sources import make_event


# ---------------------------------------------------------------------------
# VSCode Local History
# ---------------------------------------------------------------------------

VSCODE_HISTORY_DIR = os.path.join(
    os.path.expanduser("~"), "AppData", "Roaming", "Code", "User", "History"
)


class VSCodeHistoryAdapter:
    """Adapter for VSCode Local History — per-file edit timestamps."""

    name = "vscode_history"
    source_kind = "filesystem"

    def __init__(self, history_dir: str | None = None):
        self.history_dir = history_dir or VSCODE_HISTORY_DIR

    def detect(self) -> bool:
        return os.path.isdir(self.history_dir) and any(
            os.path.isfile(f) for f in glob.glob(os.path.join(self.history_dir, "**", "entries.json"), recursive=True)
        )

    def collect(self) -> Iterator[dict]:
        for entries_path in glob.glob(os.path.join(self.history_dir, "**", "entries.json"), recursive=True):
            try:
                with open(entries_path, encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue
            resource = data.get("resource", "")
            for entry in data.get("entries", []):
                ts_ms = entry.get("timestamp")
                if not ts_ms:
                    continue
                ts = ts_ms / 1000.0
                entry_id = entry.get("id", "")
                yield make_event(
                    source="vscode_history",
                    source_kind="filesystem",
                    session_id=None,
                    cwd=os.path.dirname(resource.replace("file:///", "")) if resource else None,
                    git_branch=None,
                    timestamp=ts,
                    timestamp_raw=str(ts_ms),
                    kind="file_edit",
                    text=os.path.basename(resource),
                    tool_input={"resource": resource, "entry_id": entry_id,
                                "source": entry.get("source", "")},
                )

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# iCalendar (.ics) export
# ---------------------------------------------------------------------------

class ICalendarAdapter:
    """Adapter for user-exported .ics calendar files.

    The user exports their Outlook/WeLink calendar to .ics (open format, sidesteps
    OST parsing and Graph API). This adapter parses VEVENT entries for meeting
    start/end/summary. Looks for .ics files in output/, ~/Calendar/, ~/Documents/,
    ~/Downloads/, and any path in env var RETRO_SCOPE_ICS_PATHS (os.pathsep-separated).

    Supports minimal RRULE expansion (FREQ=DAILY/WEEKLY) and TZID timezone
    parameters using stdlib only (no dateutil dependency required).
    """

    name = "icalendar"
    source_kind = "meeting"

    # Default lookback for recurring event expansion (days)
    _DEFAULT_LOOKBACK_DAYS = 365

    def __init__(self, ics_paths: list[str] | None = None):
        # Default: look for .ics files in the skill's output dir and common dirs
        self._ics_paths = ics_paths

    def _find_ics_files(self) -> list[str]:
        if self._ics_paths is not None:
            return [p for p in self._ics_paths if os.path.isfile(p)]
        paths = []
        _scripts_dir = os.path.dirname(os.path.abspath(__file__))
        _retro_dir = os.path.dirname(_scripts_dir)
        _default_out = os.path.join(os.path.dirname(_retro_dir), "output")
        output_dir = os.environ.get("RETRO_SCOPE_OUTPUT_DIR", _default_out)
        bases = [
            output_dir,
            os.path.expanduser("~/Calendar"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
        ]
        # Add paths from env var RETRO_SCOPE_ICS_PATHS (os.pathsep-separated)
        env_paths = os.environ.get("RETRO_SCOPE_ICS_PATHS", "")
        if env_paths:
            bases.extend(env_paths.split(os.pathsep))
        for base in bases:
            base = base.strip()
            if not base:
                continue
            if os.path.isfile(base) and base.lower().endswith(".ics"):
                paths.append(base)
            elif os.path.isdir(base):
                paths.extend(glob.glob(os.path.join(base, "**", "*.ics"), recursive=True))
        return paths

    def detect(self) -> bool:
        return len(self._find_ics_files()) > 0

    def collect(self) -> Iterator[dict]:
        for ics_path in self._find_ics_files():
            yield from self._parse_ics(ics_path)

    def _parse_ics(self, path: str) -> Iterator[dict]:
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except OSError:
            return

        # Unfold continuation lines (RFC 5545: line folding with leading space/tab)
        unfolded_lines = []
        for line in content.splitlines():
            if line.startswith((" ", "\t")) and unfolded_lines:
                unfolded_lines[-1] += line[1:]
            else:
                unfolded_lines.append(line)

        # Parse VEVENTs with their full property lines (preserving parameters)
        in_event = False
        ev_lines: list[str] = []
        for line in unfolded_lines:
            stripped = line.strip()
            if stripped == "BEGIN:VEVENT":
                in_event = True
                ev_lines = []
            elif stripped == "END:VEVENT":
                in_event = False
                yield from self._emit_event(ev_lines)
            elif in_event:
                ev_lines.append(stripped)

    def _emit_event(self, ev_lines: list[str]) -> Iterator[dict]:
        """Parse property lines and yield one or more events (expanding RRULE)."""
        ev: dict[str, str] = {}
        # Store full property (with parameters) for TZID handling
        full_props: dict[str, str] = {}
        for line in ev_lines:
            if ":" not in line:
                continue
            key_part, _, val = line.partition(":")
            # Strip parameters for the simple key
            key = key_part.split(";")[0]
            ev[key] = val
            full_props[key_part] = val

        dtstart_raw = ev.get("DTSTART")
        dtend_raw = ev.get("DTEND")
        summary = ev.get("SUMMARY", "(no title)")
        rrule = ev.get("RRULE")

        if not dtstart_raw:
            return

        # Parse DTSTART with TZID awareness
        dtstart_dt, tzid = self._parse_ics_dt_tzid(dtstart_raw, ev_lines)
        if dtstart_dt is None:
            return

        dtend_dt = None
        if dtend_raw:
            dtend_dt, _ = self._parse_ics_dt_tzid(dtend_raw, ev_lines)

        duration = None
        if dtend_dt is not None:
            duration = (dtend_dt - dtstart_dt).total_seconds()

        if rrule:
            # Expand recurring events within lookback window
            yield from self._expand_recurring(
                dtstart_dt, dtend_dt, duration, summary, rrule,
                ev, tzid, dtstart_raw,
            )
        else:
            yield self._make_meeting_event(
                dtstart_dt, summary, dtstart_raw, dtend_raw,
                duration, ev,
            )

    def _expand_recurring(
        self, dtstart: datetime, dtend: datetime | None,
        duration: float | None, summary: str, rrule: str,
        ev: dict[str, str], tzid: str | None,
        dtstart_raw: str,
    ) -> Iterator[dict]:
        """Expand RRULE occurrences within the lookback window.

        Supports FREQ=DAILY and FREQ=WEEKLY with INTERVAL. Complex BYDAY/MO/HR/MIN
        rules are not expanded (skipped with a comment). This is the stdlib-only
        path — dateutil is NOT a declared dependency in requirements.txt, so we
        avoid it.
        """
        # Parse RRULE components: RRULE:FREQ=DAILY;INTERVAL=2
        rrule_params: dict[str, str] = {}
        for part in rrule.split(";"):
            if "=" in part:
                k, _, v = part.partition("=")
                rrule_params[k.upper()] = v.upper()

        freq = rrule_params.get("FREQ", "")
        interval = int(rrule_params.get("INTERVAL", "1"))

        # UNTIL date if present
        until_dt: datetime | None = None
        until_str = rrule_params.get("UNTIL")
        if until_str:
            until_dt = self._parse_dt_value(until_str)

        # COUNT if present
        count = int(rrule_params.get("COUNT", "0")) if rrule_params.get("COUNT") else 0

        # Only handle DAILY and WEEKLY with simple intervals.
        # MONTHLY/YEARLY with BYDAY rules are too complex for stdlib expansion.
        if freq not in ("DAILY", "WEEKLY"):
            # Skip complex rules — emit just the first occurrence
            yield self._make_meeting_event(
                dtstart, summary, dtstart_raw,
                ev.get("DTEND", ""), duration, ev,
            )
            return

        # Expand within lookback window
        now = datetime.now(timezone.utc)
        lookback_start = now - timedelta(days=self._DEFAULT_LOOKBACK_DAYS)

        current = dtstart
        emitted = 0
        max_occurrences = 1000  # Safety cap
        while emitted < max_occurrences:
            if current.timestamp() > now.timestamp():
                break
            if until_dt is not None and current.timestamp() > until_dt.timestamp():
                break
            if count > 0 and emitted >= count:
                break

            # Emit if within lookback window
            if current.timestamp() >= lookback_start.timestamp():
                cur_end = None
                cur_duration = duration
                if dtend is not None:
                    cur_end = current + (dtend - dtstart)
                yield self._make_meeting_event(
                    current, summary,
                    current.strftime("%Y%m%dT%H%M%SZ") if current.tzinfo else current.strftime("%Y%m%dT%H%M%S"),
                    cur_end.strftime("%Y%m%dT%H%M%SZ") if cur_end and cur_end.tzinfo else (cur_end.strftime("%Y%m%dT%H%M%S") if cur_end else ""),
                    cur_duration, ev,
                )

            emitted += 1
            if freq == "DAILY":
                current = current + timedelta(days=interval)
            elif freq == "WEEKLY":
                current = current + timedelta(weeks=interval)

    def _make_meeting_event(
        self, dt: datetime, summary: str, dtstart_raw: str,
        dtend_raw: str, duration: float | None, ev: dict[str, str],
    ) -> dict:
        """Construct a single meeting event."""
        extra = None
        if duration is not None:
            extra = {"end_ts": dt.timestamp() + duration,
                     "duration_seconds": duration}
        return make_event(
            source="icalendar",
            source_kind="meeting",
            session_id=None,
            cwd=None,
            git_branch=None,
            timestamp=dt.timestamp(),
            timestamp_raw=dtstart_raw,
            kind="meeting",
            text=summary,
            tool_input={"summary": summary, "start": dtstart_raw, "end": dtend_raw,
                        "duration_seconds": duration,
                        "attendees": ev.get("ATTENDEE", "")},
            extra=extra,
        )

    def _parse_ics_dt_tzid(self, dt_str: str, ev_lines: list[str]) -> tuple[datetime | None, str | None]:
        """Parse an iCalendar datetime with TZID awareness.

        Returns (datetime, tzid). If TZID is present and not UTC, treats as
        local time (naive timestamp). If Z suffix, uses UTC. Otherwise UTC fallback.
        """
        dt_str = dt_str.strip()

        # Find the TZID parameter from the full property lines
        tzid = None
        for line in ev_lines:
            if ":" not in line:
                continue
            key_part, _, val = line.partition(":")
            if key_part.split(";")[0] == "DTSTART":
                # Look for TZID= in the key part
                for param in key_part.split(";")[1:]:
                    if param.upper().startswith("TZID="):
                        tzid = param.split("=", 1)[1]
                        break

        return self._parse_dt_value(dt_str, tzid), tzid

    def _parse_dt_value(self, dt_str: str, tzid: str | None = None) -> datetime | None:
        """Parse a datetime value, handling Z suffix, TZID, and naive timestamps."""
        dt_str = dt_str.strip()
        try:
            if dt_str.endswith("Z"):
                return datetime.strptime(dt_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
            # Date-only format: YYYYMMDD
            if "T" not in dt_str:
                dt = datetime.strptime(dt_str, "%Y%m%d")
                # If TZID present, treat as local; otherwise UTC
                if tzid and tzid.upper() != "UTC":
                    return dt  # naive local
                return dt.replace(tzinfo=timezone.utc)
            # Full datetime without Z
            dt = datetime.strptime(dt_str, "%Y%m%dT%H%M%S")
            if tzid and tzid.upper() != "UTC":
                return dt  # naive local — treat as local time
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None

    def _parse_ics_dt(self, dt_str: str) -> float | None:
        """Legacy parser for backward compatibility — returns epoch float."""
        dt = self._parse_dt_value(dt_str)
        if dt is None:
            return None
        return dt.timestamp()

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# Windows Recent files (.lnk)
# ---------------------------------------------------------------------------

WINDOWS_RECENT_DIR = os.path.join(
    os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Recent"
)


def _parse_lnk_timestamp(lnk_path: str) -> tuple[float | None, str | None]:
    """Extract the target path and timestamp from a .lnk file.

    Uses the file's mtime as a fallback if we can't parse the shell-link format.
    A proper .lnk parser is complex; for the MVP we use mtime + target-from-name.
    """
    mtime = os.path.getmtime(lnk_path)
    # The .lnk filename often encodes the target name
    target_name = os.path.splitext(os.path.basename(lnk_path))[0]
    return mtime, target_name


class WindowsRecentAdapter:
    """Adapter for Windows Recent files (.lnk shortcuts)."""

    name = "windows_recent"
    source_kind = "filesystem"

    def __init__(self, recent_dir: str | None = None):
        self.recent_dir = recent_dir or WINDOWS_RECENT_DIR

    def detect(self) -> bool:
        return os.path.isdir(self.recent_dir) and any(
            f.endswith(".lnk") for f in os.listdir(self.recent_dir)
        )

    def collect(self) -> Iterator[dict]:
        if not os.path.isdir(self.recent_dir):
            return
        for fname in os.listdir(self.recent_dir):
            if not fname.endswith(".lnk"):
                continue
            fpath = os.path.join(self.recent_dir, fname)
            ts, target = _parse_lnk_timestamp(fpath)
            if ts is None:
                continue
            yield make_event(
                source="windows_recent",
                source_kind="filesystem",
                session_id=None,
                cwd=None,
                git_branch=None,
                timestamp=ts,
                timestamp_raw=str(ts),
                kind="file_open",
                text=target or fname,
                tool_input={"lnk_path": fpath, "target_name": target},
            )

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# Jump List (.automaticDestinations-ms)
# ---------------------------------------------------------------------------

JUMP_LIST_DIR = os.path.join(
    os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows",
    "Recent", "AutomaticDestinations"
)

# Regex to find UTF-16LE-encoded file paths in binary data.
# Matches paths containing \\ or / with a file extension.
_UTF16_PATH_RE = re.compile(
    rb'(?:[\x20-\x7e]\x00){2,}'  # sequence of printable ASCII chars as UTF-16LE
)


def _scan_jump_list_paths(data: bytes) -> list[str]:
    """Heuristic byte-scan of .automaticDestinations-ms for embedded file paths.

    The MS-SHLLINK binary format contains UTF-16LE strings. We scan for
    sequences of printable ASCII (as UTF-16LE) that look like file paths
    (contain backslash or forward slash and end with an extension).

    This is intentionally a "good enough" heuristic — the same approach the
    WindowsRecentAdapter takes with .lnk files (mtime + target-from-name
    rather than a real shell-link parser).
    """
    paths = []
    seen = set()

    # Find all UTF-16LE string sequences
    for match in _UTF16_PATH_RE.finditer(data):
        try:
            s = match.group(0).decode("utf-16-le", errors="ignore").strip()
        except Exception:
            continue
        # Must look like a file path: contains \ or /, has an extension
        if not s:
            continue
        if "\\" not in s and "/" not in s:
            continue
        # Must end with a short extension (e.g. .docx, .py, .pdf, .xlsx)
        # Avoid matching partial/garbage strings
        if not re.search(r'\.[a-zA-Z0-9]{1,10}$', s):
            continue
        # Skip very short or very long strings
        if len(s) < 5 or len(s) > 500:
            continue
        # Deduplicate
        if s not in seen:
            seen.add(s)
            paths.append(s)

    return paths


class JumpListAdapter:
    """Adapter for Windows Jump List files (.automaticDestinations-ms).

    These are MS-SHLLINK binary format (compound file). A full parser is complex;
    for the MVP we use a heuristic byte-scan for UTF-16LE file paths, similar
    to how WindowsRecentAdapter uses mtime + target-from-name rather than a
    real .lnk parser.
    """

    name = "jump_list"
    source_kind = "filesystem"

    def __init__(self, jump_list_dir: str | None = None):
        self.jump_list_dir = jump_list_dir or JUMP_LIST_DIR

    def detect(self) -> bool:
        if not os.path.isdir(self.jump_list_dir):
            return False
        return any(
            f.endswith(".automaticDestinations-ms")
            for f in os.listdir(self.jump_list_dir)
        )

    def collect(self) -> Iterator[dict]:
        if not os.path.isdir(self.jump_list_dir):
            return
        for fname in os.listdir(self.jump_list_dir):
            if not fname.endswith(".automaticDestinations-ms"):
                continue
            fpath = os.path.join(self.jump_list_dir, fname)
            if not os.path.isfile(fpath):
                continue
            mtime = os.path.getmtime(fpath)
            try:
                with open(fpath, "rb") as f:
                    data = f.read()
            except OSError:
                continue
            for path in _scan_jump_list_paths(data):
                yield make_event(
                    source="jump_list",
                    source_kind="filesystem",
                    session_id=None,
                    cwd=None,
                    git_branch=None,
                    timestamp=mtime,
                    timestamp_raw=str(mtime),
                    kind="file_open",
                    text=path,
                    tool_input={"path": path, "dest_file": fpath,
                                "dest_file_name": fname},
                )

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# WeLink Meeting recordings
# ---------------------------------------------------------------------------

WELINK_RECORDINGS_DIR = "D:\\MeetingRecordings"

# Regex for WeLink recording filenames:
#   "20260713 09.55.29 会议 99997299.lnk"        — space-separated, dots in time
#   "20260713_111710_meeting_record.99997299.pdf" — underscore-separated, no time separators
#   "20260713 09.55.29 会议 99997299"             — no extension
_RECORDING_FILENAME_RE = re.compile(
    r"(?P<date>\d{8})"                     # YYYYMMDD
    r"(?:[\s_]+)"                          # separator (space or underscore)
    r"(?P<time>\d{2}[.\:]\d{2}[.\:]\d{2}|\d{6})"  # HH.MM.SS / HH:MM:SS / HHMMSS
    r".*?"                                  # middle part (subject etc.)
    r"(?P<meeting_id>\d{6,})"               # trailing meeting ID (6+ digits)
    r"(?:\.[^.]+)?$"                        # optional extension
)


def _parse_recording_filename(fname: str) -> dict:
    """Extract date, time, and meeting ID from a WeLink recording filename.

    Handles patterns like:
        "20260713 09.55.29 会议 99997299.lnk"
        "20260713_111710_meeting_record.99997299.pdf"
    Returns a dict with keys: date, time, meeting_id (or empty dict if no match).
    """
    m = _RECORDING_FILENAME_RE.search(fname)
    if not m:
        return {}
    return {
        "date": m.group("date"),
        "time": m.group("time"),
        "meeting_id": m.group("meeting_id"),
    }


def _ffprobe_duration(fpath: str) -> float | None:
    """Call ffprobe to get media duration in seconds. Returns None if unavailable."""
    if not shutil.which("ffprobe"):
        return None
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet",
             "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1",
             fpath],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except (subprocess.SubprocessError, ValueError, OSError):
        pass
    return None


class WeLinkRecordingsAdapter:
    """Adapter for WeLink Meeting recordings (.lnk + recording files).

    When ffprobe is available, extracts actual media duration. Falls back to
    mtime-only when ffprobe is absent or fails. Parses meeting subject, date,
    time, and meeting ID from the recording filename pattern.
    """

    name = "welink_recordings"
    source_kind = "meeting"

    def __init__(self, recordings_dir: str | None = None):
        self.recordings_dir = recordings_dir or WELINK_RECORDINGS_DIR

    def detect(self) -> bool:
        return os.path.isdir(self.recordings_dir)

    def collect(self) -> Iterator[dict]:
        if not os.path.isdir(self.recordings_dir):
            return
        for root, dirs, files in os.walk(self.recordings_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                mtime = os.path.getmtime(fpath)

                # Parse meeting info from filename
                parsed = _parse_recording_filename(fname)
                tool_input: dict = {"path": fpath, "size": os.path.getsize(fpath)}
                if parsed:
                    tool_input["date"] = parsed["date"]
                    tool_input["time"] = parsed["time"]
                    tool_input["meeting_id"] = parsed["meeting_id"]

                # Extract duration via ffprobe (optional)
                duration = _ffprobe_duration(fpath)
                if duration is not None:
                    tool_input["duration_seconds"] = duration

                ev = make_event(
                    source="welink_recordings",
                    source_kind="meeting",
                    session_id=parsed.get("meeting_id"),
                    cwd=None,
                    git_branch=None,
                    timestamp=mtime,
                    timestamp_raw=str(mtime),
                    kind="meeting_recording",
                    text=fname,
                    tool_input=tool_input,
                )
                if duration is not None:
                    ev["extra"] = {"end_ts": mtime + duration,
                                   "duration_seconds": duration}
                yield ev

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            if ev.get("timestamp", 0) > watermark:
                yield ev


# ---------------------------------------------------------------------------
# 3ms (via existing huawei-3ms plugin)
# ---------------------------------------------------------------------------

class ThreeMsAdapter:
    """Adapter for 3ms publish/edit timestamps via the huawei-3ms plugin.

    Gated on the plugin being installed. The plugin is invoked via opencli if available.
    For now, this is a detector-only adapter — it detects the plugin but doesn't
    collect (the plugin's search/read interface doesn't expose publish timestamps
    in a structured way yet). Marked as a placeholder for Phase 6.9.
    """

    name = "3ms"
    source_kind = "doc_authoring"

    def detect(self) -> bool:
        # Check if the huawei-3ms plugin is installed
        import shutil
        return shutil.which("opencli") is not None

    def collect(self) -> Iterator[dict]:
        # Phase 6.9 placeholder: the 3ms plugin doesn't yet expose publish timestamps
        # in a structured way. When it does, this will yield doc_authoring events.
        return
        yield  # make it a generator

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        yield from self.collect()
