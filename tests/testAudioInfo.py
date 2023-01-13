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

        audio_info.set_audio_infos_trim()

        for info in audio_info.infosTrim:
            self.assertEqual(info[0][1]['pad'], 5)
            self.assertEqual(info[0][1]['trim'], 3)

    @patch('clip_generator.editter.audio_info.get_alignment_info')
    def test_sets_audio_infos_for_edit_by_images(self, get_alignment_info_mock):
        audio_info.infosTrim = list()

        get_alignment_info_mock.return_value =[[0, {'pad': 5, 'pad_post':4, 'trim': 3, 'trim_post': 2}]]

        #audio_info.set_audio_infos_edit_by_image()
        #NEEDS better assertions
#        for info in audio_info.infosEdit:
            #self.assertEqual(info[0][1]['pad'], 5)
#            self.assertEqual(info[0][1]['trim'], 3)

    def test_get_last_seconds_for_ffmpeg_argument_to(self):
        filename = "tests/Examples/stream.mkv"
        last_seconds = audio_info.get_last_seconds_for_ffmpeg_argument_to(filename, 3)
        self.assertEqual(117.0, round(last_seconds, 1), msg="Failed to get last 3 seconds right for ffmpeg -to format: "+filename)

    def test_write_infos(self):
        audio_info.write_infos_trim(11.048, 111.72033333333333)
        audio_info.write_correlation(0.1594182825484764, 0.1481770833333333)

        #timefile = dirs.dir_clip_folder+"timestamps.json"
        #f = open(timefile, "r")
        # Later check whether it contains trim value dict or not, when there is areader
        self.assertTrue(checkTwoFilesAreTheSame(dirs.dir_clip_folder+"timestamps.json", 'tests/Examples/timestamps2.json'))

if __name__ == '__main__':
    unittest.main() 
