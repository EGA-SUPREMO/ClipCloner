from pathlib import Path
import unittest

from clip_generator.editter import chopper

class TestChopper(unittest.TestCase):
  
    def test_remove_video_from_file(self):
        chopper.dir_audio_clip = "tests/Clips/audio_clip.mp4"
        chopper.dir_clip = "tests/Clips/clip.mkv"
        chopper.removeVideo()
  
        clip_audio = Path(chopper.dir_audio_clip)

        self.assertTrue(clip_audio.is_file(), f'File clip_audio.mp4 doesnt exist')

    def test_cut_audio_into_x_seconds(self):
        chopper.dir_audio_clip = "tests/Clips/audio_clip.mp4"
        chopper.dirAudioParts = "tests/Clips/audio_clip.mp4"
        chopper.cutAudioIntoXSecondsParts("01")
  
        clip_audio = Path("clip_generator/editter/clip_aud/llio.mp4")

        self.assertTrue(clip_audio.is_file(), f'Files in audio_parts dont exist')
  
if __name__ == '__main__':
    unittest.main() 
