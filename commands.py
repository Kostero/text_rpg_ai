import random
import descriptions
import word2vec
from nltk_helper import get_nouns
from collections import *

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

commands = load_commands('commands/preprocessedCommands.txt')
fight_commands = load_commands('commands/preprocessedFightCommands.txt')

directions = ['east', 'west', 'south', 'north', 'southeast', 'northwest', 'northeast', 'southwest', 'up', 'down']
last_move = 0

def get_take_command(obj):
    return 'get ' + obj

def get_move_command(direction):
    global last_move
    try:
        last_move = directions.index(direction)
    except:
        last_move = 0
    return 'go ' + direction

def get_back_command():
    global last_move
    last_move ^= 1
    return 'go ' + directions[last_move]