import mycommands
import descriptions
from gameMap import GameMap
import sys
import os
from functools import partial
from inventory import Inventory
from place import Place

if __name__ == '__main__':
    print 'To run the agent, use golovinRunner.py instead'
    sys.exit(0)

class GolovinAgent:

    def __init__(self, text_player, start_info, params):

        self.places = {}
        self.inv = Inventory(partial(text_player.execute_command, 'inventory'))
        self.t = text_player
        self.moves = 0
        self.map = GameMap()
        self.params = params
        self.commands_queue = []

        self.path = []

        text_player.execute_command('verbose')
        text_player.execute_command('verbose')

        self.desc = self.look()
        self.map.add_to_path(self.desc)

        self.commands_history = []

        Place.update_params(params)
        
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

    def follow_path(self):
        action = self.path[0][1]
        actionType = 'command'
        response = self.t.execute_command(action)
        new_desc = self.look()
        if self.map.get_id(new_desc) != self.path[1][0]:
            self.path = []
        if new_desc != self.desc or response.endswith(self.desc) or self.desc.endswith(response):
            self.map.add_to_path(new_desc)
        self.desc = new_desc
        del self.path[0]
        return action, actionType, response, 1

    #returns tuple (action, actionType, response, number of additional commands (such as look, inventory))
    def _makeAction(self):
        if self.commands_queue != []:
            command, commandType = self.commands_queue[-1]
            del self.commands_queue[-1]
            response = self.t.execute_command(command)
            return (command, commandType, response, 0)

        if len(self.path) > 1:
            return self.follow_path()

        if self.desc not in self.places:
            self.places[self.desc] = Place(self.desc)

        command = self.places[self.desc].get_command(self.inv.content, self.moves, self.inv.nr)
        if command[0] == Place.Take:
            command_text = mycommands.get_take_command(command[1])
        elif command[0] == Place.Move:
            self.moves += 1
            if command[1] == Place.RunAway:
                command_text = mycommands.get_back_command()
            elif command[1] == Place.Explore:
                self.map.update()
                self.path = self.map.find_path()
                return self.follow_path()
            else: command_text = mycommands.get_move_command(command[1])
        else:
            command_text = command[1]
            self.map.action()

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

    #returns tuple (action, actionType, response, number of additional commands (such as look, inventory))
    def makeAction(self):
        death_texts = ['you have died', 'you are dead', 'would you like to restart',
             'please give one of the answers above']
        current_place = self.desc
        action = self._makeAction()
        self.commands_history.append((action[0], current_place))
        response = action[2].lower()
        for text in death_texts:
            if text in response or text in self.desc:
                self.handle_death()
                break
        return action

    def handle_death(self):
        #print 'Golovin is dead :(\t restaring...'
        #print 'Last place:', self.commands_history[-1][1]
        #print 'Last command:', self.commands_history[-1][0]
        self.map.break_path()
        self.map.clear_actions()
        self.t.execute_command('restart')
        self.inv.update()
        for i, (command, place) in enumerate(reversed(self.commands_history)):
            if i >= Place.dangerous_count:
                break
            if place in self.places:
                self.places[place].possibly_dangerous_command(command, i)
        self.commands_history = []
        self.desc = self.look()
        self.map.add_to_path(self.desc)

        for place in self.places.itervalues():
            place.reset()
        Place.move_action_ratio += 1