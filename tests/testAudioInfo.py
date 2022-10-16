import os.path
import unittest
from unittest.mock import patch

import clip_generator.editter.audio_info as audio_info
import clip_generator.editter.dirs as dirs

from clip_generator.common_functions import checkTwoFilesAreTheSame

class TestAudioInfo(unittest.TestCase):

    @patch('clip_generator.editter.audio_info.get_alignment_info')
    def test_sets_audio_infos_for_trim(self, get_alignment_info_mock):
        audio_info.infosTrim = list()

        get_alignment_info_mock.return_value =[[0, {'pad': 5, 'pad_post':4, 'trim': 3, 'trim_post': 2}]]

        audio_info.set_audio_infos_trim("1")

        for info in audio_info.infosTrim:
            self.assertEqual(info[0][1]['pad'], 5)
            self.assertEqual(info[0][1]['trim'], 3)

    def test_get_last_seconds_for_ffmpeg_argument_to(self):
        filename = "tests/Examples/stream.mkv"
        last_seconds = audio_info.get_last_seconds_for_ffmpeg_argument_to(filename, 3)
        self.assertEqual(118.0, round(last_seconds, 1), msg="Failed to get last 3 seconds right for ffmpeg -to format: "+filename)

    def test_write_infos(self):
        audio_info.write_infos_trim("10.048", "113.72033333333333")

        timefile = dirs.dir_clip_folder+"timestamps.txt" 
        f = open(timefile, "r")

        self.assertTrue(checkTwoFilesAreTheSame(dirs.dir_clip_folder+"timestamps.txt", 'tests/Examples/timestamps.txt'))

if __name__ == '__main__':
    unittest.main() 
