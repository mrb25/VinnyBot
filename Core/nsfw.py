import urllib.request
import discord
import re
import asyncio
import pybooru
from random import randint
import xml.etree.ElementTree

async def postR34(message, client):
    tags = message.content[4:]

    if "fur" not in tags or "furry" not in tags or "yiff" not in tags or "anthro" not in tags:
        search = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(tags) +\
                 " -fur -furry -yiff -anthro"
    else:
        search = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(tags)

    xmlFile = urllib.request.urlopen(search)
    e = xml.etree.ElementTree.parse(xmlFile)
    root = e.getroot()

    picUrls = []

    for post in root.findall('post'):
        if "furaffinity" not in post.get('source'):
            picUrls.append('http:' + post.get('file_url'))

    for post in root.findall('post'):
        picUrls.append('http:' + post.get('file_url'))

    if len(picUrls) == 0:
        await client.send_message(message.channel, "No results, try searching something less retarded next time!")

    else:
        await client.send_message(message.channel, picUrls[randint(0, len(picUrls) - 1)])
