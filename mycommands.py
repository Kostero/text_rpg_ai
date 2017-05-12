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

def load_commands(filename):
    result = defaultdict(list)
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
    return result

import json
with open('params.json') as jsonfile:
    params = json.load(jsonfile)


mode = params["SOURCES"]
if type(mode) == list:
    mode = mode[0]

commands = load_commands(path+'/commands/preprocessedCommands_'+mode+'.txt')
fight_commands = load_commands(path+'/commands/preprocessedFightCommands_'+mode+'.txt')

global directions
directions = ['east', 'west', 'south', 'north', 'southeast', 'northwest', 'northeast', 'southwest', 'up', 'down', 'left', 'right', 'get off', 'get on', 'straight', 'back']
last_move = 0

def get_take_command(obj):
    return 'get ' + obj

def get_move_command(direction):
    global last_move
    try:
        last_move = directions.index(direction)
    except:
        last_move = 0
    if direction[:3] != "get":
        direction = "go "+direction
    return direction

def get_back_command():
    global last_move
    last_move ^= 1
    if directions[last_move][:3] != "get":
        return "go "+directions[last_move]
    else:
        return directions[last_move]
