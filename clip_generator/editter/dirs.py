seconds = [3, 1, 0.5]
phase = 0
seconds_edit = [3, 0.5]
phase_edit = 0
transition_offset = 1
scale_edit = 10
scale_trim = 3

dir_temp_files = "clip_generator/editter/temp/"

dirAudioParts = dir_temp_files + "audio_parts/"
dirFixedAudioParts = dir_temp_files + "fixed_audio_parts/"
dir_audio_clip = dir_temp_files + "clip_audio.mp4"
dir_audio_stream = dir_temp_files + "stream_audio.mp4"
dir_audio_trimmed_stream = dir_temp_files + "trimmed_stream_audio.mp4"
dir_audio_clip_rounded = dir_temp_files + "clip_audio_rounded.mp4"
dir_audio_stream_rounded = dir_temp_files + "stream_audio_rounded.mp4"
dir_audio_clip_image = dir_temp_files + "clip_audio.png"
dir_audio_stream_image = dir_temp_files + "stream_audio.png"

dir_clip_folder = "../Clips/"
last_dir_clip = dir_clip_folder

dir_clip = dir_clip_folder + "clip.mkv"
dir_stream = dir_clip_folder + "stream.mkv"
dir_worstaudio_stream = dir_clip_folder + "worstaudio_stream.mkv"
dir_trimmed_stream = dir_clip_folder + "trimmed_stream.mkv"

dir_current_start_stream = dir_temp_files + "start_stream.mp4"
dir_current_start_clip = dirFixedAudioParts + "S" + str(seconds[0]) + "_clip_audio0.mp4"
dir_current_end_clip = dirFixedAudioParts + "last_S" + str(seconds[0]) + "_clip_audio.mp4"
dir_current_end_stream = dir_temp_files + "end_stream.mp4"


# TODO Needs tests
def update_clip_dirs(title):
    global dir_clip_folder, last_dir_clip, dir_clip, dir_stream, dir_worstaudio_stream, dir_trimmed_stream

    dir_clip_folder = "../Clips/" + title + "/"
    last_dir_clip = dir_clip_folder

    dir_clip = dir_clip_folder + "clip.mkv"
    dir_stream = dir_clip_folder + "stream.mkv"
    dir_worstaudio_stream = dir_clip_folder + "worstaudio_stream.mkv"
    dir_trimmed_stream = dir_clip_folder + "trimmed_stream.mkv"


def update_phase(new_phase):
    global dir_current_start_clip, dir_current_end_clip, phase

    phase = new_phase
    dir_current_start_clip = dirFixedAudioParts + "S" + str(seconds[phase]) + "_clip_audio0.mp4"
    dir_current_end_clip = dirFixedAudioParts + "last_S" + str(seconds[phase]) + "_clip_audio.mp4"


def get_second():
    return seconds[phase]
def get_second_for_edit():
    return seconds_edit[phase_edit]


