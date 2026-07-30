"""Tests for the enhanced adapters in more_adapters.py (Phase 9.1, 9.2, 9.6).

Run with: python -m unittest discover -s tests -p "test_adapters.py" -v

Covers:
- 9.1: WeLinkRecordingsAdapter ffprobe path (mocked absent), filename parser.
- 9.2: ICalendarAdapter — VEVENT with DTSTART/DTEND, RRULE:DAILY expansion, TZID.
- 9.6: JumpListAdapter — synthetic .automaticDestinations-ms with UTF-16LE paths.
"""

import unittest
import os
import sys
import time
import tempfile
import shutil
from unittest.mock import patch

# Make the scripts dir importable.
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.dirname(HERE)
sys.path.insert(0, SCRIPTS)

from more_adapters import (
    WeLinkRecordingsAdapter,
    ICalendarAdapter,
    JumpListAdapter,
    _parse_recording_filename,
    _scan_jump_list_paths,
)


# ---------------------------------------------------------------------------
# 9.1: WeLinkRecordingsAdapter — ffprobe + filename parsing
# ---------------------------------------------------------------------------

class TestRecordingFilenameParser(unittest.TestCase):
    """Test the filename parser for WeLink recording file patterns."""

    def test_parse_space_separated_with_extension(self):
        """Pattern: 20260713 09.55.29 会议 99997299.lnk"""
        result = _parse_recording_filename("20260713 09.55.29 会议 99997299.lnk")
        self.assertEqual(result["date"], "20260713")
        self.assertEqual(result["time"], "09.55.29")
        self.assertEqual(result["meeting_id"], "99997299")

    def test_parse_underscore_separated(self):
        """Pattern: 20260713_111710_meeting_record.99997299.pdf"""
        result = _parse_recording_filename("20260713_111710_meeting_record.99997299.pdf")
        self.assertEqual(result["date"], "20260713")
        self.assertEqual(result["time"], "111710")
        self.assertEqual(result["meeting_id"], "99997299")

    def test_parse_no_extension(self):
        """Pattern: 20260713 09.55.29 会议 99997299 (no extension)"""
        result = _parse_recording_filename("20260713 09.55.29 会议 99997299")
        self.assertEqual(result["date"], "20260713")
        self.assertEqual(result["time"], "09.55.29")
        self.assertEqual(result["meeting_id"], "99997299")

    def test_parse_colon_time_separator(self):
        """Pattern with colon time separator: 09:55:29"""
        result = _parse_recording_filename("20260713 09:55:29 会议 99997299.mp4")
        self.assertEqual(result["date"], "20260713")
        self.assertEqual(result["time"], "09:55:29")
        self.assertEqual(result["meeting_id"], "99997299")

    def test_parse_no_match(self):
        """Non-matching filename returns empty dict."""
        result = _parse_recording_filename("random_file.txt")
        self.assertEqual(result, {})

    def test_parse_short_meeting_id(self):
        """Meeting IDs shorter than 6 digits don't match."""
        result = _parse_recording_filename("20260713 09.55.29 会议 12345.lnk")
        self.assertEqual(result, {})


class TestWeLinkRecordingsAdapter(unittest.TestCase):
    """Test WeLinkRecordingsAdapter with and without ffprobe."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create a fake recording file
        self.recording_name = "20260713 09.55.29 会议 99997299.lnk"
        self.recording_path = os.path.join(self.tmpdir, self.recording_name)
        with open(self.recording_path, "wb") as f:
            f.write(b"fake recording content")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_detect_true_when_dir_exists(self):
        adapter = WeLinkRecordingsAdapter(recordings_dir=self.tmpdir)
        self.assertTrue(adapter.detect())

    def test_detect_false_when_dir_missing(self):
        adapter = WeLinkRecordingsAdapter(recordings_dir="C:\\nonexistent\\path\\xyz")
        self.assertFalse(adapter.detect())

    def test_collect_without_ffprobe(self):
        """Adapter works with mtime only when ffprobe is absent."""
        adapter = WeLinkRecordingsAdapter(recordings_dir=self.tmpdir)
        with patch("more_adapters.shutil.which", return_value=None):
            events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertEqual(ev["source"], "welink_recordings")
        self.assertEqual(ev["source_kind"], "meeting")
        self.assertEqual(ev["kind"], "meeting_recording")
        self.assertEqual(ev["text"], self.recording_name)
        # No duration_seconds when ffprobe is absent
        self.assertNotIn("duration_seconds", ev["tool_input"])
        self.assertNotIn("extra", ev)

    def test_collect_with_ffprobe_mocked(self):
        """Adapter calls ffprobe and stores duration + end_ts when available."""
        adapter = WeLinkRecordingsAdapter(recordings_dir=self.tmpdir)
        # Mock ffprobe: shutil.which returns a path, subprocess.run returns 3600.5
        mock_result = type("MockResult", (), {
            "returncode": 0,
            "stdout": "3600.5\n",
            "stderr": "",
        })()
        with patch("more_adapters.shutil.which", return_value="/usr/bin/ffprobe"), \
             patch("more_adapters.subprocess.run", return_value=mock_result):
            events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertEqual(ev["tool_input"]["duration_seconds"], 3600.5)
        self.assertEqual(ev["extra"]["duration_seconds"], 3600.5)
        # end_ts must be present and = timestamp + duration
        self.assertIn("end_ts", ev["extra"])
        self.assertAlmostEqual(ev["extra"]["end_ts"],
                               ev["timestamp"] + 3600.5, places=3)

    def test_collect_parses_filename_fields(self):
        """Parsed filename fields are in tool_input."""
        adapter = WeLinkRecordingsAdapter(recordings_dir=self.tmpdir)
        with patch("more_adapters.shutil.which", return_value=None):
            events = list(adapter.collect())
        ev = events[0]
        self.assertEqual(ev["tool_input"]["date"], "20260713")
        self.assertEqual(ev["tool_input"]["time"], "09.55.29")
        self.assertEqual(ev["tool_input"]["meeting_id"], "99997299")
        self.assertEqual(ev["session_id"], "99997299")

    def test_collect_since_filters_by_watermark(self):
        """collect_since only returns events after the watermark."""
        adapter = WeLinkRecordingsAdapter(recordings_dir=self.tmpdir)
        # Set file mtime to a known time
        known_time = time.time() - 3600  # 1 hour ago
        os.utime(self.recording_path, (known_time, known_time))
        with patch("more_adapters.shutil.which", return_value=None):
            all_events = list(adapter.collect())
            self.assertEqual(len(all_events), 1)
            ts = all_events[0]["timestamp"]
            # Watermark just before the event -> should include it
            recent_events = list(adapter.collect_since(ts - 1))
            self.assertEqual(len(recent_events), 1)
            # Watermark just after the event -> should exclude it
            no_events = list(adapter.collect_since(ts + 1))
            self.assertEqual(len(no_events), 0)

    def test_ffprobe_failure_falls_back_gracefully(self):
        """When ffprobe exists but fails, no duration field is emitted."""
        adapter = WeLinkRecordingsAdapter(recordings_dir=self.tmpdir)
        mock_result = type("MockResult", (), {
            "returncode": 1,
            "stdout": "",
            "stderr": "error",
        })()
        with patch("more_adapters.shutil.which", return_value="/usr/bin/ffprobe"), \
             patch("more_adapters.subprocess.run", return_value=mock_result):
            events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertNotIn("duration_seconds", ev["tool_input"])
        # No extra (no end_ts, no duration_seconds)
        self.assertNotIn("extra", ev)

    def test_collect_without_ffprobe_no_end_ts(self):
        """When ffprobe is absent, extra.end_ts must NOT be set (honest: unknown duration)."""
        adapter = WeLinkRecordingsAdapter(recordings_dir=self.tmpdir)
        with patch("more_adapters.shutil.which", return_value=None):
            events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertNotIn("extra", ev)


# ---------------------------------------------------------------------------
# 9.2: ICalendarAdapter — VEVENT, RRULE, TZID
# ---------------------------------------------------------------------------

class TestICalendarAdapter(unittest.TestCase):
    """Test the enhanced ICalendarAdapter."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_ics(self, content: str, filename: str = "test.ics") -> str:
        path = os.path.join(self.tmpdir, filename)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        return path

    def test_basic_vevent(self):
        """A simple VEVENT with DTSTART/DTEND yields one meeting event with extra.end_ts."""
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            "SUMMARY:Weekly Standup\n"
            "DTSTART:20260729T100000Z\n"
            "DTEND:20260729T103000Z\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertEqual(ev["source"], "icalendar")
        self.assertEqual(ev["source_kind"], "meeting")
        self.assertEqual(ev["text"], "Weekly Standup")
        self.assertEqual(ev["tool_input"]["duration_seconds"], 1800.0)
        # extra.end_ts must be present and = timestamp + duration
        self.assertIn("extra", ev)
        self.assertIn("end_ts", ev["extra"])
        self.assertEqual(ev["extra"]["duration_seconds"], 1800.0)
        self.assertAlmostEqual(ev["extra"]["end_ts"],
                               ev["timestamp"] + 1800.0, places=3)

    def test_rrule_daily_expansion(self):
        """RRULE:FREQ=DAILY expands to multiple events within the lookback window."""
        # Start date 10 days ago, daily recurrence
        from datetime import datetime, timezone, timedelta
        start = datetime.now(timezone.utc) - timedelta(days=10)
        start_str = start.strftime("%Y%m%dT%H%M%SZ")
        end_str = (start + timedelta(minutes=30)).strftime("%Y%m%dT%H%M%SZ")
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            f"SUMMARY:Daily Standup\n"
            f"DTSTART:{start_str}\n"
            f"DTEND:{end_str}\n"
            f"RRULE:FREQ=DAILY\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        # Should produce 11 events (10 days ago through today)
        self.assertGreaterEqual(len(events), 8)
        self.assertLessEqual(len(events), 12)
        # All should have the same summary
        for ev in events:
            self.assertEqual(ev["text"], "Daily Standup")
            self.assertEqual(ev["tool_input"]["duration_seconds"], 1800.0)
            # Each recurring occurrence must carry extra.end_ts
            self.assertIn("extra", ev)
            self.assertIn("end_ts", ev["extra"])
            self.assertAlmostEqual(ev["extra"]["end_ts"],
                                   ev["timestamp"] + 1800.0, places=3)

    def test_rrule_daily_with_count(self):
        """RRULE:FREQ=DAILY;COUNT=5 produces exactly 5 events."""
        from datetime import datetime, timezone, timedelta
        start = datetime.now(timezone.utc) - timedelta(days=100)
        start_str = start.strftime("%Y%m%dT%H%M%SZ")
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            f"SUMMARY:Limited Daily\n"
            f"DTSTART:{start_str}\n"
            f"RRULE:FREQ=DAILY;COUNT=5\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        self.assertEqual(len(events), 5)

    def test_rrule_weekly_expansion(self):
        """RRULE:FREQ=WEEKLY expands to multiple events."""
        from datetime import datetime, timezone, timedelta
        start = datetime.now(timezone.utc) - timedelta(days=30)
        start_str = start.strftime("%Y%m%dT%H%M%SZ")
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            f"SUMMARY:Weekly Sync\n"
            f"DTSTART:{start_str}\n"
            f"RRULE:FREQ=WEEKLY\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        # 30 days / 7 = ~4-5 weekly occurrences
        self.assertGreaterEqual(len(events), 3)
        self.assertLessEqual(len(events), 6)

    def test_rrule_monthly_fallback_single_event(self):
        """RRULE:FREQ=MONTHLY (not supported for expansion) falls back to one event."""
        from datetime import datetime, timezone, timedelta
        start = datetime.now(timezone.utc) - timedelta(days=100)
        start_str = start.strftime("%Y%m%dT%H%M%SZ")
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            f"SUMMARY:Monthly Review\n"
            f"DTSTART:{start_str}\n"
            f"RRULE:FREQ=MONTHLY\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        # MONTHLY not expanded — just the first occurrence
        self.assertEqual(len(events), 1)

    def test_tzid_shanghai(self):
        """DTSTART;TZID=Asia/Shanghai parses without crashing, extra.end_ts set."""
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            "SUMMARY:Shanghai Meeting\n"
            "DTSTART;TZID=Asia/Shanghai:20260729T100000\n"
            "DTEND;TZID=Asia/Shanghai:20260729T110000\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        ev = events[0]
        self.assertEqual(ev["text"], "Shanghai Meeting")
        self.assertIsNotNone(ev["timestamp"])
        # Duration should be 3600 seconds (1 hour)
        self.assertEqual(ev["tool_input"]["duration_seconds"], 3600.0)
        # extra.end_ts must be present and = timestamp + duration
        self.assertIn("extra", ev)
        self.assertIn("end_ts", ev["extra"])
        self.assertAlmostEqual(ev["extra"]["end_ts"],
                               ev["timestamp"] + 3600.0, places=3)

    def test_utc_z_suffix(self):
        """DTSTART with Z suffix parses as UTC."""
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            "SUMMARY:UTC Meeting\n"
            "DTSTART:20260729T100000Z\n"
            "DTEND:20260729T110000Z\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        # Verify timestamp: 2026-07-29T10:00:00Z = 1785319200
        self.assertAlmostEqual(events[0]["timestamp"], 1785319200.0, places=0)

    def test_no_vevents(self):
        """ICS with no VEVENTs yields no events."""
        ics = "BEGIN:VCALENDAR\nEND:VCALENDAR\n"
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        self.assertEqual(len(events), 0)

    def test_detect_with_ics_paths(self):
        """detect() returns True when valid .ics paths are given."""
        ics = "BEGIN:VCALENDAR\nEND:VCALENDAR\n"
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        self.assertTrue(adapter.detect())

    def test_detect_false_when_no_ics(self):
        """detect() returns False when no .ics files exist."""
        adapter = ICalendarAdapter(ics_paths=["/nonexistent/path.ics"])
        self.assertFalse(adapter.detect())

    def test_env_var_paths(self):
        """RETRO_SCOPE_ICS_PATHS env var adds search locations."""
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            "SUMMARY:Env Var Meeting\n"
            "DTSTART:20260729T100000Z\n"
            "DTEND:20260729T110000Z\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        # Set env var to point at the file directly
        with patch.dict(os.environ, {"RETRO_SCOPE_ICS_PATHS": path}):
            adapter = ICalendarAdapter()
            self.assertTrue(adapter.detect())
            events = list(adapter.collect())
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["text"], "Env Var Meeting")

    def test_line_folding(self):
        """RFC 5545 line folding (continuation lines) is handled."""
        ics = (
            "BEGIN:VCALENDAR\n"
            "BEGIN:VEVENT\n"
            "SUMMARY:This is a very long title that\n"
            "  continues on the next line\n"
            "DTSTART:20260729T100000Z\n"
            "DTEND:20260729T110000Z\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )
        path = self._write_ics(ics)
        adapter = ICalendarAdapter(ics_paths=[path])
        events = list(adapter.collect())
        self.assertEqual(len(events), 1)
        self.assertIn("This is a very long title that", events[0]["text"])
        self.assertIn("continues on the next line", events[0]["text"])


# ---------------------------------------------------------------------------
# 9.6: JumpListAdapter — heuristic byte-scan
# ---------------------------------------------------------------------------

class TestJumpListScan(unittest.TestCase):
    """Test the _scan_jump_list_paths heuristic byte-scanner."""

    def test_extract_single_path(self):
        """A single UTF-16LE path is extracted from binary data."""
        path = "C:\\Users\\test\\Documents\\report.docx"
        encoded = path.encode("utf-16-le")
        # Wrap in some binary noise
        data = b"\x00\x01\x02" + encoded + b"\x03\x04\x05"
        result = _scan_jump_list_paths(data)
        self.assertIn(path, result)

    def test_extract_multiple_paths(self):
        """Multiple UTF-16LE paths are extracted."""
        paths = [
            "C:\\Users\\test\\file1.py",
            "D:\\Projects\\doc.pdf",
            "\\\\server\\share\\file.xlsx",
        ]
        data = b"\x00\x00"
        for p in paths:
            data += p.encode("utf-16-le") + b"\x00\x00"
        result = _scan_jump_list_paths(data)
        for p in paths:
            self.assertIn(p, result)

    def test_forward_slash_paths(self):
        """Forward-slash paths (Unix-style) are also extracted."""
        path = "/home/user/file.txt"
        encoded = path.encode("utf-16-le")
        data = b"\x00" + encoded + b"\x00"
        result = _scan_jump_list_paths(data)
        self.assertIn(path, result)

    def test_no_paths_in_empty_data(self):
        """Empty or noise-only data yields no paths."""
        self.assertEqual(_scan_jump_list_paths(b""), [])
        self.assertEqual(_scan_jump_list_paths(b"\x00\x01\x02\x03"), [])

    def test_no_paths_without_extension(self):
        """Strings without a file extension are not extracted."""
        path = "C:\\Users\\test\\noextension"
        encoded = path.encode("utf-16-le")
        data = b"\x00" + encoded + b"\x00"
        result = _scan_jump_list_paths(data)
        self.assertEqual(result, [])

    def test_deduplicates_paths(self):
        """Duplicate paths are only returned once."""
        path = "C:\\test\\file.docx"
        encoded = path.encode("utf-16-le")
        data = encoded + b"\x00\x00" + encoded
        result = _scan_jump_list_paths(data)
        self.assertEqual(result.count(path), 1)

    def test_malformed_utf16_does_not_crash(self):
        """Garbage bytes don't cause crashes."""
        data = b"\xff\xfe\xfd\xfc\xfb\xfa" * 100
        # Should not raise
        result = _scan_jump_list_paths(data)
        self.assertIsInstance(result, list)


class TestJumpListAdapter(unittest.TestCase):
    """Test the JumpListAdapter class."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _create_dest_file(self, paths: list[str], filename: str = "test.automaticDestinations-ms") -> str:
        """Create a fake .automaticDestinations-ms file with embedded UTF-16LE paths."""
        fpath = os.path.join(self.tmpdir, filename)
        with open(fpath, "wb") as f:
            f.write(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")  # fake OLE header
            for p in paths:
                f.write(p.encode("utf-16-le"))
                f.write(b"\x00\x00")
        return fpath

    def test_detect_true_when_dest_files_exist(self):
        """detect() returns True when .automaticDestinations-ms files are present."""
        self._create_dest_file(["C:\\test\\file.docx"])
        adapter = JumpListAdapter(jump_list_dir=self.tmpdir)
        self.assertTrue(adapter.detect())

    def test_detect_false_when_dir_missing(self):
        """detect() returns False when the directory doesn't exist."""
        adapter = JumpListAdapter(jump_list_dir="C:\\nonexistent\\xyz")
        self.assertFalse(adapter.detect())

    def test_detect_false_when_no_dest_files(self):
        """detect() returns False when the dir has no .automaticDestinations-ms files."""
        # Create a non-matching file
        with open(os.path.join(self.tmpdir, "other.txt"), "w") as f:
            f.write("test")
        adapter = JumpListAdapter(jump_list_dir=self.tmpdir)
        self.assertFalse(adapter.detect())

    def test_collect_extracts_paths(self):
        """collect() yields file_open events for each extracted path."""
        paths = [
            "C:\\Users\\test\\Documents\\report.docx",
            "D:\\Projects\\presentation.pptx",
        ]
        self._create_dest_file(paths)
        adapter = JumpListAdapter(jump_list_dir=self.tmpdir)
        events = list(adapter.collect())
        self.assertEqual(len(events), 2)
        texts = [ev["text"] for ev in events]
        for p in paths:
            self.assertIn(p, texts)
        for ev in events:
            self.assertEqual(ev["source"], "jump_list")
            self.assertEqual(ev["source_kind"], "filesystem")
            self.assertEqual(ev["kind"], "file_open")
            self.assertIsNotNone(ev["timestamp"])

    def test_collect_empty_when_no_paths_found(self):
        """collect() yields nothing when the binary scan finds no paths."""
        # Create a .automaticDestinations-ms file with no paths
        fpath = os.path.join(self.tmpdir, "empty.automaticDestinations-ms")
        with open(fpath, "wb") as f:
            f.write(b"\x00\x01\x02\x03" * 100)
        adapter = JumpListAdapter(jump_list_dir=self.tmpdir)
        events = list(adapter.collect())
        self.assertEqual(len(events), 0)

    def test_collect_since_filters(self):
        """collect_since filters events by watermark."""
        self._create_dest_file(["C:\\test\\file.docx"])
        adapter = JumpListAdapter(jump_list_dir=self.tmpdir)
        all_events = list(adapter.collect())
        self.assertGreater(len(all_events), 0)
        ts = all_events[0]["timestamp"]
        # Watermark just before -> includes
        recent = list(adapter.collect_since(ts - 1))
        self.assertEqual(len(recent), len(all_events))
        # Watermark just after -> excludes
        none = list(adapter.collect_since(ts + 1))
        self.assertEqual(len(none), 0)

    def test_collect_does_not_crash_on_malformed_file(self):
        """collect() handles malformed .automaticDestinations-ms without crashing."""
        fpath = os.path.join(self.tmpdir, "bad.automaticDestinations-ms")
        with open(fpath, "wb") as f:
            f.write(b"\xff\xfe\xfd" * 500)
        adapter = JumpListAdapter(jump_list_dir=self.tmpdir)
        events = list(adapter.collect())
        self.assertEqual(len(events), 0)


if __name__ == "__main__":
    unittest.main()
