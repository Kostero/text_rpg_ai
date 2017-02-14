import textplayer.textPlayer as tp
import random
import descriptions
import sys
import commands
from functools import partial
from inventory import Inventory
from place import Place

scores = open('scores', 'a')
questions = open('questions', 'a')
fights = open('fights', 'a')
score = 0
max_score = 0
possible_score = 0

def look():
    desc = t.execute_command('look')
    dot = desc.find('.')
    if dot != -1:
        first = desc[:dot]
        if all(x.isdigit() or len(x) < 2 for x in first.split()):
            desc = desc[dot+1:]
    for i in range(min(30, len(desc))):
        if desc[i].islower() and (i == 0 or not desc[i-1].isalpha()):
            first = [''] + desc[:i].split()
            desc = first[-1] + ' ' + desc[i:]
            break
    print desc
    descriptions.add(desc)
    return desc

filename = 'zork1.z5' if len(sys.argv) < 2 else sys.argv[1]
t = tp.TextPlayer(filename)
start_info = t.run()
t.execute_command('verbose')
t.execute_command('verbose')
places = {}
inv = Inventory(partial(t.execute_command, 'inventory'))
moves = 0

try:
    print start_info
    desc = look()
    for i in range(2500):
        if desc not in places:
            places[desc] = Place(desc)
        command = places[desc].get_command(inv.content, moves, inv.nr)
        print command
        if command[0] == Place.Take:
            command_text = commands.get_take_command(command[1])
        elif command[0] == Place.Move:
            moves += 1
            if command[1] == Place.RunAway:
                command_text = commands.get_back_command()
            else: command_text = commands.get_move_command(command[1])
        else:
            command_text = command[1]
        print command_text
        command_output = t.execute_command(command_text)
        print command_output
        if '?' in command_output:
            questions.write(command_output + '\n')
        if command[0] == Place.Take:
            for c in inv.update():
                print c
                print t.execute_command(c)
        elif command[0] == Place.Fight:
            for j in range(6):
                fights.write(command_output + '\n')
                print command[1]
                command_output = t.execute_command(command[1])
                print command_output
        new_desc = look()
        if new_desc == desc:
            if command[0] == Place.Move and not command_output.endswith(desc) and not desc.endswith(command_output):
                places[desc].useless_move(command[1])
            elif command[0] in [Place.Action, Place.Fight]:
                places[desc].useless_command(command[1])
        desc = new_desc
        print inv.text
        tscore = t.get_score()
        if tscore is not None:
            global score
            global max_score
            global possible_score
            (score, possible_score) = tscore
            max_score = max(max_score, score)
            print("Score:", score, "Possible score:", possible_score)
        else:
            break
    t.quit()
except KeyboardInterrupt:
    exit(0)
except:
    pass
scores.write("{3} {0} (max {2}) / {1}\n".format(score, possible_score, max_score, filename))
