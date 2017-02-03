import urllib
import json
import urllib.request
from Core.Reddit import *
from Core.help import *
from Core.Moderation import *
from Core.VoiceCore import *
from Core.Giphy import *
from Core.Memes import *


async def parseCommand(message, client):
    #Find which command has been given
    if message.content.startswith('~test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=1000):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, message.author.name + ', you have {} messages.'.format(counter))

    elif message.content.startswith('~praise'):
        await client.send_message(message.channel, 'https://media.giphy.com/media/fr42tarocsK6Q/giphy.gif')

    elif message.content.startswith('~help'):
        await help(client, message)

    elif message.content.startswith('~permission'):
        if client.user.permissions_in(message.channel).read_messages:
            await client.send_message(message.channel, "I have permission")
        else:
            await client.send_message(message.channel, "I do not have permission")

    elif message.content.startswith('~summon'):
        await summon(client, message)

    elif message.content.startswith('~prune'):
        await prune(client, message)

    elif message.content.startswith('~play'):
        await playTest(client, message)

    elif message.content.startswith('~ayy'):
        await ayy(message, client)

    elif message.content.startswith('~kappa'):
        await kappa(message, client)

    elif message.content.startswith('~harambe'):
        harambe(message, client)

    elif message.content.startswith('~giphy'):
        giphy(message, client)

    await vote(client, message)
    await userinfo(client, message)
    await ryan(client, message)
    await moderation(client, message)