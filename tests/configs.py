import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions

import os

example_test_folder = "tests/Examples/"


def setUpModule():
    common_functions.removeAll(dirs.dir_temp_files)
    dirs.dir_temp_files = "tests/Clips/temp/"

    dirs.dir_clip = "tests/Examples/clip.mkv"
    dirs.dir_clip_folder = "tests/Clips/"
    dirs.dir_stream = "tests/Examples/stream.mkv"
    dirs.dir_worstaudio_stream = dirs.dir_clip_folder + "worstaudio_stream.mkv"
    dirs.dir_trimmed_stream = dirs.dir_clip_folder + "trimmed_stream.mkv"

    dirs.dirAudioParts = dirs.dir_temp_files + "audio_parts/"
    dirs.dirFixedAudioParts = dirs.dir_temp_files + "fixed_audio_parts/"
    dirs.dir_audio_clip = dirs.dir_temp_files + "clip_audio.mp4"
    dirs.dir_audio_stream = dirs.dir_temp_files + "stream_audio.mp4"

    dirs.update_phase(0)

    common_functions.removeAll(dirs.dir_clip_folder)
    os.makedirs(dirs.dirAudioParts, exist_ok=True)
    os.makedirs(dirs.dirFixedAudioParts, exist_ok=True)


def tearDownModule():
    dirs.dir_clip_folder = "tests/Clips/"
    common_functions.removeAll(dirs.dir_clip_folder)
