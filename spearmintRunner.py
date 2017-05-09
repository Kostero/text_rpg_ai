#import sys
import os.path
#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import golovinAgent

path = os.path.dirname(__file__)

def main(job_id, params):
    filename = 'zork1.z5'
    directory = 'textplayer/games/'
    return golovinAgent.run(params, filename, directory)

print(main(20, {"FIGHT_MODE": "on"}))
