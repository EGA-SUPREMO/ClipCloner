import unittest
from unittest import TestCase
from unittest.mock import patch

import clip_generator.editter.trimmer as trimmer
import clip_generator.editter.dirs as dirs
import clip_generator.editter.audio_info as audio_info

from tests.configs import setUpModule
from tests.configs import tearDownModule


class TestCorrelationForTrim(unittest.TestCase):

    def setUp(self) -> None:
        setUpModule()
        audio_info.infosTrim = [[[[], {'pad': 0}]], [[[], {'pad_post': 0}]]]

        audio_info.infosTrim[0][0][1]['pad'] = 10.548
        audio_info.infosTrim[1][0][1]['pad_post'] = 7.302666666666667

    def tearDown(self) -> None:
        tearDownModule()

    def test_finding_limits_for_trim(self):
        dirs.update_phase(0)
        trimmer.current_stream = dirs.dir_stream

        from_second, to_second = trimmer.find_limits_for_trim("only_start")
        self.assertEqual(from_second, 10.548, msg="From second in only start type aren't equal to expected")
        self.assertEqual(to_second, 10.548 + dirs.get_second(),
                         msg="To second in only start type aren't equal to expected")

        from_second, to_second = trimmer.find_limits_for_trim("only_end")
        self.assertEqual(from_second, 112.72033333333333 - dirs.get_second(),
                         msg="From second in only end type aren't equal to expected")
        self.assertEqual(to_second, 112.72033333333333, msg="To second in only end type aren't equal to expected")

        from_second, to_second = trimmer.find_limits_for_trim("full")
        self.assertEqual(from_second, 10.048, msg="From second in full type aren't equal to expected")
        self.assertEqual(to_second, 113.72033333333333, msg="To second in full type aren't equal to expected")

    def test_correlation_for_trim_start(self):
        dir_test_start_clip = "tests/Examples/S3_clip_audio0.mp4"
        dirs.dir_audio_stream = "tests/Examples/stream_audio.mp4"
        dirs.update_phase(0)

        correlation = trimmer.check_correlation_at(audio_info.infosTrim[0][0][1]['pad'],
                                                   audio_info.infosTrim[0][0][1]['pad'] + dirs.get_second(),
                                                   dirs.dir_audio_stream, dirs.dir_current_start_stream,
                                                   dir_test_start_clip)

        self.assertAlmostEqual(correlation, 0.91, 1, msg="check_correlation at doesnt match expected value")
        dirs.dir_audio_stream = dirs.dir_temp_files + "stream_audio.mp4"

    @patch('clip_generator.editter.audio_info.get_alignment_info')
    # @patch('clip_generator.editter.chopper.chop')
    def test_find_timestamps(self, get_alignment_info_mock):
        dirs.update_phase(1)
        dirs.dir_audio_stream = "tests/Examples/stream_audio.mp4"
        dirs.dir_audio_clip = "tests/Examples/clip_audio.mp4"
        dirs.dir_current_start_stream = "tests/Examples/start_stream.mp4"
        dirs.dir_current_end_stream = "tests/Examples/end_stream.mp4"
        dirs.dir_current_start_clip = "tests/Examples/S3_clip_audio0.mp4"
        dirs.dir_current_end_clip = "tests/Examples/last_S3_clip_audio.mp4"

        trimmer.current_stream = dirs.dir_stream

        get_alignment_info_mock.return_value = [[[], {'pad': 10.048, 'pad_post': 7.302666666666667}]]
        _, _, start_corr, end_corr = trimmer.find_timestamps_for_trim(True)
        self.assertAlmostEqual(start_corr, 0.859, 2,
                               msg="Start correlation is not equal to expected " + str(start_corr))
        self.assertAlmostEqual(end_corr, 0.859, 2,
                               msg="End correlation is not equal to expected " + str(end_corr))

        dirs.dir_audio_stream = dirs.dir_temp_files + "stream_audio.mp4"
        dirs.dir_audio_clip = dirs.dir_temp_files + "clip_audio.mp4"
        dirs.dir_current_start_stream = dirs.dir_temp_files + "start_stream.mp4"
        dirs.dir_current_start_clip = dirs.dirFixedAudioParts + "S03_clip_audio0.mp4"
        dirs.dir_current_end_clip = dirs.dirFixedAudioParts + "last_S3_clip_audio.mp4"
        dirs.dir_current_end_stream = dirs.dir_temp_files + "end_stream.mp4"

    @patch('clip_generator.editter.audio_info.get_alignment_info')
    @patch('clip_generator.editter.audio_info.get_last_seconds_for_ffmpeg_argument_to')
    @patch('clip_generator.editter.chopper.chop')
    @patch('clip_generator.editter.chopper.slow_audio')
    @patch('clip_generator.editter.correlation.correlate')
    def test_clip_duration_is_larger_than_stream_duration_raises_exception(self, correlate_mock, slow_audio_mock,
                                                                           chop_mock,
                                                                           get_last_seconds_for_ffmpeg_argument_to_mock,
                                                                           get_alignment_info_mock):
        dirs.dir_audio_clip = "tests/Examples/clip_audio.mp4"

        get_alignment_info_mock.return_value = [[[], {'pad': 20, 'pad_post': 50}]]
        correlate_mock.return_value = 0.2
        get_last_seconds_for_ffmpeg_argument_to_mock.return_value = 60

        TestCase.assertRaises(self, Exception, trimmer.find_timestamps_for_trim, True, 10)

        dirs.dir_audio_clip = dirs.dir_temp_files + "clip_audio.mp4"


if __name__ == '__main__':
    unittest.main()
