import unittest

from pathlib import Path

import clip_generator.editter.trimmer as trimmer
import clip_generator.editter.dirs as dirs

from tests.common_functions import getDuration

class TestTrimmerGeneratesFilesWithRightDuration(unittest.TestCase):

    def test_trim_to_clip(self):
        trimmer.trim_to_clip()

        filename = Path(dirs.dir_trimmed_stream)
        duration=getDuration(filename)

        self.assertEqual(103.7, round(float(duration), 1), msg="Trimmed stream doesnt match duration: "+str(filename))

if __name__ == '__main__':
    unittest.main()