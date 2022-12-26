from PIL import Image
import unittest

from clip_generator.editter.compare_sound_by_images.offset import image_blend
import clip_generator.common_functions as common_functions

class TestOffsetWriteSortedValues(unittest.TestCase):

    def test_image_blend_offset_zero(self):
        clip_image = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        stream_image = Image.new('RGBA', (100, 100), (0, 255, 0, 255))
        offset_x = 0
        blended_image = image_blend(clip_image, stream_image, offset_x)
        self.assertEqual(blended_image.size, (100, 100))
        self.assertEqual(blended_image.getpixel((50, 50)), (127, 127, 0, 255))

    def test_image_blend_positive_offset(self):
        clip_image = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        stream_image = Image.new('RGBA', (100, 100), (0, 255, 0, 255))
        offset_x = 50
        blended_image = image_blend(clip_image, stream_image, offset_x)
        self.assertEqual(blended_image.size, (50, 100))
        self.assertEqual(blended_image.getpixel((25, 50)), (127, 127, 0, 255))

    def test_image_blend_negative_offset(self):
        clip_image = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        stream_image = Image.new('RGBA', (100, 100), (0, 255, 0, 255))
        offset_x = -50

        with self.assertRaises(ValueError):
            blended_image = image_blend(clip_image, stream_image, offset_x)

    def test_image_blend_different_sizes(self):
        clip_image = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        stream_image = Image.new('RGBA', (200, 200), (0, 255, 0, 255))
        offset_x = 0
        blended_image = image_blend(clip_image, stream_image, offset_x)
        self.assertEqual(blended_image.size, (100, 100))
        self.assertEqual(blended_image.getpixel((50, 50)), (127, 127, 0, 255))

    def test_image_blend_offset_working_as_expected(self):
        clip_image = common_functions.generate_test_image()
        stream_image = common_functions.generate_test_image()
        offset_x = 25
        blended_image = image_blend(clip_image, stream_image, offset_x)
        blended_image.save("hoeeh.png")
        self.assertEqual(blended_image.getpixel((0, 0)), (255, 0, 0, 255))
        self.assertEqual(blended_image.getpixel((24, 0)), (255, 0, 0, 255))
        self.assertEqual(blended_image.getpixel((25, 0)), (127, 0, 127, 255))
        self.assertEqual(blended_image.getpixel((49, 0)), (127, 0, 127, 255))
        self.assertEqual(blended_image.getpixel((50, 0)), (0, 0, 255, 255))
        self.assertEqual(blended_image.getpixel((74, 0)), (0, 0, 255, 255))
        self.assertEqual(blended_image.getpixel((0, 99)), (255, 0, 0, 255))
        self.assertEqual(blended_image.getpixel((25, 99)), (127, 0, 127, 255))
        self.assertEqual(blended_image.getpixel((74, 99)), (0, 0, 255, 255))

     
if __name__ == '__main__':
    unittest.main()