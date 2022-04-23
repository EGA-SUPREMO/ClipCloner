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
        

hey1=Actor("Shirakami Fubuki", "https://youtube.com/chennel/ceohurc", "Fubu Ch.")
hey2=Actor("Sakura Miko","hey","Miko Ch.")
members=[Actor("Shirakami Fubuki", "https://youtube.com/chennel/ceohurc", "Fubu Ch."), Actor("Sakura Miko","hey","Miko Ch.")]
print(hey1.id)
print(hey2.id)
def getNames(title):
    words = title.split()
    for word in words:
        for member in members:
            if word.lower() in member.name:
                print("yes")
                print(word)


getNames("Fubuki se cae xd y mata a Miko")