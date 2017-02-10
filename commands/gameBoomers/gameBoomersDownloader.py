from sys import argv
import BeautifulSoup as bs
import urllib2
import nltk
import nltk.data
import nltk.tree
from stat_parser import Parser
import re


parser = Parser()
letter = "?"


def getNodes(parent):
    for node in parent:
        if type(node) is nltk.Tree:
            if not getNodes(node):
                if node.label() == "VP":
                    # we want to remove some sentences describing
                    # environment
                    sentence = node.leaves()
                    if sentence[0].lower() not in ["is", "are", "'re", "can",
                                                   "'ll", "'s", "won't",
                                                   "should", "must", "will",
                                                   "makes", "might", "'d",
                                                   "if", "need", "says", "a",
                                                   "needs", "so", "do", "'ve",
                                                   "only", "the", "to"]:
                        if sentence[0].lower() in ['and', 'then']:
                            sentence = sentence[1:]
                        f = open("result/verbs"+letter, "a")
                        f.write(" ".join(sentence)+"\n")
                        f.close()
                        return True
            else:
                return True
    return False

regex = re.compile("[^a-zA-Z\']")


def parseCommands(site):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    print(site)
    response = urllib2.urlopen(site)
    html = response.read()
    soup = bs.BeautifulSoup(html)
    ps = soup.findAll('p')
    # sometimes paragraps are not neat
    ps = " ".join([p.getText() for p in ps])
    try:
        splitedSentences = tokenizer.tokenize(ps)
        for sentence in splitedSentences:
            sentence = regex.sub(' ', sentence)
            try:
                words = [word.strip()
                         for word in sentence.split()]
                words = filter(lambda x: x != "nbsp", words)
                if len(words) > 20:
                    continue
                else:
                    words = " ".join(words)
                tree = parser.parse(words)
                getNodes(tree)
            except Exception as e:
                print "ERR in parsing", e.message
            # tokens = nltk.word_tokenize(words)
            # tagged = nltk.pos_tag(tokens)
    except Exception as e:
        print "ERR in spliting", e.message
    return


def main():
    for aletter in argv[1]:
        if aletter == "#":
            global letter
            letter = "Number"
        else:
            global letter
            letter = aletter
        print "L", letter
        # dirty way to remove file
        f = open("result/verbs"+letter, "w")
        f.close()
        response = urllib2.urlopen('http://www.gameboomers.com/Walkthroughs/'
                                   '%swalkthroughs.html' % letter)
        html = response.read()
        soup = bs.BeautifulSoup(html)
        links = soup.findAll('a')
        for link in links:
            href = link['href']
            if 'wtcheats' in href:
                try:
                    parseCommands(href)
                except Exception as e:
                    print "ERR", e.message


if __name__ == "__main__":
    main()
