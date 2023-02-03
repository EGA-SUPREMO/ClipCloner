import unittest

from clip_generator.editter.info_processor import remove_tuples_with_starts_below_previous_ends


class TestRemoveWrongTuples(unittest.TestCase):
    def test_remove_wrong_tuples(self):
        tuples_input = [[0, 3], [0, 6], [0, 9], [3, 6], [3, 9], [6, 9]]
        tuples_expected_output = [[0, 3], [0, 6], [0, 9]]
        self.assertEqual(remove_tuples_with_starts_below_previous_ends(tuples_input), tuples_expected_output)

    def test_remove_wrong_tuples_in_different_order(self):
        tuples_input = [[0, 6], [0, 3], [0, 9], [6, 9], [3, 9], [3, 6]]
        tuples_expected_output = [[0, 6], [0, 3], [0, 9]]
        self.assertEqual(remove_tuples_with_starts_below_previous_ends(tuples_input), tuples_expected_output)

    def test_empty_input(self):
        tuples_input = []
        tuples_expected_output = []
        self.assertEqual(remove_tuples_with_starts_below_previous_ends(tuples_input), tuples_expected_output)

    def test_single_tuple(self):
        tuples_input = [[0, 3]]
        tuples_expected_output = [[0, 3]]
        self.assertEqual(remove_tuples_with_starts_below_previous_ends(tuples_input), tuples_expected_output)

    def test_dont_remove_repeated_tuples(self):
        tuples_input = [[0, 3], [0, 6], [0, 9], [3, 6], [3, 9], [6, 9], [0, 9]]
        tuples_expected_output = [[0, 3], [0, 6], [0, 9], [0, 9]]
        self.assertEqual(remove_tuples_with_starts_below_previous_ends(tuples_input), tuples_expected_output)


if __name__ == '__main__':
    unittest.main()
