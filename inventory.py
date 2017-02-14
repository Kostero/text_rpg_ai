from nltk_helper import get_nouns, get_nouns_carefully, get_similar_nouns
import nltk
import commands
import random
import numpy as np

class Inventory:
    noun_bonus = 5
    commands_limit = 20
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
        com = commands.commands[word]
        result = []
        for text, nouns, freq in com:
            for w in text.split():
                if w in self.blacklist:
                    break
            else:
                text = text.replace(word, rep)
                score = k ** 2
                score *= freq
                for n in nouns:
                    if n != word:
                        if n in self.content:
                            (lk, w) = self.content[n]
                            text = text.replace(n, w)
                            score *= (lk ** 2) * self.noun_bonus
                        else: 
                            score /= self.unknown_penalty
                if score > 0:
                    result.append((score, text))
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
            return reversed([x for (_, x) in result[:self.commands_limit]])
        return []