import os
import sys
import subprocess

import clip_generator.descript.maini as maini


def downloadClip(link):
	os.system("youtube-dl -f \"bestvideo[height<=720]+bestaudio[ext=m4a]/bestvideo+bestaudio\" --merge-output-format mkv -o \"" + maini.lastDirClip + "clip\" " + link)

if __name__ == '__main__':
	maini.run(link)
	downloadClip(sys.argv[1:][0])