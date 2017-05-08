import textplayer.textPlayer as tp
import random
import descriptions
import sys
import os
import commands
from functools import partial
from inventory import Inventory
from place import Place
import gameMap

path = os.path.dirname(__file__)

def look():
    desc = t.execute_command('look')
    dot = desc.find('.')
    if dot != -1:
        first = desc[:dot]
        if all(x.isdigit() or len(x) < 2 for x in first.split()):
            desc = desc[dot+1:]
    for i in range(min(30, len(desc))):
        if desc[i].islower():
            if i == 0 or not desc[i-1].isalpha():
                first = [''] + desc[:i].split()
                desc = first[-1] + ' ' + desc[i:]
            break
    desc = desc.strip()
    descriptions.add(desc)
    return desc

def open_log():
    global log_file
    i = 0
    while True:
        newpath = path + '/logs/' + os.path.splitext(filename)[0] + '_' + str(i) + '.log'
        if not os.path.exists(newpath):
            break
        i += 1
    log_file = open(newpath, 'w')

def log(header, text):
    log_file.write('\\' + header + '\n')
    log_file.write(text.replace('\\', '_') + '\n')


def run(params, filename, directory):
    scores = open(path+'/scores', 'a')
    score = 0
    max_score = 0
    possible_score = 0
    print '\n' + filename,
    t = tp.TextPlayer(filename, directory)
    start_info = t.run()

    map = gameMap.GameMap()

    try:
        if start_info is None:
            print 'start_info is None'
            t.quit()
            exit(0)
        t.execute_command('verbose')
        t.execute_command('verbose')
        places = {}
        inv = Inventory(partial(t.execute_command, 'inventory'))
        moves = 0
        open_log()
        steps = 2000
        noneCount = 0
        #print start_info
        desc = look()
        map.add_to_path(desc)
        for i in range(steps):
            if desc not in places:
                places[desc] = Place(desc)
            command = places[desc].get_command(inv.content, moves, inv.nr)
            if command[0] == Place.Take:
                command_text = commands.get_take_command(command[1])
            elif command[0] == Place.Move:
                moves += 1
                if command[1] == Place.RunAway:
                    command_text = commands.get_back_command()
                else: command_text = commands.get_move_command(command[1])
            else:
                command_text = command[1]
            command_output = t.execute_command(command_text)
            #print desc
            #print inv.text
            #print command_text
            #print command_output
            log('description', desc)
            log('inventory', inv.text)
            log('command', command_text)
            log('response', command_output)
            if command[0] == Place.Take:
                inv_commands = inv.update()
                log('inventory', inv.text)
                for c in inv_commands:
                    #print c
                    command_output = t.execute_command(c)
                    log('inventory_command', c)
                    log('response', command_output)
            elif params["FIGHT_MODE"]=="on" and command[0] == Place.Fight:
                for j in range(6):
                    #print command[1]
                    command_output = t.execute_command(command[1])
                    #print command_output
                    log('fight_command', command[1])
                    log('response', command_output)
            new_desc = look()
            useless = False
            if new_desc == desc:
                if command[0] == Place.Move and not command_output.endswith(desc) and not desc.endswith(command_output):
                    places[desc].useless_move(command[1])
                    useless = True
                elif command[0] in [Place.Action, Place.Fight]:
                    places[desc].useless_command(command[1])
                    useless = True
            if not useless:
                map.add_to_path(new_desc, command[1] if command[0] == Place.Move else None)
            desc = new_desc
            tscore = t.get_score()
            if tscore is not None:
                (score, possible_score) = tscore
                max_score = max(max_score, score)
                #print("Score:", score, "Possible score:", possible_score)
                log('score', str(score) + ' ' + str(possible_score))
                noneCount = 0
            else:
                noneCount += 1
                if noneCount > 10:
                    break

            print '\r{0}: {1}%, score: {2} / {3}'.format(filename, (i+1) * 100 / steps, score, possible_score),

        t.quit()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print '\nexception:', e.__doc__, e.message
        t.quit()
    scores.write("{3} {0} (max {2}) / {1}\n".format(score, possible_score, max_score, filename))
    map.update()
    map.print_all()
    print(score)
    return score

def __main__():
    params = {"FIGHT_MODE" = "on"}
    filename = 'zork1.z5' if len(sys.argv) < 2 else sys.argv[1]
    directory = path + '/textplayer/games/' if len(sys.argv) < 3 else sys.argv[2]
    return run(params, filename, directory)
