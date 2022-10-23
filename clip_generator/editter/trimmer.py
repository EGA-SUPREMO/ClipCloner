import math

import clip_generator.editter.chopper as chopper
import clip_generator.editter.audio_info as audio_info
import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions
from clip_generator.editter.correlation import correlate


def trim_to_clip(offset_credits=0):
	# No need to extract audio, youtube-dl already can do it for you!, now TODO implement it!
	#chopper.remove_videos()
	#chopper.cutAudioIntoXSecondsParts("03")
	#chopper.cutLastSecondsAudio(3, offset_credits)
	#chopper.fixAudioParts()

	audio_info.set_audio_infos_trim(3)

	from_second = str(audio_info.infosTrim[0][0][1]['pad'])
	to_second = str(float(from_second) + float(dirs.seconds[dirs.phase]))#3,
	ffmpeg -i S03_clip_audio0.mp4 -filter:a "atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5" -vn clip_slow.mp4
	ffmpeg -i strat_stream.mp4 -filter:a "atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5" -vn stream_slow.mp4
	chopper.chop(dirs.dir_audio_stream, dirs.dir_current_start_stream, from_second, to_second)
	start_correlation = correlate(dirs.dir_current_start_clip, dirs.dir_current_start_stream)

	# safe correlatino is 75%

	to_second = str(
		audio_info.get_last_seconds_for_ffmpeg_argument_to(dirs.dir_stream, audio_info.infosTrim[1][0][1]['pad_post']))
	from_second = str(float(to_second) - float(dirs.seconds[dirs.phase]))
	chopper.chop(dirs.dir_audio_stream, dirs.dir_current_end_stream, from_second, to_second)
	end_correlation = correlate(dirs.dir_current_start_clip, dirs.dir_current_end_stream)

	audio_info.write_correlation(start_correlation, end_correlation)

	from_second = str(audio_info.infosTrim[0][0][1]['pad'])
	to_second = str(audio_info.get_last_seconds_for_ffmpeg_argument_to(dirs.dir_stream, audio_info.infosTrim[1][0][1]['pad_post']))

	audio_info.write_infos_trim(from_second, to_second)
	chopper.chop(dirs.dir_stream, dirs.dir_trimmed_stream, from_second, to_second)

def teste():
	#chopper.removeVideo()
	chopper.cutAudioIntoXSecondsParts("1")
	#chopper.cutAudioIntoXSecondsParts("3")
	chopper.fixAudioParts()

	#audio_info.set_audio_infos_edit("0.5", 0, 2)
	#audio_info.write_infos_edit()

#To copy clip's edition
def auto_edit(credits_offset=0):
	trim_to_clip(credits_offset)

	rounded_duraction_stream = round(common_functions.getDuration(dirs.dir_trimmed_stream))
	rounded_duraction_clip_without_credits = round(common_functions.getDuration(dirs.dir_clip)) - credits_offset
	if math.isclose(rounded_duraction_stream, rounded_duraction_clip_without_credits, rel_tol=0.01):
		print("festejo")
		return

	print(rounded_duraction_clip_without_credits)
	print(rounded_duraction_stream)
	#audio_info.set_audio_infos_edit(3)



	#audio_info.set_audio_infos_edit("0.5", 0, 2)
	#audio_info.write_infos_edit()

	#common_functions.removeAll(dirs.dirAudioParts)
	#common_functions.removeAll(dirs.dirFixedAudioParts)
