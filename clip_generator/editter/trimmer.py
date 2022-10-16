import clip_generator.editter.chopper as chopper
import clip_generator.editter.audio_info as audio_info

import clip_generator.editter.dirs as dirs

def teste():
	#chopper.removeVideo()
	chopper.cutAudioIntoXSecondsParts("1")
	#chopper.cutAudioIntoXSecondsParts("3")
	chopper.fixAudioParts()

	#audio_info.set_audio_infos_edit("0.5", 0, 2)
	#audio_info.write_infos_edit()

#To copy clip's edittion
def auto_edit():
	chopper.removeVideo()
	chopper.cutAudioIntoXSecondsParts("3")
	chopper.fixAudioParts()

	#audio_info.set_audio_infos_edit("0.5", 0, 2)
	#audio_info.write_infos_edit()


def trim_to_clip(offset_credits=1):
	chopper.removeVideo()
	chopper.cutAudioIntoXSecondsParts("03")
	chopper.cutLastSecondsAudio(3, offset_credits)
	chopper.fixAudioParts()

	audio_info.set_audio_infos_trim(3)
	
	from_second = str(audio_info.infosTrim[0][0][1]['pad'])
	to_second = str(audio_info.get_last_seconds_for_ffmpeg_argument_to(dirs.dir_stream, audio_info.infosTrim[1][0][1]['pad_post']))
	audio_info.write_infos_trim(from_second, to_second)

	chopper.chop(from_second, to_second)
