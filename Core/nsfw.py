import urllib.request
import os
from random import randint
import xml.etree.ElementTree

channels = []

async def postR34(message, client):
    if not isEnabled(message):
        await message.channel.send("NSFW not authorized in this channel. To authorize an admin must"
                                                   "use the ~togglensfw command")
        return

    tags = message.content[4:]
    with message.channel.typing():

        if "fur" not in tags or "furry" not in tags or "yiff" not in tags or "anthro" not in tags:
            search = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(tags) +\
                     " -fur -furry -yiff -anthro -canine -mammal -wolf"
        else:
            search = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(tags)
    
        try:
            xmlFile = urllib.request.urlopen(search)
        except:
            await message.channel.send("There was an error retrieving a post... :confounded: ")
            return
        e = xml.etree.ElementTree.parse(xmlFile)
        root = e.getroot()
    
        picUrls = []
    
        for post in root.findall('post'):
            if "furaffinity" not in post.get('source'):
                picUrls.append('http:' + post.get('file_url'))
    
        if len(picUrls) == 0:
            await message.channel.send("No results, try searching something less retarded next time!")
    
        else:
            try:
                await message.channel.send(picUrls[randint(0, len(picUrls) - 1)])
            except:
                await message.channel.send("There was an error retrieving a post... :confounded: ")
                return


def isEnabled(message):
    return str(message.channel.id) in channels


async def toggleChannel(message, client):
    if str(message.channel.id) in channels:
        channels.remove(str(message.channel.id))
        writeChannels()
        await message.channel.send(":x: NSFW now disabled in this channel. :x:")

    else:
        channels.append(str(message.channel.id))
        writeChannels()
        await message.channel.send(":wink: NSFW now enabled in this channel. I don't judge :wink:")


def writeChannels():
    with open("config/nsfwLocks.txt", "w") as f:
            for id in channels:
                f.write(str(id) + "\n")


def initNsfw():
    global channels

    if not os.path.exists("config"):
        os.makedirs("config")

    if not os.path.exists("config/nsfwLocks.txt"):
        f = open("config/nsfwLocks.txt", "w+")
        f.close()

    if not channels:
        with open("config/nsfwLocks.txt", "r") as f:
            channels = f.readlines()
            channels = [channel.strip() for channel in channels]
