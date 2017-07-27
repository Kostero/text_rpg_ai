from sys import argv
import BeautifulSoup as bs
import urllib2
import nltk
import nltk.data
import nltk.tree
import re
from time import sleep


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
                f = open("texts/verbs"+letter, "a")
                f.write(" ".join(words)+"\n")
                f.close()
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
        f = open("texts/verbs"+letter, "w")
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
