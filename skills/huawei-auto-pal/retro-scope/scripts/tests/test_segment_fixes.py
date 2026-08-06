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


if __name__ == "__main__":
    unittest.main()
