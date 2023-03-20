import math

from clip_generator import common_functions as common_functions
from clip_generator.editter import dirs as dirs, chopper as chopper, audio_info as audio_info


def auto_edit():
    #common_functions.removeAll(dirs.dir_temp_files)
    dirs.update_phase_edit(1)

    chopper.remove_video(dirs.dir_stream, dirs.dir_audio_stream)

    duration_stream = common_functions.getDuration(dirs.dir_stream)
    dirs.current_duration_clip = common_functions.getDuration(dirs.dir_audio_clip)
    audio_parts = math.ceil(dirs.current_duration_clip / dirs.get_second_for_edit())

    if math.isclose(duration_stream, dirs.current_duration_clip, abs_tol=0.5):
        print("The clip duration is the same as trimmed stream duration")
    #	return

    chopper.cutAudioIntoXSecondsParts(str(dirs.get_second_for_edit()))
    chopper.fixAudioParts()

    audio_info.set_audio_infos_edit(str(dirs.get_second_for_edit()), "corr", 0, audio_parts)

    # chopper.final_chop(dirs.dir_stream, dirs.dir_edited_stream, audio_info.infosEdit)
    chopper.cut_video_into_separate_files_with_increased_speed(dirs.dir_stream, audio_info.infosEdit)

    common_functions.removeAll(dirs.dir_temp_files)
