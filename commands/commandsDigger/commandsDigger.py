import sys
import re

import nltk
import word2vec
from collections import defaultdict as dd

NOUNS = ["noun", "multiinside", "multi", "multiheld", "held", "creature",
         "topic", "special", "text", "multiexcept"]

w2v = word2vec.load('../../word2vec/data/vec.bin')

if len(sys.argv) < 3:
    sys.stderr.write("usage: commandsDigger.py <+routines> <-commands>\n")
    exit(1)
foundCommands = set()
routines = open(sys.argv[1], "r")
for line in routines:
    occs = re.findall('\".*?\"', line)
    for occ in occs:
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
        for i in range(len(detRoutine)):
            if detRoutine[i].lower() in NOUNS:
            #print(" ".join(detRoutine))
                for j in range(len(detRoutine)):
                    if i != j:
                        try:
                            sim = w2v.cosine(detRoutine[j], n=50)
                            for ix, k in zip(*sim):
                                counter[w2v.vocab[ix]] += k
                        except KeyError:
                            pass
                passing = list(reversed(sorted([(y, x) for (x, y) in counter.items()])))
                candidates = nltk.word_tokenize(" ".join([x for (_, x) in passing]))
                nouns = [word.lower() for (word, tag) in nltk.pos_tag(candidates) if 'NN' in tag or 'NN' in nltk.pos_tag([word])[0][1]]
                for noun in nouns[:10]:
                    #print(detRoutine, noun)
                    foundCommands.add(" ".join(detRoutine[:i]+[noun]+detRoutine[(i+1):]).replace("_", " "))
routines.close()

commands = open(sys.argv[2], "w")
for command in foundCommands:
    commands.write(command+"\n")
commands.close()
