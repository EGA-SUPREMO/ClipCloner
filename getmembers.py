membersInClip=[]

members=[]

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
    fileMembersName = open("membersName.txt" , "r");
    fileMembersLink = open("membersLink.txt" , "r");
    names = fileMembersName.read().split("\n")
    links = fileMembersLink.read().split("\n")

    if len(names) != len(links):
        print("ERROR ARCHIVOS NO COINCIDEN\nEl archivo con los nombres tiene ")
        print(len(names))
        print("mientras que los links son: ")
        print(len(links))
        return

    for i in range(len(names)):
        members.append(Actor(names[i], links[i], "WIP"))

setMembers()

def addMatch(words):
    global membersInClip
    for word in words:
        for member in members:
            for memberName in member.name:
                if " " + word.lower() + " " in " " + memberName.lower() + " ":
                    membersInClip.append(member.id)
    membersInClip = list(dict.fromkeys(membersInClip))

def getNames(title):
    words = title.split()
    addMatch(words)

def getNamesByFile(file):
    f = open(file, "r")
    words = f.read().split()
    addMatch(words)

