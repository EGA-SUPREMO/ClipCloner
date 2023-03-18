import os
import subprocess
import unittest

from clip_generator import common_functions
from clip_generator.editter import chopper, dirs
from tests.configs import setUpModule


class TestChopperCutsWithRightDuration(unittest.TestCase):

    def test_cut_video_without_filter_complex_has_correct_duration(self):
        chopper.cut_video(dirs.dir_clip, dirs.dir_temp_files + "test_cut_video.mkv", 6.5, 3)
        self.assertTrue(os.path.exists(dirs.dir_temp_files + "test_cut_video.mkv"))
        # check that the output video has the expected duration
        duration = common_functions.getDuration(dirs.dir_temp_files + "test_cut_video.mkv")
        self.assertAlmostEqual(3, duration, delta=0.1)


if __name__ == "__main__":
    unittest.main()
