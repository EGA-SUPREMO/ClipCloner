import time
import subprocess
import json
import os.path

from align_videos_by_soundtrack.align import SyncDetector
from align_videos_by_soundtrack.align_params import *
from align_videos_by_soundtrack.utils import *

import clip_generator.editter.dirs as dirs

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


def set_audio_infos_trim(dir_stream=""):
    global infosTrim
    if not dir_stream:
        dir_stream = dirs.dir_stream

    infosTrim = [get_alignment_info([dirs.dir_current_start_clip, dir_stream]),
                 get_alignment_info([dirs.dir_current_end_clip, dir_stream])]


def get_last_seconds_for_ffmpeg_argument_to(file, seconds: int):
    seconds = seconds - dirs.transition_offset  # chopper cuts one second sonner to avoid errors with transitions/credits, so this time we subtract one to compensate and make it one second longer
    lengthFile = subprocess.run(
        ['ffprobe', '-v', '0', '-show_entries', 'format=duration', '-of', 'compact=p=0:nk=1', file],
        capture_output=True, text=True).stdout
    return float(lengthFile) - seconds


def write_infos_edit():
    for info in infosEdit:
        # format
        # appendJSON({'edit': [[from_second, to_second], [from2, to2],...]})
        f = open(dirs.dir_clip_folder + "timestamps.txt", "a")
        f.write(str(info[0][1]['pad']) + " - " + str(info[0][1]['pad_post']) + "\n")
        f.close()
        print(str(info[0][1]['pad']) + " - " + str(info[0][1]['pad_post']))


def write_infos_trim(from_second: int, to_second: int):
    appendJSON({'trim': [from_second, to_second]})
    print(str(from_second) + " - " + str(to_second))


def write_correlation(start: int, end: int):
    appendJSON({'correlation': {'trim': [start, end]}})
    print({'correlation': {'trim': [start, end]}})

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
