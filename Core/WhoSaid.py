async def findWhoSaid(message, client):
    userCount = {}
    phrase = message.content[len("~whosaid "):]
    async for channelMessage in client.logs_from(message.channel, limit = 2000):
        if message.id != channelMessage.id:
            try:
                if phrase in channelMessage.content:
                    if channelMessage.author not in userCount:
                        userCount[channelMessage.author] =0
                        userCount[channelMessage.author] += 1
            except:
                print("invalid character found")
    maxCount = -1
    maxUser = None
    for user in userCount:
        if userCount[user] > maxCount:
            maxUser = user
            maxCount = userCount[user]
    if maxCount > -1:
        await client.send_message(message.channel, maxUser.name + " has said \"" + phrase + "\", " + str(maxCount) + " times.")
    else:
        await client.send_message(message.channel, "Turns out you are the first... :thumbsup:")
