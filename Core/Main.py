import discord
import sys
from Parser import *

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
        await parseCommand(message, client)

    else:
        return


@client.event
async def on_member_join(member):
    await client.send_message(member.server, member.mention + ' has joined the server.')


@client.event
async def on_member_remove(member):
    await client.send_message(member.server, member.mention + ' has been forcefully removed from the channel.')


@client.event
async def on_voice_state_update(before, after):
    if client.is_voice_connected(after.server):
        vClient = client.voice_client_in(before.server)
        if len(vClient.channel.voice_members) == 1:
            await client.voice_client_in(before.server).disconnect()


client.run(Token)
