import os
import unittest
import filecmp
from pathlib import Path

import clip_generator.descript.maini as maini
import clip_generator.downloader
import clip_generator.downloader as main
import clip_generator.editter.dirs
import clip_generator.stream as stream
import clip_generator.editter.dirs as dirs
from clip_generator.common_functions import getDuration


class TestCorrectDownload(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        clip_generator.editter.dirs.dir_clip_folder = "tests/Clips/"
        maini.filename = "tests/Clips/"
        clip_generator.editter.dirs.last_dir_clip = "tests/Clips/"

    def test_clip_is_downloaded_as_example(self):
        main.download_clip("https://youtu.be/0UGYR8Zi8qk")

        filename = Path(clip_generator.editter.dirs.last_dir_clip + "clip.mkv")
        duration = getDuration(filename)

        self.assertEqual(2, round(float(duration), 1), msg="Downloaded clip doesnt match duration: " + str(filename))

    def test_stream_is_downloaded_as_example(self):
        dirs.dir_stream = dirs.dir_temp_files + "stream.mkv"

        clip_generator.downloader.download_stream("https://www.youtube.com/watch?v=6puvpOmoqZY", 235, 241)

        filename = Path(dirs.dir_stream)
        duration = getDuration(filename)

        dirs.dir_stream = "tests/Examples/stream.mkv"
        self.assertEqual(8, round(float(duration), 1), msg="Downloaded stream doesnt match duration: " + str(filename))

    def test_stream_download_is_too_long(self):
        dirs.dir_stream = dirs.dir_temp_files + "stream1.mkv"

        clip_generator.downloader.download_stream("https://www.youtube.com/watch?v=6puvpOmoqZY", 235, 1141)

        self.assertTrue(not os.path.isfile(dirs.dir_stream), "Stream file found: " + dirs.dir_stream)
        dirs.dir_stream = "tests/Examples/stream.mkv"


if __name__ == '__main__':
    unittest.main()
