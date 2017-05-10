import mycommands
import descriptions
from gameMap import GameMap
import sys
import os
from functools import partial
from inventory import Inventory
from place import Place

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