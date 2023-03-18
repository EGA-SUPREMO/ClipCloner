import unittest
from unittest.mock import patch
import clip_generator.editter.trimmer as trimmer
from tests.configs import setUpModule


class TestRemoveCreditsOffsets(unittest.TestCase):

    def setUp(self) -> None:
        setUpModule()

    @patch('clip_generator.editter.chopper.chop')
    @patch('clip_generator.editter.chopper.remove_video')
    @patch('clip_generator.common_functions.getDuration', return_value=110)
    def test_remove_credits_offsets(self, mock_getduration, mock_remove_video, mock_chop):
        # Mock the input arguments for the function
        start_offset = '10'
        end_offset = '20'

        # Call the function
        trimmer.remove_credits_offsets(start_offset, end_offset)

        # Check that chopper.chop() was called with the expected arguments
        expected_chop_args = ('tests/Examples/clip.mkv', 'tests/Clips/temp/clip_with_offsets.mkv', '10', '90')
        mock_chop.assert_called_once_with(*expected_chop_args)

        # Check that chopper.remove_video() was called with the expected arguments
        expected_remove_video_args = ('tests/Clips/temp/clip_with_offsets.mkv', 'tests/Clips/temp/clip_audio_with_offsets.mp4')
        actual_remove_video_args = mock_remove_video.call_args[0]

        self.assertEqual(actual_remove_video_args, expected_remove_video_args)

    @patch('clip_generator.editter.chopper.remove_video')
    @patch('clip_generator.common_functions.getDuration', return_value=110)
    def test_remove_credits_offsets_does_nothing_when_there_arent_offsets(self, mock_getduration, mock_remove_video):
        # Mock the input arguments for the function
        start_offset = '0'
        end_offset = '0'

        # Call the function
        trimmer.remove_credits_offsets(start_offset, end_offset)

        # Check that chopper.remove_video() was called with the expected arguments
        expected_remove_video_args = ('tests/Examples/clip.mkv', 'tests/Clips/temp/clip_audio.mp4')
        actual_remove_video_args = mock_remove_video.call_args[0]

        self.assertEqual(actual_remove_video_args, expected_remove_video_args)


if __name__ == '__main__':
    unittest.main()
