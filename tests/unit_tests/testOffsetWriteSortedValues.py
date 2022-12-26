import os
import unittest

from clip_generator.editter.compare_sound_by_images.offset import write_sorted_values

class TestOffsetWriteSortedValues(unittest.TestCase):

    def test_write_sorted_values(self):
        # Test with an empty list of values
        values = []
        file_path = "sorted_values.txt"
        write_sorted_values(values, file_path)
        with open(file_path, "r") as f:
            contents = f.read()
        self.assertEqual(contents, "")
        os.remove(file_path)

        # Test with a list of values that are already sorted in descending order
        values = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        file_path = "sorted_values.txt"
        write_sorted_values(values, file_path)
        with open(file_path, "r") as f:
            contents = f.read()
        self.assertEqual(contents, "9 in 0\n8 in 1\n7 in 2\n6 in 3\n5 in 4\n4 in 5\n3 in 6\n2 in 7\n1 in 8\n")
        os.remove(file_path)

        # Test with a list of values that are already sorted in ascending order
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        file_path = "sorted_values.txt"
        write_sorted_values(values, file_path)
        with open(file_path, "r") as f:
            contents = f.read()
        self.assertEqual(contents, "9 in 8\n8 in 7\n7 in 6\n6 in 5\n5 in 4\n4 in 3\n3 in 2\n2 in 1\n1 in 0\n")
        os.remove(file_path)

        # Test with a list of values that are not sorted
        values = [5, 3, 7, 2, 8, 1, 9, 4, 6]
        file_path = "sorted_values.txt"
        write_sorted_values(values, file_path)
        with open(file_path, "r") as f:
            contents = f.read()
        self.assertEqual(contents, "9 in 6\n8 in 4\n7 in 2\n6 in 8\n5 in 0\n4 in 7\n3 in 1\n2 in 3\n1 in 5\n")
        os.remove(file_path)
 
if __name__ == '__main__':
    unittest.main()