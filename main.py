import sys
import getmembers



descrClip = "- Clip original: "
descrStream = "- Stream original: "
descrChannel = "- "
tags=["#hololive", "#vtuber"]

fullDescr = ""

getmembers.getNames(sys.argv[1:][0])

def setDescrClip():
    global descrClip
    global fullDescr
    descrClip += sys.argv[1:][1]
    fullDescr += descrClip

setDescrClip()

def setChannels():
    fulldescrChannel = ""
    global fullDescr

    for i in range(len(getmembers.membersInClip)):
        fullName = getmembers.members[i].name[0] + " " + getmembers.members[i].name[1]
        fulldescrChannel += "\n" + descrChannel + fullName + ": " + getmembers.members[i].link
    fullDescr +=  fulldescrChannel

setChannels()

def setTags():
    global tags, fullDescr
    for i in range(len(getmembers.membersInClip)):
        tags.insert(i + 1, "#" + getmembers.members[i].name[1].lower())
    fullDescr += "\n"
    for tag in tags:
        fullDescr += tag + " "
setTags()

print(fullDescr)
