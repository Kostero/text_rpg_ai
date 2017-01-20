import textplayer.textPlayer as tp
import random
import Queue

directions = ['east', 'west', 'south', 'north', 'southeast', 'southwest', 'northeast', 'northwest', 'up', 'down']
graph = {}

def move(direction):
    command = 'go ' + direction
    print command
    print t.execute_command(command)
    desc = look()
    global current_place
    if desc not in graph:
        graph[desc] = []
    current_place = graph[desc]
    return desc

def explore():
    place = current_place
    if explored(place): return
    d = directions[len(place)]
    move(d)
    place.append(current_place)

def explored(place):
    return len(place) == len(directions)

def to_nearest_unexplored(place):
    q = Queue.Queue()
    vis = {id(place)}
    for i, p in enumerate(place):
        if id(p) != id(place):
            vis.add(id(p))
            q.put((p, directions[i]))
    while not q.empty():
        p, k = q.get()
        if not explored(p):
            return k
        for pp in p:
            pt = id(p)
            if not (pt in vis):
                vis.add(pt)
                q.put((pp, k))

def look():
    return t.execute_command('look')

t = tp.TextPlayer('zork1.z5')
start_info = t.run()
print start_info
current_place = []
graph[look()] = current_place
while True:
    if not explored(current_place):
        explore()
    else:
        print look()
        d = to_nearest_unexplored(current_place)
        if d is None:
            break
        move(d)
    if t.get_score() is not None:
        (score, possible_score) = t.get_score()
        print("Score:", score, "Possible score:", possible_score)
    else:
        break
t.quit()
for p in graph.keys():
    print p
print len(graph)