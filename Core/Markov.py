import gc
import markovify
from discord import ChannelType


async def generateMarkovComment(message, client):
    counter = 0
    channelCounter = 0
    textSource = ''
    usableChannels = []

    if (len(message.mentions) != 1):
        await client.send_message(message.channel, 'Please mention only 1 user')
        return

    if message.mentions[0] == client.user:
        await client.send_message(message.channel, 'I know what I would say. You dont need to ~comment me')
        return

    for channel in message.server.channels:
        if message.mentions[0].permissions_in(channel).send_messages:
            if not channel.type == ChannelType.voice:
                usableChannels.append(channel)

    print('Comment for ' + message.mentions[0].name + ' requested by ' + message.author.name + ' in Server: '
          + message.server.name + ' in channel: ' + message.channel.name)
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
        await client.send_message(message.channel, 'Not enough messages received, cannot generate message')
        return

    await client.edit_message(tmp, 'Generating comment from {} messages.'.format(counter))
    print('Generating model from {} messages'.format(counter))

    text_model = markovify.NewlineText(textSource)
    # Debugging print
    # print(textSource)
    generatedMessage = text_model.make_sentence(tries=100)
    print('Generated message: ' + generatedMessage + '\n')

    await client.edit_message(tmp, message.mentions[0].name + ' says: ' + generatedMessage.replace('@', ':at:'))


async def updateLoading(message, client, tmp, channelCounter, usableChannels):
    loading = 'Downloading messages from channels ({}/{}) |'.format(channelCounter, len(usableChannels))
    for x in range(0, len(usableChannels)):
        if channelCounter > x:
            loading += '█'
        else:
            loading += '▒'

    loading += '|'
    await client.edit_message(tmp, loading)
