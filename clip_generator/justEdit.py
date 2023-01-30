import clip_generator.editter.trimmer as trimmer
import sys

from clip_generator.editter import chopper, dirs, audio_info

credits_offset=0

if __name__ == '__main__':
    try:
        credits_offset = int(sys.argv[1:][0])
    except IndexError:
        pass

    trimmer.auto_edit(credits_offset)
    chopper.cut_video_into_separate_files(dirs.dir_stream, audio_info.infosEdit)
