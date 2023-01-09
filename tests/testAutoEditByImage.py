import unittest

from clip_generator.editter import trimmer
import clip_generator.editter.dirs as dirs
import clip_generator.editter.chopper as chopper

class MyTestCase(unittest.TestCase):

    def test_edits_are_correct(self):
        chopper.remove_video(dirs.dir_clip, dirs.dir_audio_clip)
        trimmer.auto_edit_by_images()


if __name__ == '__main__':
    unittest.main()
