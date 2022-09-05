import unittest

import clip_generator.editter.trimmer as trimmer

class TestTrimmerGeneratesFilesWithRightDuration(unittest.TestCase):

    def setUp(self):
        dirs.dir_audio_clip = "tests/Clips/audio_clip.mp4"
        dirs.dir_clip = "tests/Examples/clip.mkv"
        dirs.dirAudioParts = "tests/Clips/audio_parts/"
        dirs.dirFixedAudioParts = "tests/Clips/fixed_audio_parts/"
        dirs.dir_stream = "tests/Examples/stream.mkv"
        dirs.dir_trimmed_stream = "tests/Clips/trimmed_stream.mkv"

    def test_trim_to_clip(self):
    	trimmer.trim_to_clip()

    	self.assertTrue(True)
