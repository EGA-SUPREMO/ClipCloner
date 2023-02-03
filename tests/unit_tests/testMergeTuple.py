import unittest

from clip_generator.editter import dirs
from clip_generator.editter.info_processor import merge_tuple


class TestMergeTuple(unittest.TestCase):
    def test_merge_tuple_with_overlaps(self):
        offset_times = [(5.14, 7.14), (29.10, 30.10), (24.38, 25.38), (9.16, 10.16), (23.1, 24.1), (11.16, 54.17)]
        offset1 = [[0, 3], [0, 5], [3, 5]]
        expected_output1 = [[0, 5]]
        self.assertEqual(merge_tuple(offset1, offset_times), expected_output1)

    def test_merge_multiple_tuples(self):
        offset2 = [[0, 3], [3, 6], [6, 9]]
        offset_times = [(2.372125, 5.39225), (7.124125, 11.1195), (13.117875, 17.11325), (26.895125, 28.8935),
                   (30.758625, 37.772625), (40.43775, 44.433125), (49.664875, 55.65725), (69.781125, 70.781125),
                   (50.30375, 51.30375), (53.418, 54.418), (71.660125, 72.660125), (42.76025, 43.76025),
                   (65.521125, 74.508875), (69.247625, 70.247625), (68.871625, 69.871625), (34.316625, 36.316625)]
        expected_output2 = [[0, 9]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_multiple_tuples1(self):
        offset2 = [[0, 3], [0, 6], [0, 9], [3, 6], [3, 9], [6, 9]]
        offset_times = [(0.915125, 3.93525), (12.295875, 13.295875), (48.928, 49.928), (5.930625, 19.933875),
                        (11.7425, 12.7425), (66.926875, 67.926875), (21.92925, 44.9185), (48.462125, 49.462125),
                        (48.97725, 49.97725), (46.937125, 63.93725)]
        expected_output2 = [[0, 9]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_multiple_tuples_without_using_times(self):
        offset2 = [[0, 3], [3, 6], [6, 9], [10, 15], [15, 18], [18, 21]]
        offset_times = [(2.372125, 5.39225)]
        expected_output2 = [[0, 9], [10, 21]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_multiple_tuples_do_not_support_multi_pov_stream_or_non_chronological_order(self):
        offset2 = [[0, 3], [3, 6], [6, 9], [10, 15], [15, 18], [18, 21], [7, 16]]
        offset_times = [(2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225),
                        (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225),
                        (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225),
                        (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225),
                        (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225), (2.372125, 5.39225),
                        (2.372125, 5.39225), (2.372125, 5.39225)]
        expected_output2 = [[0, 9], [10, 21]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_tuple_overlaps_with_false_tuple(self):
        offset_times = [(5, 10), (20, 21), (11, 13), (22, 23)]
        offset2 = [[0, 2], [1, 3]]
        expected_output2 = [[0, 2]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_tuple_overlaps_with_false_tuple1(self):
        offset_times = [(9, 10), (19, 21), (11, 13), (22, 24)]
        offset2 = [[0, 2], [1, 3]]
        expected_output2 = [[1, 3]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_tuple_overlaps_with_false_tuple5(self):
        offset_times = [(9, 10), (19, 21), (11, 13), (23, 24)]
        offset2 = [[0, 2], [1, 3]]
        expected_output2 = [[1, 3]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_tuple_overlaps_with_false_tuple2(self):
        offset_times = [(8, 10), (19, 21), (11, 13), (22, 25)]
        offset2 = [[0, 2], [1, 3]]
        expected_output2 = [[1, 3]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    # TODO PARece que sta mal el valor esperado
    def test_merge_tuple_overlaps_with_false_tuple3(self):
        offset_times = [(8, 10), (19, 21), (11, 14), (22, 24)]
        offset2 = [[0, 2], [1, 3]]
        expected_output2 = [[0, 2]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_tuple_overlaps_with_false_tuple4(self):
        offset_times = [(8, 10), (19, 21), (12, 15), (22, 24)]
        offset2 = [[0, 2], [1, 3]]
        expected_output2 = [[0, 2]]
        self.assertEqual(merge_tuple(offset2, offset_times), expected_output2)

    def test_merge_tuple_returns_if_index_is_empty(self):
        offset_times = []
        offset2 = []
        self.assertEqual(merge_tuple(offset2, offset_times), None)


if __name__ == '__main__':
    unittest.main()
