membersInClip=[]

members=[]

class GetOutOfLoop( Exception ):
    pass

class Actor(object):
    currentId = -1
    """docstring for Actor"""
    def __init__(self, name, link, arroba):
        super(Actor, self).__init__()
        self.name = name.split()
        self.link = link
        self.arroba = arroba
        Actor.currentId +=1
        self.id = Actor.currentId

def setMembers():
    global members
    fileMembersName = open("membersName.txt" , "r", encoding="utf8");
    fileMembersLink = open("membersLink.txt" , "r", encoding="utf8");
    fileMembersChannelName = open("membersChannelName.txt" , "r", encoding="utf8");
    
    names = fileMembersName.read().split("\n")
    channelNames = fileMembersChannelName.read().split("\n")
    links = fileMembersLink.read().split("\n")

    if len(names) != len(links) or len(names) != len(channelNames):
        print("ERROR ARCHIVOS NO COINCIDEN\nEl archivo con los nombres tiene ")
        print(len(names))
        print("mientras que los links son: ")
        print(len(links))
        print("y que los nombres de los canales son: ")
        print(len(channelNames))
        return

    for i in range(len(names)):
        members.append(Actor(names[i], links[i], channelNames[i]))

setMembers()

def addMatch(words):
    global membersInClip
    try:
        for i in range(len(words)):
            for member in members:
                for memberName in member.name:
                    nexti = i+1
                    if "related" in words[i].lower() and "video" in words[nexti].lower():
                        raise GetOutOfLoop
                    if " " + words[i].lower() + " " in " " + memberName.lower() + " ":
                        membersInClip.append(member.id)
    except GetOutOfLoop:
        pass
    finally:
        membersInClip = list(dict.fromkeys(membersInClip))

def removeMatchs():
    global membersInClip
    membersInClip = []

def getNames(title):
    words = title.split()
    addMatch(words)

def getNamesByFile(file):
    f = open(file, "r", encoding="utf8")
    words = f.read().split()
    addMatch(words)
    f.close()
