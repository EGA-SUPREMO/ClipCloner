from align_videos_by_soundtrack.align import SyncDetector
from align_videos_by_soundtrack.align_params import *
from align_videos_by_soundtrack.utils import *
import time

dirFixedAudioParts = "fixed_audio_parts/"## REMOVE THISISISISI THIS IS DUPLICATED, IF AN ERROR HAPPENS IS BECAUSE OF THIS AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
infos = []

def get_alignment_info(fps: list):
    file_specs = check_and_decode_filenames(fps, min_num_files=2)
    # defauflt max_misalignment=1800. But this produced inaccurate results for some videos.
    # changing it to 6000 improved results although seems to make it run slower.
    summarizer_params = SyncDetectorSummarizerParams(max_misalignment=6000)
    with SyncDetector(params=summarizer_params, clear_cache=False) as det:
        result = det.align(file_specs, known_delay_map={})
    return list(zip(file_specs, result))

def set_audio_infos(fromAudio, toAudio):
    for x in range(fromAudio, toAudio+1):
        infos.extend(get_alignment_info([dirFixedAudioParts + "clip_audio"+ str(x) +".mp4", "stream.mkv"]))

set_audio_infos(6, 10)
print(infos)
for info in infos:
    print(info[0][1]['trim'])
    print(info[0][1]['pad'])
    print(info[0][1]['trim_post'])
    print(info[0][1]['pad_post'])


# [('/media/trabajo/1E8E46418E461227/Users/Tecnology Valencia/Downloads/uwu/Novaj git-oj/clip-generator/editer/parts/fixed_clip_audio010.mp4', {'trim': -0.0, 'pad': 20.053333333333335, 'orig_duration': 1.0, 'trim_post': 0.0, 'pad_post': 98.96666666666667, 'orig_streams': [{'type': 'Audio', 'sample_rate': 44100}], 'orig_streams_summary': {'max_resol_width': 0, 'max_resol_height': 0, 'max_sample_rate': 44100, 'max_fps': 0.0, 'num_video_streams': 0, 'num_audio_streams': 1}}), ('/media/trabajo/1E8E46418E461227/Users/Tecnology Valencia/Downloads/uwu/Novaj git-oj/clip-generator/editer/stream.mkv', {'trim': 20.053333333333335, 'pad': 0.0, 'orig_duration': 120.02, 'trim_post': 98.96666666666667, 'pad_post': 0.0, 'orig_streams': [{'type': 'Video', 'resolution': [[1920, 1080], '[SAR 1:1 DAR 16:9]'], 'fps': 60.0}, {'type': 'Audio', 'sample_rate': 44100}], 'orig_streams_summary': {'max_resol_width': 1920, 'max_resol_height': 1080, 'max_sample_rate': 44100, 'max_fps': 60.0, 'num_video_streams': 1, 'num_audio_streams': 1}})]

