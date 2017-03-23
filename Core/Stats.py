import glob
import json
import os
import threading
import urllib.parse
import discord
import urllib.request
from urllib.request import urlopen
from urllib.request import Request
from Config import getToken
from VoiceCore import getNumPlayers
from VoiceCore import getNumMaxPlayers

commandsCalled = 0
members = {}

VINNY_COLOR = int('008cba', 16)

async def getStats(message, client):
    serverCount = 0
    channelCount = 0
    for server in client.servers:
        serverCount += 1
        for channel in server.channels:
            channelCount += 1
        for member in server.members:
            members[member.id] = 1

    if message.channel.permissions_for(message.server.me).embed_links:
        embed = discord.Embed(title='', colour=VINNY_COLOR)
        embed.add_field(name='Servers',
                        value='{}'.format(serverCount),
                        inline=True)
        embed.add_field(name='Channels', value=channelCount, inline=True)
        embed.add_field(name='Users', value=len(members), inline=True)
        embed.add_field(name='Commands Called', value=commandsCalled, inline=True)
        embed.add_field(name='Active Voice Channels', value=getNumPlayers(), inline=True)
        embed.add_field(name='Max Active Channels', value=getNumMaxPlayers(), inline=True)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)

        return await client.send_message(message.channel, embed=embed)
    else:
        await client.send_message(message.channel, "Vinny Stats:\n`Servers: " + str(serverCount) + "\nChannels: " + str(channelCount)
                                  + "\nNumber of commands issued since last update: " + str(commandsCalled) +
                                  "`")


def commandCalled():
    global commandsCalled
    commandsCalled += 1

def initCommandCount():
    global commandsCalled
    for filename in glob.glob(os.path.join('logs', '*.txt')):
        with open(filename, 'r') as f:
            commandsCalled += sum(1 for _ in f)


def sendStatistics(client):
    url = "https://bots.discord.pw/api/bots/" + getToken('Bot ID') + "/stats"
    serverCount = 0
    for server in client.servers:
        serverCount += 1


    data = {
               "server_count": serverCount
           }

    req = Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', getToken('Bot API'))
    response = urlopen(req, json.dumps(data).encode('utf8'))
    print('Stats Posted Successfully')
    t = threading.Timer(3600.0, sendStatistics, args=(client,))
    t.setDaemon(True)
    t.start()

async def voiceStats(message, client):
    #TODO: update for scaling color
    availible = getNumMaxPlayers() - getNumPlayers()
    if availible == 0:
        color = int('ff0000', 16)
    else:
        color = int('00ff00', 16)

    embed = discord.Embed(title='', colour=color)
    embed.add_field(name='Active Voice channels', value=getNumPlayers(), inline=True)
    embed.add_field(name='Maximum Voice channels', value=getNumMaxPlayers(), inline=True)
    embed.add_field(name='Open spots', value='There are ' + str(availible) + ' stream slots available')
    await client.send_message(message.channel, embed=embed)
