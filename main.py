import discord
from discord.ext import commands, tasks
import os
from operator import itemgetter
from tqdm.asyncio import tqdm

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '$', intents=intents)
token = os.environ['.env']

# runs when the bot comes online
@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))

# --- TO DO ---
# detect most popular times
# detect most popular channels

@bot.command()
async def userlist(ctx):
  msg = ''
  for u in ctx.guild.members:
    msg += "User: " + u.name + ", ID: " + str(u.id) + "\n"
  await ctx.send(msg)

# Generates a top 3 ranking of user activity on the server.
@bot.command()
async def ranking(ctx):
  await ctx.send("Generating user rankings...")
  message = ""
  users = ctx.guild.members # list of all users in server
  chan_type = ctx.channel.type
  counters = {u.id : 0 for u in users} # keymap of users to counters
  # Get list of counters of user messages
  for channel in ctx.guild.channels:
      if channel.type == chan_type:
        async for msg in tqdm(channel.history(limit=None)):
          auth = msg.author
          if auth.id in counters.keys():
            counters[auth.id] += 1
  # Get top 3 users
  ids = sorted(counters.keys(), key=lambda c: counters[c], reverse=True)
  top3ids = ids[:3]
  for rank, id in enumerate(top3ids):
    for u in users:
      if (int(u.id) is id):
        message += f'#{rank+1}: User {u.name} with {counters[u.id]} messages\n'
        break
  await ctx.send(message)


# Generates message stats on all users or a single one.
@bot.command()
async def msgstats(ctx, *arg):
  message = ""
  chan_type = ctx.channel.type
  arg = ' '.join(arg)
  counter = 0

  # Following block runs if request is for all users.
  if arg.lower() == 'all':

    await ctx.send("Calculating message stats for all server users. May take several moments...")
    users = ctx.guild.members # list of all users in server
    counters = {u.id : 0 for u in users} # keymap of users to counters
    
    for channel in ctx.guild.channels:
      if channel.type == chan_type:
        async for msg in channel.history(limit=None):
          auth = msg.author
          if auth.id in counters.keys():
            counters[auth.id] += 1
          counter += 1
    for user in users:
        message += f'User {user.name} has {counters[user.id]} messages in the server.\n'
    message += f'There are a total of {counter} messages in this server.\n'

  # Following block runs if a single user is listed.
  else:
    contains = False
    for u in ctx.guild.members:
      if u.name == arg:
        contains = True
    if contains:
      for channel in ctx.guild.channels:
        if channel.type == chan_type:
          async for msg in channel.history(limit=None):
            if msg.author.name == arg:
              counter += 1
        message = f'User {arg} has sent {str(counter)} messages in this server.'
    else:
      message = f'User {arg} is not in this server.'
  await ctx.send(message)

bot.run(token)
