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
    matchLinks = re.findall("https://.*", text)
    fileMatch = open("../Clips/streams.txt", "w")

    #this for is only for writing all the streams linked to the description, in case the first one was wrong
    for match in matchLinks:
        if len(re.findall(".*channel.*", match))==1 or len(re.findall(".*twitter.*", match))==1 or len(re.findall(".*dova-s.jp.*", match))==1:#checking if matchs contains "twitter", channel, dova, if so, dont write it in the file
            pass
        else:
            fileMatch.write(match + "\n")

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

f = open('../Clips/descr.txt', 'w')
f.write(fullDescr)
