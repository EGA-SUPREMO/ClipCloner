import os
import sys


dirAudioParts = "audio_parts/"
dirFixedAudioParts = "fixed_audio_parts/"

def removeVideo():
	os.system("ffmpeg -y -i clip.mp4 -vn clip_audio.mp4")

# Input: String: seconds in %01d
def cutAudioIntoXSecondsParts(x):
	os.system("ffmpeg -y -i clip_audio.mp4  -segment_time 00:00:" + x + " -f segment -strict -2  -map 0 -c:a aac "+ dirAudioParts + "S" + x + "_clip_audio%01d.mp4")

# Input: Int/String: length of cutted audio from the last seconds
def cutLastSecondsAudio(seconds):
	cutted_seconds = str(seconds+1)
	real_seconds = str(seconds)
	os.system("ffmpeg -y -sseof -"+ cutted_seconds +" -i clip_audio.mp4 -c copy "+ dirAudioParts +"temp_last_S"+ real_seconds +"_clip_audio.mp4")
	os.system("ffmpeg -y -ss 0 -to 00:00:03 -i "+ dirAudioParts +"temp_last_S"+ real_seconds +"_clip_audio.mp4 -c copy "+ dirAudioParts +"last_S"+ real_seconds +"_clip_audio.mp4")

def fixAudioParts():
	filenames = next(os.walk(dirAudioParts), (None, None, []))[2]
	for filename in filenames:
		os.system("ffmpeg -y -ss 00:00:00 -i " + dirAudioParts + filename + " " + dirFixedAudioParts + filename)



#removeVideo()
#cutAudioIntoXSecondsParts("01")
#fixAudioParts()
