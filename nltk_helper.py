import nltk
import word2vec

w2v = word2vec.load('word2vec/data/vec.bin')

def get_similar_nouns(nouns):
    result = { n: (1, n) for n in nouns }
    for n in nouns:
        try:
            sim = w2v.cosine(n)
            for i, k in zip(*sim):
                w = w2v.vocab[i]
                if 'NN' in nltk.pos_tag([w]):
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