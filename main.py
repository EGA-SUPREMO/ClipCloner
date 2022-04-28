import sys
import re

import getmembers
#WRITE ONLY CODE


descrClip = "- Clip original: "
descrStream = "- Stream original: "
descrChannel = "- "
tags=["#hololive", "#vtuber"]

fullDescr = ""

fileName = "../Clips/desc.description"
getmembers.getNames(sys.argv[1:][0])
getmembers.getNamesByFile(fileName)

def setDescrClip():
    global descrClip
    global fullDescr
    descrClip += sys.argv[1:][1]
    fullDescr += descrClip

setDescrClip()

def setStream(file):
    global fullDescr
    global descrStream
    
    if len(sys.argv[1:])>=3:
        descrStream += sys.argv[1:][2]
        fullDescr += "\n" + descrStream
        return

    f = open(file, "r")
    text = f.read()
    matchs = re.findall("\n.*\s.*", text)

    if len(matchs)>=1:
        descrStream += matchs[0]
    fullDescr += "\n" + descrStream + "\n"

setStream(fileName)

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


print(fullDescr)
