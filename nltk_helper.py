import nltk
import word2vec
import os

path = os.path.dirname(__file__)
if path == '':
    path = '.'

import json
with open('params.json') as jsonfile:
    params = json.load(jsonfile)

mode = os.environ["W2V"] if os.environ.has_key("W2V") else params["W2V"]
if type(mode) == list:
    mode = mode[0]

w2v = None
if mode == "books":
    w2v = word2vec.load(path+'/word2vec/data/vec.bin')
elif mode == "wiki":
    w2v = word2vec.load(path+'/word2vec/data/wiki.bin')
elif mode == "gn":
    w2v = word2vec.load(path+'/word2vec/data/googlenews.bin')
else:
    print("invalid mode for W2V")
    exit(1)

def get_similar_nouns(nouns, number=5):
    result = { n: (1, n) for n in nouns }
    for n in nouns:
        try:
            sim = w2v.cosine(n, n=number)
            for i, k in zip(*sim):
                w = w2v.vocab[i]
                if 'NN' in nltk.pos_tag([w])[0][1]:
                    if w in result:
                        result[w] = max(result[w], (k, n))
                    else: result[w] = (k, n)
        except:
            pass
    return result

def get_nouns(text):
    if type(text) == str:
        text =  nltk.word_tokenize(text)
    return [word.lower() for (word, tag) in nltk.pos_tag(text) if 'NN' in tag]

def get_nouns_carefully(text):
    if type(text) == str:
        text =  nltk.word_tokenize(text)
    return [word.lower() for (word, tag) in nltk.pos_tag(text) if 'NN' in tag or 'NN' in nltk.pos_tag([word])[0][1]]
