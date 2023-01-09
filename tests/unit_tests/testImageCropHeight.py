import unittest
from PIL import Image
import tests.configs as configs

from clip_generator.editter.compare_sound_by_images.offset import crop_height_image


class TestCropHeightImage(unittest.TestCase):
    def test_crop_height_256_image(self):
        image = Image.open(configs.example_test_folder + "height_test_128.png")
        cropped_image = crop_height_image(image, 256, 256)

        self.assertEqual(cropped_image.size, (20, 256))
        self.assertEqual(cropped_image.getpixel((0, 127)), (0, 0, 0))
        self.assertEqual(cropped_image.getpixel((0, 128)), (255, 255, 255))
        self.assertEqual(cropped_image.getpixel((0, 255)), (255, 255, 255))

    def test_crop_height_128_image(self):
        image = Image.open(configs.example_test_folder + "height_test_64.png")
        cropped_image = crop_height_image(image, 384, 128)

        self.assertEqual(cropped_image.size, (20, 128))
        self.assertEqual(cropped_image.getpixel((0, 63)), (0, 0, 0, 255))
        self.assertEqual(cropped_image.getpixel((0, 64)), (255, 255, 255, 255))
        self.assertEqual(cropped_image.getpixel((0, 127)), (255, 255, 255, 255))



if __name__ == '__main__':
    unittest.main()
