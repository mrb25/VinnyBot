import gc

import discord
import markovify
from discord import ChannelType

VINNY_COLOR = int('008cba', 16)
currentCommentsArr = []

async def generateMarkovComment(message, client):
    counter = 0
    channelCounter = 0
    textSource = ''
    usableChannels = []

    if len(message.channel_mentions) > 0:
        await generateMarkovChannel(message, client)
        return

    if (len(message.mentions) != 1):
        await client.send_message(message.channel, 'Please mention only 1 user')
        return

    if message.mentions[0] == client.user:
        await client.send_message(message.channel, 'I know what I would say. You dont need to ~comment me')
        return

    if message.author.id in currentCommentsArr:
        await client.send_message(message.channel, 'I am already generating a comment for you. Please wait for that one'
                                                   ' to finish first')
        return

    for channel in message.server.channels:
        if message.mentions[0].permissions_in(channel).send_messages:
            if channel.permissions_for(message.server.me).read_messages:
                if not channel.type == ChannelType.voice:
                    usableChannels.append(channel)

    print('Comment for ' + message.mentions[0].name + ' requested by ' + message.author.name + ' in Server: '
          + message.server.name + ' in channel: ' + message.channel.name)
    currentCommentsArr.append(message.author.id)
    await client.send_typing(message.channel)
    tmp = await client.send_message(message.channel, 'Downloading messages...')

    await updateLoading(message, client, tmp, channelCounter, usableChannels)
    for channel in usableChannels:
        if message.mentions[0].permissions_in(channel).send_messages:
            async for log in client.logs_from(channel, limit=4000):
                # Checks for messages from the mentioned user
                if log.author == message.mentions[0]:
                    # Checks and omits commands
                    if not log.content.startswith('~'):
                        counter += 1
                        textSource += log.content + '\n'
                        # print('message received')
        channelCounter += 1
        await updateLoading(message, client, tmp, channelCounter, usableChannels)

    if counter <= 30:
        await client.edit_message(tmp, 'Not enough messages received, cannot generate message')
        currentCommentsArr.remove(message.author.id)
        return

    await client.edit_message(tmp, 'Generating comment from {} messages.'.format(counter))
    print('Generating model from {} messages'.format(counter))

    text_model = markovify.NewlineText(textSource)
    # Debugging print
    # print(textSource)
    generatedMessage = text_model.make_sentence(tries=100)
    if generatedMessage is None:
        await client.edit_message(tmp,
                                  'Failed to generate a Comment. I did not get enough comments from them :disappointed:')
        currentCommentsArr.remove(message.author.id)

    else:
        print('Generated message: ' + generatedMessage + '\n')

        if message.channel.permissions_for(message.server.me).embed_links:
            embed = discord.Embed(title='', colour=VINNY_COLOR)
            embed.set_author(name=message.mentions[0], icon_url=message.mentions[0].avatar_url)
            embed.add_field(name='Message', value=generatedMessage)

            await client.send_message(message.channel, embed=embed)
            await client.delete_message(tmp)
            currentCommentsArr.remove(message.author.id)

        else:
            await client.edit_message(tmp, message.mentions[0].name + ' says: ' + generatedMessage.replace('@', ':at:'))
            currentCommentsArr.remove(message.author.id)


async def updateLoading(message, client, tmp, channelCounter, usableChannels):
    loading = 'Downloading messages from channels ({}/{}) |'.format(channelCounter, len(usableChannels))
    for x in range(0, len(usableChannels)):
        if channelCounter > x:
            loading += '█'
        else:
            loading += '▒'

    loading += '|'
    await client.edit_message(tmp, loading)

async def updateChannelLoading(message, client, tmp, counter):
    loading = 'Downloading messages from channel ({}/10,000) |'.format(counter)
    rangeL = counter/1000

    for x in range(0, int(rangeL)):
        loading += '█'
    for x in range(0, 10 - int(rangeL)):
        loading += '▒'

    loading += '|'
    await client.edit_message(tmp, loading)

async def generateMarkovChannel(message, client):

    textSource = ''
    counter = 0
    usableCounter = 0

    if len(message.channel_mentions) != 1:
        await client.send_message(message.channel, 'Please mention only one channel')
        return

    if message.author.id in currentCommentsArr:
        await client.send_message(message.channel, 'I am already generating a comment for you. Please wait for that one'
                                                   ' to finish first')
        return

    if not message.channel_mentions[0].permissions_for(message.server.me).read_messages:
        await client.send_message(message.channel, "Error: I do not have the permissions to read messages from that channel")
        return

    currentCommentsArr.append(message.author.id)
    await client.send_typing(message.channel)
    tmp = await client.send_message(message.channel, 'Downloading messages from Channel... (0%)')

    async for log in client.logs_from(message.channel_mentions[0], limit=10000):
        # Checks and omits commands
        if not log.content.startswith('~'):
            usableCounter += 1
            textSource += log.content + '\n'

        counter += 1
        if counter % 500 == 0:
            await updateChannelLoading(message, client, tmp, counter)

    if usableCounter <= 30:
        currentCommentsArr.remove(message.author.id)
        await client.edit_message(tmp, 'Not enough messages received, cannot generate message')
        return

    await client.edit_message(tmp, 'Generating comment from {} messages.'.format(usableCounter))
    print('Generating model from {} messages'.format(usableCounter))

    text_model = markovify.NewlineText(textSource)
    # Debugging print
    # print(textSource)
    generatedMessage = text_model.make_sentence(tries=100)
    if generatedMessage is None:
        currentCommentsArr.remove(message.author.id)
        await client.edit_message(tmp, 'Failed to generate a Comment. I did not get enough comments from them :disappointed:')

    else:
        currentCommentsArr.remove(message.author.id)
        print('Generated message: ' + generatedMessage + '\n')
        if message.channel.permissions_for(message.server.me).embed_links:
            embed = discord.Embed(title='', colour=VINNY_COLOR)
            embed.set_author(name=message.channel_mentions[0], icon_url=message.server.icon_url)
            embed.add_field(name='Message', value=generatedMessage)

            await client.send_message(message.channel, embed=embed)
            await client.delete_message(tmp)

        else:
            await client.edit_message(tmp, message.mentions[0].name + ' says: ' + generatedMessage.replace('@', ':at:'))
            currentCommentsArr.remove(message.author.id)

async def generateRyzen(message, client):
    with open("res/ryzen.txt", encoding="utf8") as f:
        text = f.read()

    text_model = markovify.Text(text)

    await client.send_message(message.channel, "Hey, did you guys hear about Ryzen? " + text_model.make_sentence())
