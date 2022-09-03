import os
import subprocess
import sys

#import editter.trimmer

urlsText=subprocess.run(['youtube-dl', '-g', '--no-warnings', '--youtube-skip-dash-manifest', sys.argv[1:][0]], stdout=subprocess.PIPE).stdout.decode('utf-8')
urls = urlsText.split()

#el comando es este
#ffmpeg -y -ss '" + sys.argv[1:][1] + "' -i '" + urls[0] + "' -ss '" + sys.argv[1:][1] + "' -i '" + urls[1] + "' -map 0:v -map 1:a -ss 5 -t '" + sys.argv[1:][2] + "' -c:v libx265 -c:a aac '../Clips/stream.mkv'
noice = subprocess.run(["ffmpeg", "-y", '-ss', sys.argv[1:][1], '-i', urls[0], '-ss', sys.argv[1:][1], '-i', urls[1], '-map', '0:v', '-map', '1:a', '-ss', '5', '-t', sys.argv[1:][2], '-c:v', 'libx265', '-c:a', 'aac', '../Clips/stream.mkv'], stdout=subprocess.PIPE).stdout.decode('utf-8')
print(noice)

# para descargar el estream siempre tiene que ser sinco segundos antes de lo contrario falla y la duracion sin modificancion
#editter.trimmer.trim_to_clip()