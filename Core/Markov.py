import markovify

async def generateMarkovComment(message, client):
    counter = 0
    channelCounter = 0
    textSource = ''


    if (len(message.mentions) != 1):
        await client.send_message(message.channel, 'Please mention only 1 user')
        return

    tmp = await client.send_message(message.channel, 'Downloading messages...')
    for channel in message.server.channels:
        async for log in client.logs_from(channel, limit=2500):
            if log.author == message.mentions[0]:
                counter += 1
                textSource += log.content + '\n'
                # print('message received')
        channelCounter += 1
        updateLoading(message, channel, tmp, channelCounter)


    if counter <= 30:
        await client.send_message(message.channel, 'Not enough messages received, cannot generate message')
        return

    await client.edit_message(tmp, 'Generating comment from {} messages.'.format(counter))
    print('Generating model from {} messages'.format(counter))
    text_model = markovify.NewlineText(textSource)
    # Debugging print
    # print(textSource)
    await client.edit_message(tmp, message.mentions[0].name + ' says: ' + text_model.make_sentence(tries=100, max_overlap_total=10))

async def updateLoading(message, client, tmp, channelCounter):
    loading = 'Downloading messages ({}/{}) ['.format(channelCounter, len(message.server.channels))
    for x in range(0, len(message.server.channels)):
        if channelCounter > x:
            loading += '█'
        else:
            loading += '▒'

        loading += ']'
        await client.edit_message(tmp, loading)
