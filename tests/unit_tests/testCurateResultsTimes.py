import unittest

from clip_generator.editter.info_processor import curate_results


class TestCurateResults(unittest.TestCase):
    def test_curate_results(self):
        offset1 = [(5.14, 7.14), (29.10, 30.10), (24.38, 25.38), (9.16, 10.16), (23.1, 24.1), (11.16, 54.17)]
        expected_output1 = [(5.14, 54.17)]
        self.assertEqual(curate_results(offset1), expected_output1)

    def test_curate_results_ignore_consecutive_numbers_if_they_can_be_merged(self):
        offset2 = [(0.915125, 3.93525), (12.295875, 13.295875), (48.928, 49.928), (5.930625, 19.933875), (11.7425, 12.7425), (66.926875, 67.926875), (21.92925, 44.9185), (48.462125, 49.462125), (48.97725, 49.97725), (46.937125, 63.93725)]
        expected_output2 = [(0.915125, 63.93725)]
        self.assertEqual(curate_results(offset2), expected_output2)

    def test_curate_results_do_not_merge_if_there_is_not_an_appropriate_items_between_numbers(self):
        offset3 = [(5.14, 7.14), (9.16, 10.16), (11.16, 54.17)]
        expected_output3 = [(5.14, 7.14), (9.16, 54.17)]
        self.assertEqual(curate_results(offset3), expected_output3)


if __name__ == '__main__':
    unittest.main()
