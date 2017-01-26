import nltk

def _process(p):
    for token in nltk.word_tokenize(p):
        if token.isalpha():
            s = token.lower()
            if not s in _frequency:
                _frequency[s] = 0
            _frequency[s] += 1

def add(place):
    if place in places:
        return
    _process(place)
    places.add(place)
    _file.write(place + '\n')
    _file.flush()

def frequency(word):
    return _frequency[word] if word in _frequency else 0

_file = open('data/descriptions.txt', 'a+')
places = set(_file.readlines())
_frequency = {}

for p in places:
    _process(p)