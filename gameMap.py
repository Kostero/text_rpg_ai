import random
from pyrsistent import pvector, pmap, thaw, freeze
from Queue import Queue
from collections import defaultdict
import mycommands
import math
import cPickle

class GameMap:
    def __init__(self):
        self.descriptions = []
        self.ids = {}
        self.path = []
        self.moves = []
        self.path_actions = []
        self.path_scores = []
        self.group = []
        self.edges = {}
        self.actions = defaultdict(int)
        self.scores = defaultdict(float)
        self.updates_history = []
        self.dangerous_commands = defaultdict(set)
        self.dangerous_places = set()

    def get_id(self, desc):
        statements = desc.split('.')
        first = '' if len(statements) == 0 else statements[0]
        if not first in self.ids:
            self.ids[first] = len(self.descriptions)
            self.descriptions.append(set())
        id = self.ids[first]
        self.descriptions[id].add(desc)
        return id

    def add_to_path(self, desc, direction=None):
        self.path.append(self.get_id(desc))
        self.moves.append(direction)
        self.path_actions.append(0)
        self.path_scores.append(None)

    def action(self):
        self.path_actions[-1] += 1
        if len(self.group) == len(self.path_actions):
            self.actions[self.group[-1]] += self.path_actions[-1]

    def update_score(self, score):
        self.path_scores[-1] = score

    def clear_actions(self):
        self.path_actions = [0 for _ in self.path_actions]
        self.actions.clear()
    
    def useless(self):
        return len(self.updates_history) >= 5 and min(self.updates_history[-5:]) > 60

    def break_path(self):
        if self.moves != []:
            self.moves[-1] = None

    def add_tail(self, edges, group, actions, scores):
        for i in range(len(group), len(self.path)):
            if i == 0:
                group.append(0)
                edges[0] = {}
                actions[0] = self.path_actions[0]
                continue
            last = group[-1]
            if self.moves[i] is None or self.moves[i] not in edges[last]:
                groups = { group[j] for j, x in enumerate(self.path[:i]) if x == self.path[i] }
                back = mycommands.get_opposite_command(self.moves[i])
                if back is not None:
                    groups_filtered = filter(lambda x: back in edges[x] and edges[x][back] == last, groups)
                    if len(groups_filtered) != 0:
                        groups = groups_filtered
                if len(groups) == 0:
                    groups.add(i)
                    edges[i] = {}
                group.append(random.choice(list(groups)))
                if self.moves[i] is not None:
                    edges[last][self.moves[i]] = group[-1]
                    #if back not in edges[group[-1]]:
                    #    edges[group[-1]][back] = last
            elif self.path[edges[last][self.moves[i]]] == self.path[i]:
                group.append(group[edges[last][self.moves[i]]])
            else:
                return False
            actions[group[-1]] += self.path_actions[i]
            if self.path_scores[i] is not None:
                scores[group[-1]] = self.path_scores[i]
        return True

    def update_tail(self):
        if not self.add_tail(self.edges, self.group, self.actions, self.scores):
            self.update()

    def update(self, randfunc=lambda: (random.random() + 1)):
        n = len(self.path)
        if n == 0: return
        group = pvector(range(n))
        edges = freeze({ i: { m: i + 1 } if m is not None else {} for i, m in enumerate(self.moves[1:])})
        edges = edges.set(n - 1, pmap())
        edges_all = [{} for i in range(len(self.descriptions))]
        for k, v in edges.iteritems():
            edges_all[self.path[k]].update(v)
        consistent = set(range(len(self.descriptions)))
        for k, v in edges.iteritems():
            if self.path[k] not in consistent:
                continue
            for label, u in v.iteritems():
                if edges_all[self.path[k]][label] != u:
                    consistent.remove(self.path[k])
                    break
        items = freeze({ i: [i] for i in range(n) })

        def merge(a, b):
            if e_group[a] == e_group[b]:
                return True
            if self.path[a] != self.path[b]:
                return False
            ga = e_group[a]
            gb = e_group[b]
            if len(e_items[ga]) < len(e_items[gb]):
                ga, gb = gb, ga
            for i in e_items[gb]:
                e_group[i] = ga
            e_items[ga] += e_items[gb]
            del e_items[gb]
            merges = []
            for k, v in e_edges[gb].iteritems():
                if k in e_edges[ga]:
                    merges.append((v, e_edges[ga][k]))
            e_edges[ga] += e_edges[gb]
            del e_edges[gb]
            for a, b in merges:
                if not merge(a, b):
                    return False
            return True

        consistent_pairs = []
        inconsistent_pairs = []
        path_length = [1] * n
        for i in reversed(range(n-1)):
            if self.moves[i+1] is not None:
                path_length[i] += path_length[i+1]
        for i, a in enumerate(self.path):
            for j, b in enumerate(self.path[i+1:]):
                if a == b:
                    if a in consistent:
                        consistent_pairs.append((i, i + j + 1))
                    else:
                        inconsistent_pairs.append((i, i + j + 1))
        keyfunc = lambda (a, b): -(path_length[a] + path_length[b]) * randfunc()
        consistent_pairs.sort(key=keyfunc)
        inconsistent_pairs.sort(key=keyfunc)
        for a, b in consistent_pairs + inconsistent_pairs:
            if group[a] == group[b]:
                continue
            e_group = group.evolver()
            e_edges = edges.evolver()
            e_items = items.evolver()
            if merge(a, b):
                group = e_group.persistent()
                edges = e_edges.persistent()
                items = e_items.persistent()
        group = thaw(group)
        edges = thaw(edges)
        actions = defaultdict(int)
        scores = defaultdict(float)
        for g, a, s in zip(group, self.path_actions, self.path_scores):
            actions[g] += a
            if s is not None:
                scores[g] = s
        for u, e in edges.iteritems():
            for l, v in e.items():
                v = group[v]
                e[l] = v
                #bl = mycommands.get_opposite_command(l)
                #if bl is not None and bl not in edges[v]:
                #    edges[v][bl] = u
        self.group = group
        self.edges = edges
        self.actions = actions
        self.scores = scores
        self.updates_history.append(len(self.edges))
    
    def find_path(self):
        start = self.group[-1]
        prev = { start: None }
        dist = { start: 0 }
        q = Queue()
        q.put_nowait(start)
        while not q.empty():
            v = q.get_nowait()
            for l, u in self.edges[v].iteritems():
                if l not in self.dangerous_commands[self.path[v]] and \
                     u not in self.dangerous_places and u not in prev:
                    prev[u] = (v, l)
                    dist[u] = dist[v] + 1
                    q.put_nowait(u)
        best, _ = min(dist.items(), key=lambda (k, v):
            random.uniform(0.5, 1) * (2 * v + self.actions[k]) / (self.scores[k] + 1))
        path = [(best, None)]
        while prev[best] != None:
            path.append(prev[best])
            best = prev[best][0]
        path.reverse()
        return path

    def matches_path(self, text, nr):
        return self.get_id(text) == self.path[nr]

    def print_all(self):
        print
        print 'Places:'
        for i, j in enumerate(self.group):
            if i == j:
                print '{0}: {1}'.format(i, list(self.descriptions[self.path[i]])[0])
                print self.actions[i], 'actions'
                print 'score:', self.scores[i]
        print 'Edges:'
        for a, l in self.edges.iteritems():
            print a, '->', { k: self.group[v] for k, v in l.iteritems() }
    
    def get_description(self, id):
        return list(self.descriptions[self.path[id]])[0]

    def dangerous_command(self, place, command):
        self.dangerous_commands[self.get_id(place)].add(command)

    def dangerous_place(self, place):
        self.dangerous_places.add(place)

    def save(self):
        out = open('gamemap.pkl', 'w')
        cPickle.dump(self, out)

if __name__ == '__main__':
    mp = GameMap()
    mp.add_to_path('1')
    mp.add_to_path('3', 'a')
    mp.add_to_path('4', 'd')
    mp.add_to_path('5', 'e')
    mp.action()
    mp.action()
    mp.action()
    mp.action()
    mp.add_to_path('4', 'f')
    mp.add_to_path('6', 'g')
    mp.action()
    mp.action()
    mp.action()
    mp.action()
    mp.add_to_path('3', 'h')
    mp.add_to_path('2', 'b')
    mp.add_to_path('4', 'c')
    mp.action()
    mp.action()
    mp.action()
    mp.action()
    mp.action()
    mp.update()
    print mp.edges
    print mp.group
    print mp.actions
    print mp.find_path()