import discord
from discord.ext import commands, tasks
import os

bot = commands.Bot(command_prefix = '$')
token = os.environ['.env']

# runs when the bot comes online
@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))

# generates message stats on all users or a single one.
@bot.command()
async def msgstats(ctx, arg): 
  print('Entering msgstats configuration...')
  if arg.lower() == 'all':
    users = ctx.guild.members # list of all users in server
    counters = [0] * len(users) # list of message counters
    for channel in ctx.guild.channels:
      for msg in channel.history(limit=None):
        for u in users:
          if msg.author == u:
            counters[users.index(u)] += 1
  else:
    if ctx.guild.members.contains(arg):
      counter = 0
      for channel in ctx.guild.channels:
        for msg in channel.history(limit=None):
          if msg.author == arg:
            counter += 1
    await ctx.send('User {arg} has sent {counter} messages in this server.'.format(arg, counter))


# runs when a message is sent. checks for numerous commands.
@bot.event
async def on_message(msg):
  if msg.author == bot.user:
    return
  if msg.content.lower() == 'ping': # ping pong!
    await msg.channel.send('pong')
  await bot.process_commands(msg)

bot.run(token)