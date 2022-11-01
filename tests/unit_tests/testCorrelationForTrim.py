import unittest

from pathlib import Path

import clip_generator.editter.trimmer as trimmer
import clip_generator.editter.dirs as dirs
import clip_generator.editter.audio_info as audio_info

from clip_generator.common_functions import getDuration

from tests.runner import setUpModule


class TestCorrelationForTrim(unittest.TestCase):

    def setUp(self) -> None:
        setUpModule()
        audio_info.infosTrim = [[[[], {'pad': 0}]], [[[], {'pad_post': 0}]]]

        audio_info.infosTrim[0][0][1]['pad'] = 10.048
        audio_info.infosTrim[1][0][1]['pad_post'] = 7.302666666666667

    def test_finding_limits_for_trim(self):
        dirs.update_phase(0)

        from_second, to_second = trimmer.find_limits_for_trim("only_start")
        self.assertEqual(from_second, 10.048, msg="From second in only start type aren't equal to expected")
        self.assertEqual(to_second, 10.048 + dirs.get_second(),
                         msg="To second in only start type aren't equal to expected")

        from_second, to_second = trimmer.find_limits_for_trim("only_end")
        self.assertEqual(from_second, 113.72033333333333 - dirs.get_second(),
                         msg="From second in only end type aren't equal to expected")
        self.assertEqual(to_second, 113.72033333333333, msg="To second in only end type aren't equal to expected")

        from_second, to_second = trimmer.find_limits_for_trim("full")
        self.assertEqual(from_second, 10.048, msg="From second in full type aren't equal to expected")
        self.assertEqual(to_second, 113.72033333333333, msg="To second in full type aren't equal to expected")

    def test_correlation_for_trim_start(self):
        dir_test_start_clip = "tests/Examples/S03_clip_audio0.mp4"
        dirs.dir_audio_stream = "tests/Examples/stream_audio.mp4"


        correlation = trimmer.check_correlation_at(audio_info.infosTrim[0][0][1]['pad'],
                                     audio_info.infosTrim[0][0][1]['pad'] + dirs.get_second(),
                                     dirs.dir_current_start_stream, dir_test_start_clip)

        self.assertEqual(correlation, 0.8594182825484764, msg="check_correlation at doesnt match expected value")
        dirs.dir_audio_stream = dirs.dir_temp_files + "stream_audio.mp4"

if __name__ == '__main__':
    unittest.main()
