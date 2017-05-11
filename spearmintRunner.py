#import sys
import os.path
#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import golovinRunner

path = os.path.dirname(__file__)

def main(job_id, params):
    directory = 'textplayer/games/'
    games = open("textplayer/max_scores.txt")
    scores = []
    for _ in range(2):
        line = games.readline()
        filename = line.strip().split(" ")[0]
        score = -0
        try:
            score = golovinRunner.run(params, filename, directory, 2000, True)
        except Exception as e:
            print "exception:", e.message
        #except None:
        #    pass
        scores.append(score / float(max_score))
    games.close()
    positive = sum([1 for score in scores if score > 0])
    return -(positive * 0.2 + sum(scores))

print(main(None, {"FIGHT_MODE": "on", "SOURCES": "all"}))
