import os
import sys
import subprocess

import clip_generator.descript.maini as maini

maini.run()

os.system("youtube-dl -f \"bestvideo[height<=720]+bestaudio[ext=m4a]/bestvideo+bestaudio\" --merge-output-format mkv -o \"" + maini.dirClips + "clip\" " + sys.argv[1:][0])
