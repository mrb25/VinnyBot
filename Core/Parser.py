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
from WhoSaid import *
from Stats import *
from nsfw import *


async def parseCommand(message, client):

    if not message.channel.is_private:
        if not message.channel.permissions_for(message.server.me).send_messages:
            return

    #Find which command has been given
    if message.content.startswith('~test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=1000):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, message.author.name + ', you have {} messages.'.format(counter))

    elif message.content.startswith('~help'):
        await help(client, message)
        commandCalled()

    elif message.content.startswith('~stats'):
        await getStats(message, client)
        commandCalled()

    elif message.content.startswith('~permission'):
        commandCalled()
        if client.user.permissions_in(message.channel).read_messages:
            await client.send_message(message.channel, "I have permission")
        else:
            await client.send_message(message.channel, "I do not have permission")

    elif message.content.startswith('~prune'):
        await client.send_message(message.channel, 'Prune temporarily disabled')
        commandCalled()
        # await prune(message, client)

    elif message.content.startswith('~kick'):
        await client.send_message(message.channel, 'Kick temporarily disabled')
        commandCalled()
        # await kick(message, client)

    elif message.content.startswith('~ban'):
        await client.send_message(message.channel, 'Ban temporarily disabled')
        commandCalled()
        # await ban(message, client)

    # Voice Commands
    elif message.content.startswith('~summon'):
        await summon(message, client)
        commandCalled()

    elif message.content.startswith('~playlist'):
        await printPlaylist(message, client)
        commandCalled()

    elif message.content.startswith('~skip'):
        await skipSong(message, client)
        commandCalled()

    elif message.content.startswith("~volume "):
        await setVolume(message, client)
        commandCalled()

    elif message.content.startswith("~volume"):
        await getVolume(message, client)
        commandCalled()

    elif message.content.startswith('~play'):
        await playTest(message, client)
        commandCalled()

    elif message.content.startswith('~pause'):
        await pauseStream(message, client)
        commandCalled()

    elif message.content.startswith('~resume'):
        await resumeStream(message, client)
        commandCalled()

    elif message.content.startswith('~stop'):
        await stopPlay(message, client)
        commandCalled()

    # Meme Commands
    elif message.content.startswith('~ayy'):
        await ayy(message, client)
        commandCalled()

    elif message.content.startswith('~kappa'):
        await kappa(message, client)
        commandCalled()

    elif message.content.startswith('~hammer'):
        await banHammer(message, client)
        commandCalled()

    elif message.content.startswith('~doggo'):
        await doggo(message, client)
        commandCalled()

    elif message.content.startswith('~lenny'):
        await lenny(message, client)
        commandCalled()

    elif message.content.startswith('~hitler'):
        await hitler(message, client)
        commandCalled()

    elif message.content.startswith('~mario'):
        await mario(message, client)
        commandCalled()

    elif message.content.startswith('~megaman'):
        await megaMan(message, client)
        commandCalled()

    elif message.content.startswith('~salt'):
        await salt(message, client)
        commandCalled()

    elif message.content.startswith('~pikachu'):
        await pikachu(message, client)
        commandCalled()

    elif message.content.startswith('~feels'):
        await feels(message, client)
        commandCalled()

    elif message.content.startswith('~harambe'):
        await harambe(message, client)
        commandCalled()

    elif message.content.startswith('~giphy'):
        await giphy(message, client)
        commandCalled()

    elif message.content.startswith('~praise'):
        await client.send_message(message.channel, 'https://media.giphy.com/media/fr42tarocsK6Q/giphy.gif')
        commandCalled()

    elif message.content.startswith('~vote'):
        await vote(message, client)
        commandCalled()

    elif message.content.startswith('~whois'):
        await userInfo(message, client)
        commandCalled()

    # Reddit Commands
    elif message.content.startswith('~shit'):
        await client.send_message(message.channel, random_hot_post('shitpost', 20))
        commandCalled()

    elif message.content.startswith('~rr'):
        subreddit = message.content.split(' ')[1]
        await client.send_message(message.channel, random_hot_post(subreddit, 20))
        commandCalled()

    elif message.content.startswith('~tr'):
        subreddit = message.content.split(' ')[1]
        await client.send_message(message.channel, random_hot_post(subreddit, 2))
        commandCalled()

    elif message.content.startswith('~cosplaygirls'):
        await client.send_message(message.channel, getCosplayGirl(message, client))
        commandCalled()

    elif message.content.startswith('~cosplay'):
        await client.send_message(message.channel, getCosplay(message, client))
        commandCalled()

    #Nsfw Commands TODO: Add permissions and nsfw lock
    elif message.content.startswith('~r34 '):
        await postR34(message, client)
        commandCalled()

    # Markov Chain
    elif message.content.startswith('~comment'):
        await generateMarkovComment(message, client)
        commandCalled()

    elif message.content.startswith('~ryzen'):
        await generateRyzen(message, client)
        commandCalled()

    elif message.content.startswith('~whosaid '):
        await findWhoSaid(message,client)
        commandCalled()

    # Not a command
    elif message.content.startswith('~'):
        #await client.send_message(message.channel, 'That was not a valid command, say ~help to get the help you so des'
        #                                           'perately need')
