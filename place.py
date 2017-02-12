import descriptions
import commands
import random
import nltk
import numpy as np
from collections import namedtuple
from nltk_helper import get_nouns, get_similar_nouns, get_nouns_carefully

def weighted_choice(options):
    if len(options) == 0:
        return None
    s = sum(zip(*options)[1])
    c = random.random() * s
    for i, (n, w) in enumerate(options):
        c -= w
        if c <= 0:
            options[i] = (n, w * 0.9)
            return n

class Place:
    taken_limit = 6
    noun_bonus = 500
    init_actions = 15
    move_action_ratio = 3
    unknown_penalty = 1500.0
    Take, Move, Action, RunAway, Fight = range(5)
    
    class Command:
        def __init__(self):
            self.items = []
            self.rep = []
            self.p = []
            self.options = None

    def __init__(self, text):
        self.text = text
        self.taken = 0
        self.actions = 0
        self.commands = self.Command()
        self.fight_commands = self.Command()
        self.useless_commands = set()
        self.inventory_nr = -1
        self.nouns = sorted({n for n in get_nouns_carefully(text) if n not in commands.directions}, 
                            key=descriptions.frequency)
        self.similar_nouns = get_similar_nouns(self.nouns)
        self.directions = commands.directions[:]
        for sim, _ in self.similar_nouns.iteritems():
            if sim in commands.commands:
                self.commands.items += commands.commands[sim]
            if sim in commands.fight_commands:
                self.fight_commands.items += commands.fight_commands[sim]
    
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
                    score *= self.noun_bonus * k / float(descriptions.frequency(n) + 1)
                    com = com.replace(n, sim)
                elif n in inv_nouns:
                    (k, sim) = inv_nouns[n]
                    score *= self.noun_bonus * k / float(descriptions.frequency(n) + 1)
                    com = com.replace(n, sim)
                elif allow_unknown:
                    score /= self.unknown_penalty
                else:
                    score = 0
                    break
            if com in self.useless_commands:
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
            if opt not in self.useless_commands:
                return opt

    def get_command(self, inv_nouns, moves, inv_nr):
        if self.inventory_nr != inv_nr:
            self.inventory_nr = inv_nr
            self.useless_commands.clear()
            self.update_commands(self.commands, inv_nouns)
            self.update_commands(self.fight_commands, inv_nouns, allow_unknown=False)
        '''fight = self._get_command(self.fight_commands, inv_nouns, allow_unknown=False)
        if fight is not None:
            return (self.Fight, fight)'''
        if self.dangerous():
            return (self.Move, self.RunAway)
        if self.taken < min(len(self.nouns), self.taken_limit):
            self.taken += 1
            return (self.Take, self.nouns[self.taken-1])
        if self.actions - self.init_actions > moves / self.move_action_ratio:
            return self.random_move()
        choice = self._get_command(self.commands, inv_nouns)
        if choice is None:
            return self.random_move()
        self.actions += 1
        return (self.Action, choice)

    def random_move(self):
        return (self.Move, random.choice(commands.directions if len(self.directions) == 0 else self.directions))

    def useless_move(self, direction):
        try:
            del self.directions[self.directions.index(direction)]
        except:
            pass

    def useless_command(self, command):
        self.useless_commands.add(command)