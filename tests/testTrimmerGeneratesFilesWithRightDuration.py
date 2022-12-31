import unittest

from pathlib import Path

import clip_generator.editter.trimmer as trimmer
import clip_generator.editter.dirs as dirs

from clip_generator.common_functions import getDuration
from tests.configs import setUpModule


class TestTrimmerGeneratesFilesWithRightDuration(unittest.TestCase):

    def setUp(self) -> None:
        setUpModule()

    def test_trim_to_clip_match_duration_as_example(self):
        trimmer.trim_to_clip(True)

        filename = Path(dirs.dir_trimmed_stream)
        duration = getDuration(filename)

        self.assertEqual(103.7, round(float(duration), 1), msg="REAL Trimmed stream doesnt match duration: "+str(filename))


if __name__ == '__main__':
    unittest.main()
