import unittest
import os
import sys

from tests.order_tests import load_ordered_tests
import tests.testChopperGeneratesFilesWithRightDuration as testChopper
import tests.testTrimmerGeneratesFilesWithRightDuration as testTrimmer
import tests.testDescriptCorrect as testDescript
import tests.testCorrectDownload as testDownload
import tests.testAudioInfo as testAudio

import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions


def setUpModule():
    dirs.dir_audio_clip = "tests/Clips/audio_clip.mp4"
    dirs.dir_clip = "tests/Examples/clip.mkv"
    dirs.dir_clip_folder = "tests/Clips/"
    dirs.dirAudioParts = "tests/Clips/audio_parts/"
    dirs.dirFixedAudioParts = "tests/Clips/fixed_audio_parts/"
    dirs.dir_stream = "tests/Examples/stream.mkv"
    dirs.dir_trimmed_stream = "tests/Clips/trimmed_stream.mkv"

    os.makedirs("tests/Clips/audio_parts", exist_ok=True)
    os.makedirs("tests/Clips/fixed_audio_parts", exist_ok=True)


def tearDownModule():
    common_functions.removeAll(dirs.dir_clip_folder)


def run_tests(with_internet=True):
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
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration(
        'test_cut_audio_into_x_seconds_fixed_file_is_right_duration'))
    suite.addTest(
        testChopper.TestChopperGeneratesFilesWithRightDuration('test_cut_last_seconds_audio_file_is_right_duration'))
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_generates_video'))
    suite.addTest(testChopper.TestChopperGeneratesFilesWithRightDuration('test_chop_right_duration'))

    if with_internet:
        suite.addTest(unittest.makeSuite(testDescript.TestDescriptCorrect))
        suite.addTest(unittest.makeSuite(testDownload.TestCorrectDownload))

    suite.addTest(unittest.makeSuite(testAudio.TestAudioInfo))
    suite.addTest(unittest.makeSuite(testTrimmer.TestTrimmerGeneratesFilesWithRightDuration))
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
