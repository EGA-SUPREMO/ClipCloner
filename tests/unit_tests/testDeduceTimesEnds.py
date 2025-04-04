import unittest

from clip_generator.editter import info_processor, dirs


class TestDeduceTimesEnds(unittest.TestCase):

    def test_deduce_timestamps_start(self):
        dirs.update_phase_edit(1)

        input_clips = [(56, 57), (51, 52), (11, 12), (3, 54), (14, 17), (15, 18), (16, 20)]
        expected_output = [(0, 54), (14, 17), (15, 18), (16, 20)]
        result = info_processor.deduce_timestamps_start(input_clips)
        self.assertEqual(result, expected_output)

    def test_deduce_timestamps_end(self):
        dirs.current_duration_clip = 59
        dirs.update_phase_edit(1)

        input_clips = [(56, 57), (51, 52), (11, 12), (3, 54), (14, 15), (17, 18), (16, 17), (154, 155), (120, 121)]
        expected_output = [(56, 57), (51, 52), (11, 12), (3, 59)]
        result = info_processor.deduce_timestamps_end(input_clips)
        self.assertEqual(result, expected_output)

    def test_deduce_timestamps_end_without_enough_duration(self):
        dirs.current_duration_clip = 58
        dirs.update_phase_edit(1)

        input_clips = [(56, 57), (51, 52), (11, 12), (5, 54), (14, 15), (17, 18), (16, 17), (154, 155), (120, 121)]
        expected_output = [(56, 57), (51, 52), (11, 12), (5, 54), (14, 15), (17, 18), (16, 17), (154, 155), (120, 121)]
        result = info_processor.deduce_timestamps_end(input_clips)
        self.assertEqual(result, expected_output)

    def test_deduce_timestamps_end_with_no_duration(self):
        dirs.current_duration_clip = 0
        dirs.update_phase_edit(1)

        input_clips = [(56, 57), (51, 52), (11, 12), (3, 54), (14, 15), (17, 18), (16, 17), (154, 155), (120, 121)]
        expected_output = [(56, 57), (51, 52), (11, 12), (3, 54), (14, 15), (17, 18), (16, 17), (154, 155), (120, 121)]
        result = info_processor.deduce_timestamps_end(input_clips)
        self.assertEqual(result, expected_output)

    def test_deduce_timestamps_end_with_wrong_duration(self):
        dirs.current_duration_clip = 59
        dirs.update_phase_edit(1)

        input_clips = [(56, 57), (51, 52), (11, 12), (3, 53), (14, 15), (17, 18), (16, 17), (154, 155), (120, 121)]
        expected_output = [(56, 57), (51, 52), (11, 12), (3, 53), (14, 15), (17, 18), (16, 17), (154, 155), (120, 121)]
        result = info_processor.deduce_timestamps_end(input_clips)
        self.assertEqual(result, expected_output)

    def test_deduce_timestamps_start1(self):
        dirs.current_duration_clip = 58
        dirs.update_phase_edit(1)

        input_clips = [(51, 52), (11, 12), (2, 53)]
        expected_output = [(0, 53)]
        result = info_processor.deduce_timestamps_start(input_clips)
        self.assertEqual(result, expected_output)

    def test_deduce_timestamps_start_with_negative_value(self):
        dirs.current_duration_clip = 58
        dirs.update_phase_edit(1)

        input_clips = [(51, 52), (11, 12), (1.5, 53)]
        expected_output = [(-0.5, 53)]
        result = info_processor.deduce_timestamps_start(input_clips)
        self.assertEqual(result, expected_output)

    def test_deduce_timestamps_end_with_negative_value(self):
        dirs.current_duration_clip = 244
        dirs.update_phase_edit(1)

        input_clips = [(200, 243.5), (11, 12)]
        expected_output = [(200, 244.5)]
        result = info_processor.deduce_timestamps_end(input_clips)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
