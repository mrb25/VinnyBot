import urllib.request
import discord
import re
import asyncio
import pybooru
import os
from random import randint
import xml.etree.ElementTree

channels = []

async def postR34(message, client):
    init()
    if not isEnabled(message):
        await client.send_message(message.channel, "NSFW not authorized in this channel. To authorize an admin must"
                                                   "use the ~togglensfw command")
        return

    tags = message.content[4:]
    await client.send_typing(message.channel)

    if "fur" not in tags or "furry" not in tags or "yiff" not in tags or "anthro" not in tags:
        search = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(tags) +\
                 " -fur -furry -yiff -anthro -canine -mammal -wolf"
    else:
        search = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(tags)

    try:
        xmlFile = urllib.request.urlopen(search)
    except:
        await client.send_message(message.channel, "There was an error retrieving a post... :confounded: ")
        return
    e = xml.etree.ElementTree.parse(xmlFile)
    root = e.getroot()

    picUrls = []

    for post in root.findall('post'):
        if "furaffinity" not in post.get('source'):
            picUrls.append('http:' + post.get('file_url'))

    if len(picUrls) == 0:
        await client.send_message(message.channel, "No results, try searching something less retarded next time!")

    else:
        try:
            await client.send_message(message.channel, picUrls[randint(0, len(picUrls) - 1)])
        except:
            await client.send_message(message.channel, "There was an error retrieving a post... :confounded: ")
            return


def isEnabled(message):
    return message.channel.id in channels


async def toggleChannel(message, client):
    init()

    if message.channel.id in channels:
        channels.remove(message.channel.id)
        writeChannels()
        await client.send_message(message.channel, ":x: NSFW now disabled in this channel. :x:")

    else:
        channels.append(message.channel.id)
        writeChannels()
        await client.send_message(message.channel, ":wink: NSFW now enabled in this channel. I don't judge :wink:")


def writeChannels():
    with open("config/nsfwLocks.txt", "w") as f:
            for id in channels:
                f.write(id + "\n")


def init():
    global channels

    if not os.path.exists("config"):
        os.makedirs("config")

    if not os.path.exists("config/nsfwLocks.txt"):
        f = open("config/nsfwLocks.txt", "w+")
        f.close()

    if not channels:
        with open("config/nsfwLocks.txt", "r") as f:
            channels = f.readlines()
            channels = [id.strip() for id in channels]

