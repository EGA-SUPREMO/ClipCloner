import os
import sys

dirAudioParts = "audio_parts/"
dirFixedAudioParts = "fixed_audio_parts/"

def removeVideo():
	os.system("ffmpeg -y -i clip.mp4 -vn clip_audio.mp4")

def cutAudioIntoOneSecondParts():
	os.system("ffmpeg -y -i clip_audio.mp4  -segment_time 00:00:01 -f segment -strict -2  -map 0 -c:a aac "+ dirAudioParts +"clip_audio%03d.mp4")


def fixAudioParts():
	filenames = next(os.walk(dirAudioParts), (None, None, []))[2]
	for filename in filenames:
		os.system("ffmpeg -y -ss 00:00:00 -i " + dirAudioParts + filename + " " + dirFixedAudioParts + filename)




#removeVideo()
#cutAudioIntoOneSecondParts()
#fixAudioParts()
