import discord
import re
import asyncio

playerMap = {}
songMap = {}

async def voiceInit():
    if not discord.opus.is_loaded():
        discord.opus.load_opus('opus')

async def summon(message, client):
    summoned_channel = message.author.voice_channel
    if summoned_channel is None:
        await client.send_message(message.channel, 'You are not in a voice channel.')
        return False

    if client.is_voice_connected(message.server):
        await client.voice_client_in(message.server).move_to(summoned_channel)
    else:
        await client.join_voice_channel(summoned_channel)

    return True

async def playTest(message, client):
    audio_channel = message.author.voice_channel
    if audio_channel is None:
        await client.send_message(message.channel, 'You are not in a voice channel.')
        return False

    elif not client.voice_client_in(message.server):
        await client.send_message(message.channel, 'I am not in a voice channel please "~summon" me')

    elif client.voice_client_in(message.server).channel == message.author.voice_channel:
        try:
            if playerMap[client.voice_client_in(message.server)].is_playing():
                songMap[client.voice_client_in(message.server)].append(message.content)
                await client.send_message(message.channel, "Added song to playlist!")


            else:
                if len(playerMap) >= 2:
                    await client.send_message(message.channel,
                                              "Max amount of servers using audio. Please try again later, sorry.")

                else:
                    vClient = client.voice_client_in(message.server)
                    player = playerMap[vClient]
                    vidUrl = formatYoutube(message.content)
                    player = await vClient.create_ytdl_player(vidUrl, use_avconv=True, after=lambda: songFinished(message,client))
                    """Adding player to hashmap"""
                    playerMap[vClient] = player
                    songMap[vClient] = []
                    player.start()

        except KeyError:
            if len(playerMap) >= 2:
                await client.send_message(message.channel, "Max amount of servers using audio. Please try again later, sorry.")

            else:
                print('ayo key error!!!')
                await voiceInit()
                vClient = client.voice_client_in(message.server)
                vidUrl = formatYoutube(message.content)
                player = await vClient.create_ytdl_player(vidUrl, use_avconv=True, after=lambda: songFinished(message,client))
                """Adding player to hashmap"""
                player.use_avconv = True
                playerMap[vClient] = player
                songMap[vClient] = []
                player.start()

    else:
        await client.send_message(message.channel, 'You are not in my voice channel. Please join or "~summon" me')

    return True


async def stopPlay(message, client):
    if playerMap[client.voice_client_in(message.server)].is_playing():
        print('Stopping Stream')
        await client.send_message(message.channel, "Stopping audio Stream")
        playerMap[client.voice_client_in(message.server)].stop()
        del playerMap[client.voice_client_in(message.server)]
        del songMap[client.voice_client_in(message.server)]

async def pauseStream(message, client):
    if playerMap[client.voice_client_in(message.server)].is_playing():
        print('Pausing stream')
        await client.send_message(message.channel, 'Pausing audio stream')
        playerMap[client.voice_client_in(message.server)].pause()

    else:
        await client.send_message(message.channel, 'I could not detect an audio stream playing')

async def resumeStream(message, client):
    if not playerMap[client.voice_client_in(message.server)].is_playing():
        print('Trying to resume Stream\n')
        playerMap[client.voice_client_in(message.server)].resume()
        if playerMap[client.voice_client_in(message.server)].is_playing():
            await client.send_message(message.channel, 'Resuming audio stream')
            print('Success')
            return
        else:
            await client.send_message(message.channel, 'I could not detect an audio stream playing')
            return

    elif playerMap[client.voice_client_in(message.server)].is_playing():
        await client.send_message(message.channel, 'Stream is already playing')

    else:
        await client.send_message(message.channel, 'I could not detect an audio stream playing')


def songFinished(message, client):
    print("The song is done")
    try:
        if songMap[client.voice_client_in(message.server)][0] is None:
            del playerMap[client.voice_client_in(message.server)]
            del songMap[client.voice_client_in(message.server)]

        else:
            vClient = client.voice_client_in(message.server)
            coro = vClient.create_ytdl_player(formatYoutube(songMap[vClient][0]), use_avconv=True,
                                              after=lambda: songFinished(message, client))
            
            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
            try:
                player = fut.result()
            except:
                print("Error")

            """Adding player to hashmap"""
            playerMap[vClient] = player
            songMap[vClient].pop(0)
            player.start()

    except KeyError:
        print("Finished song key error")
        del playerMap[client.voice_client_in(message.server)]


def leaveServer(client, channel):
    print("leaving channel")
    try:
        del playerMap[client.voice_client_in(channel.server)]
        del songMap[client.voice_client_in(channel.server)]
        print("Successfully left")

    except KeyError:
        print("Tried to leave but not in the map")


def formatYoutube(url):
    return re.search("(?P<url>https?://[^\s]+)", url).group("url")

