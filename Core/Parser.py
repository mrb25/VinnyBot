from Reddit import *
from help import *
from Moderation import *
from Giphy import *
from Memes import *
from Markov import *
from Stats import *
from nsfw import *
from Logger import *
from Config import *

import sys


async def parseCommand(message, client):
    try:
        if not message.channel.position:
            if not message.channel.permissions_for(message.guild.me).send_messages:
                return
    except AttributeError:
        return
        #Find which command has been given
    if message.content.startswith('~'):
        if message.author.bot:
            return

        elif message.content.startswith('~help'):
            await sendhelp(message, client)
            commandCalled()
            logCommand(message, client, '~help')

        elif message.content.startswith('~info'):
            await info(message, client)
            commandCalled()
            logCommand(message, client, '~info')

        elif message.content.startswith('~invite'):
            await invite(message, client)
            commandCalled()
            logCommand(message, client, '~invite')

        elif message.content.startswith('~stats'):
            await getStats(message, client)
            commandCalled()
            logCommand(message, client, '~stats')

        elif message.content.startswith('~permission'):
            commandCalled()
            logCommand(message, client, '~permission')
            if message.channel.permissions_for(message.guild.me).read_messages:
                await message.channel.send("I have permission")
            else:
                await message.channel.send("I do not have permission")

        elif message.content.startswith('~prune'):
            if message.channel.permissions_for(message.guild.me).manage_messages:
                if message.channel.permissions_for(message.author).manage_messages:
                    await prune(message, client)
                else:
                    await message.channel.send(":x: You do not have permissions to use this command :x:")
            else:
                await message.channel.send(":x: I don't have permissions to delete messages here. :x:")
            commandCalled()
            logCommand(message, client, '~prune')
            # await prune(message, client)

        elif message.content.startswith('~kick'):
            if message.channel.permissions_for(message.guild.me).kick_members:
                if message.channel.permissions_for(message.author).kick_members:
                    await kick(message, client)
                else:
                    await message.channel.send(":x: You do not have permissions to use this command :x:")
            else:
                await message.channel.send(":x: I don't have permissions to kick members here. :x:")
            commandCalled()
            logCommand(message, client, '~kick')
            # await kick(message, client)

        elif message.content.startswith('~ban'):
            if message.channel.permissions_for(message.guild.me).ban_members:
                if message.channel.permissions_for(message.author).ban_members:
                    await ban(message, client)
                else:
                    await message.channel.send(":x: You do not have permissions to use this command :x:")
            else:
                await message.channel.send(":x: I don't have permissions to ban members here. :x:")

            commandCalled()
            logCommand(message, client, '~ban')

        # Voice Commands (Currently removed and moved to Vinny's new JDA module)
        elif message.content.startswith('~summon'):
            await message.channel.send("Summon command no longer used. Just use the play command "
                                                       "to summon Vinny.")
            commandCalled()
            logCommand(message, client, '~summon')

        elif message.content.startswith('~playlist'):
            commandCalled()
            logCommand(message, client, '~playlist')

        elif message.content.startswith('~skip'):
            commandCalled()
            logCommand(message, client, '~skip')

        elif message.content.startswith("~volume "):
            commandCalled()
            logCommand(message, client, '~volume (val)')

        elif message.content.startswith("~volume"):
            commandCalled()
            logCommand(message, client, '~volume')

        elif message.content.startswith('~play'):
            commandCalled()
            logCommand(message, client, '~play')

        elif message.content.startswith('~pause'):
            commandCalled()
            logCommand(message, client, '~pause')

        elif message.content.startswith('~resume'):
            commandCalled()
            logCommand(message, client, '~resume')

        elif message.content.startswith('~stop'):
            commandCalled()
            logCommand(message, client, '~stop')

        elif message.content.startswith('~voicestats'):
            commandCalled()
            logCommand(message, client, '~voicestats')

        elif message.content.startswith('~search'):
            commandCalled()
            logCommand(message, client, message.content)

        elif message.content.startswith('~leave'):
            commandCalled()
            logCommand(message, client, '~leave')

        elif message.content.startswith('~volume'):
            commandCalled()
            logCommand(message, client, '~volume')

        elif message.content.startswith('~cancel'):
            commandCalled()
            logCommand(message, client, '~cancel')

        # Meme Commands
        elif message.content.startswith('~ayy'):
            await ayy(message, client)
            commandCalled()
            logCommand(message, client, '~ayy')

        elif message.content.startswith('~kappa'):
            await kappa(message, client)
            commandCalled()
            logCommand(message, client, '~kappa')

        elif message.content.startswith('~hammer'):
            await banHammer(message, client)
            commandCalled()
            logCommand(message, client, '~hammer')

        elif message.content.startswith('~doggo'):
            await doggo(message, client)
            commandCalled()
            logCommand(message, client, '~doggo')

        elif message.content.startswith('~lenny'):
            await lenny(message, client)
            commandCalled()
            logCommand(message, client, '~lenny')

        elif message.content.startswith('~hitler'):
            await hitler(message, client)
            commandCalled()
            logCommand(message, client, '~hitler')

        elif message.content.startswith('~mario'):
            await mario(message, client)
            commandCalled()
            logCommand(message, client, '~mario')

        elif message.content.startswith('~megaman'):
            await megaMan(message, client)
            commandCalled()
            logCommand(message, client, '~megaman')

        elif message.content.startswith('~salt'):
            await salt(message, client)
            commandCalled()
            logCommand(message, client, '~salt')

        elif message.content.startswith('~pikachu'):
            await pikachu(message, client)
            commandCalled()
            logCommand(message, client, '~pikachu')

        elif message.content.startswith('~feels'):
            await feels(message, client)
            commandCalled()
            logCommand(message, client, '~feels')

        elif message.content.startswith('~harambe'):
            await harambe(message, client)
            commandCalled()
            logCommand(message, client, '~harambe')

        elif message.content.startswith('~giphy'):
            await giphy(message, client)
            commandCalled()
            logCommand(message, client, '~giphy')

        elif message.content.startswith('~8ball'):
            await magic8ball(message, client)
            commandCalled()
            logCommand(message, client, "8ball")

        elif message.content.startswith('~praise'):
            await message.channel.send('https://media.giphy.com/media/fr42tarocsK6Q/giphy.gif')
            commandCalled()
            logCommand(message, client, '~praise')

        elif message.content.startswith('~whois'):
            await userInfo(message, client)
            commandCalled()
            logCommand(message, client, '~whois')

        elif message.content.startswith('~whohas'):
            await roleInfo(message, client)
            commandCalled()
            logCommand(message, client, '~whohas')

        elif message.content.startswith('~roll'):
            await roll(message, client)
            commandCalled()
            logCommand(message, client, '~roll')

        # Reddit Commands
        elif message.content.startswith('~shit'):
            with message.channel.typing():
                await message.channel.send(random_hot_post('shitpost', 20, message))
                commandCalled()
                logCommand(message, client, '~shit')

        elif message.content.startswith('~rr'):
            with message.channel.typing():
                try:
                    subreddit = message.content.split(' ')[1]
                except IndexError:
                    await message.channel.send("No subreddit mentioned, please enter a subreddit")
                    return
                post = random_hot_post(subreddit, 20, message)
                if post is not None:
                    await message.channel.send(post)
                else:
                    await message.channel.send("There was an error retrieving a post")

                commandCalled()
                logCommand(message, client, message.content)

        elif message.content.startswith('~tr'):
            with message.channel.typing():
                try:
                    subreddit = message.content.split(' ')[1]
                except IndexError:
                    await message.channel.send("No subreddit mentioned, please enter a subreddit")
                    return
                try:
                    await message.channel.send(random_top_post(subreddit, message, 75))
                except:
                    await message.channel.send("Oops. There was an error retriving a post :confounded:")
                    print('Error with Top reddit command: ' + sys.exc_info()[0] + '\n')
                commandCalled()
                logCommand(message, client, message.content)

        elif message.content.startswith('~cosplaygirls'):
            with message.channel.typing():
                await message.channel.send(getCosplayGirl(message, client))
                commandCalled()
                logCommand(message, client, '~cosplaygirls')

        elif message.content.startswith('~cosplay'):
            with message.channel.typing():
                await message.channel.send(getCosplay(message, client))
                commandCalled()
                logCommand(message, client, message.content)

        #Nsfw Commands TODO: Add permissions and nsfw lock
        elif message.content.startswith('~nsfw'):
            if isEnabled(message):
                await message.channel.send(":sweat_drops: NSFW is currently enabled :sweat_drops:")
            else:
                await message.channel.send(":x: NSFW is not currently enabled :x:")
            commandCalled()
            logCommand(message, client, "~nsfw")

        elif message.content.startswith('~r34 '):
            await postR34(message, client)
            commandCalled()
            logCommand(message, client, message.content)

        # elif message.content.startswith('~pixiv '):
        #    await pixivSearch(message, client)

        elif message.content.startswith("~togglensfw"):
            if message.channel.permissions_for(message.author).manage_channels:
                await toggleChannel(message, client)
            else:
                await message.channel.send(":x: You do not have permissions to use this command :x:")
            commandCalled()
            logCommand(message, client, "~togglensfw")

        # Markov Chain
        elif message.content.startswith('~comment'):
            await generateMarkovComment(message, client)
            commandCalled()
            logCommand(message, client, message.content)

        elif message.content.startswith('~ryzen'):
            await generateRyzen(message, client)
            commandCalled()
            logCommand(message, client, '~ryzen')


    # else:
    #     if message.content.startswith('~help'):
    #         await help(message, client)
    #         commandCalled()
    #     elif message.author.bot:
    #         return
    #     else:
    #         await message.channel.send("Quit trying to slide into my DMs I only do ~help inside of DMs")
