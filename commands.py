import random
import descriptions
import word2vec
from nltk_helper import get_nouns

fight_actions = {'attack', 'kill', 'fight', 'shoot', 'strike', 'punch'}

with open('commands/downloadedCommands.txt', 'r') as f:
    lines = f.readlines()
lines = map(str.lower, lines)
lines = map(str.split, lines)
lines = filter(lambda x: len(x) > 1, lines)
for l in lines:
    for i, w in enumerate(l):
        if w == 'x':
            l[i] = 'examine'
commands = {}
fight_commands = {}
for l in lines:
    for n in get_nouns(l):
        if n not in commands:
            commands[n] = []
        commands[n].append(' '.join(l))
        if any(map(fight_actions.__contains__, l)):
            if n not in fight_commands:
                fight_commands[n] = []
            fight_commands[n].append(' '.join(l))

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

"""def get_command(desc):
    if dangerous(desc):
        return get_back_command()
    if desc not in taken:
        taken[desc] = set()
    if desc not in done:
        done[desc] = 0
    if desc not in score:
        score[desc] = [(n, len(commands_for_noun(n)) / (1.0 + descriptions.frequency(n))) for n in get_nouns(desc)]
    if desc not in used:
        used[desc] = {}
    tk = taken[desc]
    for freq, obj in least_common(desc, 7):
        if not obj in tk:
            tk.add(obj)
            return 'get ' + obj
    global moves
    if done[desc] - 10 > moves / 10:
        moves += 1
        return get_move_command()
    done[desc] += 1
    c = weighted_choice(score[desc])
    if c is None:
        print '\ta'
        return get_move_command()
    print '\t', c
    com = commands_for_noun(c)
    if len(com) == 0:
        print '\tb'
        return get_move_command()
    for i in range(10):
        ans = random.choice(com)
        if ans not in used[desc]:
            used[desc][ans] = 1
            return ans
        elif i == 9 and used[desc][ans] < 3:
            used[desc][ans] += 1
            return ans
    print '\td'
    return get_move_command()
"""