

async def help(client, message):
    user = message.author
    text = "`MEME COMMANDS\n"
    text += "\n~shit\n~harambe\n~lenny\n~hammer\n~doggo\n~hitler\n~mario\n~megaman\n~salt\n~feels\n~pikachu" \
            "\n~ayy\n~giphy search\n~rr subreddit -- Gives random HOT post from given subreddit\n"
    text += "~tr subreddit -- Top HOT post from subreddit right now\n" \
            "~comment @user -- Generates a unique comment based on the users post history (Experimental)\n"
    text += "\nMODERATION COMMANDS\n~prune num\n~kick @username\n~whois @username -- Gives info about a user\n"
    text += "\nVOICE COMMANDS\n~summon -- Summons Vinny to your current voice channel\n"
    text += "~play youtubeurl -- Plays audio from video in your channel\n"
    text += "~stop -- If an audio stream is playing in your server it stops it\n" \
            "~pause -- Pauses current audio stream\n ~resume -- Resumes audio stream when paused`\n"
    await client.send_message(user, text)
