from sys import argv
import BeautifulSoup as bs
import urllib2
import nltk
import nltk.data
import nltk.tree
from stat_parser import Parser
import re
from time import sleep


parser = Parser()
letter = "?"


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
                                    f = open("result/verbs"+letter, "a")
                                    f.write(command+"\n")
                                    f.close()
                                    done = True
                    return done
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
                print(words)
                print(tree)
                print("--------------")
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
            codeletter = "0-9"
        else:
            global letter
            letter = aletter.upper()
            codeletter = letter+letter.lower()
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
            if 'wtcheats/pc' + codeletter in href:
                try:
                    parseCommands(href)
                except Exception as e:
                    print "ERR", e.message


if __name__ == "__main__":
    main()
