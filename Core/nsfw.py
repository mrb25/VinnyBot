import urllib.request
import discord
import re
import asyncio
from random import randint
import xml.etree.ElementTree

async def postR34(message, client):
    tags = message.content[4:]
    search = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}".format(tags)
    xmlFile = urllib.request.urlopen(search)
    e = xml.etree.ElementTree.parse(xmlFile)
    root = e.getroot()

    picUrl = []

    for post in root.findall('post'):
        picUrl.append('http:' + post.get('file_url'))

    if len(picUrl) == 0:
        await client.send_message(message.channel, "No results, try searching something less retarded next time!")

    else:
        await client.send_message(message.channel, picUrl[randint(0, len(picUrl)-1)])