import os
import unittest

from clip_generator.common_functions import getDuration
from clip_generator.editter.chopper import cut_audio
import tests.configs as configs
import clip_generator.editter.dirs as dirs


class TestCutAudioChopper(unittest.TestCase):
    def test_cut_audio_from_the_beginning(self):
        # Test cutting audio from the beginning of the file
        input_file = configs.example_test_folder + "clip_audio.mp4"
        output_file = dirs.dir_temp_files + "output_audio.mp4"
        try:
            cut_audio(input_file, output_file, 0, 5)
        except Exception as e:
            self.fail(f"cut_audio raised exception: {e}")

        duration = getDuration(output_file)

        # Calculate the expected duration of the output file
        expected_duration = 5
        self.assertAlmostEqual(expected_duration, duration, delta=0.1,
                               msg="Trimmed clip in cut_audio doesnt match duration: " +
                                   str(output_file))
        os.remove(output_file)

    def test_cut_audio_from_the_middle(self):
        input_file = configs.example_test_folder + "clip_audio.mp4"
        output_file = dirs.dir_temp_files + "output_audio1.mp4"
        try:
            cut_audio(input_file, output_file, 2.5, 5)
        except Exception as e:
            self.fail(f"cut_audio raised exception: {e}")

        duration = getDuration(output_file)

        # Calculate the expected duration of the output file
        expected_duration = 5
        self.assertAlmostEqual(expected_duration, duration, delta=0.1,
                               msg="Trimmed clip in cut_audio doesnt match duration: " +
                                   str(output_file))
        os.remove(output_file)

    def test_cut_audio_from_the_end(self):
        input_file = configs.example_test_folder + "clip_audio.mp4"
        output_file = dirs.dir_temp_files + "output_audio2.mp4"

        try:
            cut_audio(input_file, output_file, 55, 5)
        except Exception as e:
            self.fail(f"cut_audio raised exception: {e}")

        duration = getDuration(output_file)

        # Calculate the expected duration of the output file
        expected_duration = 5
        self.assertAlmostEqual(expected_duration, duration, delta=0.1,
                               msg="Trimmed clip in cut_audio doesnt match duration: " +
                                   str(output_file))
        os.remove(output_file)

    def test_cut_audio_from_the_end_till_end(self):
        input_file = configs.example_test_folder + "clip_audio.mp4"
        output_file = dirs.dir_temp_files + "output_audio2.mp4"

        try:
            cut_audio(input_file, output_file, 55, 15)
        except Exception as e:
            self.fail(f"cut_audio raised exception: {e}")

        duration = getDuration(output_file)

        # Calculate the expected duration of the output file
        expected_duration = 7.95
        self.assertAlmostEqual(expected_duration, duration, delta=0.1,
                               msg="Trimmed clip in cut_audio doesnt match duration: " +
                                   str(output_file))
        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
