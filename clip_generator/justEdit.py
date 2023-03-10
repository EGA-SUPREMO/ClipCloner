import clip_generator.editter.trimmer as trimmer
import sys

credits_offset = 0

if __name__ == '__main__':
    try:
        trimmer.remove_credits_offsets(sys.argv[1:][0], sys.argv[1:][1])
    except IndexError:
        pass

    trimmer.auto_edit()
