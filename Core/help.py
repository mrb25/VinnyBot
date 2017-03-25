import discord


async def help(client, message):
    user = message.author
    text = "`MEME COMMANDS\n"
    text += "\n~shit ~harambe ~lenny ~hammer ~doggo ~hitler ~mario ~megaman ~salt ~feels ~pikachu" \
            " ~ayy\n~giphy *search terms*\n\nREDDIT COMMANDS" \
            "\n~rr *subreddit* -- Gives random HOT post from given subreddit\n"
    text += "~tr *subreddit* -- Top HOT post from subreddit right now\n~cosplay *search_terms* -- Searches for a " \
            "cosplay meeting the search terms. (use _ instead of spaces)\n~cosplaygirls *search_terms* -- Searches for" \
            "a girl cosplayer meeting the search terms (use _ instead of spaces)\n" \
            "\nCOMMENT COMMANDS\n~comment @user or #channel -- Generates a unique comment based on the user/channel " \
            "post history (Experimental)\n" \
            "~ryzen -- Hey did you hear about Ryzen??\n"
    text += "\nMODERATION COMMANDS\n~prune *num*\n~kick *@username*\n~whois *@username* -- Gives info about a user\n" \
            "~stats -- Gives stats about Vinny\n~info -- Gives information about Vinny\n"
    text += "\nVOICE COMMANDS\n~summon -- Summons Vinny to your current voice channel\n"
    text += "~play *youtubeurl* -- Plays audio from video in your channel (Partial livestream support)\n" \
            "~playlist -- Gets the playlist of currently playing music\n" \
            "~skip -- Starts a vote to skip the current song" \
            "~volume *#* -- Enter a number between 0.1 and 2.0 to change volume of audio. No number gives the current level"
    text += "\n~stop -- If an audio stream is playing in your server it stops it\n" \
            "~pause -- Pauses current audio stream\n~resume -- Resumes audio stream when paused" \
            "\n~voicestats -- Gives info about current audio streams" \
            "\n\nNSFW COMMANDS\n~togglensfw -- Toggles the 'NSFW lock' on each channel" \
            " (User must have 'Manage Channels' permission)\n~nsfw -- Tells whether or not" \
            "nsfw is enabled on a given channel\n~r34 *tags* (for multi-word tags replace spaces with _) -- Rule 34\n\n" \
            "Discord Server -- https://discord.gg/XMwyzxZ`\n"
    await client.send_message(user, text)

async def info(message, client):
    info = discord.Embed(title='Info', colour=VINNY_COLOR)
    info.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    info.add_field(name="About Vinny", value=ABOUT_VINNY)
    info.add_field(name="Vinny Server", value=VINNY_SERVER)
    await client.send_message(message.channel, embed=info)

ABOUT_VINNY = "Vinny is an under development discord bot created by Kikkia. Since Vinny is under current development" \
              "Vinny may rarely crash or drop offline for short periods of time as I find/fix bugs and add features. " \
              "Vinny offers a wide set of features for " \
              "any discord server. Including Music, Memes, Comment generation, and Much more. For a full list type " \
              "'~help' in a channel vinny is in. Vinny is currently run on a Raspberry Pi 3. Because of this he only" \
              "allows up to 2 servers to use music at the same time. Hopefully soon he can find a more powerful home." \
              " Vinny uses the Discord.py " \
              "framework. For some more detailed statistics run the '~stats' command."

VINNY_SERVER = "Vinny now has his own discord server where you can suggest features, report bugs, or just talk with " \
               "other users and developers of vinny. Invite Link: https://discord.gg/XMwyzxZ"

VINNY_COLOR = int('008cba', 16)
