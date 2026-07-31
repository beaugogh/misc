"""Tests pinning the current behavior of the MVP pipeline.

Run with: python -m unittest discover -s scripts/tests

These tests exist to pin behavior BEFORE the Phase 0b.2/0b.3 refactor (adapter registry,
unified event schema). The refactor must keep these passing — if one breaks, that's a
behavior change to investigate, not a test to update.

Fixtures are synthetic JSONL session transcripts that exercise the boundary heuristics
and explicit-task scoping without depending on the author's real data.
"""

import unittest
import os
import sys
import json
import tempfile
import shutil

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from claude_code_adapter import parse_session, collect_events
from segment_tasks import segment, segment_explicit, segment_implicit
from aggregate import aggregate, classify_task, render_report


def _line(typ, role=None, content=None, ts="2026-07-01T10:00:00.000Z",
          cwd="/proj", git_branch="main", tool_name=None, tool_input=None,
          tool_use_id=None, is_error=None, usage=None, stop_reason=None):
    """Build one JSONL line for a synthetic session."""
    obj = {
        "type": typ,
        "timestamp": ts,
        "cwd": cwd,
        "gitBranch": git_branch,
        "sessionId": "test-session",
    }
    if role is not None or content is not None or usage is not None or stop_reason is not None:
        msg = {"role": role}
        if content is not None:
            msg["content"] = content
        if usage is not None:
            msg["usage"] = usage
        if stop_reason is not None:
            msg["stop_reason"] = stop_reason
        obj["message"] = msg
    if typ == "assistant" and tool_name:
        # tool_use block inside assistant message content
        block = {"type": "tool_use", "name": tool_name, "input": tool_input or {}, "id": tool_use_id or "tu_1"}
        msg = obj.setdefault("message", {"role": "assistant"})
        existing = msg.get("content", [])
        if not isinstance(existing, list):
            existing = []
        existing.append(block)
        msg["content"] = existing
        msg["role"] = "assistant"
    return json.dumps(obj)


def _write_session(lines, dir_path, name="abc123.jsonl"):
    """Write synthetic JSONL lines to a session file under dir_path/<slug>/. Returns the path."""
    slug = "test-proj"
    proj_dir = os.path.join(dir_path, slug)
    os.makedirs(proj_dir, exist_ok=True)
    path = os.path.join(proj_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        for ln in lines:
            f.write(ln + "\n")
    return path


class TestAdapter(unittest.TestCase):
    def test_user_message_vs_tool_result_disambiguation(self):
        """A user message with a tool_result block yields kind=tool_result, not user_message."""
        lines = [
            _line("user", role="user", content=[{"type": "tool_result",
                    "tool_use_id": "tu_1", "content": "ok", "is_error": False}]),
            _line("user", role="user", content="hello there"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            _write_session(lines, tmp)
            events = collect_events(tmp)
            kinds = [e["kind"] for e in events]
            self.assertIn("tool_result", kinds)
            self.assertIn("user_message", kinds)
            # tool_result carries the tool_use_id
            tr = next(e for e in events if e["kind"] == "tool_result")
            self.assertEqual(tr["tool_use_id"], "tu_1")
            self.assertFalse(tr["tool_is_error"])

    def test_tool_use_carries_id_and_input(self):
        lines = [
            _line("assistant", role="assistant", tool_name="Bash",
                  tool_input={"command": "ls"}, tool_use_id="tu_99"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            _write_session(lines, tmp)
            events = collect_events(tmp)
            tu = next(e for e in events if e["kind"] == "tool_use")
            self.assertEqual(tu["tool_name"], "Bash")
            self.assertEqual(tu["tool_use_id"], "tu_99")
            self.assertEqual(tu["tool_input"], {"command": "ls"})

    def test_timestamp_normalization(self):
        lines = [_line("user", role="user", content="hi", ts="2026-07-01T10:00:00.500Z")]
        with tempfile.TemporaryDirectory() as tmp:
            _write_session(lines, tmp)
            events = collect_events(tmp)
            # ISO 8601 -> epoch seconds; 10:00:00.500 UTC on 2026-07-01
            self.assertAlmostEqual(events[0]["timestamp"], 1782900000.5, places=1)

    def test_timestampless_events_kept_by_adapter_dropped_by_segmenter(self):
        """Adapter yields them (kind=mode etc.); segment() filters them out."""
        lines = [
            _line("mode", ts=None),
            _line("user", role="user", content="hi"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            _write_session(lines, tmp)
            events = collect_events(tmp)
            # adapter keeps both
            self.assertEqual(len(events), 2)
            tasks = segment(events)
            # segmenter drops the timestampless one — at least one task with the user msg
            self.assertTrue(all(t.get("start") and t["start"] > 0 for t in tasks))


class TestSegmentation(unittest.TestCase):
    def _session_events(self, lines):
        with tempfile.TemporaryDirectory() as tmp:
            _write_session(lines, tmp)
            return collect_events(tmp)

    def test_explicit_task_completed_status(self):
        """TaskCreate ... TaskUpdate(completed) yields one explicit task, status=completed."""
        lines = [
            _line("assistant", role="assistant", tool_name="TaskCreate",
                  tool_input={"subject": "Do thing", "description": "x"}, ts="2026-07-01T10:00:00Z"),
            _line("user", role="user", content="work work"),
            _line("assistant", role="assistant", content="doing it", ts="2026-07-01T10:05:00Z"),
            _line("assistant", role="assistant", tool_name="TaskUpdate",
                  tool_input={"taskId": "1", "status": "completed"}, ts="2026-07-01T10:10:00Z"),
        ]
        events = self._session_events(lines)
        tasks = segment(events)
        explicit = [t for t in tasks if t["flavor"] == "explicit"]
        self.assertEqual(len(explicit), 1)
        self.assertEqual(explicit[0]["subject"], "Do thing")
        self.assertEqual(explicit[0]["task_status"], "completed")
        self.assertAlmostEqual(explicit[0]["duration_seconds"], 600, places=0)  # 10 min

    def test_explicit_task_unknown_status_when_no_update(self):
        """TaskCreate with no terminal TaskUpdate extends to session end, status=unknown."""
        lines = [
            _line("assistant", role="assistant", tool_name="TaskCreate",
                  tool_input={"subject": "Unterminated"}, ts="2026-07-01T10:00:00Z"),
            _line("user", role="user", content="work", ts="2026-07-01T10:05:00Z"),
        ]
        events = self._session_events(lines)
        tasks = segment(events)
        explicit = [t for t in tasks if t["flavor"] == "explicit"]
        self.assertEqual(len(explicit), 1)
        self.assertEqual(explicit[0]["task_status"], "unknown")
        # extends to last event, not 0-5s
        self.assertGreater(explicit[0]["duration_seconds"], 60)

    def test_implicit_boundary_on_large_gap(self):
        """A >30min gap between consecutive events splits into two implicit tasks."""
        lines = [
            _line("user", role="user", content="first task", ts="2026-07-01T10:00:00Z"),
            _line("assistant", role="assistant", content="ok", ts="2026-07-01T10:01:00Z"),
            # 2-hour gap
            _line("user", role="user", content="second task", ts="2026-07-01T12:00:00Z"),
            _line("assistant", role="assistant", content="ok2", ts="2026-07-01T12:01:00Z"),
        ]
        events = self._session_events(lines)
        tasks = segment(events)
        implicit = [t for t in tasks if t["flavor"] == "implicit"]
        self.assertEqual(len(implicit), 2)
        subjects = [t["subject"] for t in implicit]
        self.assertIn("first task", subjects)
        self.assertIn("second task", subjects)

    def test_implicit_correction_extends_task(self):
        """A correction user message does NOT start a new task."""
        lines = [
            _line("user", role="user", content="do the thing", ts="2026-07-01T10:00:00Z"),
            _line("assistant", role="assistant", content="done", ts="2026-07-01T10:01:00Z"),
            _line("user", role="user", content="no, fix it", ts="2026-07-01T10:02:00Z"),
            _line("assistant", role="assistant", content="fixed", ts="2026-07-01T10:03:00Z"),
        ]
        events = self._session_events(lines)
        tasks = segment(events)
        implicit = [t for t in tasks if t["flavor"] == "implicit"]
        # "no, fix it" is a correction — extends the first task, doesn't split
        self.assertEqual(len(implicit), 1)

    def test_implicit_boundary_on_cwd_shift(self):
        """A user message with a different cwd starts a new task."""
        lines = [
            _line("user", role="user", content="proj A work", ts="2026-07-01T10:00:00Z", cwd="/projA"),
            _line("assistant", role="assistant", content="ok", ts="2026-07-01T10:01:00Z", cwd="/projA"),
            _line("user", role="user", content="proj B work", ts="2026-07-01T10:02:00Z", cwd="/projB"),
            _line("assistant", role="assistant", content="ok2", ts="2026-07-01T10:03:00Z", cwd="/projB"),
        ]
        events = self._session_events(lines)
        tasks = segment(events)
        implicit = [t for t in tasks if t["flavor"] == "implicit"]
        self.assertEqual(len(implicit), 2)

    def test_outputs_capture_write_edit(self):
        """Write/Edit tool calls are captured in task.outputs."""
        lines = [
            _line("user", role="user", content="make a file", ts="2026-07-01T10:00:00Z"),
            _line("assistant", role="assistant", tool_name="Write",
                  tool_input={"file_path": "/proj/out.py", "content": "x"}, ts="2026-07-01T10:01:00Z"),
        ]
        events = self._session_events(lines)
        tasks = segment(events)
        self.assertTrue(any("/proj/out.py" in t["outputs"] for t in tasks))

    def test_error_count_from_tool_result(self):
        """tool_result with is_error=True increments the task's error count."""
        lines = [
            _line("user", role="user", content="try it", ts="2026-07-01T10:00:00Z"),
            _line("assistant", role="assistant", tool_name="Bash",
                  tool_input={"command": "bad"}, tool_use_id="tu_1", ts="2026-07-01T10:00:30Z"),
            _line("user", role="user", content=[{"type": "tool_result",
                    "tool_use_id": "tu_1", "content": "error!", "is_error": True}],
                  ts="2026-07-01T10:00:31Z"),
        ]
        events = self._session_events(lines)
        tasks = segment(events)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["errors"], 1)


class TestAggregation(unittest.TestCase):
    def test_classify_coding_vs_planning(self):
        coding = {"tool_names": ["Edit", "Bash"], "cwd": "/workspace/proj",
                  "subject": "fix bug", "event_count": 10}
        planning = {"tool_names": [], "cwd": "/tmp", "subject": "hi",
                    "event_count": 2}
        self.assertEqual(classify_task(coding), "coding")
        self.assertEqual(classify_task(planning), "planning")

    def test_aggregate_by_day(self):
        tasks = [
            {"start": 1782967200.0, "duration_seconds": 3600, "flavor": "implicit",
             "tool_names": ["Edit"], "cwd": "/p", "subject": "x", "event_count": 5},
            {"start": 1782967200.0 + 7200, "duration_seconds": 1800, "flavor": "implicit",
             "tool_names": [], "cwd": "/p", "subject": "y", "event_count": 2},
        ]
        agg = aggregate(tasks, "day")
        self.assertEqual(len(agg), 1)  # both on same day
        period = list(agg.values())[0]
        self.assertAlmostEqual(period["total_seconds"], 5400)
        self.assertEqual(period["task_count"], 2)
        # both coding (Edit) and planning present
        kinds = set(period["by_kind"].keys())
        self.assertIn("coding", kinds)

    def test_aggregate_week_iso(self):
        """Weekly aggregation uses ISO week keys like 2026-W27."""
        tasks = [
            {"start": 1782967200.0, "duration_seconds": 3600, "flavor": "implicit",
             "tool_names": ["Edit"], "cwd": "/p", "subject": "x", "event_count": 5},
        ]
        agg = aggregate(tasks, "week")
        key = list(agg.keys())[0]
        self.assertRegex(key, r"\d{4}-W\d{2}")

    def test_excised_gap_seconds_reported(self):
        """M2: excised_gap_seconds is accumulated and shown in the report."""
        tasks = [
            {"start": 1782967200.0, "duration_seconds": 7200, "wall_clock_seconds": 7200,
             "active_seconds": 3600, "excised_gap_seconds": 3600,
             "flavor": "implicit", "tool_names": ["Edit"], "cwd": "/p",
             "subject": "x", "event_count": 5},
        ]
        agg = aggregate(tasks, "day")
        period = list(agg.values())[0]
        # excised_gap_seconds accumulated at period level
        self.assertAlmostEqual(period["excised_gap_seconds"], 3600.0)
        # excised_gap_seconds accumulated at kind level
        coding = period["by_kind"]["coding"]
        self.assertAlmostEqual(coding["excised_gap_seconds"], 3600.0)
        # render_report shows the excised time
        report = render_report(agg, "day")
        self.assertIn("excised", report)


class TestWeLinkCLIAdapter(unittest.TestCase):
    """Tests for the welink-cli adapter's timestamp parsing, JSON-envelope
    extraction, and event construction — without needing welink-cli installed.

    These pin the parsing contract so that when a colleague runs it against a real
    authenticated instance, the field-name guesses and envelope shapes are at least
    covered. detect() is also pinned to the binary-in-PATH check.
    """

    def setUp(self):
        from welink_cli_adapter import _parse_welink_ts, _extract_json_list, WeLinkCLIAdapter
        self._parse = _parse_welink_ts
        self._extract = _extract_json_list
        self.Adapter = WeLinkCLIAdapter

    def test_detect_false_when_not_installed(self):
        """detect() returns False when welink-cli is absent from PATH."""
        # On the author's machine welink-cli is not installed; if it IS installed
        # in some CI env this test is skipped rather than failing.
        a = self.Adapter()
        if a.detect():
            self.skipTest("welink-cli installed in this env")
        self.assertFalse(a.detect())

    def test_parse_millis_epoch(self):
        """Millisecond epoch (the format meeting query-list uses) normalizes correctly."""
        # 1767196800000 ms = 2026-01-01 00:00:00 UTC
        self.assertAlmostEqual(self._parse(1767196800000), 1767196800.0)
        # string form too (API may return strings)
        self.assertAlmostEqual(self._parse("1767196800000"), 1767196800.0)

    def test_parse_seconds_epoch(self):
        """Small integers are treated as seconds, not millis."""
        self.assertAlmostEqual(self._parse(1767196800), 1767196800.0)

    def test_parse_iso_z(self):
        """ISO 8601 with Z suffix parses as UTC."""
        ts = self._parse("2026-05-21T10:16:00Z")
        self.assertIsNotNone(ts)
        # 8 hours earlier than the +08:00 version of the same wall-clock time
        ts_offset = self._parse("2026-05-21T10:16:00+08:00")
        self.assertAlmostEqual(ts - ts_offset, 8 * 3600)

    def test_parse_date_only(self):
        """YYYY-MM-DD parses to midnight local."""
        ts = self._parse("2026-05-21")
        self.assertIsNotNone(ts)

    def test_parse_none_and_garbage(self):
        """Unparseable values return None, not raise."""
        self.assertIsNone(self._parse(None))
        self.assertIsNone(self._parse(""))
        self.assertIsNone(self._parse("not-a-date"))

    def test_extract_bare_list(self):
        """A bare JSON array is extracted as a list of dicts."""
        self.assertEqual(len(self._extract('[{"a":1},{"b":2}]')), 2)

    def test_extract_data_envelope(self):
        """{data: [...]} envelope is unwrapped."""
        self.assertEqual(len(self._extract('{"data":[{"a":1}]}')), 1)

    def test_extract_nested_envelope(self):
        """{data: {records: [...]}} nested envelope is unwrapped."""
        self.assertEqual(len(self._extract('{"data":{"records":[{"a":1}]}}')), 1)

    def test_extract_conversation_info_envelope(self):
        """IM conversation envelope {conversation_info:[...]} is unwrapped."""
        self.assertEqual(
            len(self._extract('{"conversation_info":[{"group_id":1}],"error":{}}')), 1)

    def test_extract_respdata_chatinco_envelope(self):
        """IM message envelope {respData:{chatInfo:[...]}} is unwrapped."""
        self.assertEqual(
            len(self._extract('{"respData":{"chatInfo":[{"msgId":1}]},"resultCode":"0"}')), 1)

    def test_extract_garbage_returns_empty(self):
        """Non-JSON or non-list output yields an empty list, not an exception."""
        self.assertEqual(self._extract("not json"), [])
        self.assertEqual(self._extract("{}"), [])

    def test_meeting_event_has_duration(self):
        """A meeting with meetingStartTime + meetingEndTime carries duration_seconds —
        the signal SKILL.md ranked as the top gap. Uses real API field names."""
        a = self.Adapter()
        m = {
            "meetingId": 184531461,
            "subject": "代码QC",
            "meetingStartTime": 1778378400000,   # millis (real field name)
            "meetingEndTime": 1778382000000,      # millis — 1 hour later
            "location": "会议室A",
        }
        ev = a._meeting_to_event(m)
        self.assertIsNotNone(ev)
        self.assertEqual(ev["source"], "welink_cli")
        self.assertEqual(ev["source_kind"], "meeting")
        self.assertEqual(ev["kind"], "meeting")
        self.assertEqual(ev["text"], "代码QC")
        self.assertAlmostEqual(ev["extra"]["duration_seconds"], 3600.0)
        self.assertEqual(ev["session_id"], "184531461")

    def test_meeting_falls_back_to_estimated_times(self):
        """When meetingStartTime/EndTime are null, fall back to estimated* fields."""
        a = self.Adapter()
        m = {
            "meetingId": 182255959,
            "subject": "standup",
            "meetingStartTime": None,      # null in real data for some records
            "meetingEndTime": None,
            "estimatedStartTime": "1751525100000",  # string millis (always present)
            "estimatedEndTime": "1751528700000",
        }
        ev = a._meeting_to_event(m)
        self.assertIsNotNone(ev)
        self.assertAlmostEqual(ev["extra"]["duration_seconds"], 3600.0)
        self.assertEqual(ev["session_id"], "182255959")

    def test_mail_event_is_comm_kind(self):
        """An email event has source_kind=comm, not meeting. Uses real API field
        names (dateTimeReceived, from, fromEmail, isRead, itemId)."""
        a = self.Adapter()
        m = {
            "itemId": "AAMkADQ3...",
            "subject": "周报",
            "from": "zhang",
            "fromEmail": "zhang@example.com",
            "dateTimeReceived": "2026-05-08T09:30:00+08:00",
            "isRead": True,
            "hasAttachments": False,
        }
        ev = a._mail_to_event(m, "inbox", "received")
        self.assertIsNotNone(ev)
        self.assertEqual(ev["source_kind"], "comm")
        self.assertEqual(ev["kind"], "email")
        self.assertEqual(ev["tool_input"]["direction"], "received")
        self.assertEqual(ev["tool_input"]["from_email"], "zhang@example.com")

    def test_calendar_event_uses_iso_offset(self):
        """A calendar event with ISO +08:00 start/end yields correct duration.
        Real API returns lowercase start/end with timezone offset."""
        a = self.Adapter()
        c = {
            "itemId": "AAMk...",
            "subject": "站会",
            "start": "2026-07-22T17:00:00+08:00",
            "end": "2026-07-22T18:00:00+08:00",
            "legacyFreeBusyStatus": "Busy",
            "organizer": "liuyuyang (A)",
        }
        ev = a._calendar_to_event(c)
        self.assertIsNotNone(ev)
        self.assertEqual(ev["text"], "站会")
        self.assertAlmostEqual(ev["extra"]["duration_seconds"], 3600.0)
        self.assertEqual(ev["tool_input"]["status"], "Busy")

    def test_im_text_msg_extraction(self):
        """A TEXT_MSG IM message yields its literal content as text."""
        a = self.Adapter()
        msg = {
            "msgId": 89248477104684005,
            "sender": "l00938763",
            "serverSendTime": 1784969542093,
            "contentType": "TEXT_MSG",
            "content": "/GO/GO",
            "groupId": 986792167567683967,
        }
        ev = a._im_to_event(msg, "986792167567683967", "test group", True)
        self.assertIsNotNone(ev)
        self.assertEqual(ev["kind"], "chat_message")
        self.assertEqual(ev["text"], "/GO/GO")
        self.assertAlmostEqual(ev["timestamp"], 1784969542.093)

    def test_im_card_msg_extraction(self):
        """A CARD_MSG IM message (file-share) extracts readable text, not raw JSON."""
        a = self.Adapter()
        # Real CARD_MSG content is a JSON string with a mergeMessage.messageList
        card_content = '{"cardContext":{"mergeMessage":{"messageList":[{"msg":"file.pptx","name":"吴鼎晟","time":1784972373398}]}}}'
        msg = {
            "msgId": 89248726283801104,
            "sender": "l00938763",
            "serverSendTime": 1784974525676,
            "contentType": "CARD_MSG",
            "content": card_content,
        }
        ev = a._im_to_event(msg, "g1", "group", True)
        self.assertIsNotNone(ev)
        # text should contain the extracted file name, not raw JSON
        self.assertIn("file.pptx", ev["text"])
        self.assertNotIn("{", ev["text"])

    def test_unparseable_meeting_skipped(self):
        """A meeting with no parseable start time is skipped (None), not raised."""
        a = self.Adapter()
        self.assertIsNone(a._meeting_to_event({"subject": "no times"}))
        self.assertIsNone(a._meeting_to_event({"meetingStartTime": "garbage"}))


class TestContextExtraction(unittest.TestCase):
    """Tests for _extract_context — the 'why this took so long' signal layer.

    Verifies that meeting, browser, and coding (ai_session) events produce
    structured context dicts that the report can surface inline.
    """

    def test_context_extracted_for_meeting(self):
        """Meeting events populate organizer, attendee count/names, location."""
        from segment_tasks import _extract_context
        events = [{"kind": "meeting", "text": "站会",
                   "tool_input": {"organizer": "zhang",
                                   "attendees": [{"name": "a"}, {"name": "b"}],
                                   "location": "room1", "subject": "站会"}}]
        ctx = _extract_context(events, "meeting")
        self.assertEqual(ctx["organizer"], "zhang")
        self.assertEqual(ctx["attendees"], 2)
        self.assertEqual(ctx["attendee_names"], ["a", "b"])
        self.assertEqual(ctx["location"], "room1")

    def test_context_meeting_attendee_count_from_int(self):
        """Attendee count handles int/str/list shapes from different adapters."""
        from segment_tasks import _extract_context
        events = [{"kind": "meeting", "text": "m",
                   "tool_input": {"attendees": 5}}]
        ctx = _extract_context(events, "meeting")
        self.assertEqual(ctx["attendees"], 5)

    def test_context_extracted_for_browser(self):
        """Browser events populate queries, titles, urls, downloads, visit count."""
        from segment_tasks import _extract_context
        events = [
            {"kind": "search", "text": "pelt penalty", "tool_input": {"query": "pelt penalty"}},
            {"kind": "visit", "text": "docs", "tool_input": {"url": "http://docs", "title": "docs"}},
            {"kind": "visit", "text": "so", "tool_input": {"url": "http://so", "title": "so"}},
            {"kind": "download", "text": "f.pdf", "tool_input": {"target_path": "C:/f.pdf"}},
        ]
        ctx = _extract_context(events, "browser")
        self.assertEqual(ctx["queries"], ["pelt penalty"])
        self.assertEqual(ctx["top_titles"], ["docs", "so"])
        self.assertEqual(ctx["downloads"], 1)
        self.assertEqual(ctx["n_visits"], 2)

    def test_context_blocker_from_errors(self):
        """Coding events with errors produce a synthesized blocker + error samples."""
        from segment_tasks import _extract_context
        events = [
            {"kind": "tool_use", "tool_name": "Bash", "tool_input": {"command": "git fetch"}},
            {"kind": "tool_result", "tool_is_error": True,
             "text": "fatal: CONNECT tunnel failed, response 407"},
            {"kind": "tool_result", "tool_is_error": True,
             "text": "fatal: CONNECT tunnel failed, response 407"},
            {"kind": "tool_use", "tool_name": "Edit", "tool_input": {"file_path": "D:/p/run.py"}},
        ]
        ctx = _extract_context(events, "ai_session")
        self.assertIn("407", ctx["blocker"])
        self.assertTrue(len(ctx["error_samples"]) >= 1)
        self.assertIn("run.py", ctx["files_touched"][0])

    def test_context_retry_targets_detected(self):
        """Same tool+target called 2+× produces a retry_target entry."""
        from segment_tasks import _extract_context
        events = [
            {"kind": "tool_use", "tool_name": "Bash", "tool_input": {"command": "git fetch"}},
            {"kind": "tool_use", "tool_name": "Bash", "tool_input": {"command": "git fetch"}},
            {"kind": "tool_use", "tool_name": "Bash", "tool_input": {"command": "git fetch"}},
        ]
        ctx = _extract_context(events, "ai_session")
        self.assertTrue(len(ctx["retry_targets"]) >= 1)
        self.assertIn("Bash", ctx["retry_targets"][0])

    def test_context_empty_when_no_events(self):
        """No events → empty context (meeting returns {}, ai_session returns empty lists)."""
        from segment_tasks import _extract_context
        # Meeting with no events → no meeting event found → {}
        self.assertEqual(_extract_context([], "meeting"), {})
        # ai_session with no events → populated keys but all empty/None
        ctx = _extract_context([], "ai_session")
        self.assertIsNone(ctx.get("blocker"))
        self.assertEqual(ctx.get("error_samples"), [])
        self.assertEqual(ctx.get("files_touched"), [])

    def test_context_comm_has_reply_flag(self):
        """Email events set has_reply when both received and sent directions present."""
        from segment_tasks import _extract_context
        events = [
            {"kind": "email", "text": "re: x",
             "tool_input": {"subject": "re: x", "from": "a@b", "direction": "received"}},
            {"kind": "email", "text": "x",
             "tool_input": {"subject": "x", "from": "me", "direction": "sent"}},
        ]
        ctx = _extract_context(events, "comm")
        self.assertTrue(ctx["has_reply"])

    def test_inputs_includes_non_tool_events(self):
        """_extract_inputs now captures meeting/visit/search/email events, not just tool_use."""
        from segment_tasks import _extract_inputs
        events = [
            {"kind": "meeting", "text": "standup",
             "tool_input": {"subject": "standup", "organizer": "zhang"}},
            {"kind": "visit", "text": "docs",
             "tool_input": {"url": "http://docs", "title": "docs"}},
            {"kind": "search", "text": "query1", "tool_input": {"query": "query1"}},
        ]
        inputs = _extract_inputs(events)
        texts = " ".join(inputs)
        self.assertIn("meeting:", texts)
        self.assertIn("visit:", texts)
        self.assertIn("search:", texts)

    def test_make_task_has_context_field(self):
        """_make_task populates task['context'] for every source_kind."""
        from segment_tasks import _make_task
        events = [{"kind": "meeting", "text": "m", "timestamp": 1000.0,
                   "source_kind": "meeting",
                   "tool_input": {"organizer": "x", "attendees": 3}}]
        task = _make_task("t1", "implicit", events, None)
        self.assertIn("context", task)
        self.assertEqual(task["context"]["organizer"], "x")


if __name__ == "__main__":
    unittest.main()
