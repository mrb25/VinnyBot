import discord
import operator
import time
from random import randint

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

    # players are given weapons randomly
    weapons = ["axe", "bow", "sword", "wits"]
    user1_weapon = weapons[randint(0, 3)]
    user2_weapon = weapons[randint(0, 3)]
    await message.channel.send(user1.name + " weilds their " + user1_weapon + ", while " + user2.name +
                               " takes in their trusty " + user2_weapon + ".")

    # initilize health and begin battle loop
    attacker_health = 100
    defender_health = 100
    if randint(0, 1) is 0:
        attacker = user1
        defender = user2
    else:
        attacker = user2
        defender = user1
    while attacker_health > 0 and defender_health > 0:
        roll = randint(1, 20)
        if roll is 1:
            attacker_health -= 10
            if attacker_health < 0:
                attacker_health = 0
            await message.channel.send("Critical fail! " + attacker.name + " hurts themself for 10!")
        if roll is 20:
            defender_health -= 40
            if defender_health < 0:
                defender_health = 0
            await message.channel.send("Critical hit! " + attacker.name + " hits " + defender.name + " for 40!")
        else:
            hit = roll + 10
            defender_health -= hit
            if defender_health < 0:
                defender_health = 0
            await message.channel.send(attacker.name + " strikes " + defender.name + " for " + str(hit) +
                                       "\n" + attacker.name + ": " + str(attacker_health) + " | " +
                                       defender.name + ": " + str(defender_health))
        time.sleep(2)

        # Switch attacker <-> defender
        temp = attacker
        attacker = defender
        defender = temp

        # Switch health for each player
        temp = attacker_health
        attacker_health = defender_health
        defender_health = temp
