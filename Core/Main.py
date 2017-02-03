import discord
from Core.Parser import *

Token = input("Enter your token: ")
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    if message.content.startswith('~'):
        parseCommand(message, client)

    else:
        return
