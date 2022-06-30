import os
import sys

os.system("ffmpeg -i clip.mp4 -c copy -map 0 -segment_time 00:00:01 -f segment -reset_timestamps 1 output%03d.mp4")


# ffmpeg -i clip.mp4 -c:v libx265 -preset fast -crf 17 -ac 2 -vbr 3 -map 0 -segment_time 00:00:01 -f segment -async 1 -strict -2 zzzoutput%03d.mp4

# ffmpeg -i clip.mp4 -map 0 -segment_time 00:00:01 -f segment -async 1 -strict -2 zzzoutput%03d.mp4