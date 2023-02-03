import unittest


def remove_wrong_tuples(tuples_input):
    ends = []
    result = []
    for t in tuples_input:
        if t[0] not in ends:
            ends.append(t[1])
            result.append(t)
    return result


class TestRemoveWrongTuples(unittest.TestCase):
    def test_remove_wrong_tuples(self):
        tuples_input = [[0, 3], [0, 6], [0, 9], [3, 6], [3, 9], [6, 9]]
        tuples_expected_output = [[0, 3], [0, 6], [0, 9]]
        self.assertEqual(remove_wrong_tuples(tuples_input), tuples_expected_output)

    def test_empty_input(self):
        tuples_input = []
        tuples_expected_output = []
        self.assertEqual(remove_wrong_tuples(tuples_input), tuples_expected_output)

    def test_single_tuple(self):
        tuples_input = [[0, 3]]
        tuples_expected_output = [[0, 3]]
        self.assertEqual(remove_wrong_tuples(tuples_input), tuples_expected_output)

    def test_repeated_tuples(self):
        tuples_input = [[0, 3], [0, 6], [0, 9], [3, 6], [3, 9], [6, 9], [0, 9]]
        tuples_expected_output = [[0, 3], [0, 6], [0, 9]]
        self.assertEqual(remove_wrong_tuples(tuples_input), tuples_expected_output)


if __name__ == '__main__':
    unittest.main()
