from align_videos_by_soundtrack.align import SyncDetector
from align_videos_by_soundtrack.align_params import *
from align_videos_by_soundtrack.utils import *
import time
#    res = sd.align("hey.webm", "oo.webm")


def get_alignment_info(fps: list):
    file_specs = check_and_decode_filenames(fps, min_num_files=2)
    # defauflt max_misalignment=1800. But this produced inaccurate results for some videos.
    # changing it to 6000 improved results although seems to make it run slower.
    summarizer_params = SyncDetectorSummarizerParams(max_misalignment=6000)
    with SyncDetector(params=summarizer_params, clear_cache=False) as det:
        result = det.align(file_specs, known_delay_map={})
    return list(zip(file_specs, result))

print(time.asctime())
print(get_alignment_info(["parts/fixed_clip_audio010.mp4", "stream.mkv"]))
print(time.asctime()) 




#remove video
#ffmpeg -i clip.mp4 -vn clip_audio.mp4
#cut by one second
#ffmpeg -i clip_audio.mp4  -segment_time 00:00:01 -f segment -strict -2  -map 0 -c:a aac clip_audio%03d.mp4
#fix cuts
#for i in *.mp4 ; do
#    ffmpeg -y -ss 00:00:00 -i $i fixed_$i
#done
# [('/media/trabajo/1E8E46418E461227/Users/Tecnology Valencia/Downloads/uwu/Novaj git-oj/clip-generator/editer/parts/fixed_clip_audio010.mp4', {'trim': -0.0, 'pad': 20.053333333333335, 'orig_duration': 1.0, 'trim_post': 0.0, 'pad_post': 98.96666666666667, 'orig_streams': [{'type': 'Audio', 'sample_rate': 44100}], 'orig_streams_summary': {'max_resol_width': 0, 'max_resol_height': 0, 'max_sample_rate': 44100, 'max_fps': 0.0, 'num_video_streams': 0, 'num_audio_streams': 1}}), ('/media/trabajo/1E8E46418E461227/Users/Tecnology Valencia/Downloads/uwu/Novaj git-oj/clip-generator/editer/stream.mkv', {'trim': 20.053333333333335, 'pad': 0.0, 'orig_duration': 120.02, 'trim_post': 98.96666666666667, 'pad_post': 0.0, 'orig_streams': [{'type': 'Video', 'resolution': [[1920, 1080], '[SAR 1:1 DAR 16:9]'], 'fps': 60.0}, {'type': 'Audio', 'sample_rate': 44100}], 'orig_streams_summary': {'max_resol_width': 1920, 'max_resol_height': 1080, 'max_sample_rate': 44100, 'max_fps': 60.0, 'num_video_streams': 1, 'num_audio_streams': 1}})]
Sun Jul 10 15:28:49 2022
