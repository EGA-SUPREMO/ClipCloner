from pathlib import Path
import os
from pathlib import Path
from shutil import rmtree
import unittest

from clip_generator.editter import chopper

class TestChopperGeneratesFiles(unittest.TestCase):

    def setUp(self):
        chopper.dir_audio_clip = "tests/Clips/audio_clip.mp4"
        chopper.dir_clip = "tests/Clips/clip.mkv"
        chopper.dirAudioParts = "tests/audio_parts/"
        chopper.dirFixedAudioParts = "tests/fixed_audio_parts/"
        chopper.dir_stream = "tests/Clips/stream.mkv"
        chopper.dir_trimmed_stream = "tests/Clips/trimmed_stream.mkv"

    def tearDown(self):
        for path in Path("tests/Clips").glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
  
    def test_remove_video_from_file_file_is_being_generated(self):
        chopper.removeVideo()
  
        clip_audio = Path(chopper.dir_audio_clip)

        self.assertTrue(clip_audio.is_file(), f'File clip_audio.mp4 doesnt exist')

    def test_cut_audio_into_x_seconds_file_is_being_generated(self):
        chopper.cutAudioIntoXSecondsParts("01")
  
        for x in range(62):
            clip_audio = Path(f"{chopper.dirAudioParts}S01_clip_audio{x}.mp4")
            self.assertTrue(clip_audio.is_file(), f'Files in audio_parts dont exist')

    def test_cut_last_seconds_audio_file_is_being_generated(self):
        chopper.cutLastSecondsAudio(3)
  
        clip_audio = Path(f"{chopper.dirAudioParts}last_S3_clip_audio.mp4")
        self.assertTrue(clip_audio.is_file(), f'File last_S3_clip_audio in audio_parts doesnt exist')

    def test_fix_audio_parts_files_is_being_generated(self):
        chopper.fixAudioParts()
  
        filenames = next(os.walk(chopper.dirAudioParts), (None, None, []))[2]
        filenamesFixed = next(os.walk(chopper.dirFixedAudioParts), (None, None, []))[2]

        self.assertCountEqual(filenames, filenamesFixed, f'Files in audio_parts and fixed audio_parts arent the same')

    def test_chop_generates_video(self):
        chopper.chop("3", "5")

        trimmed_stream = Path(chopper.dir_trimmed_stream)
        self.assertTrue(trimmed_stream.is_file(), f'Trimmed stream doesnt exist')

# TODO borrar lo que esta en el audioparts con el teardwon creo
# El orden de los test no es el quiero
if __name__ == '__main__':
    unittest.main() 
