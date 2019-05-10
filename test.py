import json

with open('wishes.json') as f:
    wishes = json.load(f)
with open('aliases.json') as f:
    aliases = json.load(f)

#print(wishes['1']['message'])

wish = 'riven'

if wish in aliases:
    wish = aliases[wish]

if wish in wishes:
    print(wishes[wish]['message'])

author = "barry"

print("{}: {}".format(author, wish))