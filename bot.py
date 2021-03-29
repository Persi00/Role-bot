import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Bot is ready!")

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

client.run('ODA2OTAwMjUyMTkxODgzMzA0.YBwKaw.N2Em2Fm8nNf6KKBB0Qywm139i2c')
