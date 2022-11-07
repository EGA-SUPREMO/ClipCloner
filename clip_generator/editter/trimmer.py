import math

import clip_generator.editter.chopper as chopper
import clip_generator.editter.audio_info as audio_info
import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions
from clip_generator.editter.correlation import correlate

correct_trim = True
current_stream = dirs.dir_worstaudio_stream

def trim_to_clip(is_stream_a_video=False, offset_credits=0):
	global current_stream
	dirs.update_phase(0)

	chopper.remove_video(dirs.dir_clip, dirs.dir_audio_clip)
	if is_stream_a_video:
		current_stream = dirs.dir_worstaudio_stream
		chopper.remove_video(dirs.dir_stream, dirs.dir_audio_stream)
	chopper.cutAudioIntoXSecondsParts(str(dirs.get_second()))
	chopper.cutLastSecondsAudio(dirs.get_second(), int(offset_credits))
	chopper.fixAudioParts()

	find_timestamps_for_trim(is_stream_a_video)

	if is_stream_a_video:
		from_second, to_second = find_limits_for_trim("full")
		chopper.chop(current_stream, dirs.dir_trimmed_stream, from_second, to_second)
	return find_limits_for_trim("full")

def teste():
	#chopper.removeVideo()
	chopper.cutAudioIntoXSecondsParts("1")
	#chopper.cutAudioIntoXSecondsParts("3")
	chopper.fixAudioParts()

#audio_info.set_audio_infos_edit("0.5", 0, 2)
	#audio_info.write_infos_edit()


# To copy clip's edition
def auto_edit(credits_offset=0):
	trim_to_clip(True, credits_offset)

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


def check_correlation_at(from_second, to_second, dir_stream_input, dir_stream_output, dir_clip):
	global correct_trim

	chopper.chop(dir_stream_input, dir_stream_output, from_second, to_second)

	slowed_stream = chopper.slow_audio(dir_stream_output)
	slowed_clip = chopper.slow_audio(dir_clip)

	correlation = correlate(slowed_clip, slowed_stream)

	if correlation < 0.7:
		correct_trim = False
		print("Error correlation: " + str(correlation) + dir_stream_output)
		return correlation

	return correlation


def find_limits_for_trim(limit_type: str):
	from_second = audio_info.infosTrim[0][0][1]['pad']
	to_second = audio_info.get_last_seconds_for_ffmpeg_argument_to(current_stream, audio_info.infosTrim[1][0][1]['pad_post'])

	match limit_type:
		case "only_start":
			to_second = from_second + dirs.get_second()
			return from_second, to_second
		case "only_end":
			from_second = to_second - dirs.get_second()
			return from_second, to_second
		case "full":
			return from_second, to_second

	return from_second, to_second


def check_correlation_for_trim(limit_type: str, dir_input_stream: str, dir_output_stream: str, dir_clip: str):
	from_second, to_second = find_limits_for_trim(limit_type)

	return check_correlation_at(from_second, to_second, dir_input_stream, dir_output_stream, dir_clip)


def find_timestamps_for_trim(contains_video=False):
	while True:
		audio_info.set_audio_infos_trim(current_stream)

		input_stream = dirs.dir_worstaudio_stream
		if contains_video:
			input_stream = dirs.dir_audio_stream

		start_correlation = check_correlation_for_trim("only_start", input_stream, dirs.dir_current_start_stream, dirs.dir_current_start_clip)
		end_correlation = check_correlation_for_trim("only_end", input_stream, dirs.dir_current_end_stream, dirs.dir_current_end_clip)

		audio_info.misalignment = audio_info.misalignment + 1500
		if audio_info.misalignment > 20000 or correct_trim:
			print("Error, possibly wrong files")
			audio_info.misalignment = 6000
			if not contains_video:
				from_second, to_second = find_limits_for_trim("full")
				audio_info.write_infos_trim(from_second, to_second)
				audio_info.write_correlation(start_correlation, end_correlation)
			return
