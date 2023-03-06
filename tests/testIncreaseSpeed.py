import os
import unittest

from clip_generator.editter import chopper, dirs
from clip_generator.common_functions import getDuration
from tests.configs import setUpModule


class TestCutVideoIntoSeparateFiles(unittest.TestCase):
    def test_increase_speed_video(self):
        chopper.increase_speed_video(dirs.dir_stream, dirs.dir_clip_with_speed)
        self.assertTrue(os.path.exists(dirs.dir_clip_with_speed))

        clip_duration = getDuration(dirs.dir_stream)
        clip_with_speed_duration = getDuration(dirs.dir_clip_with_speed)

        self.assertAlmostEqual(clip_duration * 0.91, clip_with_speed_duration, delta=0.15)


if __name__ == '__main__':
    unittest.main()
