import nltk
sentence = "I'm gonna build a wall and make Mexico pay for it!"
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
nouns = [word for (word, tag) in tagged if 'NN' in tag]
verbs = [word for (word, tag) in tagged if 'VB' in tag]
print verbs
