import discord
from discord.ext import commands, tasks
import os

bot = commands.Bot(command_prefix = '$')
token = os.environ['.env']

# runs when the bot comes online
@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))

@bot.command()
async def pong(ctx):
  print('in pong')
  await ctx.send('ping')

# generates message stats on all users or a single one.
@bot.command()
# Retrieve total amount of messages user has sent
async def msgstats(ctx, arg):
    print('Entering msgstats configuration...')
    if arg.lower() == 'all':
        await ctx.send("Calculating message stats for all server users. May take several moments...")
        users = ctx.guild.members # list of all users in server
        counters = [0] * len(users) # list of message counters
        for channel in ctx.guild.channels:
            for msg in channel.history(limit=None):
                for u in users:
                    if msg.author == u:
                        counters[users.index(u)] += 1
        msg = ""
        counter = 0
        for user in users:
            msg += "User " + user + " has " + counters[user.index] + " messages in the server.\n"
            counter += counters[user.index]
        msg += "There are a total of " + counter + " messages in this server."
        await ctx.send(msg)
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