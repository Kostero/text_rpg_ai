import textplayer.textPlayer as tp
import logger
import random
import sys
import os
import numpy as np

path = os.path.dirname(__file__)
if path != "":
    path += "/"

def parse_args():
    files = []
    args = {}
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            s = arg[2:].split('=')
            if len(s) == 1:
                s.append('true')
            args[s[0]] = s[1]
        else:
            files.append(arg)
    return files, args

def run(params, filename, directory, steps = 2000, quiet = False):

    try:
        for k, v in params.items():
            if type(v) == np.ndarray:
                params[k] = v[0]

        if not directory.endswith('/'):
            directory += '/'

        import json
        with open('params.json', 'w') as out:
            json.dump(params, out)

        scores = open(path+'scores', 'a')
        score = 0
        max_score = 0
        possible_score = 0

        t = tp.TextPlayer(filename, directory)
        start_info = t.run()

        from golovinAgent import GolovinAgent

        agent = GolovinAgent(t, start_info, params)

        if start_info is None:
            print 'start_info is None'
            t.quit()
            exit(0)
        logger.open_log(path, filename)
        noneCount = 0
        for i in range(steps):
            command, command_type, response, additional = agent.makeAction()
            if not quiet:
                print 'map size:', len(agent.map.edges)
                print agent.desc
                print agent.inv.text
                print command
                print response
            logger.log('description', agent.desc)
            logger.log('inventory', agent.inv.text)
            logger.log(command_type, command)
            logger.log('response', response)

            tscore = t.get_score()
            if tscore is not None:
                (score, possible_score) = tscore
                if score > max_score:
                    agent.save_path()
                max_score = max(max_score, score)
                if not quiet:
                    print("Score:", score, "Possible score:", possible_score)

                logger.log('score', str(score) + ' ' + str(possible_score))
                noneCount = 0
            else:
                noneCount += 1
                if noneCount > 10:
                    break

            if quiet:
                print '\r{0}: {1}%, score: {2} / {3}'.format(filename, (i+1) * 100 / steps, score, possible_score),

        if not quiet:
            agent.map.update()
            agent.map.print_all()
            for _ in range(5):
                agent.map.update()
                print 'number of places:', len(agent.map.edges)
            for k, v in agent.places.items():
                print k
                print 'score:', v.score()

        if score != max_score:
            agent.run_best_path()
            tscore = t.get_score()
            if tscore is not None:
                (score, possible_score) = tscore
                max_score = max(max_score, score)
                if not quiet:
                    print("Score:", score, "Possible score:", possible_score)

        t.quit()

    except IOError:
        if not quiet:
            print "IOError"
        pass

    scores.write("{3} {0} (max {2}) / {1}\n".format(score, possible_score, max_score, filename))
    if quiet:
        print '\r{0}: finished, score: {1} / {3}, max score: {2} / {3}'.format(filename,
            score, max_score, possible_score)
    else:
        print 'final score:', score
        print 'max score:', max_score

    return (score + max_score) / 2.0



def main():
    params = {
        # spearmint says
        "FIGHT_MODE": os.environ['FIGHT_MODE'] if os.environ.has_key("FIGHT_MODE") else "on",
        "SOURCES": os.environ["SOURCES"] if os.environ.has_key("SOURCES") else "all",
        "EXPLORING": os.environ["EXPLORING"] if os.environ.has_key("EXPLORING") else "map",
        "W2V":  os.environ["W2V"] if os.environ.has_key("W2V") else "books",
        "PLACE_TAKEN_LIMIT": 6,
        "PLACE_NOUN_BONUS": 3230.47485352,
        "PLACE_INIT_ACTIONS": 15,
        "PLACE_MOVE_ACTION_RATIO": 1,
        "PLACE_UNKNOWN_PENALTY": 68.0344727,
        "PLACE_FREQUENCY_EXPONENT": 0.39831543,
        "PLACE_SIMILAR_NOUNS_NUMBER": 10
    }

    default_args = {
        "path": "textplayer/games/",
        "quiet": "false",
        "steps": "2000"
    }
    files, args = parse_args()
    default_args.update(args)
    if len(files) != 1:
        print 'Usage: python golovinRunner.py [filename] [options]'
        print 'Options:'
        print '\t --path=[path to games folder]\t <- sets the path to folder with game file (textplayer/games/ by default)'
        print '\t --quiet\t <- prevents the agent from writing all the stuff'
        print '\t --steps=[number of steps]\t <- sets the number of steps (2000 by default)'
        sys.exit(0)
    filename = files[0]
    directory = path + default_args['path']
    for k, v in default_args.iteritems():
        if k in params:
            params[k] = v
    return run(params, filename, directory, steps=int(default_args['steps']),
                                    quiet=(default_args['quiet'] == 'true'))

if __name__ == "__main__":
    main()
