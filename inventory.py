from nltk_helper import get_nouns, get_nouns_carefully, get_similar_nouns
import nltk
import commands
import random

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

class Inventory:
    noun_bonus = 5
    commands_limit = 10
    unknown_penalty = 100.0
    blacklist = {'drop', 'leave', 'throw'}

    def __init__(self, update_command):
        self.text = ''
        self.nr = 0
        self.nouns = {}
        self.content = {}
        self.update_command = update_command
        self.update()

    def get_commands(self, word, k, rep):
        if word not in commands.commands:
            return []
        com = [c.replace(word, rep) for c in commands.commands[word]]
        result = []
        for c in com:
            words = nltk.word_tokenize(c)
            for w in words:
                if w in self.blacklist:
                    break
            else:
                score = k ** 2
                for n in get_nouns(words[1:]):
                    if n != rep:
                        if n in self.content:
                            (lk, w) = self.content[n]
                            c = c.replace(n, w)
                            score *= (lk ** 2) * self.noun_bonus
                        else: 
                            score /= self.unknown_penalty
                if score > 0:
                    result.append((score, c))
        return result

    def update(self):
        text = self.update_command()
        if text != self.text:
            self.nr += 1
            self.text = text
            commands = []
            old_content = self.content
            nouns = get_nouns_carefully(self.text)
            self.content = get_similar_nouns(nouns)
            for s, (k, w) in self.content.iteritems():
                if s not in old_content:
                    commands += self.get_commands(s, k, w)
            for n in nouns:
                if n not in self.nouns:
                    commands += self.get_commands(n, 1.0, n)
            self.nouns = set(nouns)
            result = sorted(set(commands), key=lambda (x, _): -x)
            return [x for (_, x) in result[:self.commands_limit]]
        return []