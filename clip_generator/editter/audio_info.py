import time
import subprocess
import json
import os.path
import math

from PIL import Image
from align_videos_by_soundtrack.align import SyncDetector
from align_videos_by_soundtrack.align_params import *
from align_videos_by_soundtrack.utils import *

import clip_generator.editter.dirs as dirs
from clip_generator.common_functions import getDuration
import clip_generator.editter.compare_sound_by_images.offset as offset

misalignment=6000

data = {}
data['logs'] = []

infosEdit = list()
infosTrim = list()


def get_alignment_info(fps: list):
    file_specs = check_and_decode_filenames(fps, min_num_files=2)
    # defauflt max_misalignment=1800. But this produced inaccurate results for some videos.
    # changing it to 6000 improved results although seems to make it run slower.
    # Have to test if max_misalignment=1800 is good enough
    # Seems changing sample_rate could make more precise results
    summarizer_params = SyncDetectorSummarizerParams(max_misalignment=misalignment)
    with SyncDetector(params=summarizer_params, clear_cache=False) as det:
        result = det.align(file_specs, known_delay_map={})
    return list(zip(file_specs, result))


def set_audio_infos_edit(seconds: str, fromAudio, toAudio):
    for x in range(fromAudio, toAudio + 1):
        infosEdit.append(get_alignment_info(
            [dirs.dirFixedAudioParts + "S" + seconds + "_clip_audio" + str(x) + ".mp4", dirs.dir_stream]))


# TODO borrar, es inutil, ya hay otras funcitones que las replazan
def set_audio_infos_trim(dir_stream=""):
    global infosTrim
    if not dir_stream:
        dir_stream = dirs.dir_stream

    infosTrim = [get_alignment_info([dirs.dir_current_start_clip, dir_stream]),
                 get_alignment_info([dirs.dir_current_end_clip, dir_stream])]


# TODO needs tests
def set_audio_infos_trim_start(dir_stream):
    global infosTrim
    if dir_stream == dirs.dir_start_only_untrimmed_stream:
        raise Exception("Set audio info trim can't trim the start from an already trimmed stream")

    infosTrim[0] = get_alignment_info([dirs.dir_current_start_clip, dir_stream])


# TODO nedes tests
def set_audio_infos_trim_end(dir_stream):
    global infosTrim
    if dir_stream == dirs.dir_end_only_untrimmed_stream:
        raise Exception("Set audio info trim can't trim the end from an already trimmed stream")

    infosTrim[1] = get_alignment_info([dirs.dir_current_end_clip, dir_stream])


# TODO needs tests, what happens if one of the times it's just a loner, or rather, a bug and those around them are close
#  together? maybe make another function like intuir timestamp
def get_timestamps_from_times(times):
    temp_end = 0
    temp_start = times[0]
    timestamps = []

    for i in range(1, len(times)):
        if not math.isclose(times[i] - times[i - 1], dirs.get_second_for_edit(), abs_tol=(dirs.get_second_for_edit() / 10)):
            temp_end = times[i - 1]
            timestamps.append((temp_start, temp_end))
            temp_end = 0
            temp_start = times[i]

    temp_end = times[-1]
    timestamps.append((temp_start, temp_end))

    return timestamps


# TODO Needs tests
def set_audio_infos_edit_by_image():
    global infosEdit

    clip_image = Image.open(dirs.dir_audio_clip_image)
    stream_image = Image.open(dirs.dir_audio_stream_image)
    stream_image.save("stream.png")
    clip_image.save("clip.png")
    real_second = []
    average = []
    for x in range(0, clip_image.width, dirs.get_second_for_edit() * dirs.scale_edit):
        print(x)
        width = min(dirs.get_second_for_edit() * dirs.scale_edit, clip_image.width - x)
        cropped_clip = offset.crop_width_image(clip_image, x, width)
        cropped_clip.save(str(x)+".png")
        line_accuracy, line_average, line_amount = offset.compare_images(cropped_clip, stream_image)
#        infosEdit.append(offset.pixels_into_seconds(line_accuracy.index(max(line_accuracy))))
        average.append(offset.pixels_into_seconds(line_accuracy.index(max(line_accuracy))))
        real_second.append(offset.pixels_into_seconds(x))
#        offset.save_data(line_accuracy, line_average, line_amount, "typical_test/"+str(x))

    infosEdit = get_timestamps_from_times(average)
    #print(infosEdit)
    #print(average)
    #print(real_second)


def get_last_seconds_for_ffmpeg_argument_to(file, seconds: int):
    return float(getDuration(file)) - seconds


def write_infos_edit():
    for info in infosEdit:
        # format
        # appendJSON({'edit': [[from_second, to_second], [from2, to2],...]})
        f = open(dirs.dir_clip_folder + "timestamps.txt", "a")
        f.write(str(info[0][1]['pad']) + " - " + str(info[0][1]['pad_post']) + "\n")
        f.close()
        print(str(info[0][1]['pad']) + " - " + str(info[0][1]['pad_post']))


def write_infos_trim(from_second: float, to_second: float):
    print(str(from_second) + " - " + str(to_second))
    appendJSON({'trim': [from_second, to_second]})


def write_correlation(start: float, end: float):
    print({'correlation': {'trim': [start, end]}})
    appendJSON({'correlation': {'trim': [start, end]}})


def appendJSON(value):
    filepath = dirs.dir_clip_folder + "timestamps.json"
    dic = value

    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            dic = json.load(f)
            dic.update(value)

    with open(filepath, 'w') as f:
        json.dump(dic, f)
        f.close()
