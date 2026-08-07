"""Tests for segmentation fixes: PELT 0-boundary fallback and P2P session_id.

Covers two bugs fixed in v1.0.14:
1. PELT returning 0 boundaries for comm data with large gaps — now falls back
   to naive gap boundaries.
2. P2P WeLink chats getting session_id=None because group_id is None for P2P —
   now uses target_account as conv_id.
"""

import unittest
import sys
import os

# Ensure scripts dir is on path for imports
_scripts = os.path.join(os.path.dirname(__file__), "..")
if _scripts not in sys.path:
    sys.path.insert(0, _scripts)


def _make_event(ts, kind="chat_message", session_id=None, text="", cwd=None):
    return {
        "timestamp": ts,
        "kind": kind,
        "session_id": session_id,
        "text": text,
        "cwd": cwd,
        "tool_input": {},
    }


# ---------------------------------------------------------------------------
# PELT 0-boundary fallback
# ---------------------------------------------------------------------------

class TestPeltFallbackToNaive(unittest.TestCase):
    """When PELT returns 0 boundaries but data has gaps, fall back to naive."""

    def test_pelt_zero_boundaries_with_gaps_falls_back(self):
        """Simulate comm-like data: many events with large gaps that PELT misses."""
        from advanced_segment import segment_implicit_advanced

        # 30 events with 2-hour gaps — PELT may return 0 boundaries for this pattern
        events = []
        for i in range(30):
            events.append(_make_event(
                ts=1000000 + i * 7200,  # 2h apart
                kind="chat_message",
                text=f"message {i}",
            ))

        counter = [0]
        tasks = segment_implicit_advanced(events, counter)

        # Should produce multiple tasks, not 1 giant blob
        self.assertGreater(len(tasks), 1, "PELT 0-boundary should fall back to naive gaps")

    def test_pelt_zero_boundaries_with_no_gaps_stays_one_task(self):
        """If there are no gaps, 0 boundaries is correct — no fallback needed."""
        from advanced_segment import segment_implicit_advanced

        # 30 events, all within 1 minute (no gaps)
        events = []
        for i in range(30):
            events.append(_make_event(
                ts=1000000 + i * 2,  # 2s apart
                kind="chat_message",
                text=f"message {i}",
            ))

        counter = [0]
        tasks = segment_implicit_advanced(events, counter)

        # Should be 1 task (no gaps to split on)
        self.assertEqual(len(tasks), 1)

    def test_real_comm_pattern_splits_correctly(self):
        """Simulate the real bug: 200+ messages spanning days, PELT returns 0."""
        from advanced_segment import segment_implicit_advanced

        events = []
        # Burst 1: 5 messages within 5 min
        for i in range(5):
            events.append(_make_event(ts=1000000 + i * 60, text=f"burst1-{i}"))
        # Gap: 55 hours
        # Burst 2: 5 messages within 5 min
        for i in range(5):
            events.append(_make_event(ts=1000000 + 55 * 3600 + i * 60, text=f"burst2-{i}"))
        # Gap: 100 hours
        # Burst 3: 5 messages within 5 min
        for i in range(5):
            events.append(_make_event(ts=1000000 + 155 * 3600 + i * 60, text=f"burst3-{i}"))
        # Add more events to reach MIN_EVENTS_FOR_PELT (20)
        for i in range(10):
            events.append(_make_event(ts=1000000 + 200 * 3600 + i * 60, text=f"burst4-{i}"))

        events.sort(key=lambda e: e["timestamp"])

        counter = [0]
        tasks = segment_implicit_advanced(events, counter)

        # Should split into at least 3-4 tasks (one per burst)
        self.assertGreaterEqual(len(tasks), 3,
            "Large gaps between bursts must produce separate tasks")


# ---------------------------------------------------------------------------
# P2P session_id
# ---------------------------------------------------------------------------

class TestP2PSessionId(unittest.TestCase):
    """P2P WeLink chats should use target_account as session_id, not None."""

    def test_p2p_uses_target_account_as_conv_id(self):
        """Verify that _collect_im passes target_account as conv_id for P2P."""
        from unittest.mock import MagicMock, patch
        from welink_cli_adapter import WeLinkCLIAdapter

        adapter = WeLinkCLIAdapter(enable_im=True)

        # Mock _run_json to return: 1 P2P conversation, 1 message
        call_count = [0]
        def mock_run_json(args, timeout=60):
            call_count[0] += 1
            if call_count[0] == 1:
                # query-recent-conversation: 1 P2P conversation
                return [{
                    "group_id": None,  # P2P has no group_id
                    "group_name": None,
                    "recent_conversation_type": "CHAT_TYPE_P2P_MSG",
                    "target_account": "w00955441",
                    "staff_name": "Test User",
                }]
            else:
                # query-history-message: 1 message
                return [{
                    "serverSendTime": 1783502035000,  # millis
                    "sender": "w00955441",
                    "content": "test message",
                    "contentType": "TEXT_MSG",
                    "msgId": "msg-1",
                }]

        adapter._run_json = mock_run_json

        import datetime as dt
        start = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
        now = dt.datetime(2026, 8, 1, tzinfo=dt.timezone.utc)
        events = list(adapter._collect_im(start, now))

        self.assertEqual(len(events), 1)
        ev = events[0]
        # session_id should be the target_account, not None
        self.assertEqual(ev["session_id"], "w00955441")
        self.assertEqual(ev["kind"], "chat_message")
        self.assertEqual(ev["tool_input"]["conversation_id"], "w00955441")

    def test_group_chat_uses_group_id_as_conv_id(self):
        """Group chats should still use group_id as session_id."""
        from unittest.mock import MagicMock
        from welink_cli_adapter import WeLinkCLIAdapter

        adapter = WeLinkCLIAdapter(enable_im=True)

        call_count = [0]
        def mock_run_json(args, timeout=60):
            call_count[0] += 1
            if call_count[0] == 1:
                return [{
                    "group_id": "983827495621136639",
                    "group_name": "Test Group",
                    "recent_conversation_type": "CHAT_TYPE_GROUP_MSG",
                    "target_account": None,
                    "staff_name": None,
                }]
            else:
                return [{
                    "serverSendTime": 1783502035000,
                    "sender": "user1",
                    "content": "group message",
                    "contentType": "TEXT_MSG",
                    "msgId": "msg-2",
                }]

        adapter._run_json = mock_run_json

        import datetime as dt
        start = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
        now = dt.datetime(2026, 8, 1, tzinfo=dt.timezone.utc)
        events = list(adapter._collect_im(start, now))

        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertEqual(ev["session_id"], "983827495621136639")
        self.assertEqual(ev["tool_input"]["conversation_name"], "Test Group")

    def test_p2p_messages_from_different_conversations_not_lumped(self):
        """Two P2P chats with different target_accounts should get different session_ids."""
        from welink_cli_adapter import WeLinkCLIAdapter

        adapter = WeLinkCLIAdapter(enable_im=True)

        conv_index = [0]
        conversations = [
            {"group_id": None, "group_name": None,
             "recent_conversation_type": "CHAT_TYPE_P2P_MSG",
             "target_account": "user_a", "staff_name": "User A"},
            {"group_id": None, "group_name": None,
             "recent_conversation_type": "CHAT_TYPE_P2P_MSG",
             "target_account": "user_b", "staff_name": "User B"},
        ]

        def mock_run_json(args, timeout=60):
            if "query-recent-conversation" in args:
                return conversations
            else:
                # query-history-message — return one message per conversation
                conv_index[0] += 1
                return [{
                    "serverSendTime": 1783502035000 + conv_index[0] * 1000,
                    "sender": f"sender_{conv_index[0]}",
                    "content": f"message from conv {conv_index[0]}",
                    "contentType": "TEXT_MSG",
                    "msgId": f"msg-{conv_index[0]}",
                }]

        adapter._run_json = mock_run_json

        import datetime as dt
        start = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
        now = dt.datetime(2026, 8, 1, tzinfo=dt.timezone.utc)
        events = list(adapter._collect_im(start, now))

        self.assertEqual(len(events), 2)
        session_ids = {e["session_id"] for e in events}
        self.assertEqual(len(session_ids), 2, "Two P2P chats should have different session_ids")
        self.assertIn("user_a", session_ids)
        self.assertIn("user_b", session_ids)


# ---------------------------------------------------------------------------
# Sender name resolution
# ---------------------------------------------------------------------------

class TestSenderNameResolution(unittest.TestCase):
    """Test that sender account IDs are resolved to human-readable names."""

    def test_resolve_sender_names_batch(self):
        """_resolve_sender_names calls contact detail and maps account → name."""
        from welink_cli_adapter import WeLinkCLIAdapter

        adapter = WeLinkCLIAdapter(enable_im=True)

        # Mock _run_json to return contact detail response
        def mock_run_json(args, timeout=30):
            if "contact" in args and "detail" in args:
                return {
                    "code": "0",
                    "users": [
                        {"personAccount": "b00563677", "chineseName": "高博", "englishName": "gaobo"},
                        {"personAccount": "c30038754", "chineseName": "崔少攀", "englishName": "cuishaopan"},
                    ]
                }
            return {}
        adapter._run_json = mock_run_json

        events = [
            {"tool_input": {"sender": "b00563677"}},
            {"tool_input": {"sender": "c30038754"}},
            {"tool_input": {"sender": "b00563677"}},  # duplicate
        ]
        name_map = adapter._resolve_sender_names(events)
        self.assertEqual(name_map["b00563677"], "高博")
        self.assertEqual(name_map["c30038754"], "崔少攀")

    def test_resolve_sender_names_empty_events(self):
        """No events → empty mapping, no API call."""
        from welink_cli_adapter import WeLinkCLIAdapter
        adapter = WeLinkCLIAdapter(enable_im=True)
        adapter._run_json = lambda *a, **kw: (_ for _ in ()).throw(AssertionError("should not be called"))
        name_map = adapter._resolve_sender_names([])
        self.assertEqual(name_map, {})

    def test_resolve_sender_names_api_failure(self):
        """If contact API fails, return empty mapping (graceful degradation)."""
        from welink_cli_adapter import WeLinkCLIAdapter
        adapter = WeLinkCLIAdapter(enable_im=True)
        adapter._run_json = lambda *a, **kw: None  # API returns nothing
        events = [{"tool_input": {"sender": "b00563677"}}]
        name_map = adapter._resolve_sender_names(events)
        self.assertEqual(name_map, {})

    def test_collect_im_attaches_sender_name(self):
        """_collect_im resolves names and attaches sender_name to events."""
        from welink_cli_adapter import WeLinkCLIAdapter

        adapter = WeLinkCLIAdapter(enable_im=True)

        call_count = [0]
        def mock_run_json(args, timeout=60):
            call_count[0] += 1
            if call_count[0] == 1:
                # query-recent-conversation
                return [{"group_id": "983827495621136639", "group_name": "Test Group",
                         "recent_conversation_type": "CHAT_TYPE_GROUP_MSG"}]
            elif call_count[0] == 2:
                # query-history-message
                return [{"serverSendTime": 1783502035000, "sender": "b00563677",
                         "content": "hello", "contentType": "TEXT_MSG", "msgId": "m1"}]
            else:
                # contact detail
                return {"users": [{"personAccount": "b00563677", "chineseName": "高博"}]}
        adapter._run_json = mock_run_json

        import datetime as dt
        start = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
        now = dt.datetime(2026, 8, 1, tzinfo=dt.timezone.utc)
        events = list(adapter._collect_im(start, now))

        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertEqual(ev["tool_input"]["sender"], "b00563677")
        self.assertEqual(ev["tool_input"]["sender_name"], "高博")


# ---------------------------------------------------------------------------
# Enriched comm context + narrative
# ---------------------------------------------------------------------------

class TestCommContextEnrichment(unittest.TestCase):
    """Test that comm context includes participants with names and is_group."""

    def test_context_includes_participants_and_is_group(self):
        """The comm context should include im_participants and im_is_group."""
        from segment_tasks import _extract_context

        events = [
            _make_event(ts=1000, kind="chat_message", text="hello",
                        session_id="g1"),
            _make_event(ts=1001, kind="chat_message", text="world",
                        session_id="g1"),
        ]
        # Add tool_input with sender info
        events[0]["tool_input"] = {"sender": "b00563677", "sender_name": "高博",
                                    "conversation_name": "Test Group", "is_group": True}
        events[1]["tool_input"] = {"sender": "c30038754", "sender_name": "崔少攀",
                                    "conversation_name": "Test Group", "is_group": True}

        ctx = _extract_context(events, "comm")
        self.assertTrue(ctx.get("im_message_count", 0) > 0)
        self.assertTrue(ctx.get("im_is_group") is True)
        participants = ctx.get("im_participants", [])
        self.assertEqual(len(participants), 2)
        # Check that names are resolved
        accounts = {p["account"] for p in participants}
        names = {p["name"] for p in participants}
        self.assertIn("b00563677", accounts)
        self.assertIn("高博", names)

    def test_context_p2p_is_group_false(self):
        """P2P chat context should have im_is_group=False."""
        from segment_tasks import _extract_context

        events = [_make_event(ts=1000, kind="chat_message", text="hi")]
        events[0]["tool_input"] = {"sender": "b00563677", "sender_name": "高博",
                                    "conversation_name": "崔少攀", "is_group": False}
        ctx = _extract_context(events, "comm")
        self.assertFalse(ctx.get("im_is_group"))

    def test_context_falls_back_to_account_for_name(self):
        """If sender_name is missing, participant name falls back to account ID."""
        from segment_tasks import _extract_context

        events = [_make_event(ts=1000, kind="chat_message", text="hi")]
        events[0]["tool_input"] = {"sender": "b00563677", "is_group": True}
        ctx = _extract_context(events, "comm")
        participants = ctx.get("im_participants", [])
        self.assertEqual(len(participants), 1)
        self.assertEqual(participants[0]["account"], "b00563677")
        self.assertEqual(participants[0]["name"], "b00563677")  # fallback


class TestCommNarrativeWithNames(unittest.TestCase):
    """Test that _summarize_comm uses names and distinguishes P2P vs group."""

    def test_group_chat_narrative_uses_group_name(self):
        from summarize import _summarize_comm

        task = {
            "source_kind": "comm",
            "active_seconds": 600,
            "context": {
                "im_message_count": 15,
                "im_conversations": ["IT 智能体小分队"],
                "im_senders": ["b00563677", "c30038754"],
                "im_participants": [
                    {"account": "b00563677", "name": "高博"},
                    {"account": "c30038754", "name": "崔少攀"},
                ],
                "im_is_group": True,
            },
        }
        events = [_make_event(ts=1000, kind="chat_message", text="讨论一下Agent评测")]
        narrative = _summarize_comm(events, task)
        self.assertIn("群聊", narrative)
        self.assertIn("IT 智能体小分队", narrative)
        self.assertIn("高博", narrative)
        self.assertIn("崔少攀", narrative)

    def test_p2p_chat_narrative_uses_peer_name(self):
        from summarize import _summarize_comm

        task = {
            "source_kind": "comm",
            "active_seconds": 300,
            "context": {
                "im_message_count": 5,
                "im_conversations": ["崔少攀"],
                "im_senders": ["b00563677", "c30038754"],
                "im_participants": [
                    {"account": "b00563677", "name": "高博"},
                    {"account": "c30038754", "name": "崔少攀"},
                ],
                "im_is_group": False,
            },
        }
        events = [_make_event(ts=1000, kind="chat_message", text="直接帮我退库吧")]
        narrative = _summarize_comm(events, task)
        self.assertIn("私聊", narrative)
        self.assertIn("崔少攀", narrative)

    def test_narrative_falls_back_without_names(self):
        """If no names resolved, narrative still works with account IDs."""
        from summarize import _summarize_comm

        task = {
            "source_kind": "comm",
            "active_seconds": 300,
            "context": {
                "im_message_count": 5,
                "im_conversations": [],
                "im_senders": ["b00563677", "c30038754"],
                "im_participants": [
                    {"account": "b00563677", "name": "b00563677"},
                    {"account": "c30038754", "name": "c30038754"},
                ],
                "im_is_group": True,
            },
        }
        events = [_make_event(ts=1000, kind="chat_message", text="test message here")]
        narrative = _summarize_comm(events, task)
        self.assertIn("b00563677", narrative)
        self.assertIn("c30038754", narrative)


class TestTimelineEnrichment(unittest.TestCase):
    """Test that session record timeline includes kind-specific fields per rubric 12."""

    def _build_entry(self, ev):
        """Replicate the timeline construction logic from run._export_session_records."""
        entry = {
            "timestamp": ev.get("timestamp"),
            "kind": ev.get("kind"),
            "text": (ev.get("text") or "")[:200],
            "tool_name": ev.get("tool_name"),
            "tool_is_error": ev.get("tool_is_error"),
        }
        ti = ev.get("tool_input") or {}
        kind = ev.get("kind")
        if kind == "chat_message":
            entry["sender"] = ti.get("sender")
            entry["sender_name"] = ti.get("sender_name")
            entry["conversation_name"] = ti.get("conversation_name")
            entry["is_group"] = ti.get("is_group")
        elif kind == "email":
            entry["from"] = ti.get("from")
            entry["direction"] = ti.get("direction")
            entry["subject"] = (ti.get("subject") or "")[:120]
        elif kind == "meeting":
            entry["subject"] = (ti.get("subject") or "")[:120]
            entry["organizer"] = ti.get("organizer")
            entry["duration_seconds"] = ti.get("duration_seconds")
        elif kind == "visit":
            entry["url"] = (ti.get("url") or "")[:200]
            entry["visit_count"] = ti.get("visit_count")
        elif kind == "search":
            entry["query"] = (ti.get("query") or "")[:120]
        elif kind == "download":
            entry["target_path"] = (ti.get("target_path") or "")[:200]
            entry["total_bytes"] = ti.get("total_bytes")
        elif kind == "commit":
            entry["hash"] = ti.get("hash")
            entry["files"] = (ti.get("files") or [])[:10]
        elif kind == "branch_checkout":
            entry["from_branch"] = ti.get("from_branch")
            entry["to_branch"] = ti.get("to_branch")
        elif kind == "tool_use":
            entry["tool_use_id"] = ev.get("tool_use_id")
        return entry

    def test_chat_message_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "chat_message", "text": "你走过流程了吧",
            "tool_input": {"sender": "b00563677", "sender_name": "高博",
                           "conversation_name": "崔少攀", "is_group": False},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["sender"], "b00563677")
        self.assertEqual(entry["sender_name"], "高博")
        self.assertFalse(entry["is_group"])

    def test_email_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "email", "text": "Re: 报销",
            "tool_input": {"from": "崔少攀", "direction": "received", "subject": "Re: 报销"},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["from"], "崔少攀")
        self.assertEqual(entry["direction"], "received")
        self.assertEqual(entry["subject"], "Re: 报销")

    def test_meeting_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "meeting", "text": "站会",
            "tool_input": {"subject": "站会", "organizer": "高博", "duration_seconds": 1800},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["subject"], "站会")
        self.assertEqual(entry["organizer"], "高博")
        self.assertEqual(entry["duration_seconds"], 1800)

    def test_visit_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "visit", "text": "Google",
            "tool_input": {"url": "https://google.com/search?q=python", "visit_count": 5},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["url"], "https://google.com/search?q=python")
        self.assertEqual(entry["visit_count"], 5)

    def test_search_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "search", "text": "python logging",
            "tool_input": {"query": "python logging", "url": "https://google.com"},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["query"], "python logging")

    def test_download_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "download", "text": "report.pdf",
            "tool_input": {"target_path": "C:/Downloads/report.pdf", "total_bytes": 1024},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["target_path"], "C:/Downloads/report.pdf")
        self.assertEqual(entry["total_bytes"], 1024)

    def test_commit_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "commit", "text": "fix bug",
            "tool_input": {"hash": "abc123", "files": ["src/main.py", "README.md"]},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["hash"], "abc123")
        self.assertEqual(entry["files"], ["src/main.py", "README.md"])

    def test_branch_checkout_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "branch_checkout", "text": "main -> dev",
            "tool_input": {"from_branch": "main", "to_branch": "dev"},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["from_branch"], "main")
        self.assertEqual(entry["to_branch"], "dev")

    def test_tool_use_timeline_entry(self):
        ev = {
            "timestamp": 1783502035.67, "kind": "tool_use", "text": "Read file",
            "tool_name": "Read", "tool_use_id": "tu_001",
            "tool_input": {"file_path": "src/main.py"},
        }
        entry = self._build_entry(ev)
        self.assertEqual(entry["tool_use_id"], "tu_001")

    def test_unknown_kind_has_base_fields_only(self):
        """Events with unknown kinds still get the base 5 fields."""
        ev = {"timestamp": 1000, "kind": "custom_kind", "text": "something"}
        entry = self._build_entry(ev)
        self.assertEqual(entry["timestamp"], 1000)
        self.assertEqual(entry["kind"], "custom_kind")
        self.assertEqual(entry["text"], "something")
        # No kind-specific enrichment
        self.assertNotIn("sender", entry)
        self.assertNotIn("url", entry)
        self.assertNotIn("hash", entry)


class TestMergeAutomatedFragments(unittest.TestCase):
    """Test the _merge_automated_fragments function."""

    def _task(self, subject, start, end, session_id="ses-1",
              flavor="implicit", involvement="low", active=300):
        return {
            "id": f"implicit-{start}",
            "flavor": flavor,
            "subject": subject,
            "session_id": session_id,
            "start": start,
            "end": end,
            "active_seconds": active,
            "wall_clock_seconds": active,
            "event_count": 5,
            "tool_calls": 0,
            "errors": 0,
            "tool_names": [],
            "human_data": {
                "human_involvement": involvement,
                "human_engaged_seconds": active,
                "human_action_count": 1,
                "machine_autonomous_seconds": 0,
                "is_genuine_time_sink": True,
            },
        }

    def test_merges_same_subject_fragments(self):
        """Multiple fragments with same subject in same session merge into 1."""
        from segment_tasks import _merge_automated_fragments
        tasks = [
            self._task("Report progress", 1000, 1300),
            self._task("Report progress", 1300, 1600),
            self._task("Report progress", 1600, 1900),
        ]
        result = _merge_automated_fragments(tasks)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["start"], 1000)
        self.assertEqual(result[0]["end"], 1900)
        self.assertEqual(result[0]["active_seconds"], 900)
        self.assertEqual(result[0]["_merged_count"], 3)

    def test_does_not_merge_different_subjects(self):
        """Tasks with different subjects are NOT merged."""
        from segment_tasks import _merge_automated_fragments
        tasks = [
            self._task("Report A", 1000, 1300),
            self._task("Report B", 1300, 1600),
            self._task("Report A", 1600, 1900),
        ]
        result = _merge_automated_fragments(tasks)
        # Report A fragments should merge (2 → 1), Report B stays (1)
        # Total: 2 (1 merged Report A + 1 Report B)
        self.assertEqual(len(result), 2)

    def test_does_not_merge_different_sessions(self):
        """Tasks from different sessions are NOT merged."""
        from segment_tasks import _merge_automated_fragments
        tasks = [
            self._task("Report", 1000, 1300, session_id="ses-1"),
            self._task("Report", 1300, 1600, session_id="ses-2"),
        ]
        result = _merge_automated_fragments(tasks)
        self.assertEqual(len(result), 2)

    def test_does_not_merge_large_gaps(self):
        """Tasks with gaps > 30 min are NOT merged."""
        from segment_tasks import _merge_automated_fragments
        gap = 31 * 60  # 31 min
        tasks = [
            self._task("Report", 1000, 1300),
            self._task("Report", 1300 + gap, 1600 + gap),
        ]
        result = _merge_automated_fragments(tasks)
        self.assertEqual(len(result), 2)

    def test_does_not_merge_high_involvement(self):
        """High-involvement tasks are NOT merged (real user work)."""
        from segment_tasks import _merge_automated_fragments
        tasks = [
            self._task("Report", 1000, 1300, involvement="high"),
            self._task("Report", 1300, 1600, involvement="high"),
        ]
        result = _merge_automated_fragments(tasks)
        self.assertEqual(len(result), 2)

    def test_does_not_merge_explicit_tasks(self):
        """Explicit (TaskCreate) tasks are NOT merged."""
        from segment_tasks import _merge_automated_fragments
        tasks = [
            self._task("Report", 1000, 1300, flavor="explicit"),
            self._task("Report", 1300, 1600, flavor="explicit"),
        ]
        result = _merge_automated_fragments(tasks)
        self.assertEqual(len(result), 2)

    def test_merges_interleaved_subjects(self):
        """Interleaved subjects (A, B, A, B, A) merge into (A, B)."""
        from segment_tasks import _merge_automated_fragments
        tasks = [
            self._task("Report A", 1000, 1300),
            self._task("Report B", 1300, 1600),
            self._task("Report A", 1600, 1900),
            self._task("Report B", 1900, 2200),
            self._task("Report A", 2200, 2500),
        ]
        result = _merge_automated_fragments(tasks)
        self.assertEqual(len(result), 2)
        # Find which is A and which is B
        a_task = [t for t in result if "A" in t["subject"]][0]
        b_task = [t for t in result if "B" in t["subject"]][0]
        self.assertEqual(a_task["_merged_count"], 3)
        self.assertEqual(b_task["_merged_count"], 2)


if __name__ == "__main__":
    unittest.main()
