import nltk
import sys

if len(sys.argv) < 2:
    print 'Usage: python preprocess.py <in> <out>'

with open(sys.argv[1], 'r') as file:
    text = file.read().decode('utf8').lower()
tokens = nltk.word_tokenize(text)
text2 = u' '.join(tokens)
with open(sys.argv[2], 'w') as file:
    file.write(text2.encode('utf8'))
