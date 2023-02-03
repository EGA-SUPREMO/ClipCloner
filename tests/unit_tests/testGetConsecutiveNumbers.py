import unittest

from clip_generator.editter.info_processor import get_consecutive_number


class TestGetConsecutiveNumber(unittest.TestCase):
    def test_get_consecutive_number(self):
        offsets = [(0.915125, 3.93525), (12.295875, 13.295875), (48.928, 49.928), (5.930625, 19.933875),
                   (11.7425, 12.7425), (66.926875, 67.926875), (21.92925, 44.9185), (48.462125, 49.462125),
                   (48.97725, 49.97725), (46.937125, 63.93725)]
        i = 0
        j = 3
        expected_result = 2
        result = get_consecutive_number(offsets, i, j)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
