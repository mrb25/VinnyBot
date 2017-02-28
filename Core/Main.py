import discord
import sys
from Parser import *
from VoiceCore import *

Token = input("Enter your token: ")
client = discord.Client()


@client.event
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')


@client.event
async def on_message(message):
    if message.content.startswith('~'):
        await parseCommand(message, client)

    else:
        return


@client.event
async def on_member_join(member):
    if not member.channel.is_private:
        if not member.channel.permissions_for(member.server.me).send_messages:
            return
    await client.send_message(member.server, member.mention + ' has joined the server.')


@client.event
async def on_member_remove(member):
    if not member.channel.is_private:
        if not member.channel.permissions_for(member.server.me).send_messages:
            return

    await client.send_message(member.server, member.mention + ' has been forcefully removed from the channel.')


@client.event
async def on_voice_state_update(before, after):
    if client.is_voice_connected(after.server):
        vClient = client.voice_client_in(before.server)
        if len(vClient.channel.voice_members) == 1:
            leaveServer(client, before)
            await client.voice_client_in(before.server).disconnect()


client.run(Token)
