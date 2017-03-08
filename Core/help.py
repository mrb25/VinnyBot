

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
            "~stats -- Gives stats about Vinny\n"
    text += "\nVOICE COMMANDS\n~summon -- Summons Vinny to your current voice channel\n"
    text += "~play *youtubeurl* -- Plays audio from video in your channel\n" \
            "~playlist -- Gets the playlist of currently playing music\n" \
            "~skip -- Starts a vote to skip the current song" \
            "~volume *#* -- Enter a number between 0.1 and 2.0 to change volume of audio. No number gives the current level"
    text += "\n~stop -- If an audio stream is playing in your server it stops it\n" \
            "~pause -- Pauses current audio stream\n~resume -- Resumes audio stream when paused" \
            "\n\nNSFW COMMANDS\n~togglensfw -- Toggles the 'NSFW lock' on each channel" \
            " (User must have 'Manage Channels' permission)\n~nsfw -- Tells wether or not" \
            "nsfw is enabled on a given channel\n~r34 *tags* (for multi-word tags replace spaces with _) -- Rule 34`\n"
    await client.send_message(user, text)
