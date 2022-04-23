descrClip = "- Clip Original:"
descrStream = "- Link del Stream:"
descrChannel = "- "
tags={"#Hololive", "#Vtuber"}




class Actor(object):
    currentId = 0
    """docstring for Actor"""
    def __init__(self, name, link, arroba):
        super(Actor, self).__init__()
        self.name = name
        self.link = link
        self.arroba = arroba
        Actor.currentId +=1
        self.id = Actor.currentId
        print(self)

hey1=Actor("Shirakami Fubuki", "https://youtube.com/chennel/ceohurc", "Fubu Ch.")
hey2=Actor("he","hey","hey")
print(hey1.id)
print(hey2.id)
def getNames(title):
    words = title.split()
    for word in words:
        if word in hey1.name:
            print("yes")
            print(word)


getNames("Fubuki se cae xd y mata a towa")