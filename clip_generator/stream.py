import os
import subprocess
import sys

import clip_generator.editter.dirs as dirs


def download_stream(link: str, from_second: int, to_second: int):
    if to_second - from_second > 300:
        print("SON MAS DE 5 MINUTOS LA DESCARGA, SALTANDO DESCARGA DE STREAM: " + str(to_second - from_second))
        return
    print("Stream duration: " + str(to_second - from_second))
    # para descargar el estream siempre tiene que ser unos segundos antes y unos despues de lo contrario no se descarga
    # al 100 %
    from_second = str(from_second - 1)
    to_second = str(to_second + 1)
    noice = subprocess.run(['yt-dlp', '-R', 'infinite', '--no-warnings', '-o', dirs.dir_stream, '--merge-output-format',
                        'mkv',  '--download-sections', '*' + from_second + '-' + to_second + '', link], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(noice)

if __name__ == '__main__':
    from_second = sys.argv[1:][1]
    to_second = sys.argv[1:][2]

    download_stream(sys.argv[1:][0], from_second, to_second)
