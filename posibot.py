import discord
import os
import requests
import json
import random
from replit import db

# my_secret = os.environ["DISCORD_API"]
discord_api_key = os.environ['DISCORD_API']
#go to bot in discord and copy token
#create new secret and enter relivant info

client = discord.Client()  # create a discord client
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable']

starter_encouragements = [
    "Cheer up!", "Chillout B-bot", "You are a great robot!",
    "Eat some rice man", "grab a cold one", "take a swim"
]

# @client.event
# async def on_ready():
#     print('Ready!')

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    options = starter_encouragements
    if "encouragements" in db.keys():
        options = options + list(db["encouragements"])

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$hello"):
        await message.channel.send("Hello " + message.author.name + '!')

    if msg.startswith("$instructions"):
        await message.channel.send("Here is how you use me commands: type $hello and I will respond, type $inspire and I will give you an inspirational quote from Zen quotes, if you type in a word like, sad, depressed or miserable and I will respond with a nice statement or a suggestion of something you can do, type $new to add a new positive statement for when hard emotions are expressed.")

    if msg.startswith("$encouragements"):
      await message.channel.send(starter_encouragements)

    if msg.startswith("$words"):
      await message.channel.send(sad_words)

    if msg.startswith("$test"):
      await message.channel.send(db["encouragements"])

client.run(discord_api_key)
