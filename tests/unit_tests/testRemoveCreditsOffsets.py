import unittest
from unittest.mock import patch
from clip_generator.editter.trimmer import remove_credits_offsets
from tests.configs import setUpModule


class TestRemoveCreditsOffsets(unittest.TestCase):

    @patch('clip_generator.editter.chopper.chop')
    @patch('clip_generator.editter.chopper.remove_video')
    @patch('clip_generator.common_functions.getDuration', return_value=110)
    def test_remove_credits_offsets(self, mock_remove_video, mock_chop, mock_getduration):
        # Mock the input arguments for the function
        start_offset = '10'
        end_offset = '20'

        # Call the function
        remove_credits_offsets(start_offset, end_offset)

        # Check that chopper.chop() was called with the expected arguments
        expected_chop_args = ('tests/Examples/clip.mkv', 'tests/Clips/temp/clip_audio_with_offsets.mp4', '10', '110')
        #mock_chop.assert_called_once_with(*expected_chop_args)

        # Check that chopper.remove_video() was called with the expected arguments
        expected_remove_video_args = ('tests/Clips/temp/clip_audio.mp4', 'dirs/dir_temp_files/clip_audio_with_offsets.mp4')
        actual_remove_video_args = mock_remove_video.call_args[0]
        print(mock_remove_video.call_args)
        self.assertEqual(actual_remove_video_args, expected_remove_video_args)


if __name__ == '__main__':
    unittest.main()
