import math
import os.path

import clip_generator.editter.chopper as chopper
import clip_generator.editter.audio_info as audio_info
import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions
import clip_generator.editter.correlation as correlation

correct_trim = True
current_stream = dirs.dir_worstaudio_stream


def trim_to_clip(is_stream_a_video=False, offset_credits=0):
	global current_stream
	dirs.update_phase(0)

	chopper.remove_video(dirs.dir_clip, dirs.dir_audio_clip)

	current_stream = dirs.dir_worstaudio_stream
	if is_stream_a_video:
		current_stream = dirs.dir_stream
		chopper.remove_video(dirs.dir_stream, dirs.dir_audio_stream)
		
	#chopper.cutAudioIntoXSecondsParts(str(dirs.get_second()))
	chopper.cut_audio(dirs.dir_audio_clip, dirs.dir_current_start_clip, 0.5, 3)
	chopper.cutLastSecondsAudio(dirs.get_second(), int(offset_credits))
	chopper.fixAudioParts()

	find_timestamps_for_trim(is_stream_a_video, int(offset_credits))

	if is_stream_a_video:
		from_second, to_second = find_limits_for_trim("full")
		chopper.chop(current_stream, dirs.dir_trimmed_stream, from_second, to_second)

	#common_functions.removeAll(dirs.dir_temp_files)
	return find_limits_for_trim("full")


# To copy clip's edition
def auto_edit(credits_offset=0):
	trim_to_clip(True, credits_offset)

	rounded_duration_stream = round(common_functions.getDuration(dirs.dir_trimmed_stream))
	rounded_duration_clip_without_credits = round(common_functions.getDuration(dirs.dir_clip)) - credits_offset
	if math.isclose(rounded_duration_stream, rounded_duration_clip_without_credits, rel_tol=0.01):
		print("festejo")
		return

	print(rounded_duration_clip_without_credits)
	print(rounded_duration_stream)

	audio_info.set_audio_infos_edit(3)

	#audio_info.set_audio_infos_edit("0.5", 0, 2)
	#audio_info.write_infos_edit()

	#common_functions.removeAll(dirs.dirAudioParts)
	#common_functions.removeAll(dirs.dirFixedAudioParts)


# TODO Needs tests
def auto_edit_by_images():
	chopper.remove_video(dirs.dir_trimmed_stream, dirs.dir_audio_trimmed_stream)

	chopper.round_duration_cutting_existing_video_for_compare_image(dirs.dir_audio_clip, dirs.dir_audio_clip_rounded)
	chopper.round_duration_cutting_existing_video_for_compare_image(dirs.dir_audio_trimmed_stream, dirs.dir_audio_stream_rounded)

	chopper.convert_audio_into_wave_image(dirs.dir_audio_clip_rounded, dirs.dir_audio_clip_image, "red", dirs.scale_edit)
	chopper.convert_audio_into_wave_image(dirs.dir_audio_stream_rounded, dirs.dir_audio_stream_image, "blue", dirs.scale_edit)

	audio_info.set_audio_infos_edit_by_image()

	chopper.final_chop(dirs.dir_trimmed_stream, dirs.dir_edited_stream, audio_info.infosEdit)


def check_correlation_at(from_second, to_second, dir_stream_input, dir_stream_output, dir_clip):
	global correct_trim

	chopper.chop(dir_stream_input, dir_stream_output, from_second, to_second)

	slowed_stream = chopper.slow_audio(dir_stream_output)
	slowed_clip = chopper.slow_audio(dir_clip)

	correl = correlation.correlate(slowed_clip, slowed_stream)

	if correl < 0.80:
		correct_trim = False
		print("Error correlation: " + str(correl) + dir_stream_output)
		return correl

	return correl


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
			return from_second  - 0.5, to_second  + dirs.transition_offset  # chopper cuts one second sooner to avoid
							# errors with transitions/credits, so this time we subtract one to compensate and make it
							# one second longer
							# We chop 0.5 after clip starts because it may have some transiction,
							# if you change this, change at the begining also

	return from_second, to_second


def check_correlation_for_trim(limit_type: str, dir_input_stream: str, dir_output_stream: str, dir_clip: str):
	from_second, to_second = find_limits_for_trim(limit_type)

	return check_correlation_at(from_second, to_second, dir_input_stream, dir_output_stream, dir_clip)


def find_timestamps_for_trim(contains_video=False, offset_credits=0):
	clip_duration = common_functions.getDuration(dirs.dir_audio_clip) - 5 - offset_credits
	start_correlation = 0
	end_correlation = 0

	input_stream = dirs.dir_worstaudio_stream
	if contains_video:
		input_stream = dirs.dir_audio_stream

	while True:
		if start_correlation < 0.8:
			audio_info.set_audio_infos_trim_start(input_stream)
			start_correlation = check_correlation_for_trim("only_start", input_stream, dirs.dir_current_start_stream, dirs.dir_current_start_clip)
		elif not os.path.exists(dirs.dir_start_only_untrimmed_stream):
			from_second, to_second = find_limits_for_trim("only_start")
			chopper.chop(current_stream, dirs.dir_start_only_untrimmed_stream, from_second, to_second)
			input_stream = dirs.dir_start_only_untrimmed_stream

		if end_correlation < 0.8:
			audio_info.set_audio_infos_trim_end(input_stream)
			end_correlation = check_correlation_for_trim("only_end", input_stream, dirs.dir_current_end_stream, dirs.dir_current_end_clip)
		elif not os.path.exists(dirs.dir_end_only_untrimmed_stream):
			from_second, to_second = find_limits_for_trim("only_end")
			chopper.chop(current_stream, dirs.dir_end_only_untrimmed_stream, from_second, to_second)
			input_stream = dirs.dir_end_only_untrimmed_stream

		audio_info.misalignment = audio_info.misalignment + 2000

		from_second, to_second = find_limits_for_trim("full")
		stream_duration = to_second - from_second

		if audio_info.misalignment > 8000:
			print("Error, wrong files perhaps?")

			if stream_duration <= clip_duration:
				print("Wrong match, stream duration is smaller than clip duration")
				raise Exception("Clip duration is significantly bigger than stream duration")

		if (correct_trim and stream_duration >= clip_duration) or audio_info.misalignment > 8000:
			audio_info.misalignment = 6000
			from_second, to_second = find_limits_for_trim("full")
			if not contains_video:
				audio_info.write_infos_trim(from_second, to_second)
				audio_info.write_correlation(start_correlation, end_correlation)

			return from_second, to_second, start_correlation, end_correlation
