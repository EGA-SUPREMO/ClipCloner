import time
import subprocess

from align_videos_by_soundtrack.align import SyncDetector
from align_videos_by_soundtrack.align_params import *
from align_videos_by_soundtrack.utils import *

import clip_generator.editter.dirs as dirs

infosEdit=list()
infosTrim=list()

def get_alignment_info(fps: list):
    file_specs = check_and_decode_filenames(fps, min_num_files=2)
    # defauflt max_misalignment=1800. But this produced inaccurate results for some videos.
    # changing it to 6000 improved results although seems to make it run slower.
    # Have to test if max_misalignment=1800 is good enough
    # Seems changing sample_rate could make more precise results
    summarizer_params = SyncDetectorSummarizerParams(max_misalignment=6000)
    with SyncDetector(params=summarizer_params, clear_cache=False) as det:
        result = det.align(file_specs, known_delay_map={})
    return list(zip(file_specs, result))

def set_audio_infos_edit(seconds, fromAudio, toAudio):
    for x in range(fromAudio, toAudio+1):
        infosEdit.append(get_alignment_info([dirs.dirFixedAudioParts + "S"+ seconds +"_clip_audio"+ str(x) +".mp4", dirs.dir_stream]))

def set_audio_infos_trim(seconds):
    global infosTrim
    infosTrim=list()
    seconds = str(seconds)

    infosTrim.append(get_alignment_info([dirs.dirFixedAudioParts + "S0"+ seconds +"_clip_audio0.mp4", dirs.dir_stream]))
    infosTrim.append(get_alignment_info([dirs.dirFixedAudioParts + "last_S"+ seconds +"_clip_audio.mp4", dirs.dir_stream]))

def get_last_seconds_for_ffmpeg_argument_to(file, seconds):
    seconds = seconds-1# chopper cuts one second sonner to avoid errors with transitions/credits, so this time we subtract one to compensate and make it one second longer
    lengthFile = subprocess.run(['ffprobe', '-v', '0', '-show_entries','format=duration', '-of', 'compact=p=0:nk=1', file], capture_output=True, text=True).stdout
    return float(lengthFile) - seconds

def write_infos_edit():
    for info in infosEdit:
        f = open(dirs.dir_clip_folder + "timestamps.txt", "a")
        f.write(str(info[0][1]['pad']) + " - " + str(info[0][1]['pad_post']) + "\n")
        f.close()
        print(str(info[0][1]['pad']) + " - " + str(info[0][1]['pad_post']))

def write_infos_trim(from_second, to_second):
    f = open(dirs.dir_clip_folder + "timestamps.txt", "a")
    f.write("Trim: From second - to second:\n")
    f.write(from_second + " - " + to_second + "\n")
    f.close()
    print(from_second + " - " + to_second)
