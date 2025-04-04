import math
import os
import subprocess

import clip_generator.editter.dirs as dirs
from clip_generator import common_functions, common_functions as common_functions
from clip_generator.common_functions import remove_file_extension
from clip_generator.common_functions import getDuration
from clip_generator.editter import dirs as dirs


def remove_video(dir_input: str, dir_output: str):
    os.system(f"ffmpeg -loglevel error -stats -y -i '{dir_input}' -vn '{dir_output}'")

# untested and seems like useless
# def extract_audio(file):
#
#    os.system(f" ffmpeg -i '{file}' -c:a pcm_s24le '{filepath_wo_suffix}.wav'")


def cut_audio(input_file: str, output_file: str, start_time: float, duration: float, filter_complex=None):
    if filter_complex is None:
        filter_complex = []
    command = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-i", input_file,
        "-ss", str(start_time),
        "-t", str(duration),
        "-preset", "ultrafast",
        *filter_complex,
        output_file
    ]
    subprocess.run(command)


# TODO duplicate, but it has tests
def cut_video(input_file: str, output_file: str, start_time: float, duration: float, filter_complex=None):
    if filter_complex is None:
        filter_complex = []
    command = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-i", input_file,
        "-ss", str(start_time),
        "-t", str(duration),
        "-preset", "ultrafast",
        *filter_complex,
        output_file
    ]
    subprocess.run(command)


def slow_audio(input_audio):
    output_audio = str(remove_file_extension(input_audio)) + "_slowed.mp4"

    slowness = "atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5"
    if dirs.get_second() == 3:
        slowness = "atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5"
    elif dirs.get_second() == 5:
        slowness = "atempo=0.5,atempo=0.5,atempo=0.5"

    os.system(f'ffmpeg  -loglevel error -stats -y -i "{input_audio}" -preset ultrafast -filter:a "{slowness}" -vn "{output_audio}"')
    return output_audio


def increase_speed_video(input_video, output_video):
    cut_video(input_video, output_video, 0, 999999, ["-filter_complex",
                                                     "[0:v]setpts=0.9*PTS[v];[0:a]atempo=1.1[a]",
                                                     "-map", '[v]', "-map", '[a]'])


def cutAudioIntoXSecondsParts(x: str):
    os.system(
        f"ffmpeg -loglevel error -stats -y -i '{dirs.dir_audio_clip}' -preset ultrafast -segment_time 00:00:{x} -f segment -strict -2  -map 0 -c:a aac '{dirs.dirAudioParts}S{x}_clip_audio%01d.mp4'")


def cut_audio_into_x_time_parts():
    # Get the duration of the input video file
    input_duration = common_functions.getDuration(dirs.dir_audio_stream)
    offset = dirs.get_second()

    # Calculate the number of parts to split the video into
    num_parts = common_functions.calculate_part_audio_files(input_duration, dirs.max_duration_for_stream_trimmer)

    # Cut the video into parts of duration `duration + offset`
    for i in range(num_parts):
        start_time = i * dirs.max_duration_for_stream_trimmer
        part_file = f"{dirs.dirAudioParts}stream_audio_{i}.mp4"
        cut_video(dirs.dir_audio_stream, part_file, start_time, dirs.max_duration_for_stream_trimmer + offset)


# Input: Int: length of cut audio from the last seconds
def cutLastSecondsAudio(seconds: int, offset_credits=0):
    cut_seconds = str(
        seconds + offset_credits + dirs.transition_offset)  # Usually the last second is a transition from the clip to credits or it simply loses volume to zero in the span of 1-2 seconds, this could interfere with the comparasons, so it gets left out
    real_seconds = str(seconds)
    os.system(
        f"ffmpeg -loglevel error -stats -y -sseof -{cut_seconds} -i '{dirs.dir_audio_clip}' -c copy '{dirs.dirAudioParts}temp_last_S{real_seconds}_clip_audio.mp4'")
    os.system(
        f"ffmpeg -loglevel error -stats -y -ss 0 -to 00:00:0{real_seconds} -i '{dirs.dirAudioParts}temp_last_S{real_seconds}_clip_audio.mp4' -c copy '{dirs.dirAudioParts}last_S{real_seconds}_clip_audio.mp4'")


def convert_audio_into_wave_image(audio_file: str, image_file: str, color: str, scale: int, filters=""):
    duration = round(getDuration(audio_file))
    command = [
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-i", audio_file,
        "-lavfi", "showwavespic=s=" + str(duration * scale) + "x1024:draw=scale:colors=" + color + filters,
        image_file
    ]
    subprocess.run(command)

def fixAudioParts():
    filenames = next(os.walk(dirs.dirAudioParts), (None, None, []))[2]
    for filename in filenames:
        os.system(
            "ffmpeg -loglevel error -stats -y -ss 00:00:00 -i '" + dirs.dirAudioParts + filename + "' -preset ultrafast '" + dirs.dirFixedAudioParts + filename + "'")


def chop(input_file, output_file, from_second: str, to_second: str):
    os.system(
        f"ffmpeg -loglevel error -stats -y -ss {from_second} -to {to_second} -i '{input_file}' -preset ultrafast '{output_file}'")


# Given a array, it will make the edits given timestamps, it does not increase speed unlike cut videos into separate
# files
def final_chop(input_file, output_file, time_intervals):
    # Create the select and aselect filters for FFmpeg
    select_filter = "select='"
    aselect_filter = "aselect='"
    for interval in time_intervals:
        start, end = interval
        select_filter += f"between(t,{start},{end})+"
        aselect_filter += f"between(t,{start},{end})+"
    select_filter = select_filter[:-1] + "',setpts=N/FRAME_RATE/TB"
    aselect_filter = aselect_filter[:-1] + "',asetpts=N/SR/TB"

    # Call FFmpeg with the select and aselect filters
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", input_file, "-preset", "ultrafast",
                    "-vf", select_filter, "-af", aselect_filter, output_file])


def cut_video_into_separate_files_with_increased_speed(input_video: str, cut_times):
    for i, cut_time in enumerate(cut_times):
        start_time, end_time = cut_time
        start_time = start_time * 0.9
        end_time = end_time * 0.9
        duration = end_time - start_time
        os.makedirs(dirs.dir_clip_folder + "cuts", exist_ok=True)
        output_video = f"{dirs.dir_clip_folder}cuts/{i}.mkv"
        cut_video(input_video, output_video, start_time, duration, ["-filter_complex",
                                                                    "[0:v]setpts=0.9*PTS[v];[0:a]atempo=1.1[a]",
                                                                    "-map", '[v]', "-map", '[a]'])


def remove_credits_offsets(start_offset: str, end_offset: str):
    common_functions.removeAll(dirs.dir_temp_files)

    dirs.offset_clip_start = int(start_offset)
    dirs.offset_clip_end = int(end_offset)
    dirs.current_duration_clip = common_functions.getDuration(dirs.dir_clip)

    if dirs.offset_clip_start == 0 and dirs.offset_clip_end == 0:
        remove_video(dirs.dir_clip, dirs.dir_audio_clip)
        return

    new_clip_dir = dirs.dir_temp_files + "clip_with_offsets.mkv"
    new_audio_clip_dir = dirs.dir_temp_files + "clip_audio_with_offsets.mp4"

    chop(dirs.dir_clip, new_clip_dir, str(dirs.offset_clip_start), str(dirs.current_duration_clip - dirs.offset_clip_end))
    remove_video(new_clip_dir, new_audio_clip_dir)

    dirs.dir_clip = new_clip_dir
    dirs.dir_audio_clip = new_audio_clip_dir

    dirs.current_duration_clip = common_functions.getDuration(dirs.dir_clip)
