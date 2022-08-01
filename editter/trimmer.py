import editter.chopper as chopper
import editter.audio_info as audio_info

#For auto edit
#removeVideo()
#cutAudioIntoXSecondsParts("01")
#fixAudioParts()

def trim_to_clip():
	chopper.removeVideo()
	chopper.cutAudioIntoXSecondsParts("03")
	chopper.cutLastSecondsAudio(3)
	chopper.fixAudioParts()

	audio_info.set_audio_infos_trim(3)
	#audio_info.print_infos_trim()

	chopper.chop()
