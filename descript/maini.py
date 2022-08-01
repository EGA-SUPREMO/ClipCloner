import sys
import re
import os
import subprocess
from pathlib import Path

import descript.getmembers as getmembers
#WRITE ONLY CODE

title=subprocess.run(['youtube-dl', '--skip-download', '--get-title', '--no-warnings', '--youtube-skip-dash-manifest', sys.argv[1:][0]], stdout=subprocess.PIPE).stdout.decode('utf-8')

title_without_special_chars = re.sub('[^A-Za-z0-9 ]+', '', title)
dirClips = f"../Clips/{title_without_special_chars}/"

Path(dirClips).mkdir(parents=True, exist_ok=True)

os.system("youtube-dl --write-thumbnail --skip-download  --no-warnings --youtube-skip-dash-manifest -o \"" + dirClips + "thumb\"" + " " + sys.argv[1:][0])
os.system("youtube-dl --skip-download --no-warnings --write-description --youtube-skip-dash-manifest -o desc " + sys.argv[1:][0])

descrClip = "- Clip original: "
descrStream = "- Stream original: "
descrChannel = "- "
tags=["#hololive", "#vtuber"]

fullDescr = ""

fileName = "../desc.description"
dir = os.path.dirname(__file__)
realdir = os.path.join(dir, fileName)

getmembers.getNames(title)
getmembers.getNamesByFile(realdir)

def setTitle():
    global fullDescr
    global title
    fullDescr += title + '\n'

setTitle()

def setDescrClip():
    global descrClip
    global fullDescr
    descrClip += sys.argv[1:][0]
    fullDescr += descrClip

setDescrClip()

def setStream(file):
    global fullDescr
    global descrStream
    
    if len(sys.argv[1:])>=2:
        descrStream += sys.argv[1:][1]
        fullDescr += "\n" + descrStream
        return

    f = open(file, "r", encoding="utf8")
    text = f.read()
    matchs = re.findall("\n.*\s.*", text)
    matchLinks = re.findall("https://.*", text)
    realMatchs = []
    fileMatch = open(f"{dirClips}streams.txt", "w")

    #this for is only for writing all the streams linked to the description, in case the first one was wrong
    for match in matchLinks:
        if len(re.findall(".*channel.*", match))==1 or len(re.findall(".*twitter.*", match))==1 or len(re.findall(".*dova-s.jp.*", match))==1 or len(re.findall(".*pixiv.*", match))==1:#checking if matchs contains "twitter", channel, dova, if so, dont write it in the file
            pass
        else:
            fileMatch.write(match + "\n")

    for match in matchs:
        if len(re.findall(".*channel.*", match))==1 or len(re.findall(".*twitter.*", match))==1 or len(re.findall(".*dova-s.jp.*", match))==1 or len(re.findall(".*pixiv.*", match))==1:
            continue
        if len(re.findall(".*youtu*", match))==1:
            realMatchs.append(match+"")


    if len(realMatchs)>=1:
        descrStream += realMatchs[0]
    fullDescr += "\n" + descrStream + "\n"

setStream(realdir)

def setChannels():
    fulldescrChannel = ""
    global fullDescr

    for i in range(len(getmembers.membersInClip)):
        fullName = getmembers.members[getmembers.membersInClip[i]].name[0] + " " + getmembers.members[getmembers.membersInClip[i]].name[1]
        fulldescrChannel += "\n" + descrChannel + fullName + " / @" + getmembers.members[getmembers.membersInClip[i]].arroba + ": " + getmembers.members[getmembers.membersInClip[i]].link
    fullDescr +=  fulldescrChannel

setChannels()

def setTags():
    global tags, fullDescr
    for i in range(len(getmembers.membersInClip)):
        tags.insert(i + 1, "#" + getmembers.members[getmembers.membersInClip[i]].name[1].lower())
    fullDescr += "\n"
    fullDescr += "\n"
    for tag in tags:
        fullDescr += tag + " "
setTags()


f = open(f"{dirClips}descr.txt", 'w', encoding="utf8")
f.write(fullDescr)
