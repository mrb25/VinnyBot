import re

async def prune(message, client):
    input = message.content
    number = list(map(int, re.findall('\d+', input)))
    await client.purge_from(message.channel, limit=number[0])
    await client.send_message(message.channel, "Pruning the last " + str(number[0]) + " messages.")

async def kick(message, client):
    if len(message.mentions) == 0:
        text = "You must @mention a user to kick."
    else:
        for i in range(0, len(message.mentions)):
            await client.kick(message.mentions[i])
    await client.send_message(message.channel, text)