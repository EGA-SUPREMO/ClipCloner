import unittest

from pathlib import Path

import clip_generator.editter.chopper
import clip_generator.editter.trimmer as trimmer
import clip_generator.editter.dirs as dirs

from clip_generator.common_functions import getDuration
from tests.configs import setUpModule
import tests.configs as configs


class TestTrimmerGeneratesFilesWithRightDuration(unittest.TestCase):

    def setUp(self) -> None:
        setUpModule()

    def test_trim_to_clip_match_duration_as_example(self):
        dirs.dir_clip = configs.example_test_folder + "clip.mkv"
        dirs.dir_stream = configs.example_test_folder + "stream.mkv"
        dirs.dir_audio_clip = dirs.dir_temp_files + "audio_clip.mp4"

        clip_generator.editter.chopper.remove_credits_offsets("0", "0")
        start, end = trimmer.trim_to_clip(True)

        duration = end - start

        self.assertAlmostEqual(103.7, float(duration), delta=0.1, msg="REAL Trimmed stream doesnt match duration")

    def test_trim_to_clip_match_duration_as_example_from_worstaudio_with_1_second(self):
        dirs.dir_clip = configs.example_test_folder + "clip_fubu.mkv"
        dirs.dir_worstaudio_stream = configs.example_test_folder + "worstaudio_stream.mkv"
        dirs.dir_audio_clip = dirs.dir_temp_files + "audio_clip.mp4"

        clip_generator.editter.chopper.remove_credits_offsets("0", "0")
        from_second, to_second = trimmer.trim_to_clip(False, 0, 1)
        self.assertAlmostEqual(2853.94, from_second, delta=0.1, msg="REAL Trimmed stream from worstaudio doesnt match duration")
        self.assertAlmostEqual(3092.89, to_second, delta=0.1, msg="REAL Trimmed stream from worstaudio doesnt match duration")


if __name__ == '__main__':
    unittest.main()
