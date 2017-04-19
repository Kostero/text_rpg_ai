def LCS(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C[-1][-1]

descriptions = []
ids = {}
title_ids = {}

def get_title(desc):
    if desc == '':
        return
    firstline = desc.split('\n')[0]
    if all(x not in firstline for x in '.!?:><'):
        return firstline

match_factor = 0.9
def id_from_descriptions(desc):
    a = desc.split()
    for i, s in enumerate(descriptions):
        for d in s:
            b = d.split()
            if LCS(a, b) >= min(len(a), len(b)) * match_factor:
                print 'similar strings:', LCS(a, b), desc, d
                return i

def get_id(desc):
    if not desc in ids:
        title = get_title(desc)
        if title is not None and title in title_ids:
            ids[desc] = title_ids[title]
        else:
            id = id_from_descriptions(desc)
            if id is None:
                id = len(descriptions)
                descriptions.append(set())
            if title is not None:
                title_ids[title] = id
            ids[desc] = id
    descriptions[ids[desc]].add(desc)
    return ids[desc]

def analyse():
    max_diff, min_nei, min_nearest_nei = 0, 1, 1
    for i, s1 in enumerate(descriptions):
        for s2 in descriptions[:i]:
            for d1 in s1:
                for d2 in s2:
                    w1, w2 = d1.split(), d2.split()
                    if len(w1) == 0 or len(w2) == 0:
                        continue
                    x = 1.0 * LCS(w1, w2) / min(len(w1), len(w2))
                    if x > 0.5:
                        print 'different:', x, d1, '\n', d2
                    max_diff = max(max_diff, x)
        slist = list(s1)
        for j, d1 in enumerate(slist):
            nearest = 0
            for d2 in slist[:j]:
                w1, w2 = d1.split(), d2.split()
                if len(w1) == 0 or len(w2) == 0:
                    continue
                x = 1.0 * LCS(w1, w2) / min(len(w1), len(w2))
                if x < 0.5:
                    print 'same:', x, d1, '\n', d2
                nearest = max(nearest, x)
                min_nei = min(min_nei, x)
            if j > 0:
                min_nearest_nei = min(min_nearest_nei, nearest)
    print 'most similar different places:', max_diff
    print 'least similar same places:', min_nei
    print 'least similar nearest neighbour:', min_nearest_nei