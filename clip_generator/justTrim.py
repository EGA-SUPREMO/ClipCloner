import clip_generator.editter.trimmer as trimmer
import sys

credits_offset=0
is_video=0
phase=0

if __name__ == '__main__':
	is_video = sys.argv[1:][0].lower() == "true"
	credits_offset = int(sys.argv[1:][1])
	
	if len(sys.argv[1:])>2:
		phase = int(sys.argv[1:][2])

	trimmer.trim_to_clip(is_video, offset_credits=credits_offset, phase=phase)
