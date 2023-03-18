import math
import unittest
import os.path
from unittest.mock import patch, call

import clip_generator.editter.chopper as chopper
from clip_generator import common_functions
from clip_generator.editter import dirs


class TestCutAudioIntoXTime(unittest.TestCase):

    @patch("clip_generator.common_functions.getDuration", return_value=30.0)
    @patch("clip_generator.editter.chopper.cut_video")
    def test_cut_audio_into_x_time_parts(self, mock_cut_video, mock_getduration):
        # Create a sample input video file for testing
        input_file = dirs.dir_audio_stream

        # Call the function to split the video into parts
        dirs.max_duration_for_stream_trimmer = 10.0
        dirs.update_phase(1)
        chopper.cut_audio_into_x_time_parts()
        input_duration = common_functions.getDuration(dirs.dir_audio_stream)
        part_files = common_functions.calculate_part_audio_files(input_duration, dirs.max_duration_for_stream_trimmer)

        expected_calls = [
            call(input_file, f"{dirs.dirAudioParts}stream_audio_0.mp4", 0.0, 13.0),
            call(input_file, f"{dirs.dirAudioParts}stream_audio_1.mp4", 10.0, 13.0),
            call(input_file, f"{dirs.dirAudioParts}stream_audio_2.mp4", 20.0, 13.0)
        ]
        # Check that the correct number of part files were created
        self.assertEqual(part_files, len(expected_calls))

        # Check that each part file exists and has the correct duration
        self.assertEqual(mock_cut_video.call_args_list, expected_calls)


if __name__ == "__main__":
    unittest.main()
