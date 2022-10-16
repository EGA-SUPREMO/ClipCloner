import unittest
import filecmp

import clip_generator.descript.maini as maini
from clip_generator.common_functions import checkTwoFilesAreTheSame
# TODO check if image is generated
class TestDescriptCorrect(unittest.TestCase): 

	@classmethod
	def setUpClass(cls):
		maini.dirClips = "tests/Clips/"
		maini.filename = "tests/Clips/"

	def test_files_is_being_generated_exactly_as_examples(self):
		maini.run("https://www.youtube.com/watch?v=EJBd-AttAMI")

		title_without_special_chars = maini.getTitleWithoutSpecialChars(maini.title)
		self.assertTrue(checkTwoFilesAreTheSame(f"tests/Clips/{title_without_special_chars}/descr.txt", 'tests/Examples/descr.txt'))

		maini.run("https://www.youtube.com/watch?v=MUtJLmQlboc")
		title_without_special_chars = maini.getTitleWithoutSpecialChars(maini.title)

		self.assertTrue(checkTwoFilesAreTheSame(f"tests/Clips/{title_without_special_chars}/descr.txt", 'tests/Examples/descr1.txt'))

		maini.run("https://www.youtube.com/watch?v=5l-NyZOf1JM")
		title_without_special_chars = maini.getTitleWithoutSpecialChars(maini.title)

		self.assertTrue(checkTwoFilesAreTheSame(f"tests/Clips/{title_without_special_chars}/descr.txt", 'tests/Examples/descr2.txt'))


if __name__ == '__main__':
    unittest.main()
