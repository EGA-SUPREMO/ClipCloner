import os
import sys
import subprocess

import clip_generator.descript.maini as maini
import clip_generator.editter.dirs as dirs


def download_video(format: str, dir_video: str, link: str):
    os.system("yt-dlp -q --progress -f \"" + format + "\" --merge-output-format mkv -o \"" + dir_video + "\" " + link)


def download_clip(link: str):
    download_video("bestvideo[height<=720]+bestaudio[ext=m4a]/bestvideo+bestaudio", dirs.last_dir_clip + 'clip', link)


def download_stream(link: str, from_second: int, to_second: int):
    if to_second - from_second > 900:
        print("SON MAS DE 15 MINUTOS LA DESCARGA, SALTANDO DESCARGA DE STREAM: " + str(to_second - from_second))
        return
    print("Stream duration: " + str(to_second - from_second))
    # para descargar el estream siempre tiene que ser unos segundos antes y unos despues de lo contrario no se descarga
    # al 100 %
    from_second = str(from_second - 1)
    to_second = str(to_second + 1)
    noice = subprocess.run(['yt-dlp', '-q', '--progress', '-R', 'infinite', '--force-keyframes-at-cuts', '--no-warnings', '-o', dirs.dir_stream,
                            '--merge-output-format', 'mkv',  '--download-sections',
                            '*' + from_second + '-' + to_second + '', link],
                           stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(noice)


if __name__ == '__main__':
    maini.run(sys.argv[1:][0])
    download_clip(sys.argv[1:][0])
