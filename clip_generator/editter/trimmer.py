import math
import os.path

import clip_generator.editter.chopper as chopper
import clip_generator.editter.audio_info as audio_info
import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions
import clip_generator.editter.correlation as correlation
import clip_generator.editter.info_processor

correct_trim = True
current_stream = dirs.dir_worstaudio_stream


def trim_to_clip(is_stream_a_video=False, offset_credits=0, phase=0):
    global current_stream

    dirs.update_phase(phase)

    set_current_stream(is_stream_a_video)
    set_start_and_end_clip(offset_credits)
    set_timestamps_for_trim(is_stream_a_video, offset_credits)

    return get_timestamps_for("full")


# TODO needs tests
def set_current_stream(is_stream_a_video: bool):
    global current_stream
    current_stream = dirs.dir_worstaudio_stream
    if is_stream_a_video:
        current_stream = dirs.dir_stream
        chopper.remove_video(dirs.dir_stream, dirs.dir_audio_stream)


# TODO needs tests
def set_start_and_end_clip(offset_credits: int):
    chopper.cut_audio(dirs.dir_audio_clip, dirs.dir_current_start_clip, 0.5, dirs.get_second())
    chopper.cutLastSecondsAudio(dirs.get_second(), offset_credits)
    chopper.fixAudioParts()


def check_correlation_at(from_second, to_second, dir_stream_input, dir_stream_output, dir_clip):
    global correct_trim
    chopper.chop(dir_stream_input, dir_stream_output, from_second, to_second)

    slowed_stream = chopper.slow_audio(dir_stream_output)
    slowed_clip = chopper.slow_audio(dir_clip)

    correl = correlation.correlate(slowed_clip, slowed_stream)

    if correl < 0.80:
        correct_trim = False
        print("Error correlation: " + str(correl) + dir_stream_output)
        return correl

    return correl


def get_timestamps_for(limit_type: str):
    match limit_type:
        case "only_start":
            from_second = audio_info.infosTrim[0][0][1]['pad']
            to_second = from_second + dirs.get_second()
            return from_second, to_second
        case "only_end":
            to_second = audio_info.get_last_seconds_for_ffmpeg_argument_to(current_stream,
                                                                           audio_info.infosTrim[1][0][1]['pad_post'])
            from_second = to_second - dirs.get_second()
            return from_second, to_second
        case "full":
            from_second = audio_info.infosTrim[0][0][1]['pad']
            to_second = audio_info.get_last_seconds_for_ffmpeg_argument_to(current_stream,
                                                                           audio_info.infosTrim[1][0][1]['pad_post'])
            return from_second - 0.5, to_second + dirs.transition_offset  # chopper cuts one second sooner to avoid
        # errors with transitions/credits, so this time we subtract one to compensate and make it
        # one second longer
        # We chop 0.5 after clip starts because it may have some transiction,
        # if you change this, change at the begining also


def check_correlation_for_trim(limit_type: str, dir_input_stream: str, dir_output_stream: str, dir_clip: str):
    from_second, to_second = get_timestamps_for(limit_type)

    return check_correlation_at(from_second, to_second, dir_input_stream, dir_output_stream, dir_clip)


def set_timestamps_for_trim(contains_video=False, offset_credits=0):
    clip_duration = common_functions.getDuration(dirs.dir_audio_clip) - 5 - offset_credits
    start_correlation = 0
    end_correlation = 0

    input_stream = set_input_stream(contains_video)

    while True:
        start_correlation, end_correlation, input_stream = get_correlation(end_correlation, input_stream,
                                                                           start_correlation)

        audio_info.increase_accuracy()

        stream_duration = get_stream_duration()

        if audio_info.misalignment > 8000 and stream_duration <= clip_duration:
            print("Wrong match, stream duration is smaller than clip duration")
            raise Exception("Clip duration is significantly bigger than stream duration")

        if (correct_trim and stream_duration >= clip_duration) or audio_info.misalignment > 8000:
            audio_info.misalignment = 6000
            from_second, to_second = get_timestamps_for("full")
            if not contains_video:
                clip_generator.editter.info_processor.write_infos_trim(from_second, to_second)
                clip_generator.editter.info_processor.write_correlation(start_correlation, end_correlation)

            return from_second, to_second, start_correlation, end_correlation


# TODO NO TESTS
def get_stream_duration() -> float:
    from_second, to_second = get_timestamps_for("full")
    stream_duration = to_second - from_second
    return stream_duration


# TODO NO TESTS USED
def set_input_stream(contains_video):
    input_stream = dirs.dir_worstaudio_stream
    if contains_video:
        input_stream = dirs.dir_audio_stream
        audio_info.sample_rate = 12000
    return input_stream


def get_correlation(end_correlation, input_stream, start_correlation):
    if start_correlation < 0.8:
        audio_info.set_audio_infos_trim_start(input_stream)
        start_correlation = check_correlation_for_trim("only_start", current_stream, dirs.dir_current_start_stream,
                                                       dirs.dir_current_start_clip)
    if start_correlation > 0.8 and not os.path.exists(dirs.dir_start_only_untrimmed_stream):
        from_second, __ = get_timestamps_for("only_start")
        chopper.chop(current_stream, dirs.dir_start_only_untrimmed_stream, from_second, "999999999")
        input_stream = dirs.dir_start_only_untrimmed_stream

    if end_correlation < 0.8:
        audio_info.set_audio_infos_trim_end(input_stream)
        end_correlation = check_correlation_for_trim("only_end", current_stream, dirs.dir_current_end_stream,
                                                     dirs.dir_current_end_clip)
    if end_correlation > 0.8 and not os.path.exists(dirs.dir_end_only_untrimmed_stream):
        __, to_second = get_timestamps_for("only_end")
        chopper.chop(current_stream, dirs.dir_end_only_untrimmed_stream, "0", to_second)
        input_stream = dirs.dir_end_only_untrimmed_stream

    return start_correlation, end_correlation, input_stream
