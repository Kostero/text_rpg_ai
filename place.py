import mycommands
import descriptions
import random
import nltk
import numpy as np
import attention
import math
import mycommands
from collections import namedtuple, defaultdict, Counter
from nltk_helper import get_nouns, get_similar_nouns, get_nouns_carefully

class Place:
    taken_limit = 7
    noun_bonus = 2000
    init_actions = 15
    move_action_ratio = 7
    move_take_ratio = 50
    unknown_penalty = 500.0
    fight_mode = True
    game_map_mode = False
    dangerous_count = 5
    Take, Move, Action, RunAway, Explore, Fight = range(6)

    class Command:
        def __init__(self):
            self.items = []
            self.rep = []
            self.p = []
            self.options = None

    def __init__(self, text):
        self.text = text
        self.taken = 0
        self.taken_all = False
        self.actions = 0
        self.commands = self.Command()
        self.fight_commands = self.Command()
        self.useless_commands = set()
        self.dangerous_commands = set()
        self.inventory_nr = -1
        self.weights = defaultdict(lambda: 0.5, attention.compute_weights(text))
        self.nouns = sorted({n for n in get_nouns_carefully(text) if n not in mycommands.directions},
                            key=lambda x: math.sqrt(descriptions.frequency(x) + 2) / self.weights[x])
        self.similar_nouns = get_similar_nouns(self.nouns)
        self.directions = mycommands.directions[:]
        for sim, _ in self.similar_nouns.iteritems():
            if sim in mycommands.commands:
                self.commands.items += mycommands.commands[sim]
            if sim in mycommands.fight_commands:
                self.fight_commands.items += mycommands.fight_commands[sim]
        self.dangerous_counter = [Counter() for i in range(self.dangerous_count)]

    def reset(self):
        self.taken = 0
        self.taken_all = False
        self.actions = 0
        self.inventory_nr = -1

    def dangerous(self):
        return ' grue' in self.text

    def random_choice(self, rep, p, k):
        return list(np.random.choice(rep, size=k, p=p))

    def update_commands(self, commands, inv_nouns, allow_unknown=True):
        p = np.zeros(len(commands.items))
        rep = []
        for i, c in enumerate(commands.items):
            score = c.freq
            com = c.text
            for n in c.nouns:
                if n in self.similar_nouns:
                    (k, sim) = self.similar_nouns[n]
                    score *= self.noun_bonus * k * self.weights[n] / math.sqrt(descriptions.frequency(n) + 2)
                    com = com.replace(n, sim)
                elif n in inv_nouns:
                    (k, sim) = inv_nouns[n]
                    score *= self.noun_bonus * k * self.weights[n] / math.sqrt(descriptions.frequency(n) + 2)
                    com = com.replace(n, sim)
                elif allow_unknown:
                    score /= self.unknown_penalty
                else:
                    score = 0
                    break
            if com in self.useless_commands or com in self.dangerous_commands:
                score = 0
            rep.append(com)
            p[i] = score
        options = None
        s = p.sum()
        if s > 0.0000001:
            p /= s
            try:
                options = self.random_choice(rep, p, 50)
            except:
                pass
        commands.p = p
        commands.rep = rep
        commands.options = options

    def _get_command(self, commands, inv_nouns, allow_unknown=True):
        for i in range(5):
            if commands.options == None:
                return
            if commands.options == []:
                self.update_commands(commands, inv_nouns)
                continue
            opt = commands.options[-1]
            del commands.options[-1]
            if opt not in self.useless_commands and opt not in self.dangerous_commands:
                return opt

    def get_command(self, inv_nouns, moves, inv_nr):
        if self.inventory_nr != inv_nr:
            self.inventory_nr = inv_nr
            self.useless_commands.clear()
            self.update_commands(self.commands, inv_nouns)
            self.update_commands(self.fight_commands, inv_nouns, allow_unknown=False)
        if self.fight_mode:
            fight = self._get_command(self.fight_commands, inv_nouns, allow_unknown=False)
            if fight is not None:
                return (self.Fight, fight)
        if self.dangerous():
            return (self.Move, self.RunAway)
        if self.taken < min(len(self.nouns), max(self.taken_limit, moves / self.move_take_ratio)):
            self.taken += 1
            return (self.Take, self.nouns[self.taken-1])
        if not self.taken_all:
            self.taken_all = True
            return (self.Take, 'all')
        if self.actions - self.init_actions > moves / self.move_action_ratio:
            return self.make_move()
        choice = self._get_command(self.commands, inv_nouns)
        if choice is None:
            return self.make_move()
        self.actions += 1
        return (self.Action, choice)

    def make_move(self):
        if self.game_map_mode:
            if len(self.directions) == 0:
                return (self.Move, self.Explore)
            index = random.randrange(len(self.directions))
            result = self.directions[index]
            del self.directions[index]
            return (self.Move, result)

        return (self.Move, random.choice(mycommands.directions if len(self.directions) == 0 else self.directions))

    def useless_move(self, direction):
        try:
            del self.directions[self.directions.index(direction)]
        except:
            pass

    def useless_command(self, command):
        self.useless_commands.add(command)

    def dangerous_command(self, command):
        #print 'Dangerous command!!!', command
        #print 'in: ', self.text
        self.dangerous_commands.add(command)
        if command.startswith('go '):
            self.useless_move(command[3:])

    def possibly_dangerous_command(self, command, nr):
        if nr < self.dangerous_count:
            self.dangerous_counter[nr][command] += 1
            if self.dangerous_counter[nr][command] > nr:
                self.dangerous_command(command)