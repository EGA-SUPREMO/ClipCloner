import clip_generator.editter.trimmer as trimmer
import sys

credits_offset=0
is_video=0
phase=0

if __name__ == '__main__':
	is_video = sys.argv[1:][0].lower() == "true"
	
	if len(sys.argv[1:])>3:
		phase = int(sys.argv[1:][3])

	trimmer.remove_credits_offsets(sys.argv[1:][1], sys.argv[1:][2])
	trimmer.trim_to_clip(is_video, offset_credits=0, phase=phase)
