import unittest

from clip_generator.editter.compare_sound_by_images.offset import count_colored_pixels

class TestOffsetCountPixels(unittest.TestCase):

    def test_count_colored_pixels(self):
        # Test with an empty list of pixels
        pixels = []
        expected_result = {'purple': 0, 'blue': 0, 'red': 0, 'none': 0, 'other': 0}
        self.assertEqual(count_colored_pixels(pixels), expected_result)

        # Test with a list of pixels that only contains purple pixels
        pixels = [(127, 0, 127, 254)] * 10
        expected_result = {'purple': 10, 'blue': 0, 'red': 0, 'none': 0, 'other': 0}
        self.assertEqual(count_colored_pixels(pixels), expected_result)

        # Test with a list of pixels that only contains blue pixels
        pixels = [(0, 0, 127, 127)] * 10
        expected_result = {'purple': 0, 'blue': 10, 'red': 0, 'none': 0, 'other': 0}
        self.assertEqual(count_colored_pixels(pixels), expected_result)

        # Test with a list of pixels that only contains red pixels
        pixels = [(127, 0, 0, 127)] * 10
        expected_result = {'purple': 0, 'blue': 0, 'red': 10, 'none': 0, 'other': 0}
        self.assertEqual(count_colored_pixels(pixels), expected_result)

        # Test with a list of pixels that only contains transparent pixels
        pixels = [(0, 0, 0, 0)] * 10
        expected_result = {'purple': 0, 'blue': 0, 'red': 0, 'none': 10, 'other': 0}
        self.assertEqual(count_colored_pixels(pixels), expected_result)

        # Test with a list of pixels that contains a mix of different colors
        pixels = [(127, 0, 127, 254), (0, 0, 127, 127), (127, 0, 0, 127), (127, 0, 0, 127), (0, 0, 0, 0), (255, 0, 0, 127)]
        expected_result = {'purple': 1, 'blue': 1, 'red': 2, 'none': 1, 'other': 1}
        self.assertEqual(count_colored_pixels(pixels), expected_result)
     
if __name__ == '__main__':
    unittest.main()