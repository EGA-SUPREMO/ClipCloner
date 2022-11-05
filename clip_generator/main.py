import os
import sys
import subprocess

import clip_generator.descript.maini as maini


def downloadClip(link: str):
	os.system("yt-dlp -f \"bestvideo[height<=720]+bestaudio[ext=m4a]/bestvideo+bestaudio\" --merge-output-format mkv -k -o \"" + maini.lastDirClip + "clip\" " + link)


if __name__ == '__main__':
	maini.run(sys.argv[1:][0])
	downloadClip(sys.argv[1:][0])