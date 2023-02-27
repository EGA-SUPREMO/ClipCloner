import unittest
from unittest.mock import patch

from clip_generator.editter import dirs
from clip_generator.editter.trimmer import get_correlation


class TestGetCorrelationTrimmer(unittest.TestCase):

    def test_correlation_above_threshold(self):
        # Test the case where both start and end correlation are above 0.8
        start_correlation = 0.9
        end_correlation = 0.9
        input_stream = "input_stream"
        expected_output = (start_correlation, end_correlation, dirs.dir_start_only_untrimmed_stream)

        def mock_chop(*args):
            pass

        def mock_find_limits_for_trim(*args):
            return 0, 10

        def mock_exist(*args):
            return dirs.dir_end_only_untrimmed_stream == args[0]

        with unittest.mock.patch("clip_generator.editter.trimmer.find_limits_for_trim",
                                 side_effect=mock_find_limits_for_trim):
            with unittest.mock.patch("clip_generator.editter.chopper.chop", side_effect=mock_chop):
                with unittest.mock.patch("os.path.exists", side_effect=mock_exist):
                    # Call the function with the given inputs
                    output = get_correlation(end_correlation, input_stream, start_correlation)

        # Check that the output matches the expected output
        self.assertEqual(output, expected_output)

    def test_correlation_below_threshold(self):
        # Test the case where both start and end correlation are below 0.8
        start_correlation = 0.7
        end_correlation = 0.6
        input_stream = "input_stream"
        expected_output = (0.9, 0.9, dirs.dir_end_only_untrimmed_stream)

        # Mock the calls to other functions to return expected values
        def mock_check_correlation_for_trim(*args):
            return 0.9

        def mock_set_audio_infos_trim_start(*args):
            return

        def mock_set_audio_infos_trim_end(*args):
            return

        def mock_find_limits_for_trim(*args):
            return 0, 10

        def mock_chop(*args):
            pass
        def mock_exist(*args):
            return False

        with unittest.mock.patch("clip_generator.editter.trimmer.check_correlation_for_trim", side_effect=mock_check_correlation_for_trim):
            with unittest.mock.patch("clip_generator.editter.trimmer.find_limits_for_trim", side_effect=mock_find_limits_for_trim):
                with unittest.mock.patch("clip_generator.editter.chopper.chop", side_effect=mock_chop):
                    with unittest.mock.patch("clip_generator.editter.audio_info.set_audio_infos_trim_start", side_effect=mock_set_audio_infos_trim_start):
                        with unittest.mock.patch("clip_generator.editter.audio_info.set_audio_infos_trim_end", side_effect=mock_set_audio_infos_trim_end):
                            with unittest.mock.patch("os.path.exists", side_effect=mock_exist):
                                # Call the function with the given inputs
                                output = get_correlation(end_correlation, input_stream, start_correlation)

        # Check that the output matches the expected output
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
