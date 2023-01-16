import unittest
import os

from clip_generator.editter.compare_sound_by_images.offset import draw_plot_indexes


class TestDrawAveragePlotLines(unittest.TestCase):
    def test_image_is_being_generated(self):
        line_accuracy = [0.9, 0.8, 0.7, 0.6, 0.5]
        line_amount = [1, 2, 3, 4, 5]
        line_average = [0.5, 0.6, 0.7, 0.8, 0.9]
        filename = "test_image.png"
        draw_plot_indexes(line_accuracy, line_amount, line_average, filename)
        # Check that the file was created
        self.assertTrue(os.path.exists(filename))
        # Delete the file after the test
        os.remove(filename)


if __name__ == '__main__':
    unittest.main()
