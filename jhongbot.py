import discord
from discord.ext import commands
from discord_slash import SlashCommand
import json
import requests
import random
from datetime import datetime
from pymongo import MongoClient

import logging

historyEnable = False

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename='jhongbot.log',
                    filemode='a')

logger = logging.getLogger('jhongbot')

with open('config.json') as f:
    config = json.load(f)

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

cat_reactions = [
    '\U0001F408',
    '\U0001F431',
    '\U0001F63A',
    '\U0001F63B',
    '\U0001F638',
    '\U0001F43E'
]

emoji = {
    'tick':     '\U00002705',
    'cross':    '\U0000274C',
    'question': '\U00002753'
}

# initialise DB connection
client = MongoClient(config['database'])
db = client['jhongbot']

bot = commands.Bot(command_prefix='?', description='A pretty useless bot')

guild_ids = config['guilds']
slash = SlashCommand(bot, sync_commands=True)

def check_wish(msg: str):
    with open('data/wishes.json') as f:
        wishes = json.load(f)
    with open('data/aliases.json') as f:
        aliases = json.load(f)

    wish = msg.lower()

    logger.info('Received command /wish {}'.format(wish))

    if wish in aliases:
        wish = aliases[wish]
    if wish == 'source':
        response = "Shamelessly stolen from https://idleanimation.com/last-wish-plates"
        return response
    elif wish in wishes:
        title = "YOU WISH {}".format(wishes[wish]['message'])
        description = wishes[wish]['description']
        embed = discord.Embed(title=title, description=description)
        embed.set_image(url=wishes[wish]['image_url'])
        embed.set_footer(text="https://idleanimation.com/last-wish-plates")
        return embed
    else:
        response = "I don't know what you mean"
        return response

@bot.event
async def on_ready():
    logger.info('Logged in as {} id {}'.format(bot.user.name, bot.user.id))

@bot.listen('on_message')
async def history(message):
    if historyEnable:
        if message.author.id == bot.user.id:
            return
        
        history = db['history']
        record = { "user": message.author.name, "message": message.content, "timestamp": message.created_at }
        history.insert(record)

@bot.command(hidden=True)
async def hello(ctx):
    message = 'Hello {}!'.format(ctx.author.mention)
    await ctx.send(message)

@bot.command(brief='Link to the GitHub page for this bot.')
async def jhongbot(ctx):
    await ctx.send('GitHub repo: https://github.com/rougesheep/jhongbot')

@bot.command(brief='Wish-wall solutions for the Last Wish Raid.', name="wish", aliases=['wishwall'])
async def com_wish(ctx, msg: str):
    response = check_wish(msg)
    if type(response) == str:
        await ctx.send(response)
    else:
        await ctx.send(embed=response)

@slash.slash(name="wish", description="Riven Wishwall solutions")
async def slash_wish(ctx, msg: str):
    response = check_wish(msg)
    if type(response) == str:
        await ctx.send(response)
    else:
        await ctx.send(embed=response)

@bot.command(brief='Dawning oven recipes.')
async def dawning(ctx):
    title = 'Dawning Recipes'
    img = 'https://i.imgur.com/nVMYk7R.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@bot.command(hidden=True, aliases=['meow', 'nyan', 'cat', '🐈', '🐱'])
async def poncho(ctx):
    title = random.choice(cat_reactions)
    img = 'https://i.imgur.com/78sGyE2.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@bot.command(brief="DING")
async def ding(ctx):
    title = 'Ding'
    img = 'https://media.giphy.com/media/32681KwrcXqrFIpI0P/giphy.gif'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@bot.command(brief="Wheel of Fortune. But for raids.")
async def raid(ctx):
    raids = [
        'Last Wish',
        'Garden of Salvation',
        'Deep Stone Crypt',
        'Vault of Glass'
    ]

    raid_lines = [
        'How about {}?',
        'Maybe {} this time?',
        'You should do {}.',
        '{}. My Favourite!',
        'Just do {}.',
        '{}.'
    ]

    await ctx.send(random.choice(raid_lines).format(random.choice(raids)))

@bot.command(brief="Callouts for symbols/positions in the Riven fight.", aliases=['callouts', 'symbols'])
async def riven(ctx):
    title = 'Riven Callouts'
    img = 'https://i.imgur.com/Nxr4AO9.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@bot.command(brief="Names are hard.", aliases=['names', 'roster'])
async def whois(ctx, name=''):
    names = db['names']

    if not name:
        title='People'
        embed = discord.Embed(title=title)
        for person in names.find({}).sort("steam_lower"):
            embed.add_field(name=person['steam'], value=person['name'])
        await ctx.send(embed=embed)
    else:
        name=name.lower()
        match = []
        for person in names.find({ "$or": [ { 'name_lower': name}, { 'steam_lower': name }]}):
            match.append(person)
        if not match:
            fail_lines = [
                "I don't know",
                "Never heard of them",
                "I only know about important people"
            ]
            await ctx.send(random.choice(fail_lines))
        else:
            title='People'
            embed=discord.Embed(title=title)
            for person in match:
                embed.add_field(name=person['steam'], value=person['name'])
            await ctx.send(embed=embed)

bot.run(config['token'])
