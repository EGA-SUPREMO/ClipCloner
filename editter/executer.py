import chopper
import audio_info
import trimmer

#For auto edit
#removeVideo()
#cutAudioIntoXSecondsParts("01")
#fixAudioParts()

chopper.removeVideo()
chopper.cutAudioIntoXSecondsParts("03")
chopper.cutLastSecondsAudio(3)
chopper.fixAudioParts()

audio_info.set_audio_infos_trim(3)

trimmer.trim()
#audio_info.print_infos_trim()

