import os

import chopper
import audio_info

def trim():
	to_second = audio_info.last_seconds_to_argument_to("stream_audio.mp4", audio_info.infosTrim[1][0][1]['pad_post'])
	os.system("ffmpeg -y -ss "+str(audio_info.infosTrim[0][0][1]['pad'])+" -to "+ str(to_second) + " -i stream.mkv pls.mkv ")
