import discord
import operator
import time
from random import randint

async def nowPlaying(message, client):
    server = message.guild
    members = server.members
    gamelist = []
    for member in members:
        if member.game is not None and not member.bot:
            gamelist.append(member.game.name)
    if not gamelist:  # if list is empty
        await message.channel.send(":X: No one appears to be playing anything... :thinking:")
        return
    # Creates dictionary where word is the game and definition is # of people playing
    countedgames = {i: gamelist.count(i) for i in gamelist}
    # Sorts dict by # of people playing
    sortedgames = sorted(countedgames.items(), key=operator.itemgetter(1))
    finalstring = "Games being played by members now: \n"
    for (game, players) in sortedgames:
        finalstring += game + ": " + str(players) + "\n"
    await message.channel.send(finalstring)


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
    await message.channel.send(user1.name + " and " + user2.name + " are battling!")

    # players are given weapons randomly
    weapons = ["dagger :dagger:", "bow :bow_and_arrow:", "sword :crossed_swords:", "wits :thinking:"]
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

    # Someday the great spaghetti code monster will be summoned and reap all our lives, And I will be a bit at fault.
    flipthis = True  # To keep users' HP on the same side each time

    while attacker_health > 0 and defender_health > 0:
        time.sleep(2)  # Damn humans need time to read
        roll = randint(1, 20)
        battlerecord = ""
        if roll is 1:
            attacker_health -= 10
            battlerecord += "Critical fail! " + attacker.name + " hurts themself for 10!"

        if roll is 20:
            defender_health -= 40
            battlerecord += "Critical hit! " + attacker.name + " hits " + defender.name + " for 40!"

        else:
            hit = roll + 10
            defender_health -= hit
            battlerecord += attacker.name + " strikes " + defender.name + " for " + str(hit)

        if defender_health < 0:
            attacker_health = 0
        elif attacker_health < 0:
            defender_health = 0

        if flipthis:
            battlerecord += "\n" + defender.name + ": " + str(defender_health) + " | " + \
                            attacker.name + ": " + str(attacker_health)
        else:
            battlerecord += "\n" + attacker.name + ": " + str(attacker_health) + " | " + \
                            defender.name + ": " + str(defender_health)
        await message.channel.send(battlerecord)

        # Switch attacker <-> defender
        temp = attacker
        attacker = defender
        defender = temp

        # Switch health for each player
        temp = attacker_health
        attacker_health = defender_health
        defender_health = temp

        flipthis = not flipthis

    if defender_health < 1:
        loser = defender
        winner = attacker
    else:
        loser = attacker
        winner = defender
    await message.channel.send(winner.name + " defeated " + loser.name + "!")
