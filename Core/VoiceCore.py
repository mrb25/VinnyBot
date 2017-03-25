import urllib.request
import discord
import re
import asyncio
import lxml
from lxml import etree

NUM_MAX_PLAYERS = 2
playerMap = {}
songMap = {}
skipMap = {}

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
    if not isYoutube(message):
        await client.send_message(message.channel, "Not a valid youtube url. Please try again")
        return

    if isList(message):
        await client.send_message(message.channel, "Link is to a playlist. Please link to the song from outside "
                                                   "of the playlist")
        return

    audio_channel = message.author.voice_channel
    if audio_channel is None:
        await client.send_message(message.channel, 'You are not in a voice channel.')
        return False

    elif not client.is_voice_connected(message.server):
        await client.join_voice_channel(audio_channel)

    if client.voice_client_in(message.server).channel == message.author.voice_channel:
        try:
            if playerMap[client.voice_client_in(message.server)].is_playing():
                songMap[client.voice_client_in(message.server)].append(message.content)
                await client.send_message(message.channel, "Added song to playlist!")

            else:
                if len(playerMap) >= NUM_MAX_PLAYERS:
                    await client.send_message(message.channel,
                                              "Max amount of servers using audio. Please try again later, sorry.")

                else:
                    vClient = client.voice_client_in(message.server)
                    player = playerMap[vClient]
                    vidUrl = formatYoutube(message.content)
                    try:
                        player = await vClient.create_ytdl_player(vidUrl, use_avconv=True, after=lambda: songFinished(message,client))
                    except:
                        await client.send_message(message.channel, "The video does not exist or is private. Please try again")
                        return
                    """Adding player to hashmap"""
                    playerMap[vClient] = player
                    songMap[vClient] = []
                    songMap[vClient].append(message.content)
                    player.start()

        except KeyError:
            if len(playerMap) >= NUM_MAX_PLAYERS:
                await client.send_message(message.channel, "Max amount of servers using audio. Please try again later, sorry.")

            else:
                print('ayo key error!!!')
                await voiceInit()
                vClient = client.voice_client_in(message.server)
                vidUrl = formatYoutube(message.content)
                try:
                    player = await vClient.create_ytdl_player(vidUrl, use_avconv=True, after=lambda: songFinished(message,client))
                except:
                    await client.send_message(message.channel, "The video does not exist or is private. Please try again")
                    return
                """Adding player to hashmap"""
                player.use_avconv = True
                playerMap[vClient] = player
                songMap[vClient] = []
                songMap[vClient].append(message.content)
                player.start()

    else:
        await client.send_message(message.channel, 'You are not in my voice channel. Please join or "~summon" me')

    return True


async def stopPlay(message, client):
    try:
        if playerMap[client.voice_client_in(message.server)].is_playing():
            print('Stopping Stream')
            await client.send_message(message.channel, "Stopping audio Stream")
            playerMap[client.voice_client_in(message.server)].stop()
            del playerMap[client.voice_client_in(message.server)]
            del songMap[client.voice_client_in(message.server)]
            del skipMap[client.voice_client_in(message.server)]
    except KeyError:
        await client.send_message(message.channel, "Not currently playing")

async def pauseStream(message, client):
    try:
        if playerMap[client.voice_client_in(message.server)].is_playing():
            print('Pausing stream')
            await client.send_message(message.channel, 'Pausing audio stream')
            playerMap[client.voice_client_in(message.server)].pause()

        else:
            await client.send_message(message.channel, 'I could not detect an audio stream playing')
    except KeyError:
        await client.send_message(message.channel, "Not currently playing")

async def resumeStream(message, client):
    try:
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

    except KeyError:
        await client.send_message(message.channel, "No current audio stream")


async def setVolume(message, client):
    try:
        player = playerMap[client.voice_client_in(message.server)]
        volume = float(message.content[7:])
        if volume > 2.0 or volume < 0.1:
            await client.send_message(message.channel, "Please enter a number between 0.1 and 2.0")

        else:
            player.volume = volume
            await client.send_message(message.channel, "Volume changed to {}".format(volume))

    except:
        await client.send_message(message.channel, "Please enter a valid number between 0.1 and 2.0")


async def getVolume(message, client):
    try:
        volume = playerMap[client.voice_client_in(message.server)].volume
        await client.send_message(message.channel, "Volume is currently: " + str(volume))

    except:
        await client.send_message(message.channel, "I have no volume :(")



def songFinished(message, client):
    print("The song is done")
    try:
        if songMap[client.voice_client_in(message.server)][1] is None:
            del playerMap[client.voice_client_in(message.server)]
            del songMap[client.voice_client_in(message.server)]

        else:
            try:
                vClient = client.voice_client_in(message.server)
                coro = vClient.create_ytdl_player(formatYoutube(songMap[vClient][1]), use_avconv=True,
                                                    after=lambda: songFinished(message, client))

                fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                player = fut.result()
            except:
                print("Error")
                pass
                return

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

async def printPlaylist(message, client):
    try:
        msg = await client.send_message(message.channel, "Grabbing playlist")
        list = ""
        count = 0
        for u in songMap[client.voice_client_in(message.server)]:
            if count == 0:
                list += "Now Playing: " + getYTTitle(u[6:]) + "\n"

            else:
                list += str(count) + ": " + getYTTitle(u[6:]) + "\n"

            count += 1
        await client.edit_message(msg, list)


    except KeyError:
        await client.send_message(message.channel, "There are currently no songs playing")

async def skipSong(message, client):
    try:
        if playerMap[client.voice_client_in(message.server)].is_playing():
            try:
                if message.author.voice_channel == client.voice_client_in(message.server).channel:
                    if message.author in skipMap[client.voice_client_in(message.server)]:
                        await client.send_message(message.channel, "You have already voted")
                        return

                    skipMap[client.voice_client_in(message.server)].append(message.author)
                    if len(skipMap[client.voice_client_in(message.server)]) >= \
                                    (len(client.voice_client_in(message.server).channel.voice_members) - 1)/2:
                        try:
                            vClient = client.voice_client_in(message.server)
                            try:
                                player = await vClient.create_ytdl_player(formatYoutube(songMap[vClient][1]), use_avconv=True,
                                                                after=lambda: songFinished(message, client))
                            except:
                                client.send_message(message.channel, "Video does not exist or is private, skipping song")
                                songMap[vClient].pop(0)
                                skipSong(message, client)

                            playerMap[vClient].stop()
                            playerMap[vClient] = player
                            songMap[vClient].pop(0)
                            player.start()
                            await client.send_message(message.channel, "Skipping song")
                            del skipMap[vClient]

                        except IndexError:
                            await client.send_message(message.channel, "Skip vote passed. No next song. Stopping audio stream.")
                            await stopPlay(message, client)

                    else:
                        await client.send_message(message.channel, "Vote recorded. {} more needed to skip".format(
                            ((len(client.voice_client_in(message.server)) - 1) / 2) -
                            len(skipMap[client.voice_client_in(message.server)])))

            except KeyError:
                await client.send_message(message.channel,
                                          "Starting skip vote. Everyone who wants to skip the current song "
                                          "type ~skip to vote to skip")
                skipMap[client.voice_client_in(message.server)] = []
                skipMap[client.voice_client_in(message.server)].append(message.author)
                if len(skipMap[client.voice_client_in(message.server)]) >= \
                                (len(client.voice_client_in(message.server).channel.voice_members) - 1) / 2:
                    try:
                        vClient = client.voice_client_in(message.server)
                        try:
                            player = await vClient.create_ytdl_player(formatYoutube(songMap[vClient][1]), use_avconv=True,
                                                                after=lambda: songFinished(message, client))
                        except:
                            client.send_message(message.channel, "Video does not exist or is private, skipping song")
                            songMap[vClient].pop(0)
                            skipSong(message, client)
                        playerMap[vClient].stop()
                        playerMap[vClient] = player
                        songMap[vClient].pop(0)
                        player.start()
                        await client.send_message(message.channel, "Skipping song")
                        del skipMap[vClient]

                    except IndexError:
                        await client.send_message(message.channel, "Skip vote passed. No next song. Stopping audio stream.")
                        await stopPlay(message, client)


    except KeyError:
        await client.send_message(message.channel, "I am not currently playing on this server.")


def getYTTitle(url):
    youtube = etree.HTML(urllib.request.urlopen(url).read())
    video_title = youtube.xpath("//span[@id='eow-title']/@title")
    return ''.join(video_title)


def isYoutube(message):
    youtube_regex = (r'(https?://)?(www\.)?'
                     '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                     '(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.match(youtube_regex, message.content[6:])


def isList(message):
    return "list=" in message.content

def getNumPlayers():
    return len(playerMap)

def getNumMaxPlayers():
    return NUM_MAX_PLAYERS
