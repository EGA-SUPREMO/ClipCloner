seconds = ["3", "1", "0.5"]
phase = 0

dir_temp_files = "clip_generator/editter/temp/"

dirAudioParts = dir_temp_files + "audio_parts/"
dirFixedAudioParts = dir_temp_files + "fixed_audio_parts/"
dir_audio_clip = dir_temp_files + "clip_audio.mp4"

dir_clip_folder = "../Clips/"

dir_clip = dir_clip_folder + "clip.mkv"
dir_stream = dir_clip_folder + "stream.mkv"
dir_trimmed_stream = dir_clip_folder + "trimmed_stream.mkv"

dir_current_start_clip = dirFixedAudioParts + "S0" + seconds[0] + "_clip_audio0.mp4"
dir_current_end_clip = dirFixedAudioParts + "last_S0" + seconds[0] + "_clip_audio0.mp4"


def update_phase(new_phase):
    global dir_current_start_clip, dir_current_end_clip, phase

    phase = new_phase
    dir_current_start_clip = dirFixedAudioParts + "S0" + seconds[phase] + "_clip_audio0.mp4"
    dir_current_end_clip = dirFixedAudioParts + "last_S0" + seconds[phase] + "_clip_audio0.mp4"
