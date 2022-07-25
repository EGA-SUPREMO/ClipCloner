import chopper
import audio_info

chopper.cutAudioIntoXSecondsParts("03")
chopper.cutLastSecondsAudio(3)
chopper.fixAudioParts()

audio_info.set_audio_infos_trim(3)
audio_info.print_infos_trim()

#10.048
#109.696
#106.952
#6.304000000000002

#10.048
#109.696
#106.952
#7.323999999999998

#ss 10
#sseof 7