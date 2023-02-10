import math
import os.path

import clip_generator.editter.chopper as chopper
import clip_generator.editter.audio_info as audio_info
import clip_generator.editter.dirs as dirs
import clip_generator.common_functions as common_functions
import clip_generator.editter.correlation as correlation
import clip_generator.editter.info_processor
from clip_generator.editter import info_processor

correct_trim = True
current_stream = dirs.dir_worstaudio_stream


def trim_to_clip(is_stream_a_video=False, offset_credits=0, phase=0):
	global current_stream

	common_functions.removeAll(dirs.dir_temp_files)
	dirs.update_phase(phase)

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

	common_functions.removeAll(dirs.dir_temp_files)
	return find_limits_for_trim("full")


# To copy clip's edition
def auto_edit(credits_offset=0):
	common_functions.removeAll(dirs.dir_temp_files)
	dirs.update_phase(1)

	rounded_duration_stream = round(common_functions.getDuration(dirs.dir_stream))
	rounded_duration_clip_without_credits = round(common_functions.getDuration(dirs.dir_clip)) - credits_offset
	audio_parts = round(rounded_duration_clip_without_credits/dirs.get_second_for_edit())

	if math.isclose(rounded_duration_stream, rounded_duration_clip_without_credits, rel_tol=0.01):
		print("The clip duration is the same as trimmed stream duration")
	#	return

	chopper.remove_video(dirs.dir_clip, dirs.dir_audio_clip)
	chopper.remove_video(dirs.dir_stream, dirs.dir_audio_stream)

	chopper.cutAudioIntoXSecondsParts(str(dirs.get_second_for_edit()))
	chopper.fixAudioParts()

	# audio_info.set_audio_infos_edit("3", "video_align", 0, 20)
	audio_info.set_audio_infos_edit(str(dirs.get_second_for_edit()), "corr", 0, audio_parts)
	# audio_info.set_audio_infos_edit("0.5", 0, 2)

	chopper.final_chop(dirs.dir_stream, dirs.dir_edited_stream, audio_info.infosEdit)
	chopper.cut_video_into_separate_files(dirs.dir_stream, audio_info.infosEdit)

	common_functions.removeAll(dirs.dir_temp_files)


# TODO Needs no tests
def auto_edit_by_images():
	chopper.remove_video(dirs.dir_trimmed_stream, dirs.dir_audio_trimmed_stream)

	chopper.round_duration_cutting_existing_video_for_compare_image(dirs.dir_audio_clip, dirs.dir_audio_clip_rounded)
	chopper.round_duration_cutting_existing_video_for_compare_image(dirs.dir_audio_trimmed_stream, dirs.dir_audio_stream_rounded)

	chopper.convert_audio_into_wave_image(dirs.dir_audio_clip_rounded, dirs.dir_audio_clip_image, "red", dirs.scale_edit, ":filter=average:scale=sqrt")
	chopper.convert_audio_into_wave_image(dirs.dir_audio_stream_rounded, dirs.dir_audio_stream_image, "blue", dirs.scale_edit, ":filter=average:scale=sqrt")

	audio_info.set_audio_infos_edit_by_image()
	#audio_info.offset_info_edit()
	
	# TODO write the results in the timestamps json file
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
	match limit_type:
		case "only_start":
			from_second = audio_info.infosTrim[0][0][1]['pad']
			to_second = from_second + dirs.get_second()
			return from_second, to_second
		case "only_end":
			to_second = audio_info.get_last_seconds_for_ffmpeg_argument_to(current_stream, audio_info.infosTrim[1][0][1]['pad_post'])
			from_second = to_second - dirs.get_second()
			return from_second, to_second
		case "full":
			from_second = audio_info.infosTrim[0][0][1]['pad']
			to_second = audio_info.get_last_seconds_for_ffmpeg_argument_to(current_stream, audio_info.infosTrim[1][0][1]['pad_post'])
			return from_second  - 0.5, to_second  + dirs.transition_offset  # chopper cuts one second sooner to avoid
							# errors with transitions/credits, so this time we subtract one to compensate and make it
							# one second longer
							# We chop 0.5 after clip starts because it may have some transiction,
							# if you change this, change at the begining also


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
		audio_info.sample_rate = 24000

	while True:
		if start_correlation < 0.8:
			audio_info.set_audio_infos_trim_start(input_stream)
			start_correlation = check_correlation_for_trim("only_start", current_stream, dirs.dir_current_start_stream, dirs.dir_current_start_clip)
		if start_correlation > 0.8 and not os.path.exists(dirs.dir_start_only_untrimmed_stream):
			from_second, __ = find_limits_for_trim("only_start")
			chopper.chop(current_stream, dirs.dir_start_only_untrimmed_stream, from_second, "999999999")
			input_stream = dirs.dir_start_only_untrimmed_stream

		if end_correlation < 0.8:
			audio_info.set_audio_infos_trim_end(input_stream)
			end_correlation = check_correlation_for_trim("only_end", current_stream, dirs.dir_current_end_stream, dirs.dir_current_end_clip)
		if end_correlation > 0.8 and not os.path.exists(dirs.dir_end_only_untrimmed_stream):
			__, to_second = find_limits_for_trim("only_end")
			chopper.chop(current_stream, dirs.dir_end_only_untrimmed_stream, "0", to_second)
			input_stream = dirs.dir_end_only_untrimmed_stream

		audio_info.misalignment = audio_info.misalignment + 2000
		audio_info.sample_rate += 4000

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
				clip_generator.editter.info_processor.write_infos_trim(from_second, to_second)
				clip_generator.editter.info_processor.write_correlation(start_correlation, end_correlation)

			return from_second, to_second, start_correlation, end_correlation
