import unittest

from clip_generator.editter.info_processor import remove_close_numbers_by_abs_diff


class TestRemoveCloseNumbers(unittest.TestCase):

    def test_remove_close_numbers(self):
        # Test the function with some input lists and their expected output
        self.assertEqual(remove_close_numbers_by_abs_diff([1.5, 1.1, 3.2, 3.9, 5, 5.9, 0.5, 3.3, 3.3]), [1.5, 3.2, 3.9, 5, 5.9, 0.5])
        self.assertEqual(remove_close_numbers_by_abs_diff([1, 1, 2.2, 2.3, 2.5, 3.5, 4.4, 4.8]), [1, 2.2, 3.5, 4.4])
        self.assertEqual(remove_close_numbers_by_abs_diff([10, 10, 2.2, 2.3, 2.5, 1.5, 1, 0.8]), [10, 2.2, 1.5, 0.8])
        self.assertEqual(remove_close_numbers_by_abs_diff([2, 3]), [2, 3])
        self.assertEqual(remove_close_numbers_by_abs_diff([1, 3, 5, 7, 9]), [1, 3, 5, 7, 9])
        self.assertEqual(remove_close_numbers_by_abs_diff([]), [])


if __name__ == '__main__':
    unittest.main()
