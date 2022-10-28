import math

import clip_generator.editter.chopper as chopper
import clip_generator.editter.audio_info as audio_info
import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions
from clip_generator.editter.correlation import correlate


def trim_to_clip(offset_credits=0):
	# No need to extract audio, youtube-dl already can do it for you!, now TODO implement it!
	chopper.remove_videos()
	chopper.cutAudioIntoXSecondsParts("03")
	chopper.cutLastSecondsAudio(3, offset_credits)
	chopper.fixAudioParts()

	audio_info.set_audio_infos_trim()

	wrong_trim=True

	while wrong_trim:

	from_second = str(audio_info.infosTrim[0][0][1]['pad'])
	to_second = str(float(from_second) + float(dirs.seconds[dirs.phase]))

	start_correlation = find_limits_for_trim(from_second, to_second, dirs.dir_current_start_stream, dirs.dir_current_start_clip)

	to_second = str(
		audio_info.get_last_seconds_for_ffmpeg_argument_to(dirs.dir_stream, audio_info.infosTrim[1][0][1]['pad_post']))
	from_second = str(float(to_second) - float(dirs.seconds[dirs.phase]))

	end_correlation = find_limits_for_trim(from_second, to_second, dirs.dir_current_end_stream, dirs.dir_current_end_clip)

	audio_info.write_correlation(start_correlation, end_correlation)

	if

	from_second = str(audio_info.infosTrim[0][0][1]['pad'])
	to_second = str(
		audio_info.get_last_seconds_for_ffmpeg_argument_to(dirs.dir_stream, audio_info.infosTrim[1][0][1]['pad_post']))

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

	rounded_duration_stream = round(common_functions.getDuration(dirs.dir_trimmed_stream))
	rounded_duraction_clip_without_credits = round(common_functions.getDuration(dirs.dir_clip)) - credits_offset
	if math.isclose(rounded_duration_stream, rounded_duraction_clip_without_credits, rel_tol=0.01):
		print("festejo")
		return

	print(rounded_duraction_clip_without_credits)
	print(rounded_duration_stream)
	#audio_info.set_audio_infos_edit(3)



	#audio_info.set_audio_infos_edit("0.5", 0, 2)
	#audio_info.write_infos_edit()

	#common_functions.removeAll(dirs.dirAudioParts)
	#common_functions.removeAll(dirs.dirFixedAudioParts)

# TODO test it
def find_limits_for_trim(from_second: str, to_second: str, dir_stream_output, dir_clip):
	chopper.chop(dirs.dir_audio_stream, dir_stream_output, from_second, to_second)

	slowed_stream = chopper.slow_audio(dir_stream_output)
	slowed_clip = chopper.slow_audio(dir_clip)

	correlation = correlate(slowed_clip, slowed_stream)

	if correlation < 0.7:
		print("Error")
		return correlation
		
	return correlation
