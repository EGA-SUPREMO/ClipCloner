import clip_generator.editter.chopper as chopper
import clip_generator.editter.dirs as dirs
import sys
import ast

time_intervals = []

if __name__ == '__main__':
    try:
        time_intervals = ast.literal_eval(sys.argv[1:][0])
    except IndexError:
        pass

    chopper.final_chop(dirs.dir_stream, dirs.dir_edited_stream, time_intervals)
    chopper.cut_video_into_separate_files(dirs.dir_stream, time_intervals)
