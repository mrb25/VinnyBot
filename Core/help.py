import discord


async def help(client, message):
    user = message.author
    text = "```MEME COMMANDS\n"
    text += "\n~shit ~harambe ~lenny ~hammer ~doggo ~hitler ~mario ~megaman ~salt ~feels ~pikachu" \
            " ~ayy\n~giphy *search terms*\n~8ball -- Get a response from the magic 8 ball\nREDDIT COMMANDS" \
            "\n~rr *subreddit* -- Gives random HOT post from given subreddit\n"
    text += "~tr *subreddit* -- Top HOT post from subreddit right now\n~cosplay *search_terms* -- Searches for a " \
            "cosplay meeting the search terms. (use _ instead of spaces)\n~cosplaygirls *search_terms* -- Searches for" \
            "a girl cosplayer meeting the search terms (use _ instead of spaces)\n" \
            "\nCOMMENT COMMANDS\n~comment @user or #channel -- Generates a unique comment based on the user/channel " \
            "post history (Experimental)\n" \
            "~ryzen -- Hey did you hear about Ryzen??\n"
    text += "\nMODERATION COMMANDS\n~prune @user \"example\" *num* -- Removes the messages from the last *num* messages " \
            "from user containing \"example\". Mentioning users and defining text are both optional and can be used for as many " \
            "users or phrases as needed in a single prune command" \
            "\n~kick *@username*\n~whois *@username* -- Gives info about a user\n" \
            "~stats -- Gives stats about Vinny\n~info -- Gives information about Vinny\n"
    text += "\nVOICE COMMANDS\n"
    text += "~play *URL* -- Plays audio from video in your channel. Works well with Youtube, Soundcloud, Twitch," \
            "Vimeo, etc.\n" \
            "~playlist -- Gets the playlist of currently playing music\n" \
            "~skip -- Starts a vote to skip the current song"
    text += "\n~stop -- If an audio stream is playing in your server it stops it\n" \
            "~pause -- Pauses current audio stream\n~resume -- Resumes audio stream when paused" \
            "\n~voicestats -- Gives info about current audio streams" \
            "\n\nNSFW COMMANDS\n~togglensfw -- Toggles the 'NSFW lock' on each channel" \
            " (User must have 'Manage Channels' permission)\n~nsfw -- Tells whether or not" \
            "nsfw is enabled on a given channel\n~r34 *tags* (for multi-word tags replace spaces with _) -- Rule 34\n\n" \
            "Discord Server -- https://discord.gg/XMwyzxZ```\n"
    await client.send_message(user, text)

async def info(message, client):
    info = discord.Embed(title='Info', colour=VINNY_COLOR)
    info.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    info.add_field(name="About Vinny", value=ABOUT_VINNY)
    info.add_field(name="Vinny Server", value=VINNY_SERVER)
    info.add_field(name="Invite Vinny", value=VINNY_INVITE)
    await client.send_message(message.channel, embed=info)

ABOUT_VINNY = "Vinny is an under development discord bot created by Kikkia. Since Vinny is under current development" \
              "Vinny may rarely crash or drop offline for short periods of time as I find/fix bugs and add features. " \
              "Vinny offers a wide set of features for " \
              "any discord server. Including Music, Memes, Comment generation, and Much more. For a full list type " \
              "'~help' in a channel vinny is in. " \
              " Vinny uses the Discord.py " \
              "framework, as well as voice with JDA and lavaplayer For some more detailed statistics run the '~stats' command."

VINNY_SERVER = "Vinny now has his own discord server where you can suggest features, report bugs, or just talk with " \
               "other users and developers of vinny. Invite Link: https://discord.gg/XMwyzxZ"

VINNY_INVITE = "To invite Vinny to your server go to: https://discordapp.com/oauth2/authorize?client_id=276855867796881408&scope=bot&permissions=67628096"

VINNY_COLOR = int('008cba', 16)
