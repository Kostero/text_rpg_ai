import sys
import os.path
#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import golovinRunner

path = os.path.dirname(__file__)

def main(job_id, params):
    directory = 'textplayer/games/'
    games = open("textplayer/max_scores_selected.txt", 'r')
    scores = []
    for line in games.readlines():
        words = line.split()
        print line
        if len(words) != 2: continue
        filename, max_score = words
        score = 0
        try:
            score = golovinRunner.run(params, filename, directory, steps=1000, quiet=True)
        except Exception as e:
            print "exception:", e.message
        #except None:
        #    pass
        scores.append(score / float(max_score))
    games.close()
    positive = sum([1 for score in scores if score > 0])
    return -(positive * 0.2 + sum(scores))

#print(main(None, {"FIGHT_MODE": "on"}))