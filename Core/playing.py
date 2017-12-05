import discord
import operator

async def nowPlaying(message, client):
    server = message.guild
    members = server.members
    gamelist = []
    for member in members:
        if member.game is not None:
            gamelist.append(member.game.name)
    if gamelist is None:
        await message.channel.send("No one appears to be playing anything... :thinking:")
    # Creates dictionary where word is the game and definition is # of people playing
    countedgames = {i: gamelist.count(i) for i in gamelist}
    # Sorts dict by # of people playing
    sortedgames = sorted(countedgames.items(), key=operator.itemgetter(1))
    print(str(sortedgames))

async def battle(message, client):
    # Get the people that are fighting & initial error finding
    mentioned = message.mentions
    if len(mentioned) > 2 or len(mentioned) is 0:
        await message.channel.send("Please mention only 1 or 2 members")
        return
    if len(mentioned) is 2:
        user1 = mentioned[0]
        user2 = mentioned[1]
    else:
        user1 = message.author
        user2 = mentioned[0]
    if user1 is user2:  # If user mentions themself or the same person twice
        await message.channel.send("You'll have to fight your inner demons on your own...")
        return
    print(user1.name + ", " + user2.name)
    await message.channel.send(user1.name + " and " + user2.name + " are battling!")
