descrClip = "- Clip Original:"
descrStream = "- Link del Stream:"
descrChannel = "- "
tags={"#Hololive", "#Vtuber"}




class Actor(object):
    currentId = 0
    """docstring for Actor"""
    def __init__(self, name, link, arroba):
        super(Actor, self).__init__()
        self.name = name.split()
        self.link = link
        self.arroba = arroba
        Actor.currentId +=1
        self.id = Actor.currentId
        
members=[Actor("Shirakami Fubuki", "https://youtube.com/chennel/ceohurc", "Fubu Ch."), Actor("Sakura Miko","hey","Miko Ch.")]

def getNames(title):
    words = title.split()
    for word in words:
        for member in members:
            for memberName in member.name:
                if " " + word.lower() + " " in " " + memberName.lower() + " ":
                    print(word)
                    print(memberName)
                    print(member.id)


getNames("Fubuki se cae xd y mata a Miko Fubu")