#!/usr/bin/env python3
"""Unit tests for youtube_transcript.py pure functions.

Run: python3 skills/youtube-transcript/scripts/test_youtube_transcript.py
No network, no yt-dlp, no opencli — pure parsing/formatting logic only.
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_transcript import (
    extract_json_array,
    fmt_ts,
    parse_json3,
    parse_vtt,
    parse_video_id,
    slugify,
)


class TestParseVideoId(unittest.TestCase):
    def test_bare_id(self):
        self.assertEqual(parse_video_id('8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_watch_url(self):
        self.assertEqual(parse_video_id('https://www.youtube.com/watch?v=8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_watch_url_with_params(self):
        self.assertEqual(parse_video_id('https://www.youtube.com/watch?v=8jPQjjsBbIc&list=xyz&t=30'), '8jPQjjsBbIc')

    def test_youtubedotbe_with_timestamp(self):
        self.assertEqual(parse_video_id('https://youtu.be/8jPQjjsBbIc?t=30'), '8jPQjjsBbIc')

    def test_youtubedotbe_path_suffix(self):
        self.assertEqual(parse_video_id('https://youtu.be/8jPQjjsBbIc/featured'), '8jPQjjsBbIc')

    def test_shorts_url(self):
        self.assertEqual(parse_video_id('https://www.youtube.com/shorts/8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_embed_url(self):
        self.assertEqual(parse_video_id('https://www.youtube.com/embed/8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_live_url(self):
        self.assertEqual(parse_video_id('https://www.youtube.com/live/8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_mobile_url(self):
        self.assertEqual(parse_video_id('https://m.youtube.com/watch?v=8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_music_url(self):
        self.assertEqual(parse_video_id('https://music.youtube.com/watch?v=8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_no_scheme_url(self):
        self.assertEqual(parse_video_id('youtube.com/watch?v=8jPQjjsBbIc'), '8jPQjjsBbIc')

    def test_rejects_vimeo(self):
        with self.assertRaises(SystemExit):
            parse_video_id('https://vimeo.com/12345')

    def test_rejects_garbage(self):
        with self.assertRaises(SystemExit):
            parse_video_id('not-a-valid-url')

    def test_rejects_short_id(self):
        with self.assertRaises(SystemExit):
            parse_video_id('8jPQjjsBbI')

    def test_rejects_watch_without_v(self):
        with self.assertRaises(SystemExit):
            parse_video_id('https://www.youtube.com/watch')


class TestExtractJsonArray(unittest.TestCase):
    def test_clean_array(self):
        self.assertEqual(extract_json_array('[{"a": 1}]'), [{'a': 1}])

    def test_trailing_junk(self):
        # opencli appends update notices to stdout
        self.assertEqual(
            extract_json_array('[{"a": 1}]\n  Update available: v1 → v2'),
            [{'a': 1}])

    def test_junk_before_array(self):
        self.assertEqual(extract_json_array('Warning: something\n[{"a": 1}]'), [{'a': 1}])

    def test_bracket_inside_string(self):
        self.assertEqual(
            extract_json_array('[{"text": "see [1] here"}, {"text": "done"}]'),
            [{'text': 'see [1] here'}, {'text': 'done'}])

    def test_brace_inside_string(self):
        self.assertEqual(extract_json_array('[{"t": "a {b} c"}]'), [{'t': 'a {b} c'}])

    def test_malformed_first_array_then_valid(self):
        # a junk line starting with '[' precedes the real array
        self.assertEqual(extract_json_array('[oops not json]\n[{"a": 1}]'), [{'a': 1}])

    def test_no_array(self):
        self.assertIsNone(extract_json_array('no brackets at all'))

    def test_empty_string(self):
        self.assertIsNone(extract_json_array(''))

    def test_escaped_quote_inside_string(self):
        self.assertEqual(extract_json_array('[{"t": "he said \\"hi\\" [x]"}]'),
                         [{'t': 'he said "hi" [x]'}])


class TestParseJson3(unittest.TestCase):
    def _write(self, data):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.json3', delete=False)
        json.dump(data, f)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_basic_events(self):
        path = self._write({'events': [
            {'tStartMs': 1000, 'dDurationMs': 2000, 'segs': [{'utf8': 'hello world'}]},
            {'tStartMs': 3000, 'dDurationMs': 1000, 'segs': [{'utf8': 'second'}]},
        ]})
        rows = parse_json3(path)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], {'start': 1.0, 'end': 3.0, 'text': 'hello world'})

    def test_skips_empty_events(self):
        path = self._write({'events': [
            {'tStartMs': 0, 'dDurationMs': 0, 'segs': [{'utf8': '\n'}]},
            {'tStartMs': 1000, 'dDurationMs': 500, 'segs': [{'utf8': 'real'}]},
        ]})
        rows = parse_json3(path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['text'], 'real')

    def test_flattens_real_newlines(self):
        path = self._write({'events': [
            {'tStartMs': 0, 'dDurationMs': 100, 'segs': [{'utf8': 'line one\nline two'}]},
        ]})
        rows = parse_json3(path)
        self.assertEqual(rows[0]['text'], 'line one line two')

    def test_flattens_literal_backslash_n(self):
        # YouTube sometimes ships literal backslash-n two-char sequences
        path = self._write({'events': [
            {'tStartMs': 0, 'dDurationMs': 100, 'segs': [{'utf8': 'line one\\nline two'}]},
        ]})
        rows = parse_json3(path)
        self.assertEqual(rows[0]['text'], 'line one line two')

    def test_multi_segment_join(self):
        path = self._write({'events': [
            {'tStartMs': 0, 'dDurationMs': 100, 'segs': [{'utf8': 'foo '}, {'utf8': 'bar'}]},
        ]})
        rows = parse_json3(path)
        self.assertEqual(rows[0]['text'], 'foo bar')


VTT_BASIC = """WEBVTT
Kind: captions
Language: en

00:00:01.200 --> 00:00:03.360
All right, so here we are

00:00:05.318 --> 00:00:07.974
and that's pretty much all there is to say
"""

VTT_NO_TRAILING_NEWLINE = """WEBVTT

00:00:01.200 --> 00:00:03.360
first cue

00:00:05.318 --> 00:00:07.974
last cue no trailing newline"""

VTT_ROLLING = """WEBVTT

00:00:01.000 --> 00:00:02.000
hello there

00:00:02.000 --> 00:00:03.000
hello there
my friends

00:00:03.000 --> 00:00:04.000
my friends
goodbye
"""

VTT_TAGS = """WEBVTT

00:00:01.000 --> 00:00:02.000 align:start position:0%
<c>tagged</c> text
"""


class TestParseVtt(unittest.TestCase):
    def _write(self, content):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.vtt', delete=False)
        f.write(content)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_basic_two_cues(self):
        rows = parse_vtt(self._write(VTT_BASIC))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['start'], 1.2)
        self.assertEqual(rows[0]['end'], 3.36)
        self.assertEqual(rows[0]['text'], 'All right, so here we are')

    def test_last_cue_without_trailing_newline(self):
        rows = parse_vtt(self._write(VTT_NO_TRAILING_NEWLINE))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]['text'], 'last cue no trailing newline')

    def test_rolling_dedup(self):
        rows = parse_vtt(self._write(VTT_ROLLING))
        texts = [r['text'] for r in rows]
        # each cue should contribute only its NEW line
        self.assertEqual(texts, ['hello there', 'my friends', 'goodbye'])

    def test_strips_inline_tags_and_cue_settings(self):
        rows = parse_vtt(self._write(VTT_TAGS))
        self.assertEqual(rows[0]['text'], 'tagged text')

    def test_wrapped_cue_lines_flattened(self):
        content = 'WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nline one\nline two\n'
        rows = parse_vtt(self._write(content))
        self.assertEqual(rows[0]['text'], 'line one line two')


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify('How to stay calm'), 'how-to-stay-calm')

    def test_all_punctuation(self):
        self.assertEqual(slugify('《【】》'), 'video')

    def test_whitespace_only(self):
        self.assertEqual(slugify('   '), 'video')

    def test_truncation(self):
        self.assertEqual(len(slugify('a' * 200)), 60)
        self.assertFalse(slugify('a' * 200).endswith('-'))

    def test_unicode_kept(self):
        # CJK chars are \w — preserved
        self.assertEqual(slugify('测试 视频'), '测试-视频')


class TestFmtTs(unittest.TestCase):
    def test_seconds_only(self):
        self.assertEqual(fmt_ts(5), '0:05')

    def test_minutes(self):
        self.assertEqual(fmt_ts(65), '1:05')

    def test_hours(self):
        self.assertEqual(fmt_ts(3723), '1:02:03')

    def test_zero(self):
        self.assertEqual(fmt_ts(0), '0:00')


if __name__ == '__main__':
    unittest.main(verbosity=2)
