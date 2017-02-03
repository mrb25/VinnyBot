

async def help(client, message):
    user = message.author
    text = "`MEME COMMANDS\n"
    text += "\n~shit\n~harambe\n~kappa\n~ayy\n~giphy search\n~rr subreddit -- Gives random HOT post from given subreddit\n"
    text += "~tr subreddit -- Top HOT post from subreddit right now\n"
    text += "\nMODERATION COMMANDS\n~prune num\n~kick @username\n~whois @username -- Gives info about a user\n"
    text += "\nVOICE COMMANDS\n~summon\n~play youtubeurl\n`"
    text += ""
    await client.send_message(user, text)
