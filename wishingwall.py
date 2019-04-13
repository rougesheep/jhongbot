import discord
import json

with open('config.json') as f:
    config = json.load(f)
with open('wishes.json') as f:
    wishes = json.load(f)
with open('aliases.json') as f:
    aliases = json.load(f)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!wishwall'):
        msgs = message.content.split(' ', 1)
        msgs.remove('!wishwall')
        wish = msgs.pop(0)
        print("{} - {}: {}".format(message.guild, message.author, wish))
        if wish in aliases:
            wish = aliases[wish]
        if wish == 'source':
            await message.channel.send('Shamelessly stolen from https://idleanimation.com/last-wish-plates')
            await message.delete()
        elif wish in wishes:
            msg = '{} WISHES {}'.format(message.author.mention, wishes[wish]['message'])
            embed = discord.Embed(description=msg)
            embed.set_image(url=wishes[wish]['image_url'])
            await message.channel.send(embed=embed)
            await message.delete()
        else:
            await message.add_reaction('\U0001F44E')
            await message.channel.send('You wish for the impossible.')

client.run(config['token'])