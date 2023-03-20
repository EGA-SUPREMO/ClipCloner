import unittest
import sys

from tests.order_tests import load_ordered_tests
import tests.testChopperGeneratesFilesWithRightDuration as testChopper
import tests.testCutVideoIntoSeparateFiles as cutVideoIntoSeparateFiles
import tests.testTrimmerGeneratesFilesWithRightDuration as testTrimmer
import tests.testChopperCutsWithRightDuration as testChopperCutWithRightDuration
import tests.unit_tests.testCorrelationForTrim as testUnitTrimmer
import tests.unit_tests.testOffsetWriteSortedValues as testWriteSortedValues
import tests.unit_tests.testCutAudio as testCutAudio
import tests.unit_tests.testCurateResultsTimes as testCurateResultsTimes
import tests.unit_tests.testMergeTuple as testMergeTuple
import tests.unit_tests.testSetTransitions as testSetTransititons
import tests.unit_tests.testGetCorrelationTrimmer as testGetCorrelationTrimmer
import tests.unit_tests.testDeduceTimesEnds as testDeduceTimesEnds
import tests.unit_tests.testRemoveCreditsOffsets as testRemoveCreditsOffsets
import tests.unit_tests.testCutAudioIntoXTime as testCutAudioXTime
import tests.unit_tests.testRemoveCloseNumbers as testRemoveCloseNumbers
import tests.testDescriptCorrect as testDescript
import tests.testCorrectDownload as testDownload
import tests.testAudioInfo as testAudio

from tests.configs import setUpModule
from tests.configs import tearDownModule


def run_tests(options="ni"):
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
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration(
        'test_cut_last_second_audio_file_is_being_generated'))
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_generates_video'))
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_right_duration'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_slow_audio_is_being_generated'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_slow_audio_is_being_slowed'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_final_chop_generates_files_with_right_duration'))

    if "ni" not in options:
        suite.addTest(unittest.makeSuite(testDescript.TestDescriptCorrect))
        suite.addTest(unittest.makeSuite(testDownload.TestCorrectDownload))

    suite.addTest(unittest.makeSuite(testAudio.TestAudioInfo))
    suite.addTest(unittest.makeSuite(testChopperCutWithRightDuration.TestChopperCutsWithRightDuration))
    suite.addTest(unittest.makeSuite(cutVideoIntoSeparateFiles.TestCutVideoIntoSeparateFiles))

    if "fast" not in options:
        suite.addTest(unittest.makeSuite(testTrimmer.TestTrimmerGeneratesFilesWithRightDuration))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    tearDownModule()


def run_unit_tests():
    setUpModule()
    load_tests = load_ordered_tests
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testUnitTrimmer.TestCorrelationForTrim))
    suite.addTest(unittest.makeSuite(testWriteSortedValues.TestOffsetWriteSortedValues))
    suite.addTest(unittest.makeSuite(testCutAudio.TestCutAudioChopper))
    suite.addTest(unittest.makeSuite(testMergeTuple.TestMergeTuple))
    suite.addTest(unittest.makeSuite(testCurateResultsTimes.TestCurateResults))
    suite.addTest(unittest.makeSuite(testSetTransititons.TestSetTransitions))
    suite.addTest(unittest.makeSuite(testGetCorrelationTrimmer.TestGetCorrelationTrimmer))
    suite.addTest(unittest.makeSuite(testDeduceTimesEnds.TestDeduceTimesEnds))
    suite.addTest(unittest.makeSuite(testRemoveCreditsOffsets.TestRemoveCreditsOffsets))
    suite.addTest(unittest.makeSuite(testCutAudioXTime.TestCutAudioIntoXTime))
    suite.addTest(unittest.makeSuite(testRemoveCloseNumbers.TestRemoveCloseNumbers))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    tearDownModule()


if __name__ == '__main__':
    # unittest.main()
    run_unit_tests()
    if "unit" not in sys.argv[1:][0]:
        run_tests(sys.argv[1:][0])
