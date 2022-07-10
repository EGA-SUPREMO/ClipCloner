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
print(get_alignment_info(["zzzoutput010.mp4", "stream.mkv"]))
print(time.asctime()) 




#remove video
ffmpeg -i clip.mp4 -vn clip_audio.mp4
#cut by one second
ffmpeg -i clip_audio.mp4  -segment_time 00:00:01 -f segment -strict -2  -map 0 -c:a aac clip_audio%03d.mp4
#fix cuts
for i in *.mp4 ; do
    ffmpeg -y -ss 00:00:00 -i $i nov$i
done
