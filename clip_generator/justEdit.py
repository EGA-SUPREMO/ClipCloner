import clip_generator.editter.trimmer as trimmer
import sys

credits_offset=0

if __name__ == '__main__':
	try:
		credits_offset = int(sys.argv[1:][0])
	except IndexError:
	    pass

	trimmer.auto_edit(credits_offset)
