import sys
import re

places = ["noun", "OBJ", "creature", "topic", "ATTRIBUTE(1)",
          "inventory", "multi", "held", "showobj", "showverb",
          "multiheld", "multiinside"]

if len(sys.argv) < 4:
    sys.stderr.write("usage: randomRunner.py <routines> <words> <commands>\n")
    exit(1)
routines = open(sys.argv[1], "r")
words = open(sys.argv[2], "r")

W = []
for line in words:
    _words = filter(None, line.strip().split(" "))
    for word in _words:
        W.append(word)
words.close()

C = []
commands = open(sys.argv[3], "w")


def go(index, routine, fixedRoutine=[], used=0):
    if len(routine) == index:
        commands.write(" ".join(fixedRoutine)+"\n")
        return
    if routine[index] not in places:
        return go(index+1, routine, fixedRoutine+[routine[index]], used)
    if used == 0:
        for w in W:
            go(index+1, routine, fixedRoutine+[w], used+1)


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
        go(0, detRoutine)
routines.close()
commands.close()
