import unittest
import filecmp
from pathlib import Path

import clip_generator.descript.maini as maini
import clip_generator.main as main
from tests.common_functions import getDuration

class TestCorrectDownload(unittest.TestCase): 

	@classmethod
	def setUpClass(cls):
		maini.dirClips = "tests/Clips/"
		maini.filename = "tests/Clips/"
		maini.lastDirClip = "tests/Clips/"

	def test_clip_is_downloaded_as_example(self):
		main.downloadClip("https://www.youtube.com/watch?v=rnqQPIod3pA")

		filename = Path(maini.lastDirClip+"clip.mkv")
		duration=getDuration(filename)

		self.assertEqual(30.7, round(float(duration), 1), msg="Downloaded clip doesnt match duration: "+str(filename))

if __name__ == '__main__':
	unittest.main()
