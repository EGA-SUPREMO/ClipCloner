import os
import subprocess
import sys

urlsText=subprocess.run(['youtube-dl', '-g', '--no-warnings', '--youtube-skip-dash-manifest', sys.argv[1:][0]], stdout=subprocess.PIPE).stdout.decode('utf-8')
urls = urlsText.split()

#el comando es este
#ffmpeg -y -ss '" + sys.argv[1:][1] + "' -i '" + urls[0] + "' -ss '" + sys.argv[1:][1] + "' -i '" + urls[1] + "' -map 0:v -map 1:a -ss 5 -t '" + sys.argv[1:][2] + "' -c:v libx265 -c:a aac '../Clips/stream.mkv'
noice = subprocess.run(["ffmpeg", "-y", '-ss', sys.argv[1:][1], '-i', urls[0], '-ss', sys.argv[1:][1], '-i', urls[1], '-map', '0:v', '-map', '1:a', '-ss', '5', '-t', sys.argv[1:][2], '-c:v', 'libx265', '-c:a', 'aac', '../Clips/stream.mkv'], stdout=subprocess.PIPE).stdout.decode('utf-8')
print(noice)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ cambiar el ss del final a 5 pero antes usarlo con el dos con cuatro segundos de duracion