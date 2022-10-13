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
    summarizer_params = SyncDetectorSummarizerParams(max_misalignment=5000)
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

def print_infos_edit():
    for info in infosEdit:
        #print(info[0][1]['trim'])
        print(info[0][1]['pad'] + " - " + info[0][1]['pad_post'])
        #print(info[0][1]['trim_post'])
        #print(info[0][1]['pad_post'])
    #for info in infosEdit:
        #print(info[0][1]['trim'])
        #print(info[0][1]['pad'])
        #print(info[0][1]['trim_post'])
        #print()

def print_infos_trim():
    for info in infosTrim:
        #print(info[0][1]['trim'])
        print(info[0][1]['pad'])
        #print(info[0][1]['trim_post'])
        #print(info[0][1]['pad_post'])
    for info in infosTrim:
        #print(info[0][1]['trim'])
        #print(info[0][1]['pad'])
        #print(info[0][1]['trim_post'])
        print(info[0][1]['pad_post'])

#print(get_alignment_info(["fixed_audio_parts/S0.5_clip_audio1.mp4", "fixed_audio_parts/S3_clip_audio0.mp4"]))
#print(get_alignment_info(["clip_generator/editter/fixed_audio_parts/S01_clip_audio0.mp4", "clip_generator/editter/stream.webm"]))


# [('/media/trabajo/1E8E46418E461227/Users/Tecnology Valencia/Downloads/uwu/Novaj git-oj/clip-generator/editer/parts/fixed_clip_audio010.mp4', {'trim': -0.0, 'pad': 20.053333333333335, 'orig_duration': 1.0, 'trim_post': 0.0, 'pad_post': 98.96666666666667, 'orig_streams': [{'type': 'Audio', 'sample_rate': 44100}], 'orig_streams_summary': {'max_resol_width': 0, 'max_resol_height': 0, 'max_sample_rate': 44100, 'max_fps': 0.0, 'num_video_streams': 0, 'num_audio_streams': 1}}), ('/media/trabajo/1E8E46418E461227/Users/Tecnology Valencia/Downloads/uwu/Novaj git-oj/clip-generator/editer/stream.mkv', {'trim': 20.053333333333335, 'pad': 0.0, 'orig_duration': 120.02, 'trim_post': 98.96666666666667, 'pad_post': 0.0, 'orig_streams': [{'type': 'Video', 'resolution': [[1920, 1080], '[SAR 1:1 DAR 16:9]'], 'fps': 60.0}, {'type': 'Audio', 'sample_rate': 44100}], 'orig_streams_summary': {'max_resol_width': 1920, 'max_resol_height': 1080, 'max_sample_rate': 44100, 'max_fps': 60.0, 'num_video_streams': 1, 'num_audio_streams': 1}})]
