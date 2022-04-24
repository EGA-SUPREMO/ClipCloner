import sys
import getmembers



descrClip = "- Clip original:"
descrStream = "- Stream original: "
descrChannel = "- "
tags={"#Hololive", "#Vtuber"}


getmembers.getNames(sys.argv[1:][0])

def setChannels():
    fulldescrChannel = ""

    for i in range(len(getmembers.membersInClip)):
        fullName = getmembers.members[i].name[0] + " " + getmembers.members[i].name[1]
        fulldescrChannel += "\n" + descrChannel + fullName + ": " + getmembers.members[i].link
    print(fulldescrChannel)

setChannels()

def setDescrClip():
    global descrClip
    descrClip += sys.argv[1:][1]

setDescrClip()

print(descrClip)