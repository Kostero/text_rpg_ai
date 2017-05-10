#import sys
import os.path
#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import golovinRunner

path = os.path.dirname(__file__)

def main(job_id, params):
<<<<<<< HEAD
    filename = 'zork1.z5'
    directory = path + '/textplayer/games/'
    return golovinRunner.run(params, filename, directory)
=======
    directory = 'textplayer/games/'
    games = open("textplayer/max_scores.txt")
    scores = []
    for _ in range(2):
        line = games.readline()
        filename = line.strip().split(" ")[0]
        score = -0
        try:
            score = golovinAgent.run(params, filename, directory, job_id)
        except Exception as e:
            print "exception:", e.message
        scores.append(score)
        print filename, score
    games.close()
    positive = sum([1 for score in scores if score > 0])
    return positive * sum(scores)

print(main(None, {"FIGHT_MODE": "on"}))
>>>>>>> 4572a2218bb160d2acf959e82d10e35646428506
