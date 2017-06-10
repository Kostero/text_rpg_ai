import sys
import re

import nltk
import numpy as np
import word2vec
from collections import defaultdict as dd

NOUNS = ["noun", "multiinside", "multi", "multiheld", "held", "creature",
         "topic", "special", "text", "multiexcept", "obj"]

w2v = word2vec.load('../../word2vec/data/vec.bin')

if len(sys.argv) < 4:
    sys.stderr.write("usage: commandsDigger.py <+routines> <+words> <-commands>\n")
    exit(1)
foundCommands = set()
routines = open(sys.argv[1], "r")
WORDS = []
words = open(sys.argv[2], "r")
for word in words.readlines():
    word = word.strip()
    if len(word) != 0 and word[0] != "(":
        WORDS.append(word.lower())
words.close()
#print(WORDS)
for line in routines:
    occs = re.findall('\".*?\"', line)
    for occ in occs:
        if "[parse" in occ:
            continue
        routine = occ[1:-1].split(" ")
        detRoutine = []
        i = 0
        while i < len(routine):
            if routine[i] == '/':
                i += 2
            else:
                detRoutine.append(routine[i])
                i += 1
        counter = dd(float)
        ile = sum([1 for word in detRoutine if word.lower() in NOUNS])
        if ile == 0:
            foundCommands.add(" ".join(detRoutine))
        if ile != 1:
            continue
        prop = dd(float)
        for i in range(len(detRoutine)):
            if detRoutine[i].lower() in NOUNS:
                for j in range(len(detRoutine)):
                    if i != j:
                        for word in WORDS:
                            try:
                                prop[word] += np.dot(w2v[detRoutine[j]], w2v[word])
                            except KeyError:
                                pass
                passing = list(reversed(sorted([(y, x) for (x, y) in prop.items()])))
                nouns = [x.replace("_", " ") for (_, x) in passing]
                for noun in nouns[:5]:
                    #print(detRoutine, noun)
                    foundCommands.add(" ".join(detRoutine[:i]+[noun]+detRoutine[(i+1):]).replace("_", " "))
routines.close()
words.close()

commands = open(sys.argv[3], "w")
for command in foundCommands:
    commands.write(command+"\n")
commands.close()
