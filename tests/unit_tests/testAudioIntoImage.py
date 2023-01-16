import os
import tempfile
import unittest

from PIL import Image

from clip_generator.editter.chopper import convert_audio_into_wave_image
import clip_generator.editter.dirs as dirs
from tests.configs import setUpModule
from tests.configs import example_test_folder

class TestConvertAudioIntoWaveImage(unittest.TestCase):

    def setUp(self) -> None:
        setUpModule()

    def test_convert_audio_into_wave_image(self):
        # Test with a sample audio file and a random color
        audio_file = example_test_folder + "clip_audio.mp4"
        with tempfile.TemporaryDirectory() as tmpdir:
            image_file = os.path.join(tmpdir, "wave_image.png")
            color = "red"
            convert_audio_into_wave_image(audio_file, image_file, color, 1)

            # Check that the output file was created
            self.assertTrue(os.path.exists(image_file))
            image = Image.open(image_file)
            self.assertEqual(image.width, 63, "Image width doesn't match expected value")
            self.assertEqual(image.height, 1024, "Image height doesn't match expected value")
            # Check that the output file is a valid image file with the expected size

            os.remove(image_file)
            image.close()
            convert_audio_into_wave_image(audio_file, image_file, "blue", 10)

            # Check that the output file was created
            self.assertTrue(os.path.exists(image_file))
            image = Image.open(image_file)
            self.assertEqual(image.width, 630, "Image width doesn't match expected value")
            self.assertEqual(image.height, 1024, "Image height doesn't match expected value")
            # Check that the output file is a valid image file with the expected size

            os.remove(image_file)
            image.close()

    def test_convert_audio_into_wave_image_with_filters(self):
        # Test with a sample audio file and a random color
        audio_file = example_test_folder + "start_stream.mp4"
        with tempfile.TemporaryDirectory() as tmpdir:
            image_file = os.path.join(tmpdir, "wave_image.png")
            color = "white"
            convert_audio_into_wave_image(audio_file, image_file, color, 1, ":filter=peak")

            # Check that the output file was created
            self.assertTrue(os.path.exists(image_file))
            image = Image.open(image_file)
            self.assertEqual(image.width, 3, "Image width doesn't match expected value")
            self.assertEqual(image.height, 1024, "Image height doesn't match expected value")
            # Check that the output file is a valid image file with the expected size

            os.remove(image_file)
            image.close()
            convert_audio_into_wave_image(audio_file, image_file, "black", 10, ":scale=sqrt")

            # Check that the output file was created
            self.assertTrue(os.path.exists(image_file))
            image = Image.open(image_file)
            self.assertEqual(image.width, 30, "Image width doesn't match expected value")
            self.assertEqual(image.height, 1024, "Image height doesn't match expected value")
            # Check that the output file is a valid image file with the expected size

            os.remove(image_file)
            image.close()



if __name__ == '__main__':
    unittest.main()
