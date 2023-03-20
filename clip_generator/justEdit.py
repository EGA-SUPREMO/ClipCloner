import clip_generator.editter.auto_editter
import clip_generator.editter.chopper
import clip_generator.editter.trimmer as trimmer
import sys

credits_offset = 0

if __name__ == '__main__':
    try:
        clip_generator.editter.chopper.remove_credits_offsets(sys.argv[1:][0], sys.argv[1:][1])
    except IndexError:
        print("error. Not enough arguments")

    clip_generator.editter.auto_editter.auto_edit()
