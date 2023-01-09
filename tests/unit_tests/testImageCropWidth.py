import unittest
from PIL import Image
import tests.configs as configs

from clip_generator.editter.compare_sound_by_images.offset import crop_width_image


class TestCropWidthImage(unittest.TestCase):
    def test_crop_width_3_image(self):
        image = Image.open(configs.example_test_folder + "width_test_3.png")
        cropped_image = crop_width_image(image, 0, 3)

        self.assertEqual(cropped_image.size, (3, 1024))
        self.assertEqual(cropped_image.getpixel((0, 0)), (0, 0, 0, 255))
        self.assertEqual(cropped_image.getpixel((1, 128)), (0, 0, 0, 255))
        self.assertEqual(cropped_image.getpixel((2, 255)), (0, 0, 0, 255))

    def test_crop_width_6_at_12_offset_image(self):
        image = Image.open(configs.example_test_folder + "width_test_6_at_12.png")
        cropped_image = crop_width_image(image, 12, 6)

        self.assertEqual(cropped_image.size, (6, 1024))
        self.assertEqual(cropped_image.getpixel((0, 0)), (255, 255, 255, 255))
        self.assertEqual(cropped_image.getpixel((5, 64)), (255, 255, 255, 255))


if __name__ == '__main__':
    unittest.main()
