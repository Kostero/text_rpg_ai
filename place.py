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
    move_action_ratio = 10
    Take, Move, Action, RunAway, Fight = range(5)
    fight_actions = ['attack', 'kill', 'fight', 'destroy', 'shoot', 'strike', 'hit', 'punch', 'kick']

    def __init__(self, text):
        self.text = text
        self.taken = 0
        self.actions = 0
        self.commands = []
        self.nouns = sorted({n for n in get_nouns(text) if n not in commands.directions}, key=descriptions.frequency)
        self.similar_nouns = get_similar_nouns(self.nouns)
        for sim, _ in self.similar_nouns.iteritems():
            if sim in commands.commands:
                self.commands += commands.commands[sim]
    
    def dangerous(self):
        return ' grue' in self.text

    def get_command(self, inv_nouns, moves):
        if self.dangerous():
            return (self.Move, self.RunAway)
        if self.taken < min(len(self.nouns), self.taken_limit):
            self.taken += 1
            return (self.Take, self.nouns[self.taken-1])
        if self.actions - self.init_actions > moves / self.move_action_ratio:
            return (self.Move, random.choice(commands.directions))
        options = []
        for i, com in enumerate(self.commands):
            score = 1.0
            for n in get_nouns(com):
                if n in self.similar_nouns:
                    (k, sim) = self.similar_nouns[n]
                    score *= k / float(descriptions.frequency(n))
                    com = com.replace(n, sim)
                elif n in inv_nouns:
                    (k, sim) = inv_nouns[n]
                    score *= k / float(descriptions.frequency(n))
                    com = com.replace(n, sim)
                else:
                    score = -1
                    break
                score *= self.noun_bonus
            if score > 0:
                options.append(((i, com), score))
        choice = weighted_choice(options)
        if choice is None:
            return (self.Move, random.choice(commands.directions))
        del self.commands[choice[0]]
        self.actions += 1
        for w in choice[1].split():
            if w in self.fight_actions:
                return (self.Fight, choice[1])
        return (self.Action, choice[1])