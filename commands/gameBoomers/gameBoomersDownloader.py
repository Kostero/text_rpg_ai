import BeautifulSoup as bs
import urllib2
import nltk
import nltk.data
import nltk.tree
from stat_parser import Parser


parser = Parser()


def getNodes(parent):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == "S":
                f = open("result/sentences", "a")
                f.write(" ".join(node.leaves())+"\n")
                f.close()
            if node.label() == "VP":
                f = open("result/verbs", "a")
                f.write(" ".join(node.leaves())+"\n")
                f.close()
            if node.label() == "NP":
                f = open("result/nouns", "a")
                f.write(" ".join(node.leaves())+"\n")
                f.close()

            getNodes(node)


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
            try:
                words = " ".join([word.strip()
                                  for word in sentence.split()])
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
    for fileName in ["sentences", "nouns", "verbs"]:
        # dirty way to remove file
        f = open("result/"+fileName, "w")
        f.close()

    for letter in list("QWERTYUIOPASDFGHJKLZXCVBNM")+["Number"]:
        print "L", letter
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
