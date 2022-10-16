import clip_generator.editter.trimmer as trimmer
import sys

credits_offset=1

if __name__ == '__main__':
	try:
		credits_offset = int(sys.argv[1:][0])
	except IndexError:
	    pass

	trimmer.trim_to_clip(credits_offset)
