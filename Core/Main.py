import discord
from Parser import *
from Logger import *
from Config import *

initConfig()
Token = getToken('Discord')
client = discord.AutoShardedClient()


@client.event
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')
    await client.change_presence(game=discord.Game(name='~help for command list'))
    initCommandCount()
    ##sendStatistics(client)


@client.event
async def on_message(message):
        if message.content.startswith('~'):
            await parseCommand(message, client)

        else:
            return


client.run(Token)
