import unittest


def remove_close_numbers(nums):
    result = []
    nums = sorted(nums)
    for i in range(len(nums)):
        if i == 0 or abs(nums[i] - nums[i-1]) > 1:
            result.append(nums[i])
    return result


class TestRemoveCloseNumbers(unittest.TestCase):

    def test_remove_close_numbers(self):
        # Test the function with some input lists and their expected output
        self.assertEqual(remove_close_numbers([1, 2, 3, 4, 5]), [1, 5])
        self.assertEqual(remove_close_numbers([1, 2, 3, 5, 6]), [1, 5, 6])
        self.assertEqual(remove_close_numbers([2, 3]), [2, 3])
        self.assertEqual(remove_close_numbers([1, 3, 5, 7, 9]), [1, 3, 5, 7, 9])
        self.assertEqual(remove_close_numbers([]), [])


if __name__ == '__main__':
    unittest.main()
