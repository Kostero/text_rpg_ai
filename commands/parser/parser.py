import sys
import nltk
import nltk.data
import nltk.tree
from stat_parser import Parser
import re


parser = Parser()


def getNodes(parent):
    for node in parent:
        if type(node) is nltk.Tree:
            if not getNodes(node):
                if node.label() == "VP":
                    # we want to remove some sentences describing
                    # environment
                    sentence = " ".join(node.leaves()).lower()
                    commands = re.split(
                        r';|\,|\.|\>|\band\b|\bor\b|\bthen\b', sentence)
                    done = False
                    for command in commands:
                        if re.match(r'^[a-zA-Z0-9\;\,\.\-\*\:\'\"\/\s]{1,80}$',
                                    command) \
                                and re.search(r'[a-zA-Z]', command):
                            tokens = nltk.word_tokenize(command)
                            if len(tokens) > 0 and len(tokens) <= 5:
                                tagged = nltk.pos_tag(tokens)
                                if tagged[0][1] not in \
                                        ["VBZ", "VBN", "VBD", "VBP", "VBG",
                                         "MD", "NNS", "DT", "JJ"]:
                                    print(command)
                                    done = True
                    return done
            else:
                return True
    return False


gameText = sys.argv[1]
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
with open(gameText, "r") as f:
    for line in f.readlines():
        splitted = line.strip().split(" ")
        #print(splitted)
        try:
            if '0' <= splitted[0][0] <= '9' and splitted[0][-1] == ':':
                line = " ".join(splitted[1:])
        except:
            pass
        tokenized =  tokenizer.tokenize(line.strip())
        for token in tokenized:
            #print "T", token.strip()
            token = token.strip().split()
            for i in range(len(token)-5):
                fragment = " ".join(token[i:i+5])
                try:
                    #print "F", fragment
                    tree = parser.parse(fragment.strip())
                    getNodes(tree)
                except:
                    pass
