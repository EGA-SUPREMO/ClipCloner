import unittest

from tests.order_tests import load_ordered_tests
import tests.testChopperGeneratesFilesWithRightDuration as testChopper
import tests.testTrimmerGeneratesFilesWithRightDuration as testTrimmer

import clip_generator.editter.dirs as dirs

def run_tests():
	load_tests = load_ordered_tests
	suite = unittest.TestSuite()
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_remove_video_from_file_file_is_being_generated'))
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_audio_into_x_seconds_file_is_being_generated'))
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_last_seconds_audio_file_is_being_generated'))
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_fix_audio_parts_files_is_being_generated'))
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_audio_into_x_seconds_fixed_file_is_right_duration'))
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_last_seconds_audio_file_is_right_duration'))
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_generates_video'))
	suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_right_duration'))
	suite.addTest(unittest.makeSuite(testTrimmer.TestTrimmerGeneratesFilesWithRightDuration))
	runner = unittest.TextTestRunner()
	runner.run(suite)




if __name__ == '__main__':
    #unittest.main() 
    run_tests()
