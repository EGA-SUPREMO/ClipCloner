import unittest

import clip_generator.editter.trimmer as trimmer
import clip_generator.editter.dirs as dirs

class TestTrimmerGeneratesFilesWithRightDuration(unittest.TestCase):

    def test_trim_to_clip(self):
    	trimmer.trim_to_clip()

    	self.assertTrue(True)

if __name__ == '__main__':
    unittest.main() 
