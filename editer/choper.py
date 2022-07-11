import os
import sys

def removeVideo():
	os.system("ffmpeg -i clip.mp4 -vn clip_audio.mp4")
