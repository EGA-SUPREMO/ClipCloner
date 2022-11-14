import unittest
import os
import sys

from tests.order_tests import load_ordered_tests
import tests.testChopperGeneratesFilesWithRightDuration as testChopper
import tests.testTrimmerGeneratesFilesWithRightDuration as testTrimmer
import tests.unit_tests.testCorrelationForTrim as testUnitTrimmer
import tests.testDescriptCorrect as testDescript
import tests.testCorrectDownload as testDownload
import tests.testAudioInfo as testAudio

from tests.configs import setUpModule
from tests.configs import tearDownModule


def run_tests(is_with_internet=True):
    setUpModule()

    load_tests = load_ordered_tests
    suite = unittest.TestSuite()
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_remove_video_from_file_file_is_being_generated'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_audio_into_x_seconds_file_is_being_generated'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_last_seconds_audio_file_is_being_generated'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_fix_audio_parts_files_is_being_generated'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_last_seconds_audio_file_is_right_duration'))
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration(
        'test_cut_audio_into_x_seconds_fixed_file_is_right_duration'))
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_generates_video'))
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_right_duration'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_slow_audio_is_being_generated'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_slow_audio_is_being_slowed'))

    if not is_with_internet == "ni":
        suite.addTest(unittest.makeSuite(testDescript.TestDescriptCorrect))
        suite.addTest(unittest.makeSuite(testDownload.TestCorrectDownload))

    suite.addTest(unittest.makeSuite(testAudio.TestAudioInfo))
    #suite.addTest(unittest.makeSuite(testTrimmer.TestTrimmerGeneratesFilesWithRightDuration))
    suite.addTest(unittest.makeSuite(testUnitTrimmer.TestCorrelationForTrim))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    tearDownModule()


def run_unit_tests():
    setUpModule()
    load_tests = load_ordered_tests
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(testAudio.TestAudioInfo))
    suite.addTest(unittest.makeSuite(testTrimmer.TestTrimmerGeneratesFilesWithRightDuration))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    tearDownModule()


if __name__ == '__main__':
    # unittest.main()
    run_tests(sys.argv[1:][0])
# run_unit_tests()
