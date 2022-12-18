import clip_generator.editter.trimmer as trimmer
import sys

credits_offset=0
is_video=0

if __name__ == '__main__':
	try:
		is_video = bool(sys.argv[1:][0])
		credits_offset = int(sys.argv[1:][1])
	except IndexError:
	    pass

	trimmer.trim_to_clip(is_video, offset_credits=credits_offset)
