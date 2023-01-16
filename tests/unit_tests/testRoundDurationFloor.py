import math
import os
import unittest

from clip_generator.common_functions import getDuration
from clip_generator.editter import dirs
from clip_generator.editter.chopper import round_duration_cutting_existing_video_for_compare_image
from tests import configs


class TestRoundDurationFloor(unittest.TestCase):
    def test_round_duration_cutting_existing_video1(self):
        input_file = configs.example_test_folder + "clip_audio.mp4"
        output_file = dirs.dir_temp_files + "output_audio.mp4"
        returning_duration = round_duration_cutting_existing_video_for_compare_image(input_file, output_file)

        # Calculate the expected duration of the output file
        input_duration = getDuration(input_file)
        expected_duration = math.floor(input_duration - 0.5 - 1)

        # Check that the output file has the expected duration
        self.assertAlmostEqual(expected_duration, getDuration(output_file), delta=0.001)
        self.assertAlmostEqual(expected_duration, returning_duration, delta=0.001)

        os.remove(output_file)

    def test_round_duration_cutting_existing_video2(self):
        input_file = configs.example_test_folder + "stream_audio.mp4"
        output_file = dirs.dir_temp_files + "output_audio2.mp4"
        returning_duration = round_duration_cutting_existing_video_for_compare_image(input_file, output_file)

        # Calculate the expected duration of the output file
        input_duration = getDuration(input_file)
        expected_duration = math.floor(input_duration - 0.5 - 1)

        # Check that the output file has the expected duration
        self.assertAlmostEqual(expected_duration, getDuration(output_file), delta=0.001)
        self.assertAlmostEqual(expected_duration, returning_duration, delta=0.001)

        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
