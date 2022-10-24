import os

import clip_generator.editter.dirs as dirs
from clip_generator.common_functions import remove_file_extension


def remove_videos():
    os.system(f"ffmpeg -loglevel error -stats -y -i {dirs.dir_clip} -vn {dirs.dir_audio_clip}")
    os.system(f"ffmpeg -loglevel error -stats -y -i {dirs.dir_stream} -vn {dirs.dir_audio_stream}")

# untested and seems like useless
#def extract_audio(file):
#
#    os.system(f" ffmpeg -i '{file}' -c:a pcm_s24le '{filepath_wo_suffix}.wav'")
# TODO TEST IT
def slow_audio(input_audio):
    output_audio = str(remove_file_extension(input_audio)) + "_slowed.mp4"
    if dirs.seconds[dirs.phase] == "3":
        slowness = "atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5"
    os.system(f'ffmpeg -i {input_audio} -filter:a "{slowness}" -vn {output_audio}')
    return output_audio

# Input: String: seconds in %01d
def cutAudioIntoXSecondsParts(x):
    os.system(
        f"ffmpeg -loglevel error -stats -y -i {dirs.dir_audio_clip}  -segment_time 00:00:{x} -f segment -strict -2  -map 0 -c:a aac {dirs.dirAudioParts}S{x}_clip_audio%01d.mp4")


# Input: Int: length of cutted audio from the last seconds
def cutLastSecondsAudio(seconds, offset_credits=0):
    cutted_seconds = str(
        seconds + offset_credits + 1)  # Usually the last second is a transition from the clip to credits or it simply loses volume to zero in the span of 1-2 seconds, this could interfere with the comparasons, so it gets left out
    real_seconds = str(seconds)
    os.system(
        f"ffmpeg -loglevel error -stats -y -sseof -{cutted_seconds} -i {dirs.dir_audio_clip} -c copy {dirs.dirAudioParts}temp_last_S{real_seconds}_clip_audio.mp4")
    os.system(
        "ffmpeg -loglevel error -stats -y -ss 0 -to 00:00:03 -i " + dirs.dirAudioParts + "temp_last_S" + real_seconds + "_clip_audio.mp4 -c copy " + dirs.dirAudioParts + "last_S" + real_seconds + "_clip_audio.mp4")


def fixAudioParts():
    filenames = next(os.walk(dirs.dirAudioParts), (None, None, []))[2]
    for filename in filenames:
        os.system(
            "ffmpeg -loglevel error -stats -y -ss 00:00:00 -i " + dirs.dirAudioParts + filename + " " + dirs.dirFixedAudioParts + filename)


def chop(input_file, output_file, from_second, to_second):
    os.system(
        f"ffmpeg -loglevel error -stats -y -ss {from_second} -to {to_second} -i {input_file} {output_file}")
