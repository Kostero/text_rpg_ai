import random
from pyrsistent import pvector, pmap, thaw, freeze

class GameMap:
    def __init__(self):
        self.descriptions = []
        self.ids = {}
        self.path = []
        self.moves = []
        self.group = []
        self.edges = {}

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
        self.group.append(-1)
    
    def break_path(self):
        if self.moves != []:
            self.moves[-1] = None

    def update(self):
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
        for i, a in enumerate(self.path):
            for j, b in enumerate(self.path[i+1:]):
                if a == b:
                    if a in consistent:
                        consistent_pairs.append((i, i + j + 1))
                    else:
                        inconsistent_pairs.append((i, i + j + 1))
        random.shuffle(consistent_pairs)
        random.shuffle(inconsistent_pairs)
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
        self.group = thaw(group)
        self.edges = thaw(edges)

    def print_all(self):
        print
        print 'Places:'
        for i, j in enumerate(self.group):
            if i == j:
                print '{0}: {1}'.format(i, list(self.descriptions[self.path[i]])[0])
        print 'Edges:'
        for a, l in self.edges.iteritems():
            print a, '->', { k: self.group[v] for k, v in l.iteritems() }
    

if __name__ == '__main__':
    mp = GameMap()
    mp.add_to_path('a')
    mp.add_to_path('b', 'x')
    mp.add_to_path('c', 'x')
    mp.add_to_path('a', 'x')
    mp.add_to_path('b', 'x')
    mp.add_to_path('b', 'x')
    mp.update()
    mp.print_all()