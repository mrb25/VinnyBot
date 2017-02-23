import discord

commandsSinceLastReboot = 0

VINNY_COLOR = int('008cba', 16)

async def getStats(message, client):
    serverCount = 0
    channelCount = 0
    for server in client.servers:
        serverCount += 1
        for channel in server.channels:
            channelCount += 1

    if message.channel.permissions_for(message.server.me).embed_links:
        embed = discord.Embed(title='', colour=VINNY_COLOR)
        embed.add_field(name='Servers',
                        value='{}'.format(serverCount),
                        inline=True)
        embed.add_field(name='Channels', value=channelCount, inline=True)
        embed.add_field(name='Commands since last update', value=commandsSinceLastReboot, inline=True)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)

        return await client.send_message(message.channel, embed=embed)
    else:
        await client.send_message(message.channel, "Vinny Stats:\n`Servers: " + str(serverCount) + "\nChannels: " + str(channelCount)
                                  + "\nNumber of commands issued since last update: " + str(commandsSinceLastReboot) +
                                  "`")


def commandCalled():
    global commandsSinceLastReboot
    commandsSinceLastReboot += 1
