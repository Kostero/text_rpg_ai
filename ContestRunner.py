from subprocess import Popen, PIPE, STDOUT
from random import randint
import binascii
import os
import fcntl

from golovinAgent import GolovinAgent

def startZplet(jardir, gamedir):
    if(gamedir != ''):
        p = Popen(['java', '-jar', jardir, 'ieeecig.advent.IOAgent', gamedir], stdin=PIPE, stdout=PIPE)
    else:
        p = Popen(['java', '-jar', jardir, 'ieeecig.advent.IOAgent'], stdin=PIPE, stdout=PIPE)
    return (readNarrative(p),p)

def postCommand(p, command):
    print("Response: " + command)
    p.stdin.write(command + "\n")
    p.stdin.flush()
    return readNarrative(p)

def readNarrative(p):
    narrative=""
    cont = True
    while cont:
        for line in iter(p.stdout.readline, ''):
            if(line.startswith("BREAK-NARRATIVE")):
                print("BREAK")
                cont = False
                break
            narrative = narrative + line + "\n"
    print "Narrative: ", narrative
    return narrative

class ContestTextPlayer:

    def __init__(self, p):
        self.p = p

    def execute_command(self, command):
        return postCommand(self.p, command)


print("Booting Z Machine...")
(narrative, p) = startZplet('Example Project/lib3rd/ieee-cig-advent-1.5.jar','resources/monkey-and-bananas-v1.z8')
print("Z Machine Launched")
ct = ContestTextPlayer(p)

import json
with open('params.json', 'r') as ins:
    params = json.load(ins)


g = GolovinAgent(ct, narrative, params)
print("Golovin Launched")
while True:
    g.makeAction()
