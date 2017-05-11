#import sys
import os.path
#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import golovinRunner

path = os.path.dirname(__file__)

def main(job_id, params):
    directory = 'textplayer/games/'
    games = open("textplayer/max_scores_selected.txt")
    scores = []
    for _ in range(20):
        line = games.readline()
        [filename, max_score] = line.strip().split(" ")
        score = -0
        try:
            score = golovinRunner.run(params, filename, directory, 2000, True)
        except Exception as e:
            print "exception:", e.message
        #except None:
        #    pass
        if score > 0:
            score += 0.2
        scores.append(score / float(max_score))
    games.close()
    return 1.2 + -(1.0*sum(scores)/len(scores))

#print(main(None, {"FIGHT_MODE": "on", "SOURCES": "all"}))
