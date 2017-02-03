import re

votes=[]
voteStrings=[]
voters = []

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

async def ban(message, client):
    if len(message.mentions) == 0:
        text = "You must @mention a user to kick."
        await client.send_message(message.channel, text)
    elif len(message.mentions) > 1:
        text = "You can only ban a single user at a time."
        await client.send_message(message.channel, text)
    else:
        await client.ban(message.mentions[0], 0)
        await client.send_message(message.channel, message.mentions[0].name + 'has been successfully banned')

async def count(message, client):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=1000):
        if log.author == message.author:
            counter += 1

    await client.edit_message(tmp, message.author.name + ', you have {} messages.'.format(counter))

async def userInfo(message, client):
    text = ''
    if len(message.mentions) == 0:
        text = "You must @mention a user."
    elif len(message.mentions) > 1:
        text = "You may only @mention one user."
    else:
        user = message.mentions[0]
        text += user.mention + "\n"
        text += "avatar url: " + user.avatar_url + "\n"
        text += "username: " + user.name + "\n"
        text += "joined: " + str(user.joined_at) + "\n"
    await client.send_message(message.channel, text)

async def avatar(message, client):
    if len(message.mentions) == 0:
        text = "You must @mention a user."
    elif len(message.mentions) > 1:
        text = "You may only @mention one user."
    else:
        text = message.mentions[0].mention + " " + message.mentions[0].avatar_url
    await client.send_message(message.channel, text)

async def vote(message, client):
    global voteStrings
    text = ""
    if message.content.startswith('~vote'):
        text += "Voting has begun make you vote now.\n"
        inVote = True
        voteStrings = message.content[5:].split(';')
        for i, v in enumerate(voteStrings):
            votes.append(0)
            text += ("~v" + str(i + 1) + ": " + v + "\n")
            i += 1
        await client.send_message(message.channel, text)

    elif message.content.startswith('~endvote'):
        text += "End Vote\n"
        for i, v in enumerate(voteStrings):
            text += str(votes[i]) + ": " + v + "\n"
        voteStrings.clear()
        votes.clear()
        await client.send_message(message.channel, text)

    elif not (message.author.id in voters) and message.content.startswith('~v'):
        try:
            votes[int(message.content[2:]) - 1] += 1
            voters.append(message.author.id)
        except ValueError:
            print("VALUE ERROR")
