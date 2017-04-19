descriptions = []
ids = {}

def get_id(desc):
    statements = desc.split('.')
    first = '' if len(statements) == 0 else statements[0]
    if not first in ids:
        ids[first] = len(descriptions)
        descriptions.append(set())
    id = ids[first]
    descriptions[id].add(desc)
    return id