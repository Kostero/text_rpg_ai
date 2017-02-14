import textplayer.textPlayer as tp
import descriptions
import nltk
import attention
import sys

def look():
    desc = t.execute_command('look')
    dot = desc.find('.')
    if dot != -1:
        first = desc[:dot]
        if all(x.isdigit() or len(x) < 2 for x in first.split()):
            desc = desc[dot+1:]
    for i in range(min(30, len(desc))):
        if desc[i].islower() and (i == 0 or not desc[i-1].isalpha()):
            first = [''] + desc[:i].split()
            desc = first[-1] + ' ' + desc[i:]
            break
    descriptions.add(desc)
    return desc

def least_common(desc, k):
    tokens = nltk.word_tokenize(desc)
    tagged = nltk.pos_tag(tokens)
    nouns = [word.lower() for (word, tag) in tagged if 'NN' in tag]
    freq = list({(descriptions.frequency(word), word) for word in nouns})
    freq.sort()
    freq = freq[:min(len(freq), k)]
    return freq

def get_command():
    print '\n>>',
    return raw_input()

t = tp.TextPlayer('zork1.z5' if len(sys.argv) < 2 else sys.argv[1])
start_info = t.run()
print start_info
while True:
    command = get_command()
    if command == 'look':
        desc = look()
        print desc
        att = dict (attention.compute_weights(desc))
        for l in least_common(desc, 20):
            print l[0], l[1], (att[l[1]] if l[1] in att else 1.5) ** 3
    else:
        command_output = t.execute_command(command)
        print command_output
    
    if t.get_score() is not None:
        (score, possible_score) = t.get_score()
        print("Score:", score, "Possible score:", possible_score)
    else:
        break
t.quit()
