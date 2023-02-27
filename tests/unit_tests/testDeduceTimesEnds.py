import unittest

from clip_generator.editter import info_processor


class TestDeduceTimesEnds(unittest.TestCase):

    def test_deduce_timestamps_start(self):
        input_clips = [(56, 57), (51, 52), (11, 12), (3, 54), (14, 17), (15, 18), (16, 20)]
        expected_output = [(0, 54), (14, 17), (15, 18), (16, 20)]
        result = info_processor.deduce_timestamps_ends(input_clips)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
