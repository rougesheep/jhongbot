import discord
from discord.ext import commands
import json
import random
from datetime import datetime

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename='jhongbot.log',
                    filemode='a')

logger = logging.getLogger('jhongbot')

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

cat_reactions = [
    '\U0001F408',
    '\U0001F431',
    '\U0001F63A',
    '\U0001F63B',
    '\U0001F638',
    '\U0001F43E'
]

bot = commands.Bot(command_prefix='?', description='A pretty useless bot')

@bot.event
async def on_ready():
    logger.info('Logged in as {} id {}'.format(bot.user.name, bot.user.id))

@bot.command(hidden=True)
async def hello(ctx):
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))
    await ctx.send('Hello {}!'.format(ctx.author.mention))

@bot.command(brief='Link to the GitHub page for this bot.')
async def jhongbot(ctx):
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))
    await ctx.send('GitHub repo: https://github.com/rougesheep/jhongbot')

@bot.command(brief='Wish-wall solutions for the Last Wish Raid.', aliases=['wishwall', 'riven'])
async def wish(ctx, *msg: str):
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))
    global bad_reactions
    wish = ' '.join(msg)
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
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))
    title = 'Niobe Labs puzzle'
    img = 'https://i.imgur.com/qaPwWnZ.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    embed.add_field(name='Guide', value='https://gamerant.com/destiny-2-niobe-labs-puzzle-how-to-beat/', inline=False)
    embed.add_field(name='Infographic', value='https://imgur.com/a/qQjV9zI', inline=False)
    await ctx.send(embed=embed)

@bot.command(brief='Dawning oven recipes.')
async def dawning(ctx):
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))
    title = 'Dawning Recipes'
    img = 'https://i.imgur.com/nVMYk7R.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    await ctx.send(embed=embed)

@bot.command(brief='Menagerie chalice combinations.', aliases=['menagerie'])
async def chalice(ctx, msg=''):
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))
    title = 'Chalice Combinations'
    armour_img = 'https://i.imgur.com/6tdW1Fs.png'
    weapon_img = 'https://i.imgur.com/EzOgjqy.png'
    armour_embed = discord.Embed(title=title)
    armour_embed.set_image(url=armour_img)
    weapon_embed = discord.Embed(title=title)
    weapon_embed.set_image(url=weapon_img)
    if msg == 'armour':
        await ctx.send(embed=armour_embed)
    elif msg == 'weapons':
        await ctx.send(embed=weapon_embed)
    else:
        await ctx.send('{} weapons or armour?'.format(ctx.author.mention))

@bot.command(brief='Days before season end.')
async def season(ctx):
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))

    season_name = 'Dawn'
    season_end = datetime(2020, 3, 10, 17, 00)
    now = datetime.now()

    s = (season_end - now).total_seconds()
    
    days, r1 = divmod(s, 86400)
    hours, r2 = divmod(r1, 3600)

    msg = "Season of {} ends in {:00} days {} hours".format(season_name, int(days), int(hours))
    await ctx.send(msg)

@bot.command(hidden=True, aliases=['meow', 'nyan', 'cat', '🐈', '🐱'])
async def poncho(ctx):
    logger.info('{} - {}'.format(ctx.author, ctx.message.content))
    title = random.choice(cat_reactions)
    img = 'https://i.imgur.com/78sGyE2.png'
    embed = discord.Embed(title=title)
    embed.set_image(url=img)
    await ctx.send(embed=embed)
        
bot.run(config['token'])