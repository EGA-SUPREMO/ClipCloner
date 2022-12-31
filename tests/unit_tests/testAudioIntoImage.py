import os
import tempfile
import unittest

from clip_generator.editter.chopper import convert_audio_into_wave_image
import clip_generator.editter.dirs as dirs
from tests.configs import setUpModule

class TestConvertAudioIntoWaveImage(unittest.TestCase):

    def setUp(self) -> None:
        setUpModule()

    def test_convert_audio_into_wave_image(self):
        # Test with a sample audio file and a random color
        audio_file = dirs.dir_clip
        with tempfile.TemporaryDirectory() as tmpdir:
            image_file = os.path.join(tmpdir, "wave_image.png")
            color = "red"
            convert_audio_into_wave_image(audio_file, image_file, color, 1)

            # Check that the output file was created
            self.assertTrue(os.path.exists(image_file))

            # Check that the output file is a valid image file
            with open(image_file, "rb") as f:
                self.assertTrue(f.read(4).startswith(b"\x89PNG"))

            os.remove(image_file)


if __name__ == '__main__':
    unittest.main()
