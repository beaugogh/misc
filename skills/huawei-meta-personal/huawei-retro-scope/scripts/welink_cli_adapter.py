"""WeLink CLI adapter — meetings, calendar, mail, and IM history.

`welink-cli` is a single npm tool (OAuth2 scan-to-login) that exposes four data domains
relevant to retrospective time tracking. This one adapter collects all four:

  - `meeting query-list`  → meeting start/end (millis epoch). **This is the meeting-DURATION
    signal that was the #1 ranked gap in SKILL.md** ("Meeting DURATION weak"). Each meeting
    carries an actual start_time + end_time, giving wall-clock duration directly — no need
    to infer from recordings or calendar free/busy. Page size capped at 30 by the API.
  - `calendar list`       → calendar events with start/end (ISO 8601, +08:00). Scheduled
    meeting duration + subject + location + organizer. Overlaps with `meeting query-list`
    but covers non-WeLink meetings (personal calendar entries) too.
  - `mail list`           → email send/receive times + subjects + sender. Each email thread
    = a communication task instance. Duration is weak (send time ≠ composing time) but the
    occurrence + subject feeds task reconstruction and categorization.
  - `im query-history-message` → WeLink chat messages. Two-step: first
    `query-recent-conversation` to enumerate conversations, then `query-history-message`
    per conversation. Chat duration is weak (SKILL.md ranks it last among meeting sources)
    but the occurrence signal fills gaps between coding sessions.

Gated on `welink-cli` being in PATH and authenticated (`welink-cli auth login`). If not
installed, `detect()` returns False and the registry skips it with a clear reason in the
per-run discovery report.

This is a **local-CLI-to-remote-service** source (like nga.cmd / Graph API): the binary
sits locally but data is fetched from WeLink's servers over the network, needing auth.
The CLI manages its own OAuth2 + WebSocket connection; we just shell out and parse JSON.

Output format: `calendar` and `mail` accept `--format json` (placed after the domain,
before the subcommand: `calendar --format json list`) and return bare JSON arrays.
`meeting` and `im` have NO `--format` flag — they return JSON by default, wrapped in
envelopes: meeting → {"code":200,"data":{"data":[...]}}, im conversations →
{"conversation_info":[...]}, im messages → {"respData":{"chatInfo":[...]}}. The
`_extract_json_list` helper unwraps all these shapes.

Timestamps: welink-cli uses millis-epoch for meeting query params (`--meeting-start-time
1767196800000`) and YYYY-MM-DD (end-exclusive!) for calendar/mail date ranges. Response
timestamps are millis-epoch (meetings: meetingStartTime/meetingEndTime; im: serverSendTime)
or ISO 8601 with offset (calendar/mail: start/end/dateTimeReceived, e.g.
"2026-07-22T17:00:00+08:00"). We normalize all to Unix epoch seconds.

Prerequisites (verified 2026-07 against a real authenticated instance):
  - `welink-cli` installed (npm global; Windows postinstall has a PowerShell bug —
    install with `--ignore-scripts`, the .CMD shim lands in npm's global bin which is
    normally already on PATH).
  - `welink-cli auth login` completed (token valid ~30min; refresh handled by the CLI).
  - For calendar/mail: `welink-cli mail autodiscover --email <you>@huawei.com` must have
    been run once to discover the Exchange server (e.g. imailie.email.huawei.com).
  - Intranet registry access: if behind the corporate proxy, set
    `NO_PROXY=cmc.centralrepo.rnd.huawei.com` for the install.

Field names verified against real API responses (2026-07-30): meeting uses
meetingStartTime/meetingEndTime (may be null → fall back to estimatedStartTime/
estimatedEndTime strings), subject, meetingId, location; calendar uses lowercase
start/end/itemId/subject/organizer/legacyFreeBusyStatus; mail uses dateTimeReceived/
from/fromEmail/itemId/subject/isRead/hasAttachments; im uses serverSendTime/sender/
content/contentType/msgId/groupId (content is a JSON string for CARD_MSG — see
`_extract_im_text`).
"""

from __future__ import annotations

import os
import json
import shutil
import subprocess
from typing import Iterator, Any
from datetime import datetime, timedelta

from sources import make_event


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_welink_ts(val: Any) -> float | None:
    """Parse a welink-cli timestamp to Unix epoch seconds.

    Handles: millis-epoch (int/str, large), seconds-epoch (small int), ISO 8601
    (with/without 'Z' / offset), and YYYY-MM-DD. Returns None if unparseable.
    """
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return val / 1000.0 if val > 1e12 else float(val)
    s = str(val).strip()
    if not s:
        return None
    # Pure-digit → epoch (millis if large, seconds if small)
    if s.isdigit():
        n = int(s)
        return n / 1000.0 if n > 1e12 else float(n)
    # ISO 8601
    try:
        s2 = s[:-1] + "+00:00" if s.endswith("Z") else s
        return datetime.fromisoformat(s2).timestamp()
    except (ValueError, TypeError):
        pass
    # YYYY-MM-DD
    try:
        return datetime.strptime(s, "%Y-%m-%d").timestamp()
    except (ValueError, TypeError):
        return None


def _first_key(d: dict, candidates: list[str]) -> Any:
    """Return the first non-empty value among candidate keys in d."""
    for k in candidates:
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return None


def _looks_like_api_error(stdout: str) -> bool:
    """Detect a welink-cli API error envelope (subprocess exits 0 but the JSON
    body is an error, e.g. {"code":"400","message":{"message":"BAD_REQUEST"}})."""
    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, ValueError, TypeError):
        return False
    if not isinstance(data, dict):
        return False
    code = data.get("code")
    # Success codes seen: 200 (int) and "0" (str). Anything else is an error.
    if code is not None and code not in (200, "0", "200"):
        return True
    # Some envelopes carry an explicit error block
    err = data.get("error") or data.get("Error")
    if isinstance(err, dict):
        ec = err.get("error_code") or err.get("code")
        if ec is not None and ec not in (0, "0", "IM.0000"):
            return True
    return False


def _api_error_msg(stdout: str) -> str:
    """Extract a human-readable message from an API error envelope."""
    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, ValueError, TypeError):
        return stdout[:200]
    if not isinstance(data, dict):
        return stdout[:200]
    msg = data.get("message")
    if isinstance(msg, dict):
        details = msg.get("details")
        if isinstance(details, list) and details:
            return str(details[0])
        return str(msg.get("message", msg))[:200]
    return str(msg or data)[:200]


def _extract_json_list(stdout: str) -> list[dict]:
    """Extract a list of dicts from welink-cli JSON output.

    welink-cli wraps results in various envelopes depending on the command, verified
    against real authenticated responses (2026-07):

      - calendar / mail        → bare JSON array [{"subject":...}, ...]
      - meeting query-list     → {"code":200,"data":{"data":[...]}}
      - im query-recent-conv   → {"conversation_info":[...], "error":{...}}
      - im query-history-msg   → {"respData":{"chatInfo":[...]}, "resultCode":"0"}

    We try: a bare list; a top-level list under any common key; a nested
    {outer: {inner: [...]}}; or a single object. Returns [] if nothing parseable.
    """
    try:
        data = json.loads(stdout)
    except (json.JSONDecodeError, ValueError, TypeError):
        return []
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    if isinstance(data, dict):
        # Top-level list under a common key (covers most envelopes in one pass).
        for key in ("data", "items", "list", "records", "result",
                    "meetings", "events", "mails", "conversations",
                    "conversation_info", "chatInfo", "respData", "rows"):
            v = data.get(key)
            if isinstance(v, list):
                return [d for d in v if isinstance(d, dict)]
            if isinstance(v, dict):
                # Nested envelope: {outer: {inner: [...]}}
                for k2 in ("records", "list", "items", "data", "result",
                           "rows", "chatInfo", "conversation_info", "data"):
                    v2 = v.get(k2)
                    if isinstance(v2, list):
                        return [d for d in v2 if isinstance(d, dict)]
        # Maybe a single object (e.g. one meeting detail)
        if any(k in data for k in ("subject", "Subject", "meetingId", "ItemId", "itemId")):
            return [data]
    return []


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

MAX_PAGES = 40          # cap pagination across all commands
DEFAULT_LOOKBACK_DAYS = 90
IM_MAX_CONVERSATIONS = 50
IM_MESSAGES_PER_CONVERSATION = 20


class WeLinkCLIAdapter:
    """Adapter for WeLink CLI — meetings, calendar, mail, and IM.

    One tool, four data domains. `detect()` checks the binary is in PATH; `collect()`
    shells out to each subcommand with `--format json` and parses defensively. If
    welink-cli is installed but not authenticated, every subcommand returns non-zero
    and we yield nothing — the per-run report shows the source as detected, and a
    colleague seeing 0 events knows to run `welink-cli auth login`.

    `lookback_days` caps how far back we fetch (default 90, matching the git adapter).
    `collect_since(watermark)` starts from the watermark but never earlier than the
    lookback cap.
    """

    name = "welink_cli"
    # Primary category is meeting (the highest-value domain + the duration signal).
    # Per-event source_kind varies: meetings/calendar → "meeting", mail/IM → "comm".
    source_kind = "meeting"

    def __init__(self, lookback_days: int = DEFAULT_LOOKBACK_DAYS,
                 binary: str | None = None, enable_im: bool = False):
        self._lookback_days = lookback_days
        self._binary = binary or shutil.which("welink-cli") or "welink-cli"
        self._enable_im = enable_im

    # -- detection ----------------------------------------------------------

    def detect(self) -> bool:
        """True if welink-cli is in PATH."""
        return shutil.which("welink-cli") is not None

    # -- subprocess helper --------------------------------------------------

    def _run(self, args: list[str], timeout: int = 60) -> str | None:
        """Run `welink-cli <args>`, return stdout or None on any failure."""
        try:
            result = subprocess.run(
                [self._binary] + args,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return None
        if result.returncode != 0:
            return None
        return result.stdout

    def _run_json(self, args: list[str], timeout: int = 60) -> list[dict]:
        """Run a command and return parsed JSON list of dicts ([] on failure)."""
        out = self._run(args, timeout=timeout)
        if out is None:
            return []
        items = _extract_json_list(out)
        if items:
            return items
        # No items extracted — could be a legitimate empty result OR an API error
        # envelope (e.g. {"code":"400","message":{...}}) that exits 0 but isn't data.
        # Detect the latter so callers can distinguish "no meetings" from "request
        # rejected"; here we just return [] (silent skip), but log to stderr for
        # debuggability.
        if _looks_like_api_error(out):
            import sys as _sys
            _msg = _api_error_msg(out)
            _sys.stderr.write(
                f"[welink_cli] {args[0]} request returned an error: {_msg}\n")
        return []

    # -- time window --------------------------------------------------------

    def _window(self, watermark: float | None) -> tuple[datetime, datetime]:
        """Return (start, end) datetimes for this collection.

        start = max(watermark, now - lookback_days); end = now.
        """
        now = datetime.now()
        start = now - timedelta(days=self._lookback_days)
        if watermark is not None:
            wm_dt = datetime.fromtimestamp(watermark)
            if wm_dt > start:
                start = wm_dt
        return start, now

    # -- collection: meetings ----------------------------------------------

    def _collect_meetings(self, start_dt: datetime, now: datetime) -> Iterator[dict]:
        """Query ended/all meetings with start/end millis → meeting events.

        `meeting query-list` returns meetings with start_time + end_time (millis),
        giving us direct meeting DURATION — the signal SKILL.md ranked as the top gap.
        type=4 (all); the time window excludes future meetings. Paginated.
        """
        start_ms = int(start_dt.timestamp() * 1000)
        end_ms = int(now.timestamp() * 1000)
        page = 1
        size = 30  # API max is 30 ("size不能超过30"); larger values return HTTP 400.
        while page <= MAX_PAGES:
            # meeting has no --format flag (only mail/calendar do); JSON is default.
            items = self._run_json([
                "meeting", "query-list",
                "--meeting-start-time", str(start_ms),
                "--meeting-end-time", str(end_ms),
                "--type", "4",
                "--meeting-sort", "asc",
                "--page", str(page),
                "--size", str(size),
            ], timeout=90)
            if not items:
                return
            for m in items:
                ev = self._meeting_to_event(m)
                if ev:
                    yield ev
            if len(items) < size:
                return  # last page
            page += 1

    def _meeting_to_event(self, m: dict) -> dict | None:
        subject = _first_key(m, ["subject", "Subject", "meetingSubject",
                                 "title", "name"]) or "(no subject)"
        # Real API uses meetingStartTime/meetingEndTime (millis, can be null for
        # some records), with estimatedStartTime/estimatedEndTime (millis strings,
        # always present) as a reliable fallback.
        start_val = _first_key(m, ["meetingStartTime", "startTime", "start_time",
                                   "estimatedStartTime", "beginTime", "Start", "start"])
        end_val = _first_key(m, ["meetingEndTime", "endTime", "end_time",
                                 "estimatedEndTime", "finishTime", "End", "end"])
        ts = _parse_welink_ts(start_val)
        if ts is None:
            return None
        end_ts = _parse_welink_ts(end_val)
        duration = (end_ts - ts) if (end_ts and end_ts > ts) else None
        meeting_id = _first_key(m, ["meetingId", "meeting_id", "id", "Id"])
        organizer = _first_key(m, ["organizer", "Organizer", "scheduler",
                                   "creator", "booker"])
        attendees = _first_key(m, ["meetingUserList", "attendees", "members",
                                   "participants"])
        location = _first_key(m, ["location", "Location"])
        return make_event(
            source="welink_cli",
            source_kind="meeting",
            session_id=str(meeting_id) if meeting_id else None,
            cwd=None,
            git_branch=None,
            timestamp=ts,
            timestamp_raw=str(start_val),
            kind="meeting",
            text=str(subject),
            tool_input={
                "domain": "meeting",
                "meeting_id": meeting_id,
                "subject": subject,
                "start": start_val,
                "end": end_val,
                "duration_seconds": duration,
                "organizer": organizer,
                "attendees": attendees,
                "location": location,
            },
            extra={"end_ts": end_ts, "duration_seconds": duration},
        )

    # -- collection: calendar ----------------------------------------------

    def _collect_calendar(self, start_dt: datetime, now: datetime) -> Iterator[dict]:
        """Query calendar events → meeting events (scheduled, with duration).

        `calendar list --start YYYY-MM-DD --end YYYY-MM-DD` (end is EXCLUSIVE, so we
        pass tomorrow to include today). Returns Subject/Start/End/Location/Status.
        Overlaps with meeting query-list but covers non-WeLink calendar entries too.
        """
        start_date = start_dt.strftime("%Y-%m-%d")
        # end is exclusive → add 1 day to include today
        end_date = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        items = self._run_json([
            "calendar", "--format", "json", "list",
            "--start", start_date,
            "--end", end_date,
            "--max", "500",
        ], timeout=60)
        for ev in items:
            mapped = self._calendar_to_event(ev)
            if mapped:
                yield mapped

    def _calendar_to_event(self, c: dict) -> dict | None:
        subject = _first_key(c, ["subject", "Subject", "title", "Title"]) or "(no title)"
        start_val = _first_key(c, ["start", "Start", "startTime", "begin"])
        end_val = _first_key(c, ["end", "End", "endTime", "finish"])
        ts = _parse_welink_ts(start_val)
        if ts is None:
            return None
        end_ts = _parse_welink_ts(end_val)
        duration = (end_ts - ts) if (end_ts and end_ts > ts) else None
        item_id = _first_key(c, ["itemId", "ItemId", "id", "Id"])
        location = _first_key(c, ["location", "Location"])
        # Real API field is legacyFreeBusyStatus (Free/Tentative/Busy/OOF)
        status = _first_key(c, ["legacyFreeBusyStatus", "Status", "status",
                                "freeBusy", "showAs"])
        organizer = _first_key(c, ["organizer", "Organizer"])
        organizer_email = _first_key(c, ["organizerEmail", "organizer_email"])
        is_all_day = _first_key(c, ["isAllDay", "allDay"])
        is_cancelled = _first_key(c, ["isCancelled", "cancelled"])
        return make_event(
            source="welink_cli",
            source_kind="meeting",
            session_id=str(item_id) if item_id else None,
            cwd=None,
            git_branch=None,
            timestamp=ts,
            timestamp_raw=str(start_val),
            kind="meeting",
            text=str(subject),
            tool_input={
                "domain": "calendar",
                "item_id": item_id,
                "subject": subject,
                "start": start_val,
                "end": end_val,
                "duration_seconds": duration,
                "location": location,
                "status": status,
                "organizer": organizer,
                "organizer_email": organizer_email,
                "is_all_day": is_all_day,
                "is_cancelled": is_cancelled,
            },
            extra={"end_ts": end_ts, "duration_seconds": duration},
        )

    # -- collection: mail ---------------------------------------------------

    def _collect_mail(self, start_dt: datetime, now: datetime) -> Iterator[dict]:
        """Query received + sent mail → email events.

        `mail list --start --end` (end exclusive). We query both inbox (received)
        and sentitems (sent) to capture both directions. Each email = a communication
        task instance; duration is weak but occurrence + subject feeds reconstruction.
        """
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        for folder, folder_id, direction in [
            ("inbox", "inbox", "received"),
            ("sent", "sentitems", "sent"),
        ]:
            items = self._run_json([
                "mail", "--format", "json", "list",
                "--folder-id", folder_id,
                "--start", start_date,
                "--end", end_date,
                "--max", "500",
            ], timeout=60)
            for m in items:
                ev = self._mail_to_event(m, folder, direction)
                if ev:
                    yield ev

    def _mail_to_event(self, m: dict, folder: str, direction: str) -> dict | None:
        subject = _first_key(m, ["Subject", "subject", "title"]) or "(no subject)"
        # Real API field is dateTimeReceived (ISO 8601 +08:00); sentitems uses the
        # same field for the sent timestamp.
        date_val = _first_key(m, ["dateTimeReceived", "Date", "date", "received",
                                  "receivedTime", "sentTime", "dateTimeSent", "time"])
        ts = _parse_welink_ts(date_val)
        if ts is None:
            return None
        item_id = _first_key(m, ["ItemId", "itemId", "id", "Id"])
        sender = _first_key(m, ["from", "From", "sender", "Sender"])
        sender_email = _first_key(m, ["fromEmail", "from_email", "senderEmail"])
        is_read = _first_key(m, ["isRead", "Read", "read"])
        has_attachments = _first_key(m, ["hasAttachments", "HasAttachments",
                                         "attachments"])
        preview = _first_key(m, ["preview", "Preview"])
        return make_event(
            source="welink_cli",
            source_kind="comm",
            session_id=str(item_id) if item_id else None,
            cwd=None,
            git_branch=None,
            timestamp=ts,
            timestamp_raw=str(date_val),
            kind="email",
            text=str(subject),
            tool_input={
                "domain": "mail",
                "folder": folder,
                "direction": direction,
                "item_id": item_id,
                "subject": subject,
                "from": sender,
                "from_email": sender_email,
                "date": date_val,
                "is_read": is_read,
                "has_attachments": has_attachments,
                "preview": str(preview)[:200] if preview else None,
            },
        )

    # -- collection: IM -----------------------------------------------------

    def _collect_im(self, start_dt: datetime, now: datetime) -> Iterator[dict]:
        """Query recent conversations → chat_message events.

        Two-step: `im query-recent-conversation` enumerates conversations, then
        `im query-history-message` fetches recent messages per conversation. IM has
        no time-range filter (paginated by message-id), so we fetch recent messages
        and filter by timestamp post-hoc. Chat duration is weak but the occurrence
        signal fills gaps between coding sessions.

        Real API shapes (verified 2026-07):
          - conversations: {"conversation_info":[{group_id, group_name, group_type,
            recent_conversation_type, target_account, staff_name}, ...]}
          - messages: {"respData":{"chatInfo":[{content, contentType, msgId, sender,
            serverSendTime, groupId, groupType}, ...]}}
          - group_type: "DISCUSS_GROUP" | "NORMAL_GROUP"; DMs have target_account set
            and recent_conversation_type "CHAT_TYPE_P2P_MSG".

        Capped at IM_MAX_CONVERSATIONS × IM_MESSAGES_PER_CONVERSATION to bound cost.
        Disabled by default (enable_im=False) — IM is the lowest-ranked signal (SKILL.md)
        AND the slowest to collect (N+1 subprocess calls: one per conversation). The
        high-value domains (meetings w/ duration, calendar, mail) run by default; opt
        into IM explicitly via WeLinkCLIAdapter(enable_im=True) when chat gaps matter.
        """
        if not self._enable_im:
            return
        start_ts = start_dt.timestamp()
        # Step 1: recent conversations (im has no --format flag; JSON is default)
        convs = self._run_json([
            "im", "query-recent-conversation",
            "--count", str(IM_MAX_CONVERSATIONS),
        ], timeout=60)
        for conv in convs[:IM_MAX_CONVERSATIONS]:
            group_id = _first_key(conv, ["group_id", "groupId", "id", "Id"])
            group_name = _first_key(conv, ["group_name", "groupName", "name", "Name"])
            conv_type = _first_key(conv, ["recent_conversation_type",
                                          "conversation_type", "type"])
            target_account = _first_key(conv, ["target_account", "targetAccount",
                                               "staff_name", "staffName"])
            # A group chat has a group_id and CHAT_TYPE_GROUP_MSG; a P2P chat has a
            # target_account and CHAT_TYPE_P2P_MSG.
            is_group = bool(group_id) and conv_type != "CHAT_TYPE_P2P_MSG"

            # Step 2: fetch recent messages for this conversation
            msg_args = ["im", "query-history-message",
                        "--query-count", str(IM_MESSAGES_PER_CONVERSATION)]
            if is_group:
                if group_id:
                    msg_args += ["--group-id", str(group_id)]
                else:
                    continue
            else:
                # P2P: use target_account (the peer's account)
                if target_account:
                    msg_args += ["--user-account", str(target_account)]
                else:
                    continue
            messages = self._run_json(msg_args, timeout=60)
            for msg in messages:
                ev = self._im_to_event(msg, group_id, group_name, is_group)
                if ev and ev["timestamp"] >= start_ts:
                    yield ev

    def _im_to_event(self, msg: dict, conv_id: Any, conv_name: Any,
                     is_group: bool) -> dict | None:
        # Real API fields: serverSendTime (millis), sender, content, contentType, msgId
        ts_val = _first_key(msg, ["serverSendTime", "createTime", "create_time",
                                  "sendTime", "sentTime", "timestamp", "time"])
        ts = _parse_welink_ts(ts_val)
        if ts is None:
            return None
        sender = _first_key(msg, ["sender", "Sender", "from", "From",
                                  "senderAccount", "sender_account"])
        msg_id = _first_key(msg, ["msgId", "messageId", "message_id", "id", "Id"])
        content_type = _first_key(msg, ["contentType", "content_type", "type"])
        raw_content = _first_key(msg, ["content", "Content", "text", "Text",
                                       "body", "Body", "message", "msg"])
        # CARD_MSG content is itself a JSON string; extract readable text if possible.
        text = self._extract_im_text(raw_content, content_type)
        return make_event(
            source="welink_cli",
            source_kind="comm",
            session_id=str(conv_id) if conv_id else None,
            cwd=None,
            git_branch=None,
            timestamp=ts,
            timestamp_raw=str(ts_val),
            kind="chat_message",
            text=text,
            tool_input={
                "domain": "im",
                "conversation_id": conv_id,
                "conversation_name": conv_name,
                "is_group": is_group,
                "message_id": msg_id,
                "sender": sender,
                "content_type": content_type,
                "content": str(raw_content)[:500] if raw_content else None,
            },
        )

    def _extract_im_text(self, raw_content: Any, content_type: Any) -> str:
        """Extract a readable text snippet from an IM message body.

        TEXT_MSG: content is the literal text. CARD_MSG: content is a JSON string
        encoding a card (mergeMessage / file share / etc.) — we try to pull the
        inner msg fields; if that fails, fall back to the contentType label.
        """
        if not raw_content:
            return "(message)"
        s = str(raw_content)
        ct = str(content_type or "")
        if ct != "CARD_MSG":
            return s[:200]
        # CARD_MSG: content is a JSON string. Try to extract embedded text.
        try:
            card = json.loads(s)
        except (json.JSONDecodeError, ValueError, TypeError):
            return s[:200]
        # mergeMessage.cardContext.mergeMessage.messageList[].msg — file-share cards
        try:
            ctx = card.get("cardContext", {})
            merge = ctx.get("mergeMessage", {})
            msgs = merge.get("messageList", [])
            if msgs:
                parts = []
                for mm in msgs:
                    m = mm.get("msg", "")
                    name = mm.get("name", "")
                    if m:
                        parts.append(f"[{name}] {m}" if name else m)
                if parts:
                    return " | ".join(parts)[:200]
        except (AttributeError, TypeError):
            pass
        return f"({ct})"

    # -- top-level collect --------------------------------------------------

    def collect(self) -> Iterator[dict]:
        start_dt, now = self._window(watermark=None)
        yield from self._collect_meetings(start_dt, now)
        yield from self._collect_calendar(start_dt, now)
        yield from self._collect_mail(start_dt, now)
        yield from self._collect_im(start_dt, now)

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        if watermark is None:
            yield from self.collect()
            return
        start_dt, now = self._window(watermark=watermark)
        yield from self._collect_meetings(start_dt, now)
        yield from self._collect_calendar(start_dt, now)
        yield from self._collect_mail(start_dt, now)
        yield from self._collect_im(start_dt, now)
