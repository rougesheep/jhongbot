import discord
from discord.ext import commands
import json
import requests
import random
from datetime import datetime
from pymongo import MongoClient

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename='jhongbot.log',
                    filemode='a')

logger = logging.getLogger('jhongbot')

with open('config.json') as f:
    config = json.load(f)
with open('data/abuse.json') as f:
    abuse = json.load(f)

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

def isToBeAbused(username):
    return username in config['abuseList']

def getAbuse(username):
    return random.choice(abuse).format(username)

bot = commands.Bot(command_prefix='?', description='A pretty useless bot')

@bot.event
async def on_ready():
    logger.info('Logged in as {} id {}'.format(bot.user.name, bot.user.id))

@bot.listen('on_message')
async def history(message):
    if message.author.id == bot.user.id:
        return
    
    history = db['history']
    record = { "user": message.author.name, "message": message.content, "timestamp": message.created_at }
    history.insert(record)

@bot.command(hidden=True)
async def hello(ctx):
    if (isToBeAbused(str(ctx.author))):
        message = getAbuse(ctx.author.mention)
    else:
        message = 'Hello {}!'.format(ctx.author.mention)
    await ctx.send(message)

@bot.command(brief='Link to the GitHub page for this bot.')
async def jhongbot(ctx):
    await ctx.send('GitHub repo: https://github.com/rougesheep/jhongbot')

@bot.command(brief='Wish-wall solutions for the Last Wish Raid.', aliases=['wishwall'])
async def wish(ctx, *msg: str):
    with open('data/wishes.json') as f:
        wishes = json.load(f)
    with open('data/aliases.json') as f:
        aliases = json.load(f)

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
        embed.set_footer(text='https://idleanimation.com/last-wish-plates')
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

@bot.command(brief='Menagerie chalice combinations.', aliases=['menagerie'])
async def chalice(ctx, msg=''):
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
    season_name = 'the Worthy'
    season_end = datetime(2020, 3, 10, 17, 00)
    now = datetime.now()

    s = (season_end - now).total_seconds()
    
    days, r1 = divmod(s, 86400)
    hours, r2 = divmod(r1, 3600)

    msg = "Season of {} ends in {:00} days {} hours".format(season_name, int(days), int(hours))
    await ctx.send(msg)

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

@bot.command(brief="Vendor Power Drops", aliases=['engrams'])
async def vendors(ctx):
    uri = "https://api.vendorengrams.xyz/getVendorDrops"
    r = requests.get(url=uri)
    vendors = r.json()
    vendor_names = {
        'devrim': 'Devrim Kay',
        'bray': 'Ana Bray',
        'asher': 'Asher Mir',
        'benedict': 'Benedict 99-40',
        'failsafe': 'Failsafe',
        'zavala': 'Zavala',
        'shaxx': 'Shaxx',
        'banshee': 'Banshee-44',
        'werner': 'Werner 99-40',
        'sloane': 'Sloane',
        'fanboy': 'Brother Vance',
        'saladin': 'Lord Saladin'
    }
    good = []
    bad = []
    unknown = []
    for vendor in vendors:
        if vendor['display'] == '1':
            if vendor['drop'] == '2':
                good.append(vendor_names[vendor['shorthand']])
            elif vendor['drop'] == '1':
                bad.append(vendor_names[vendor['shorthand']])
            else:
                unknown.append(vendor_names[vendor['shorthand']])
    
    title = 'Vendor Engrams'
    embed = discord.Embed(title=title)
    if len(good) > 0:
        embed.add_field(name='High', value="\n".join(good), inline=True)
    if len(bad) > 0:
        embed.add_field(name='Low', value="\n".join(bad), inline=True)
    if len(unknown) > 0:
        embed.add_field(name='Unknown', value="\n".join(unknown), inline=True)
    embed.set_footer(text='https://vendorengrams.xyz/')
    await ctx.send(embed=embed)

@bot.command(brief="Wheel of Fortune. But for raids.")
async def raid(ctx):
    raids = [
        'Leviathan',
        'Eater of Worlds',
        'Spire of Stars',
        'Last Wish',
        'Scourge of the Past',
        'Crown of Sorrow',
        'Garden of Salvation'
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
