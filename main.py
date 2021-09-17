import discord
import os

client = discord.Client()
token = os.environ['.env']

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(msg): # on message received
  if msg.author == client.user:
    return

  if msg.content.startswith('ping') or msg.content.startswith('PING') or msg.content.startswith('ping.'):
    await msg.channel.send('pong')

client.run(token)