import discord
from discord.ext import commands
import json
import random

import logging

logging.basicConfig(level=logging.INFO)

with open('config.json') as f:
    config = json.load(f)
with open('data/wishes.json') as f:
    wishes = json.load(f)
with open('data/aliases.json') as f:
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

bot = commands.Bot(command_prefix='?', description='A pretty useless bot')

@bot.event
async def on_ready():
    print('Logged in as {} id {}'.format(bot.user.name, bot.user.id))
    print('------')

@bot.command(hidden=True)
async def hello(ctx):
    await ctx.send('Hello {}!'.format(ctx.author.mention))

@bot.command(brief='Link to the GitHub page for this bot.')
async def jhongbot(ctx):
    await ctx.send('GitHub repo: https://github.com/rougesheep/jhongbot')

@bot.command(brief='Wish-wall solutions for the Last Wish Raid.', aliases=['wishwall', 'riven'])
async def wish(ctx, *msg: str):
    global bad_reactions
    wish = ' '.join(msg)
    print('{} wished for {}'.format(ctx.author.name, wish))
    if wish in aliases:
        wish = aliases[wish]
    if wish == 'source':
        await ctx.send('Shamelessly stolen from https://idleanimation.com/last-wish-plates')
    elif wish in wishes:
        title = 'YOU WISH {}'.format(wishes[wish]['message'])
        description = wishes[wish]['description']
        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=wishes[wish]['image_url'])
        await ctx.send(embed=embed)
    else:
        await ctx.message.add_reaction(random.choice(bad_reactions))

@bot.command(brief='Guide for the Niobe Labs puzzle from Black Armoury.')
async def niobe(ctx):
    title = 'Niobe Labs puzzle'
    img = 'https://i.imgur.com/qaPwWnZ.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    embed.add_field(name='Guide', value='https://gamerant.com/destiny-2-niobe-labs-puzzle-how-to-beat/', inline=False)
    embed.add_field(name='Infographic', value='https://imgur.com/a/qQjV9zI', inline=False)
    await ctx.send(embed=embed)

@bot.command(brief='Dawning oven recipes.')
async def dawning(ctx):
    title = 'Dawning Recipes'
    img = 'https://i.imgur.com/nVMYk7R.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    await ctx.send(embed=embed)

bot.run(config['token'])