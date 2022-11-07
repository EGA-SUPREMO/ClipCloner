import sys

import clip_generator.editter.dirs as dirs
import clip_generator.descript.maini as maini
import clip_generator.downloader as downloader
import clip_generator.editter.trimmer as trimmer

if __name__ == '__main__':
    #maini.run(sys.argv[1:][0])
    #downloader.download_clip(sys.argv[1:][0])
    #downloader.download_video("worstaudio", dirs.dir_worstaudio_stream, maini.stream_links[0])

    print(trimmer.trim_to_clip(False, sys.argv[1:][1]))
    #downloader.download_stream(, from_second, to_second)