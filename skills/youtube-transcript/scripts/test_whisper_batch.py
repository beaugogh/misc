#!/usr/bin/env python3
"""Unit tests for whisper_batch.py's video-ID parsing (no network, no models).

Run:  python3 skills/youtube-transcript/scripts/test_whisper_batch.py

Covers the resume bug fixed 2026-09-10: done_ids()/audio_path_for() used
rsplit('__', 1), which eats the leading '_' of IDs like '_IMww7gwIus'
(separator + ID merge into '___'), so completed videos were misdetected as
not-done and re-processed. Also covers the '-'-prefixed '-TDVKQjmf7c'.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whisper_batch as wb  # noqa: E402


class TestVideoIdFrom(unittest.TestCase):
    def test_normal_id(self):
        self.assertEqual(wb.video_id_from('2019-10-02__超出你想象的深海世界__dNmwPWRdv_0'), 'dNmwPWRdv_0')

    def test_underscore_leading_id_dir(self):
        # separator '__' + ID '_IMww7gwIus' = '___IMww7gwIus' — rsplit used to eat the '_'
        self.assertEqual(wb.video_id_from('2021-10-13__普通人成为有钱人的唯一方法___IMww7gwIus'), '_IMww7gwIus')

    def test_underscore_leading_id_audio_file(self):
        self.assertEqual(
            wb.video_id_from('2021-10-13__普通人成为有钱人的唯一方法___IMww7gwIus.webm'),
            '_IMww7gwIus')

    def test_dash_leading_id(self):
        self.assertEqual(wb.video_id_from('2020-11-04__目前信息量最大的一期，重力__-TDVKQjmf7c'), '-TDVKQjmf7c')

    def test_dash_leading_id_audio_file(self):
        self.assertEqual(
            wb.video_id_from('2020-11-04__目前信息量最大的一期，重力__-TDVKQjmf7c.m4a'),
            '-TDVKQjmf7c')

    def test_audio_extensions_all_recognized(self):
        stem = '2021-08-11__超出你想象的地球故事__'
        for ext in ('.webm', '.m4a', '.opus', '.mp3'):
            self.assertEqual(wb.video_id_from(stem + '5AseSLCG7wI' + ext), '5AseSLCG7wI', ext)

    def test_non_id_names_return_none(self):
        for name in ('README.md', 'todo.md', '._2023-03-08__某标题__XMyJ1F8MsRY.txt',
                     '2019-10-02__超出你想象的深海世界__short', 'laogao-channel-catalog.json'):
            self.assertIsNone(wb.video_id_from(name), name)

    def test_id_charset_enforced(self):
        # 11 chars but containing '.' — not a valid ID tail
        self.assertIsNone(wb.video_id_from('2019-10-02__标题__abc.def.ghi'))

    def test_done_ids_and_audio_path_for_integration(self):
        """dir/file listing integration against a temp tree shaped like output/."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            wdir = os.path.join(tmp, 'whisper')
            adir = os.path.join(tmp, 'audio')
            os.makedirs(os.path.join(wdir, '2021-10-13__有钱人___IMww7gwIus'))
            os.makedirs(os.path.join(wdir, '2020-11-04__重力__-TDVKQjmf7c'))
            os.makedirs(os.path.join(wdir, '2019-10-02__深海__dNmwPWRdv_0'))
            os.makedirs(os.path.join(wdir, 'junk-no-id'))
            os.makedirs(adir)
            for n in ('2021-10-13__有钱人___IMww7gwIus.webm',
                      '2020-11-04__重力__-TDVKQjmf7c.m4a'):
                open(os.path.join(adir, n), 'w').close()
            open(os.path.join(adir, 'not-a-video.txt'), 'w').close()

            old_a = wb.AUDIO_DIR
            wb.AUDIO_DIR = adir
            try:
                ids = wb.done_ids(wdir)  # out_dir is now an explicit arg
                self.assertIn('_IMww7gwIus', ids)   # the bug: was 'IMww7gwIus'
                self.assertIn('-TDVKQjmf7c', ids)
                self.assertIn('dNmwPWRdv_0', ids)
                self.assertNotIn('IMww7gwIus', ids)
                self.assertNotIn('TDVKQjmf7c', ids)
                self.assertEqual(len(ids), 3)        # junk-no-id must not count

                self.assertTrue(wb.audio_path_for('_IMww7gwIus').endswith(
                    '2021-10-13__有钱人___IMww7gwIus.webm'))
                self.assertTrue(wb.audio_path_for('-TDVKQjmf7c').endswith(
                    '2020-11-04__重力__-TDVKQjmf7c.m4a'))
                self.assertIsNone(wb.audio_path_for('dNmwPWRdv_0'))  # no audio file
            finally:
                wb.AUDIO_DIR = old_a


if __name__ == '__main__':
    unittest.main(verbosity=2)
