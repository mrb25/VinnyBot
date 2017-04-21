import re

import discord

votes=[]
voteStrings=[]
voters = []

async def prune(message, client):
    params = message.content.split(' ')
    phrases = []
    num = None

    for param in params:
        if param.startswith('"'):
            phrases.append(param[1:-1])
        elif param.isdigit():
            num = int(param)

    if num is None:
        await client.send_message(message.channel, "Please include a number of messages for me to look back through")
        return

    elif num > 500:
        await client.send_message(message.channel, "I can only go through a max of 500 messages at a time. Please "
                                                   "enter a number 500 or less.")
        return
    elif len(params) == 2:
        await client.purge_from(message.channel, limit=num)
        await client.send_message(message.channel, "Pruning the last `" + str(num) + "` messages.")
    elif len(message.mentions) != 0:
        if len(phrases) == 0:
            await pruneUsers(message, client, num)
            return
        else:
            await pruneUserPhrases(message, client, phrases, num)
            return

    elif len(phrases) > 0:
        await prunePhrases(message, client, phrases, num)
        return

    else:
        await client.send_message(message.channel, "Argument Error: Please make sure you follow proper argument format."
                                             " For example:\n `~prune \"hey!\" @user 50` goes through the last `50`"
                                             " messages and removes all messages from `user` containing `hey!`")
async def kick(message, client):
    try:
        if len(message.mentions) == 0:
            text = "You must @mention a user to kick."
        else:
            text = "Successfully kicked: \n"
            for member in message.mentions:
                await client.kick(member)
                text += "`" + member.name + "`\n"
        await client.send_message(message.channel, text)
    except discord.errors.Forbidden:
        await client.send_message(message.channel, ":x: Error while trying to kick member (My Role may be lower ranked than a person I am trying to kick) :x:")

async def ban(message, client):
    try:
        if len(message.mentions) == 0:
            text = "You must @mention a user to ban."
            await client.send_message(message.channel, text)
        else:
            text = "Successfully banned:\n"
            for member in message.mentions:
                await client.ban(member, 0)
                text += "`" + member.name + "`\n"
            await client.send_message(message.channel, text)
    except discord.errors.Forbidden:
        await client.send_message(message.channel, ":x: Error while trying to ban member (My Role may be lower ranked than a person I am trying to ban) :x:")

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

async def pruneUsers(message, client, num):
    delcount = 0
    async for log in client.logs_from(message.channel, limit=num):
        if log.author in message.mentions:
            await client.delete_message(log)
            delcount += 1

    msg = "Removed `"+ str(delcount) +"` messages from the last `" + str(num) + "` messages from users: \n`"
    for member in message.mentions:
        msg += member.name + "\n"

    msg += "`"

    await client.send_message(message.channel, msg)


async def prunePhrases(message, client, phrases, num):
    delcount = 0
    async for log in client.logs_from(message.channel, limit=num):
        for phrase in phrases:
            if phrase in log.content:
                await client.delete_message(log)
                delcount += 1

    msg = "Removed `" + str(delcount) + "` messages from the last `" + str(num) + "` messages containing one of the " \
                                                                               "following substrings: \n`"

    for phrase in phrases:
        msg += phrase + "\n"

    msg += "`"

    await client.send_message(message.channel, msg)

async def pruneUserPhrases(message, client, phrases, num):
    delcount = 0
    async for log in client.logs_from(message.channel, limit=num):
        for phrase in phrases:
            if phrase in log.content:
                if log.author in message.mentions:
                    await client.delete_message(log)
                    delcount += 1

    msg = "Removed `"+ str(delcount) +"` messages in the last `" + str(num) + "` messages from users: \n`"
    for member in message.mentions:
        msg += member.name + "\n"

    msg += "`\ncontaining one of the following substrings: \n`"

    for phrase in phrases:
        msg += phrase + "\n"

    msg += "`"

    await client.send_message(message.channel, msg)
