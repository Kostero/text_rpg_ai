import mycommands
import descriptions
<<<<<<< HEAD
from gameMap import GameMap
=======
import sys
import os
import mycommands
from functools import partial
>>>>>>> 4572a2218bb160d2acf959e82d10e35646428506
from inventory import Inventory
from place import Place
from functools import partial


class GolovinAgent:

    def __init__(self, text_player, start_info, params):

        self.places = {}
        self.inv = Inventory(partial(text_player.execute_command, 'inventory'))
        self.t = text_player
        self.moves = 0
        self.map = GameMap()
        self.params = params
        self.commands_queue = []

        text_player.execute_command('verbose')
        text_player.execute_command('verbose')

<<<<<<< HEAD
        self.desc = self.look()
        self.map.add_to_path(self.desc)
        
    def look(self):
        desc = self.t.execute_command('look')
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

    #returns tuple (action, actionType, response, number of additional commands (such as look, inventory))
    def makeAction(self):
        if self.commands_queue != []:
            command, commandType = self.commands_queue[-1]
            del self.commands_queue[-1]
            response = self.t.execute_command(command)
            return (command, commandType, response, 0)

        if self.desc not in self.places:
            self.places[self.desc] = Place(self.desc)

        command = self.places[self.desc].get_command(self.inv.content, self.moves, self.inv.nr)
        if command[0] == Place.Take:
            command_text = mycommands.get_take_command(command[1])
        elif command[0] == Place.Move:
            self.moves += 1
            if command[1] == Place.RunAway:
                command_text = mycommands.get_back_command()
            else: command_text = mycommands.get_move_command(command[1])
        else:
            command_text = command[1]

        additional_commands = 0

        response = self.t.execute_command(command_text)
        if command[0] == Place.Take:
            inv_commands = self.inv.update()
            additional_commands += 1
            self.commands_queue += zip(inv_commands, ['inventory_command'] * len(inv_commands))
        elif command[0] == Place.Fight:
            self.commands_queue += [(command[1], 'fight_command')] * 6
            self.places[self.desc].useless_command(command[1])
            return (command_text, 'fight_command', response, 0)
        new_desc = self.look()
        additional_commands += 1
        useless = False
        if new_desc == self.desc:
            if command[0] == Place.Move and not response.endswith(self.desc) and \
                 not self.desc.endswith(response):
                self.places[self.desc].useless_move(command[1])
                useless = True
            elif command[0] != Place.Move:
                useless = True
                if command[0] == Place.Action:
                    self.places[self.desc].useless_command(command[1])
        if not useless:
            self.map.add_to_path(new_desc, command_text if command[0] == Place.Move else None)
        self.desc = new_desc
        return (command_text, 'command', response, additional_commands)
=======
def run(params, filename, directory, job_id = None):
    global path
    path = os.path.dirname(__file__)
    if path != "":
        path += "/"
    scores = open(path+'scores', 'a')
    score = 0
    max_score = 0
    possible_score = 0
    #print '\n' + filename,
    try:
        global t
        t = tp.TextPlayer(filename, directory)
        start_info = t.run()

        map = gameMap.GameMap()
        if start_info is None:
            print 'start_info is None'
            t.quit()
            exit(0)
        t.execute_command('verbose')
        t.execute_command('verbose')
        places = {}
        inv = Inventory(partial(t.execute_command, 'inventory'))
        moves = 0
        open_log(filename)
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
                command_text = mycommands.get_take_command(command[1])
            elif command[0] == Place.Move:
                moves += 1
                if command[1] == Place.RunAway:
                    command_text = mycommands.get_back_command()
                else: command_text = mycommands.get_move_command(command[1])
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
            if job_id is None:
                print '\r{0}: {1}%, score: {2} / {3}'.format(filename, (i+1) * 100 / steps, score, possible_score),

        t.quit()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print '\nexception:', e.__doc__, e.message
        try:
            t.quit()
        except:
            pass
        #print(score)
        return score
    scores.write("{3} {0} (max {2}) / {1}\n".format(score, possible_score, max_score, filename))
    #map.update()
    #map.print_all()
    #print(score)
    return score

def main():
    params = {
        "FIGHT_MODE": "on",
        "SOURCES": "all",
        "EXPLORING": "random",
    }
    filename = 'zork1.z5' if len(sys.argv) < 2 else sys.argv[1]
    directory = os.path.dirname(__file__) + 'textplayer/games/' if len(sys.argv) < 3 else sys.argv[2]
    return run(params, filename, directory)
>>>>>>> 4572a2218bb160d2acf959e82d10e35646428506

    def handle_death(self):
        self.map.break_path()