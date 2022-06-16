import os
import sys
import subprocess
import descript.maini

#clip_path = os.path.join('..', 'clip')
#clip_path = os.path.join(os.getcwd(), script_path)
#print(clip_path)

os.system("youtube-dl -f \"bestvideo[height<=720]+bestaudio/best[height<=720]\" -o ../Clips/clip " + sys.argv[1:][0])

#script_path = os.path.join('Description-generator', 'main.py')
#script_path = os.path.join(os.getcwd(), script_path)

#subprocess.Popen("python '"+script_path +"' '" + sys.argv[1:][0]+"'")