

async def help(client, message):
    user = message.author
    text = "`MEME COMMANDS\n"
    text += "\n~shit\n~harambe\n~lenny\n~hammer\n~doggo\n~hitler\n~mario\n~megaman\n~salt\n~feels\n~pikachu" \
            "\n~ayy\n~giphy search\n~rr subreddit -- Gives random HOT post from given subreddit\n"
    text += "~tr subreddit -- Top HOT post from subreddit right now\n" \
            "~comment @user or #channel -- Generates a unique comment based on the user/channel post history (Experimental)\n" \
            "~ryzen -- Hey did you hear about Ryzen??\n"
    text += "\nMODERATION COMMANDS\n~prune num\n~kick @username\n~whois @username -- Gives info about a user\n" \
            "~stats -- Gives stats about Vinny\n"
    text += "\nVOICE COMMANDS\n~summon -- Summons Vinny to your current voice channel\n"
    text += "~play youtubeurl -- Plays audio from video in your channel\n" \
            "~playlist -- Gets the playlist of currently playing music\n" \
            "~volume -- Enter a number between 0.1 and 2.0 to change volume of audio. No number gives the current level"
    text += "\n~stop -- If an audio stream is playing in your server it stops it\n" \
            "~pause -- Pauses current audio stream\n~resume -- Resumes audio stream when paused`\n"
    await client.send_message(user, text)
