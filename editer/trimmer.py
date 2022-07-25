import chopper
import audio_info

chopper.cutAudioIntoXSecondsParts("03")
chopper.cutLastSecondsAudio(3)
chopper.fixAudioParts()

audio_info.set_audio_infos_trim(3)
audio_info.print_infos_trim()