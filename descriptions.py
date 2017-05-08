from collections import Counter
import os

path = os.path.dirname(__file__)

def _process(p):
    for token in p.split():
        if token.isalpha():
            _frequency[token.lower()] += 1

def add(place):
    place = place.strip()
    if place in places:
        return
    _process(place)
    places.add(place)
    _file.write(place + '\n')
    _file.flush()

def frequency(word):
    return _frequency[word]

_file = open(path+'/data/descriptions.txt', 'a+')
places = set(map(str.strip, _file.readlines()))
_frequency = Counter()

for p in places:
    _process(p)
