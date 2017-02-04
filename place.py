import descriptions
import commands
import random
import nltk
from nltk_helper import get_nouns, get_similar_nouns

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
    noun_bonus = 100
    init_actions = 10
    move_action_ratio = 3
    unknown_penalty = 500.0
    Take, Move, Action, RunAway, Fight = range(5)

    def __init__(self, text):
        self.text = text
        self.taken = 0
        self.actions = 0
        self.commands = []
        self.fight_commands = []
        self.useless_commands = set()
        self.inventory_nr = 0
        self.nouns = sorted({n for n in get_nouns(text) if n not in commands.directions}, key=descriptions.frequency)
        self.similar_nouns = get_similar_nouns(self.nouns)
        self.directions = commands.directions[:]
        for sim, _ in self.similar_nouns.iteritems():
            if sim in commands.commands:
                self.commands += commands.commands[sim]
            if sim in commands.fight_commands:
                self.fight_commands += commands.fight_commands[sim]
    
    def dangerous(self):
        return ' grue' in self.text

    def get_command_from_list(self, commands, inv_nouns):
        options = []
        for i, com in enumerate(commands):
            score = 1.0
            for n in get_nouns(nltk.word_tokenize(com)[1:]):
                if n in self.similar_nouns:
                    (k, sim) = self.similar_nouns[n]
                    score *= k / float(descriptions.frequency(n))
                    com = com.replace(n, sim)
                elif n in inv_nouns:
                    (k, sim) = inv_nouns[n]
                    score *= k / float(descriptions.frequency(n))
                    com = com.replace(n, sim)
                else:
                    score /= self.unknown_penalty
                    break
                score *= self.noun_bonus
            if score > 0 and not com in self.useless_commands:
                options.append(((i, com), score))
        return weighted_choice(options)

    def get_command(self, inv_nouns, moves, inv_nr):
        if self.inventory_nr != inv_nr:
            self.inventory_nr = inv_nr
            self.useless_commands.clear()
        fight = self.get_command_from_list(self.fight_commands, inv_nouns)
        if fight is not None:
            del self.fight_commands[fight[0]]
            return (self.Fight, fight[1])
        if self.dangerous():
            return (self.Move, self.RunAway)
        if self.taken < min(len(self.nouns), self.taken_limit):
            self.taken += 1
            return (self.Take, self.nouns[self.taken-1])
        if self.actions - self.init_actions > moves / self.move_action_ratio:
            return self.random_move()
        choice = self.get_command_from_list(self.commands, inv_nouns)
        if choice is None:
            return self.random_move()
        del self.commands[choice[0]]
        self.actions += 1
        return (self.Action, choice[1])

    def random_move(self):
        return (self.Move, random.choice(commands.directions if len(self.directions) == 0 else self.directions))

    def useless_move(self, direction):
        try:
            del self.directions[self.directions.index(direction)]
        except:
            pass

    def useless_command(self, command):
        self.useless_commands.add(command)