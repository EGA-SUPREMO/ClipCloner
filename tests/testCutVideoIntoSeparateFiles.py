import os
import unittest

from clip_generator.editter import chopper, dirs
from clip_generator.common_functions import getDuration
from tests.configs import setUpModule
import tests.configs as configs


class TestCutVideoIntoSeparateFiles(unittest.TestCase):
    def test_cut_video_into_separate_files(self):
        stream_video = dirs.dir_stream
        cut_times = [[10.0835, 31.099125], [61.495875, 71.48375], [78.005375, 96.002375], [99.800875, 114.804]]

        chopper.cut_video_into_separate_files_with_increased_speed(stream_video, cut_times)

        # Check that 4 videos were created
        video_files = [f for f in os.listdir(dirs.dir_clip_folder+"cuts/") if f.endswith(".mkv")]
        self.assertEqual(len(video_files), len(cut_times), f"Expected 4 video files but got {len(video_files)}")

        # Check that each video has the expected duration
        for i, video_file in enumerate(video_files):
            duration = getDuration(dirs.dir_clip_folder + "cuts/" + video_file)
            expected_duration = (cut_times[i][1] - cut_times[i][0]) * 0.9
            self.assertAlmostEqual(duration, expected_duration, delta=0.15, msg=
                    f"Expected duration of {expected_duration} but got {duration}")


if __name__ == '__main__':
    unittest.main()
