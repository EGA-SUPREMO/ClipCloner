import os
import subprocess
import unittest
from pathlib import Path

from clip_generator.editter import chopper
from tests.order_tests import load_ordered_tests

import clip_generator.editter.dirs as dirs
from clip_generator.common_functions import getDuration


class TestChopperGeneratesFilesWithRightDuration(unittest.TestCase):

    def test_remove_video_from_file_file_is_being_generated(self):
        chopper.remove_video(dirs.dir_clip, dirs.dir_audio_clip)

        clip_audio = Path(dirs.dir_audio_clip)

        self.assertTrue(clip_audio.is_file(), f'File clip_audio.mp4 doesnt exist')

    def test_cut_audio_into_x_seconds_file_is_being_generated(self):
        chopper.cutAudioIntoXSecondsParts("01")

        for x in range(62):
            clip_audio = Path(f"{dirs.dirAudioParts}S01_clip_audio{x}.mp4")
            self.assertTrue(clip_audio.is_file(), f'Files in audio_parts dont exist')

    def test_cut_last_seconds_audio_file_is_being_generated(self):
        chopper.cutLastSecondsAudio(3)

        clip_audio = Path(f"{dirs.dirAudioParts}last_S3_clip_audio.mp4")
        self.assertTrue(clip_audio.is_file(), f'File last_S3_clip_audio in audio_parts doesnt exist')

    def test_fix_audio_parts_files_is_being_generated(self):
        chopper.fixAudioParts()

        filenames = next(os.walk(dirs.dirAudioParts), (None, None, []))[2]
        filenamesFixed = next(os.walk(dirs.dirFixedAudioParts), (None, None, []))[2]
        self.assertCountEqual(filenames, filenamesFixed, f'Files in audio_parts and fixed audio_parts arent the same')

    def test_cut_audio_into_x_seconds_fixed_file_is_right_duration(self):
        for x in range(62):
            filename = Path(f"{dirs.dirFixedAudioParts}S01_clip_audio{x}.mp4")
            duration = getDuration(filename)

            self.assertEqual(round(1.0, 1), round(float(duration), 1), msg="Files in fixed audio dont match duration"+str(filename))

    def test_cut_last_seconds_audio_file_is_right_duration(self):
        filename = Path(f"{dirs.dirFixedAudioParts}last_S3_clip_audio.mp4")
        duration = getDuration(filename)

        self.assertEqual(round(3.0, 1), round(float(duration), 1), msg="Last 3 sec audio clip doesnt match duration: "+str(filename))

    def test_slow_audio_is_being_generated(self):
        dir_output = chopper.slow_audio(dirs.dirFixedAudioParts+"S01_clip_audio0.mp4")

        path_audio = Path(dir_output)

        self.assertTrue(path_audio.is_file(), 'Audio slowed not found: '+dir_output)

    def test_slow_audio_is_being_slowed(self):
        dir_output = chopper.slow_audio(dirs.dir_current_end_clip)
        self.assertEqual(getDuration(dir_output), 47.8, 'Audio slowed not match expected duration: '+dir_output)

    def test_chop_generates_video(self):
        chopper.chop(dirs.dir_stream, dirs.dir_trimmed_stream, "3", "3.8")

        trimmed_stream = Path(dirs.dir_trimmed_stream)
        self.assertTrue(trimmed_stream.is_file(), f'Trimmed stream doesnt exist')

    def test_chop_right_duration(self):
        filename = Path(dirs.dir_trimmed_stream)
        duration = getDuration(filename)

        self.assertEqual(round(0.8, 1), round(float(duration), 1), msg="Trimmed clip in chop doesnt match duration: "+str(filename))

    def test_final_chop_generates_files_with_right_duration(self):
        # Test the apply_filters function with a single time interval
        chopper.final_chop(dirs.dir_stream, dirs.dir_trimmed_stream, [(4, 6.5)])
        # Check that the output file has been created
        self.assertTrue(os.path.exists(dirs.dir_trimmed_stream))
        # Check the duration of the output file to make sure the correct time interval has been selected
        duration = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", dirs.dir_trimmed_stream], capture_output=True).stdout.strip()
        self.assertAlmostEqual(float(duration), 2.5, delta=0.1)
        os.remove(dirs.dir_trimmed_stream)

        # Test the apply_filters function with multiple time intervals2.528.5
        chopper.final_chop(dirs.dir_stream, dirs.dir_trimmed_stream, [(4, 6.5), (17, 26), (74, 91)])
        # Check that the output file has been created
        self.assertTrue(os.path.exists(dirs.dir_trimmed_stream))
        # Check the duration of the output file to make sure the correct time intervals have been selected
        duration = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", dirs.dir_trimmed_stream], capture_output=True).stdout.strip()
        self.assertAlmostEqual(float(duration), 28.5, delta=0.1)
        os.remove(dirs.dir_trimmed_stream)


if __name__ == '__main__':
    # This orders the tests to be run in the order they were declared.
    # It uses the unittest load_tests protocol.
    # This is bad practice and could be avoided, but I dont care enough, and I dont think this is going to cause a real
    # problem in the future
    load_tests = load_ordered_tests
    unittest.main()
