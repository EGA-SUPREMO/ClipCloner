import re
import os
import subprocess
from pathlib import Path

import clip_generator.descript.getmembers as getmembers
import clip_generator.editter.dirs as dirs


# WRITE ONLY CODE

def getTitle(link):
    return subprocess.run(
        ['yt-dlp', '--skip-download', '--get-title', '--no-warnings', '--youtube-skip-dash-manifest', link],
        stdout=subprocess.PIPE).stdout.decode('utf-8')


def getTitleWithoutSpecialChars(title):
    return re.sub('[^A-Za-z0-9 ]+', '', title).strip()


def downloadSmallFiles(dirClips, link):
    Path(dirClips).mkdir(parents=True, exist_ok=True)

    os.system(
        "yt-dlp --write-thumbnail --skip-download  --no-warnings --youtube-skip-dash-manifest -o \"" + dirClips + "thumb\"" + " " + link)
    os.system(
        "yt-dlp --skip-download --no-warnings --write-description --youtube-skip-dash-manifest -o desc " + link)


descrClip = "- Clip original: "
descrStream = "- Stream original: "
descrChannel = "- "
tags = ["#hololive", "#vtuber"]

title = ""
stream_links = []

fileName = "../../desc.description"

fullDescr = ""


def resetVars():
    global fullDescr, title, descrClip, descrStream, descrChannel, tags, title
    descrClip = "- Clip original: "
    descrStream = "- Stream original: "
    descrChannel = "- "
    tags = ["#hololive", "#vtuber"]

    fullDescr = ""
    getmembers.removeMatchs()


def setTitle(title):
    global fullDescr
    fullDescr += title + '\n'


def setDescrClip(link):
    global descrClip
    global fullDescr
    descrClip += link
    fullDescr += descrClip


def setStream(file, dirClips):
    global fullDescr
    global descrStream
    global stream_links

    f = open(file, "r", encoding="utf8")
    text = f.read()
    matchs = re.findall("\n.*\s.*", text)
    matchLinks = re.findall("https://([^\s]+)", text) # Get the whole line starting with https:// until the first space
    realMatchs = []
    fileMatch = open(f"{dirClips}streams.txt", "w")

    # this for is only for writing all the streams linked to the description, in case the first one was wrong
    for match in matchLinks:
        if len(re.findall(".*channel.*", match)) == 1 or len(re.findall(".*twitter.*", match)) == 1 or len(
                re.findall(".*dova-s.jp.*", match)) == 1 or len(re.findall(".*pixiv.*", match)) == 1 or len(
                re.findall(".*facebook.*", match)) == 1 or len(re.findall(".*youtube.com/c/.*", match)) == 1:
            # checking if matchs contains "twitter", channel, dova, if so, dont write it in the file
            pass
        else:
            fileMatch.write(match + "\n")
            stream_links.append(match + "")

    for match in matchs:
        if len(re.findall(".*channel.*", match)) == 1 or len(re.findall(".*twitter.*", match)) == 1 or len(
                re.findall(".*dova-s.jp.*", match)) == 1 or len(re.findall(".*pixiv.*", match)) == 1 or len(
                re.findall(".*facebook.*", match)) == 1 or len(re.findall(".*youtube.com/c/.*", match)) == 1:
            continue
        if len(re.findall(".*youtu*", match)) == 1:
            realMatchs.append(match + "")

    fileMatch.close()
    f.close()
    if len(realMatchs) >= 1:
        descrStream += realMatchs[0]
    fullDescr += "\n" + descrStream + "\n"


def setChannels():
    fulldescrChannel = ""
    global fullDescr

    for i in range(len(getmembers.membersInClip)):
        fullName = getmembers.members[getmembers.membersInClip[i]].name[0] + " " + \
                   getmembers.members[getmembers.membersInClip[i]].name[1]
        fulldescrChannel += "\n" + descrChannel + fullName + " / @" + getmembers.members[
            getmembers.membersInClip[i]].arroba + ": " + getmembers.members[getmembers.membersInClip[i]].link
    fullDescr += fulldescrChannel


def setRecruitmentAd():
    global fullDescr
    fullDescr += "\n\n" + """Te interesa formar parte del equipo? Escribenos en: usadatranslations@gmail.com
Discord: ElNo Studió # 5137"""


def setTags():
    global tags, fullDescr
    for i in range(len(getmembers.membersInClip)):
        if len(getmembers.members[getmembers.membersInClip[i]].name[1].lower())>1:
            tags.insert(i + 1, "#" + getmembers.members[getmembers.membersInClip[i]].name[1].lower())
    fullDescr += "\n"
    fullDescr += "\n"
    for tag in tags:
        fullDescr += tag + " "


def writeDescr(dirClips):
    f = open(f"{dirClips}descr.txt", 'w', encoding="utf8")
    f.write(fullDescr)
    f.close()


def run(link):  # Write only code, but dont ever dare to change function's order
    global title
    title = getTitle(link)
    title_without_special_chars = getTitleWithoutSpecialChars(title)

    dirClip = dirs.dir_clip_folder + title_without_special_chars + "/"
    dirs.update_clip_dirs(title_without_special_chars)

    dir = os.path.dirname(__file__)
    realdir = os.path.join(dir, fileName)

    downloadSmallFiles(dirClip, link)

    getmembers.getNames(title)
    getmembers.getNamesByFile(realdir)

    setTitle(title)
    setDescrClip(link)
    setStream(realdir, dirClip)
    setChannels()
    setRecruitmentAd()
    setTags()

    writeDescr(dirClip)
    resetVars()
