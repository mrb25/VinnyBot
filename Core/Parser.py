import urllib
import json
import urllib.request
from Reddit import *
from help import *
from Moderation import *
from VoiceCore import *
from Giphy import *
from Memes import *
from Markov import *


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
        await summon(message, client)

    elif message.content.startswith('~prune'):
        await client.send_message(message.channel, 'Prune temporarily disabled')
    #    await prune(message, client)

    elif message.content.startswith('~play'):
        await playTest(message, client)

    elif message.content.startswith('~pause'):
        await pauseStream(message, client)

    elif message.content.startswith('~resume'):
        await resumeStream(message, client)

    elif message.content.startswith('~ayy'):
        await ayy(message, client)

    elif message.content.startswith('~kappa'):
        await kappa(message, client)

    elif message.content.startswith('~harambe'):
        await harambe(message, client)

    elif message.content.startswith('~giphy'):
        await giphy(message, client)

    elif message.content.startswith('~vote'):
        await vote(message, client)

    elif message.content.startswith('~whois'):
        await userInfo(message, client)

    elif message.content.startswith('~shit'):
        await client.send_message(message.channel, random_hot_post('shitpost', 20))

    elif message.content.startswith('~rr'):
        subreddit = message.content.split(' ')[1]
        await client.send_message(message.channel, random_hot_post(subreddit, 20))

    elif message.content.startswith('~tr'):
        subreddit = message.content.split(' ')[1]
        await client.send_message(message.channel, random_hot_post(subreddit, 2))

    elif message.content.startswith('~kick'):
        await client.send_message(message.channel, 'Kick temporarily disabled')
    #    await kick(message, client)

    elif message.content.startswith('~ban'):
        await client.send_message(message.channel, 'Ban temporarily disabled')
    #    await ban(message, client)

    elif message.content.startswith('~stop'):
        await stopPlay(message, client)

    elif message.content.startswith('~comment'):
        await generateMarkovComment(message, client)

    elif message.content.startswith('~'):
        await client.send_message(message.channel, 'That was not a valid command, say ~help to get the help you so des'
                                                   'perately need')
