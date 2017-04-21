import json
import urllib
import urllib.request

async def harambe(message, client):
    data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/random?tag=silverback+gorilla&api_key=dc6zaTOxFJmzC").read().decode('utf-8'))
    data = json.loads(json.dumps(data['data']))
    await client.send_message(message.channel, data['url'])

async def giphy(message, client):
    await client.send_typing(message.channel)
    text = message.content[6:].replace(' ', '+')
    try:
        data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/random?tag="+text+"&api_key=dc6zaTOxFJmzC").read().decode('utf-8'))
        data = json.loads(json.dumps(data['data']))
        try:
            await client.send_message(message.channel, data['url'])
        except TypeError:
            await client.send_message(message.channel, "No results returned :cry:")
    except UnicodeEncodeError:
        await client.send_message(message.channel, "Error attempting to send giphy search. (Does the search have wierd characters or formatting?)")
