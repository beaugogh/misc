"""Tests for the Outlook mail adapter (Phase 9.3).

Run with: python -m unittest tests.test_outlook -v

Covers:
- Event shape: emitted events match the welink-cli mail event shape
  (kind="email", source_kind="comm", same tool_input keys).
- _item_to_event: synthetic COM-like objects → correct event fields.
- _safe_str / _com_datetime_to_epoch: encoding + timestamp conversion.
- detect(): returns False when win32com is unavailable (mocked).
- collect(): yields nothing without raising when COM is unavailable.
- collect_since: watermark filtering.
- _find_folder_by_name: case-insensitive lookup.
- Integration: if Outlook is live on this machine, events have real data.
"""

import unittest
import os
import sys
import datetime
from unittest.mock import patch, MagicMock

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from outlook_adapter import (
    OutlookAdapter,
    _safe_str,
    _com_datetime_to_epoch,
    _find_folder_by_name,
    DEFAULT_MAX_ITEMS_PER_FOLDER,
)
from sources import make_event


# ---------------------------------------------------------------------------
# Mock COM objects
# ---------------------------------------------------------------------------

_UNSET = object()  # sentinel to distinguish "not provided" from "explicitly None"

class MockMailItem:
    """Simulates a COM MailItem for testing _item_to_event."""

    def __init__(self, subject="Test subject", sender="Alice",
                 sender_email="alice@example.com",
                 received_time=_UNSET, sent_on=_UNSET,
                 unread=False, attachments_count=0,
                 entry_id="ABC123", to_recipients=None):
        # Default to a valid timestamp if neither received nor sent is set
        if received_time is _UNSET and sent_on is _UNSET:
            received_time = datetime.datetime(2026, 7, 29, 10, 0, 0)
        elif received_time is _UNSET:
            received_time = None
        elif sent_on is _UNSET:
            sent_on = None
        self._subject = subject
        self._sender = sender
        self._sender_email = sender_email
        self._received = received_time
        self._sent = sent_on
        self._unread = unread
        self._attachments_count = attachments_count
        self._entry_id = entry_id
        self._to = to_recipients

    @property
    def Subject(self):
        return self._subject

    @property
    def SenderName(self):
        return self._sender

    @property
    def SenderEmailAddress(self):
        return self._sender_email

    @property
    def ReceivedTime(self):
        return self._received

    @property
    def SentOn(self):
        return self._sent

    @property
    def UnRead(self):
        return self._unread

    @property
    def Attachments(self):
        m = MagicMock()
        m.Count = self._attachments_count
        return m

    @property
    def EntryID(self):
        return self._entry_id

    @property
    def To(self):
        return self._to


class MockItems:
    """Simulates a COM Items collection."""

    def __init__(self, items):
        self._items = items

    @property
    def Count(self):
        return len(self._items)

    def Sort(self, field, descending):
        pass  # no-op for tests

    def Item(self, index):
        return self._items[index - 1]  # COM is 1-indexed


class MockFolder:
    """Simulates a COM Folder."""

    def __init__(self, name, items):
        self._name = name
        self._items = items

    @property
    def Name(self):
        return self._name

    @property
    def Items(self):
        return MockItems(self._items)


class MockStore:
    """Simulates a COM Store."""

    def __init__(self, display_name, root_folder):
        self._name = display_name
        self._root = root_folder

    @property
    def DisplayName(self):
        return self._name

    @property
    def FilePath(self):
        return None

    def GetRootFolder(self):
        return self._root


class MockRootFolder:
    """Simulates a COM root folder with sub-folders."""

    def __init__(self, folders):
        self._folders = folders

    @property
    def Name(self):
        return "root"

    @property
    def Folders(self):
        return self._folders


class MockMAPINamespace:
    """Simulates the MAPI namespace."""

    def __init__(self, stores):
        self._stores = stores

    @property
    def Stores(self):
        return self._stores


class MockOutlookApp:
    """Simulates the Outlook.Application COM object."""

    def __init__(self, stores):
        self._ns = MockMAPINamespace(stores)

    def GetNamespace(self, name):
        return self._ns


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------

class TestSafeStr(unittest.TestCase):
    """Test _safe_str encoding handling."""

    def test_none(self):
        self.assertIsNone(_safe_str(None))

    def test_simple_string(self):
        self.assertEqual(_safe_str("hello"), "hello")

    def test_long_string_truncated(self):
        s = "x" * 600
        result = _safe_str(s, max_len=100)
        self.assertEqual(len(result), 100)

    def test_unicode_string(self):
        # Chinese characters
        self.assertEqual(_safe_str("测试邮件"), "测试邮件")

    def test_object_with_str(self):
        class Obj:
            def __str__(self):
                return "obj_str"
        self.assertEqual(_safe_str(Obj()), "obj_str")


class TestComDatetimeToEpoch(unittest.TestCase):
    """Test _com_datetime_to_epoch timestamp conversion."""

    def test_none(self):
        self.assertIsNone(_com_datetime_to_epoch(None))

    def test_datetime_object(self):
        dt = datetime.datetime(2026, 7, 29, 12, 0, 0, tzinfo=datetime.timezone.utc)
        ts = _com_datetime_to_epoch(dt)
        self.assertIsNotNone(ts)
        self.assertAlmostEqual(ts, dt.timestamp(), places=1)

    def test_naive_datetime(self):
        dt = datetime.datetime(2026, 7, 29, 12, 0, 0)
        ts = _com_datetime_to_epoch(dt)
        self.assertIsNotNone(ts)
        self.assertAlmostEqual(ts, dt.timestamp(), places=1)

    def test_object_with_timestamp_method(self):
        class MockTime:
            def timestamp(self):
                return 1722000000.0
        self.assertEqual(_com_datetime_to_epoch(MockTime()), 1722000000.0)

    def test_string_fallback(self):
        # A string that can be parsed as ISO
        dt_str = "2026-07-29T12:00:00"
        ts = _com_datetime_to_epoch(dt_str)
        self.assertIsNotNone(ts)


class TestFindFolderByName(unittest.TestCase):
    """Test _find_folder_by_name case-insensitive lookup."""

    def test_exact_match(self):
        root = MockRootFolder([MockFolder("Inbox", [])])
        result = _find_folder_by_name(root, "inbox")
        self.assertIsNotNone(result)
        self.assertEqual(result.Name, "Inbox")

    def test_case_insensitive(self):
        root = MockRootFolder([MockFolder("Sent Items", [])])
        result = _find_folder_by_name(root, "sent")
        self.assertIsNotNone(result)

    def test_substring_match(self):
        root = MockRootFolder([MockFolder("Sent Items", [])])
        result = _find_folder_by_name(root, "sent")
        self.assertIsNotNone(result)

    def test_no_match(self):
        root = MockRootFolder([MockFolder("Drafts", [])])
        result = _find_folder_by_name(root, "inbox")
        self.assertIsNone(result)

    def test_exception_returns_none(self):
        result = _find_folder_by_name(None, "inbox")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# Event shape tests
# ---------------------------------------------------------------------------

class TestEventShape(unittest.TestCase):
    """Verify emitted events match the welink-cli mail event shape."""

    def setUp(self):
        self.adapter = OutlookAdapter()
        # Bypass COM connection
        self.adapter._ns = MagicMock()

    def test_received_email_event_shape(self):
        """A received email event has the same keys as welink-cli mail."""
        dt = datetime.datetime(2026, 7, 29, 10, 30, 0)
        item = MockMailItem(
            subject="Weekly report",
            sender="boss@huawei.com",
            sender_email="boss@huawei.com",
            received_time=dt,
            unread=False,
            attachments_count=2,
            entry_id="ENTRY123",
        )
        ev = self.adapter._item_to_event(item, "Inbox", "received", "mbox")
        self.assertIsNotNone(ev)

        # Core event fields
        self.assertEqual(ev["source"], "outlook")
        self.assertEqual(ev["source_kind"], "comm")
        self.assertEqual(ev["kind"], "email")
        self.assertEqual(ev["text"], "Weekly report")
        self.assertAlmostEqual(ev["timestamp"], dt.timestamp(), places=1)

        # tool_input must match welink-cli mail shape
        ti = ev["tool_input"]
        self.assertEqual(ti["domain"], "mail")
        self.assertEqual(ti["folder"], "Inbox")
        self.assertEqual(ti["direction"], "received")
        self.assertEqual(ti["subject"], "Weekly report")
        self.assertEqual(ti["from"], "boss@huawei.com")
        self.assertEqual(ti["from_email"], "boss@huawei.com")
        self.assertIsNotNone(ti["date"])
        self.assertEqual(ti["is_read"], True)  # UnRead=False → is_read=True
        self.assertEqual(ti["has_attachments"], True)
        self.assertEqual(ti["item_id"], "ENTRY123")

    def test_sent_email_event_shape(self):
        """A sent email event uses SentOn and direction='sent'."""
        dt = datetime.datetime(2026, 7, 29, 14, 0, 0)
        item = MockMailItem(
            subject="Re: Weekly report",
            sender="me",
            sender_email="me@huawei.com",
            sent_on=dt,
            unread=False,
            attachments_count=0,
            entry_id="ENTRY456",
            to_recipients="team@huawei.com",
        )
        ev = self.adapter._item_to_event(item, "Sent Items", "sent", "mbox")
        self.assertIsNotNone(ev)
        self.assertEqual(ev["tool_input"]["direction"], "sent")
        self.assertEqual(ev["tool_input"]["folder"], "Sent Items")
        self.assertEqual(ev["tool_input"]["to"], "team@huawei.com")
        self.assertAlmostEqual(ev["timestamp"], dt.timestamp(), places=1)

    def test_unread_email(self):
        """UnRead=True → is_read=False."""
        item = MockMailItem(unread=True)
        ev = self.adapter._item_to_event(item, "Inbox", "received", "mbox")
        self.assertFalse(ev["tool_input"]["is_read"])

    def test_no_subject(self):
        """Missing subject → '(no subject)'."""
        item = MockMailItem(subject="")
        ev = self.adapter._item_to_event(item, "Inbox", "received", "mbox")
        self.assertEqual(ev["text"], "(no subject)")
        self.assertEqual(ev["tool_input"]["subject"], "(no subject)")

    def test_no_timestamp_returns_none(self):
        """If timestamp can't be parsed, return None (skip the item)."""
        item = MockMailItem(received_time=None, sent_on=None)
        ev = self.adapter._item_to_event(item, "Inbox", "received", "mbox")
        self.assertIsNone(ev)

    def test_extra_field_has_tool(self):
        """Event extra dict records the access method."""
        item = MockMailItem()
        ev = self.adapter._item_to_event(item, "Inbox", "received", "mbox")
        self.assertEqual(ev.get("extra", {}).get("tool"), "outlook_com")


# ---------------------------------------------------------------------------
# Adapter behavior tests (no live COM needed)
# ---------------------------------------------------------------------------

class TestDetectNoCOM(unittest.TestCase):
    """detect() returns False when win32com is unavailable."""

    @patch("outlook_adapter._try_import_win32com", return_value=None)
    def test_detect_no_win32com(self, mock_import):
        adapter = OutlookAdapter()
        self.assertFalse(adapter.detect())

    @patch("outlook_adapter._try_import_win32com", return_value=None)
    def test_collect_no_win32com(self, mock_import):
        """collect() yields nothing without raising when COM unavailable."""
        adapter = OutlookAdapter()
        events = list(adapter.collect())
        self.assertEqual(events, [])

    @patch("outlook_adapter._try_import_win32com", return_value=None)
    def test_collect_since_no_win32com(self, mock_import):
        """collect_since() yields nothing without raising."""
        adapter = OutlookAdapter()
        events = list(adapter.collect_since(1000.0))
        self.assertEqual(events, [])


class TestCollectWithMockCOM(unittest.TestCase):
    """Test collect() with mocked COM objects."""

    def _build_mock_outlook(self):
        """Build a mock Outlook with 2 inbox + 1 sent item."""
        inbox_items = [
            MockMailItem(
                subject="Inbox 1",
                sender="alice",
                sender_email="alice@huawei.com",
                received_time=datetime.datetime(2026, 7, 28, 9, 0, 0),
                entry_id="I1",
            ),
            MockMailItem(
                subject="Inbox 2",
                sender="bob",
                sender_email="bob@huawei.com",
                received_time=datetime.datetime(2026, 7, 29, 10, 0, 0),
                entry_id="I2",
            ),
        ]
        sent_items = [
            MockMailItem(
                subject="Sent 1",
                sender="me",
                sender_email="me@huawei.com",
                sent_on=datetime.datetime(2026, 7, 29, 11, 0, 0),
                entry_id="S1",
                to_recipients="team@huawei.com",
            ),
        ]
        inbox = MockFolder("Inbox", inbox_items)
        sent = MockFolder("Sent Items", sent_items)
        root = MockRootFolder([inbox, sent])
        store = MockStore("mbox@huawei.com", root)
        return MockOutlookApp([store])

    def _make_mock_win32com(self, mock_outlook):
        """Create a mock that mimics win32com.client (what _try_import_win32com returns).

        _try_import_win32com returns the win32com.client module, and the adapter
        calls win32com_client.Dispatch("Outlook.Application"). So the mock needs
        a .Dispatch method.
        """
        mock_client = MagicMock()
        mock_client.Dispatch.return_value = mock_outlook
        return mock_client

    @patch("outlook_adapter._try_import_win32com")
    def test_collect_yields_events(self, mock_import):
        """collect() yields email events from all folders."""
        mock_outlook = self._build_mock_outlook()
        mock_import.return_value = self._make_mock_win32com(mock_outlook)

        adapter = OutlookAdapter()
        events = list(adapter.collect())

        self.assertEqual(len(events), 3)

        # Check directions
        received = [e for e in events if e["tool_input"]["direction"] == "received"]
        sent = [e for e in events if e["tool_input"]["direction"] == "sent"]
        self.assertEqual(len(received), 2)
        self.assertEqual(len(sent), 1)

        # All are email events
        for ev in events:
            self.assertEqual(ev["kind"], "email")
            self.assertEqual(ev["source_kind"], "comm")
            self.assertEqual(ev["source"], "outlook")

    @patch("outlook_adapter._try_import_win32com")
    def test_collect_since_filters_by_watermark(self, mock_import):
        """collect_since() yields only events after the watermark."""
        mock_outlook = self._build_mock_outlook()
        mock_import.return_value = self._make_mock_win32com(mock_outlook)

        adapter = OutlookAdapter()
        # Watermark = 2026-07-29 00:00:00 → should filter out Inbox 1 (July 28)
        watermark = datetime.datetime(2026, 7, 29, 0, 0, 0).timestamp()
        events = list(adapter.collect_since(watermark))

        self.assertEqual(len(events), 2)  # Inbox 2 + Sent 1
        for ev in events:
            self.assertGreater(ev["timestamp"], watermark)

    @patch("outlook_adapter._try_import_win32com")
    def test_collect_since_none_does_full_collect(self, mock_import):
        """collect_since(None) does full collect."""
        mock_outlook = self._build_mock_outlook()
        mock_import.return_value = self._make_mock_win32com(mock_outlook)

        adapter = OutlookAdapter()
        events = list(adapter.collect_since(None))
        self.assertEqual(len(events), 3)

    @patch("outlook_adapter._try_import_win32com")
    def test_collect_respects_max_items(self, mock_import):
        """max_items_per_folder caps the number of events per folder."""
        # Build 10 inbox items
        items = [
            MockMailItem(
                subject=f"Item {i}",
                received_time=datetime.datetime(2026, 7, 29, i, 0, 0),
                entry_id=f"ID{i}",
            )
            for i in range(10)
        ]
        inbox = MockFolder("Inbox", items)
        root = MockRootFolder([inbox])
        store = MockStore("mbox", root)
        mock_outlook = MockOutlookApp([store])

        mock_import.return_value = self._make_mock_win32com(mock_outlook)

        adapter = OutlookAdapter(max_items_per_folder=3)
        events = list(adapter.collect())
        self.assertEqual(len(events), 3)

    @patch("outlook_adapter._find_ost_files_no_com", return_value=["mail.ost"])
    @patch("outlook_adapter._try_import_win32com")
    def test_detect_returns_true_when_pywin32_and_store_file_exist(self, mock_import, _mock_find):
        """detect() stays file-based and does not create a COM session."""
        mock_outlook = self._build_mock_outlook()
        mock_import.return_value = self._make_mock_win32com(mock_outlook)

        adapter = OutlookAdapter()
        self.assertTrue(adapter.detect())

    @patch("outlook_adapter._try_import_win32com")
    def test_collect_handles_com_error_gracefully(self, mock_import):
        """collect() doesn't crash when a store errors."""
        # Store that raises on GetRootFolder
        bad_store = MagicMock()
        bad_store.GetRootFolder.side_effect = Exception("corrupt")
        mock_outlook = MockOutlookApp([])  # empty stores
        # Inject the bad store
        mock_outlook._ns._stores = [bad_store]

        mock_import.return_value = self._make_mock_win32com(mock_outlook)

        adapter = OutlookAdapter()
        events = list(adapter.collect())  # should not raise
        self.assertEqual(events, [])

    @patch("outlook_adapter._try_import_win32com")
    def test_collect_skips_folder_without_items(self, mock_import):
        """Empty folders yield nothing without error."""
        empty_inbox = MockFolder("Inbox", [])
        root = MockRootFolder([empty_inbox])
        store = MockStore("mbox", root)
        mock_outlook = MockOutlookApp([store])

        mock_import.return_value = self._make_mock_win32com(mock_outlook)

        adapter = OutlookAdapter()
        events = list(adapter.collect())
        self.assertEqual(events, [])


# ---------------------------------------------------------------------------
# Integration test (only runs if Outlook is installed on this machine)
# ---------------------------------------------------------------------------

class TestLiveOutlookIntegration(unittest.TestCase):
    """Integration test against the real Outlook instance.

    detect() uses filesystem/registry checks (no COM) — so these tests run
    whenever Outlook is installed, even if the Outlook application isn't open.
    collect() lazily connects via COM (Dispatch starts Outlook if needed).
    """

    @classmethod
    def setUpClass(cls):
        cls.adapter = OutlookAdapter()
        # detect() is filesystem-based — doesn't require Outlook to be running.
        cls.detected = cls.adapter.detect()

    def setUp(self):
        if not self.detected:
            self.skipTest("Outlook not installed (no OST/PST files found)")

    def test_detect_finds_outlook(self):
        """detect() returns True when Outlook data files exist."""
        self.assertTrue(self.detected)

    def test_collect_yields_events(self):
        """collect() yields at least some email events from Outlook."""
        events = list(self.adapter.collect())
        self.assertGreater(len(events), 0, "Expected at least some email events")

        # Verify event shape
        for ev in events:
            self.assertEqual(ev["source"], "outlook")
            self.assertEqual(ev["source_kind"], "comm")
            self.assertEqual(ev["kind"], "email")
            self.assertIn("tool_input", ev)
            ti = ev["tool_input"]
            self.assertEqual(ti["domain"], "mail")
            self.assertIn(ti["direction"], ("received", "sent"))
            self.assertIsNotNone(ti["subject"])
            self.assertIsNotNone(ev["timestamp"])

    def test_collect_since_filters(self):
        """collect_since() with a recent watermark returns fewer events."""
        all_events = list(self.adapter.collect())
        if len(all_events) < 2:
            self.skipTest("Not enough events to test watermark filtering")

        # Use the median timestamp as watermark
        timestamps = sorted(e["timestamp"] for e in all_events)
        median_ts = timestamps[len(timestamps) // 2]
        filtered = list(self.adapter.collect_since(median_ts))

        # Filtered should have fewer events than full
        self.assertLess(len(filtered), len(all_events))
        for ev in filtered:
            self.assertGreater(ev["timestamp"], median_ts)


if __name__ == "__main__":
    unittest.main()
