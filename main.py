import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up or whatever",
  "Just fall already",
  "You are really a pain in the ass"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

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
  if message.author == client:
    return

  msg = message.content

  if msg.startswith('tx!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("tx!new"):
    encouraging_message = msg.split("tx!new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("tx!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("tx!del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  
  if msg.startswith('tx!hello'):
    await message.channel.send("Hello there!")
  
  if msg.startswith('tx!help'):
    await message.channel.send('This is a test command, my creator is working hard to get me working right!')

  if msg.startswith("tx!list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("responding"):
    value = msg.split("tx!responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("responding is on")
    else:
      db["responding"] = False
      await message.channel.send("responding is off")

keep_alive()
client.run(os.getenv('TOKEN'))