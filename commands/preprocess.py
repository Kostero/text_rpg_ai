import nltk
from collections import Counter

def get_nouns(text):
    return [word.lower() for (word, tag) in nltk.pos_tag(text) if 'NN' in tag]

def save(commands, filename, min_freq=1):
    with open(filename, 'w') as f:
        for c, freq in commands.items():
            if len(c) == 0 or freq < min_freq: continue
            nouns = list(set(get_nouns(c)) - {c[0]})
            f.write('#'.join([' '.join(c)] + nouns + [str(freq)]) + '\n')

fight_actions = {'attack', 'kill', 'fight', 'shoot', 'punch'}


for mode in ["walkthroughs", "tutorials", "games", "commands", "all"]:
    files = []
    if mode in ["walkthroughs", "all"]:
        files += ['plover/downloadedCommands.txt']
        files += ['solutionarchive/downloadedCommands.txt']
    if mode in ["tutorials", "all"]:
        files += ["gameBoomers/result/verbs"+x for x in
                  list("QWERTYUIOPASDFGHJKLZXCVBNM")+["Number"]]
    if mode in ["games"]:
        files += ["textsParser/parsedCommands.txt"]
    if mode in ["commands", "all"]:
        files += ["commandsDigger/diggedCommands.txt"]
    output = 'preprocessedCommands_'+mode+'.txt'
    output_fight = 'preprocessedFightCommands_'+mode+'.txt'


    lines = []
    for file in files:
        try:
            with open(file, 'r') as f:
                lines += f.readlines()
        except:
            print file, "missing"

    lines = map(str.lower, lines)
    lines = map(lambda x: x.replace('#', ''), lines)
    lines = map(str.split, lines)
    lines = filter(lambda x: len(x) > 1 and len(x) < 6, lines)
    print "commands:", len(lines)
    for l in lines:
        for i, w in enumerate(l):
            if w == 'x':
                l[i] = 'examine'

    commands = Counter()
    fight_commands = Counter()

    for l in lines:
        commands[tuple(l)] += 1
        if any(map(fight_actions.__contains__, l)):
            fight_commands[tuple(l)] += 1

    print commands.most_common(20)
    print fight_commands.most_common(20)
    save(commands, output)
    save(fight_commands, output_fight, min_freq=4)
