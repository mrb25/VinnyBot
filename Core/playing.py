import discord
import operator

async def nowPlaying(message, client):
    server = message.guild
    members = server.members
    gamelist = []
    for member in members:
        if member.game is not None:
            gamelist.append(member.game.name)
    # Creates dictionary where word is the game and definition is # of people playing
    countedgames = {i: gamelist.count(i) for i in gamelist}
    # Sorts dict by # of people playing
    sortedgames = sorted(countedgames.items(), key=operator.itemgetter(1))
    print(str(sortedgames))
