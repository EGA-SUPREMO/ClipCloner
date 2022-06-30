import os
import sys

os.system("ffmpeg -i clip.mp4 -c copy -map 0 -segment_time 00:00:01 -f segment -reset_timestamps 1 output%03d.mp4")
