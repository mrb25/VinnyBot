import json
import urllib
import urllib.request

async def harambe(message, client):
    data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/random?tag=silverback+gorilla&api_key=dc6zaTOxFJmzC").read().decode('utf-8'))
    data = json.loads(json.dumps(data['data']))
    await client.send_message(message.channel, data['url'])

async def giphy(message, client):
    text = message.content[6:].replace(' ', '+')
    data = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/random?tag="+text+"&api_key=dc6zaTOxFJmzC").read().decode('utf-8'))
    data = json.loads(json.dumps(data['data']))
    await client.send_message(message.channel, data['url'])