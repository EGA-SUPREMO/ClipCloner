import os
import subprocess
import sys

#import clip_generator.editter.trimmer


def download_stream(link: str, from_second: int, to_second: int):
    # BORRRRRRRARRR COMENTARIOS VIEJOS' ESTO NO TIENE TESTS PORQUE NO ESTA COMPLETOOOOOOOOOOOOo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # para descargar el estream siempre tiene que ser sinco segundos antes de lo contrario falla y la duracion sin modificancion
    noice = subprocess.run(['yt-dlp', '-R', 'infinite', '--no-warnings', '-o', '../../Clips/clip', '--merge-output-format',
                        'mkv',  '--download-sections', '*' + from_second + '-' + to_second + '', link], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(noice)
    #editter.trimmer.trim_to_clip()

if __name__ == '__main__':
    from_second = sys.argv[1:][1]
    to_second = sys.argv[1:][2]

    download_stream(sys.argv[1:][0], from_second, to_second)
