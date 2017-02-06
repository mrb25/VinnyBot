import markovify

async def generateMarkovComment(message, client):
    counter = 0
    textSource = ''

    if (len(message.mentions) != 1):
        await client.send_message(message.channel, 'Please mention only 1 user')
        return

    tmp = await client.send_message(message.channel, 'Downloading messages...')
    async for log in client.logs_from(message.channel, limit=5000):
        if log.author == message.mentions:
            counter += 1
            textSource += ' ' + message.content + ' '

    if (counter < 30):
        await client.send_message(message.channel, 'Too few messages received. Cannot generate a message from user')

    await client.edit_message(tmp, 'Generating comment from {} messages.'.format(counter))

    text_model = markovify.Text(textSource)

    await client.edit_message(tmp, text_model.make_sentence())



