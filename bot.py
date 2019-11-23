import discord
from discord.ext import commands
import json
import random

with open('config.json') as f:
    config = json.load(f)
with open('wishes.json') as f:
    wishes = json.load(f)
with open('aliases.json') as f:
    aliases = json.load(f)

bad_reactions = [
    '\U0001F44E',
    '\U0001F621',
    '\U0001F4A9',
    '\U0001F47A',
    '\U0001F4A2',
    '\U0001F4A5',
    '\U0001F937',
    '\U0001F438',
    '\U0001F6AB',
    '\U0000274C',
    '\U00002049'
]

description = 'Jhongbot'

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as {} id {}'.format(bot.user.name, bot.user.id))
    print('------')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello {}!'.format(ctx.author.mention))

@bot.command()
async def wish(ctx, *msg: str):
    wish = ' '.join(msg)
    print('{} wished for {}'.format(ctx.author.name, wish))
    if wish in aliases:
        wish = aliases[wish]
    if wish == 'source':
        await ctx.send('Shamelessly stolen from https://idleanimation.com/last-wish-plates')
    elif wish in wishes:
        msg = '{} WISHES {}'.format(ctx.author.mention, wishes[wish]['message'])
        embed = discord.Embed(description=msg)
        embed.set_image(url=wishes[wish]['image_url'])
        await ctx.send(embed=embed)
    else:
        await ctx.message.add_reaction(random.choice(bad_reactions))

bot.run(config['token'])