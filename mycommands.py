import random
import descriptions
import word2vec
from nltk_helper import get_nouns
from collections import *
import os

path = os.path.dirname(__file__)
if path == '':
    path = '.'

Command = namedtuple('Command', ['text', 'nouns', 'freq'])

def load_commands(result, filename):
    with open(filename, 'r') as f:
        for l in f.readlines():
            try:
                items = l.split('#')
                text = items[0]
                nouns = items[1:-1]
                freq = int(items[-1])
                for n in nouns:
                    result[n].append(Command(text, nouns, freq))
            except:
                print 'failed to parse', l

import json
with open('params.json') as jsonfile:
    params = json.load(jsonfile)


mode = os.environ["SOURCES"] if os.environ.has_key("SOURCES") else params["SOURCES"]
if type(mode) == list:
    mode = mode[0]

commands = defaultdict(list)
fight_commands = defaultdict(list)
for mod in mode.split("_"):
    load_commands(commands, path+'/commands/preprocessedCommands_'+mode+'.txt')
    load_commands(fight_commands, path+'/commands/preprocessedFightCommands_'+mode+'.txt')

global directions
directions = ['east', 'west', 'south', 'north', 'southeast', 'northwest', 'northeast', 'southwest', 'up', 'down', 'left', 'right', 'get off', 'get on', 'straight', 'back']
primary_directions = 10
last_move = 0

def get_take_command(obj):
    return 'get ' + obj

def get_move_command(direction=None):
    if direction is None:
        direction = random.choice(directions[:primary_directions])
    global last_move
    try:
        last_move = directions.index(direction)
    except:
        last_move = 0
    if direction[:3] != "get":
        direction = "go "+direction
    return direction

def get_opposite_command(command):
    if command is None:
        return None
    if command.startswith('go '):
        command = command[3:]
    try:
        i = directions.index(command)
        result = directions[i^1]
        if not result.startswith('get'):
            result = 'go ' + result
        return result
    except:
        return

def get_back_command():
    global last_move
    last_move ^= 1
    if directions[last_move][:3] != "get":
        return "go "+directions[last_move]
    else:
        return directions[last_move]
