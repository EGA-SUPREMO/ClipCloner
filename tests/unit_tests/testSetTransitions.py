import unittest

from clip_generator.editter.info_processor import set_transitions


class TestSetTransitions(unittest.TestCase):
    def test_set_transitions(self):
        times = [(83.21625, 90.207), (1290.893, 1291.893), (483.314, 494.32175), (281.37075, 282.37075),
                 (789.127, 790.127), (866.378, 871.39525)]
        expected_output = [(83.21625, 90.707), (482.814, 494.32175), (281.37075, 282.37075), (789.127, 790.127),
                           (866.378, 871.39525)]

        self.assertEqual(set_transitions(times), expected_output)

    def test_set_transitions1(self):
        times = [(83.21625, 90.207), (1290.893, 1291.893), (483.314, 494.32175), (866.378, 871.39525)]
        expected_output = [(83.21625, 90.707), (482.814, 494.32175), (866.378, 871.39525)]

        self.assertEqual(set_transitions(times), expected_output)

    def test_set_transitions2(self):
        times = [(0.05625, 13.0625), (24.17775, 30.19325), (34.375, 49.37675), (230.884, 231.884),
                 (94.822, 112.819), (251.595, 268.5935), (98.8525, 99.8525), (231.1565, 233.1565)]
        expected_output = [(0.05625, 13.0625), (24.17775, 30.19325), (34.375, 49.87675), (94.322, 112.819),
                           (251.595, 269.0935), (230.6565, 233.1565)]

        self.assertEqual(set_transitions(times), expected_output)


if __name__ == '__main__':
    unittest.main()
