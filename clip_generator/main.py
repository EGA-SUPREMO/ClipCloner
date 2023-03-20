import sys

import clip_generator.editter.auto_editter
import clip_generator.editter.chopper
import clip_generator.editter.dirs as dirs
import clip_generator.descript.maini as maini
import clip_generator.downloader as downloader
import clip_generator.editter.trimmer as trimmer
import clip_generator.editter.chopper as chopper

if __name__ == '__main__':
    maini.run(sys.argv[1:][0])
    downloader.download_clip(sys.argv[1:][0])
    downloader.download_video("worstaudio", dirs.dir_worstaudio_stream, maini.stream_links[0])
    chopper.increase_speed_video(dirs.dir_clip, dirs.dir_clip_with_speed)
    clip_generator.editter.chopper.remove_credits_offsets(sys.argv[1:][1], sys.argv[1:][2])

    from_second, to_second = trimmer.trim_to_clip(False)
    downloader.download_stream(maini.stream_links[0], from_second, to_second)

    clip_generator.editter.auto_editter.auto_edit()
