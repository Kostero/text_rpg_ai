import textplayer.textPlayer as tp
from logsAnalysis import parser
import sys
import random
import math

path = [x for k, x in parser.parse(sys.argv[2]) if 'command' in k]
directory = 'textplayer/games/' if len(sys.argv) < 4 else sys.argv[3]
filename = sys.argv[1]

def evaluate(path):
    t = tp.TextPlayer(sys.argv[1], directory)
    t.run()
    n = len(path)
    score = 0
    first = 0
    i = 0
    for i, value in enumerate(path):
        try:
            t.execute_command(value)
            got_score = t.get_score()
            if got_score is None:
                break
            new_score, possible_score = got_score
            if new_score != score:
                first = i
                score = new_score
            print '\r{0}: {1}%, score: {2} / {3}'.format(filename, (i+1) * 100 / n, score, possible_score),
        except IOError:
            break
    try:
        t.quit()
    except:
        pass
    return score, i

score = evaluate(path)[0]
fails = 5
initial_n = len(path)
i = 128

while i > 0:
    current_fails = 0
    print '\ndropping', i, 'random actions'
    while current_fails < fails:
        dropped = { random.randrange(len(path)) for _ in range(i) }
        new_path = [ x for (j, x) in enumerate(path) if j not in dropped ]
        try:
            new_score, pos = evaluate(new_path)
            new_path = new_path[:pos+1]
            if new_score >= score:
                print '\nreduced path length from', initial_n, 'to', len(new_path)
                path = new_path
                current_fails = 0
            else:
                current_fails += 1
        except IOError:
            print '\nPipe error'
    i /= 2
    fails += 1

print path
