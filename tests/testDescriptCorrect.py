import unittest
import filecmp

import clip_generator.descript.maini as maini
from clip_generator.common_functions import checkTwoFilesAreTheSame
from clip_generator.common_functions import check_two_large_files_are_equal


class TestDescriptCorrect(unittest.TestCase): 

	@classmethod
	def setUpClass(cls):
		maini.dirClips = "tests/Clips/"
		maini.filename = "tests/Clips/"

	def test_files_is_being_generated_exactly_as_examples(self):
		maini.run("https://www.youtube.com/watch?v=EJBd-AttAMI")

		title_without_special_chars = maini.getTitleWithoutSpecialChars(maini.title)
		self.assertTrue(checkTwoFilesAreTheSame(f"tests/Clips/{title_without_special_chars}/descr.txt", 'tests/Examples/descr.txt'))
		self.assertTrue(
			check_two_large_files_are_equal(f"tests/Clips/{title_without_special_chars}/thumb.jpg", 'tests/Examples/thumb.jpg'), msg="Thumbnails aren't equals")

		maini.run("https://www.youtube.com/watch?v=MUtJLmQlboc")
		title_without_special_chars = maini.getTitleWithoutSpecialChars(maini.title)

		self.assertTrue(checkTwoFilesAreTheSame(f"tests/Clips/{title_without_special_chars}/descr.txt", 'tests/Examples/descr1.txt'))
		self.assertTrue(
			check_two_large_files_are_equal(f"tests/Clips/{title_without_special_chars}/thumb.webp", 'tests/Examples/thumb1.webp'), msg="Thumbnails aren't equals")

		maini.run("https://www.youtube.com/watch?v=5l-NyZOf1JM")
		title_without_special_chars = maini.getTitleWithoutSpecialChars(maini.title)

		self.assertTrue(checkTwoFilesAreTheSame(f"tests/Clips/{title_without_special_chars}/descr.txt", 'tests/Examples/descr2.txt'))
		self.assertTrue(
			check_two_large_files_are_equal(f"tests/Clips/{title_without_special_chars}/thumb.webp", 'tests/Examples/thumb2.webp'), msg="Thumbnails aren't equals")


if __name__ == '__main__':
    unittest.main()
