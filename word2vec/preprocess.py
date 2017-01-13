import sys

def preprocess(line):
    line = line.decode('utf8').lower()
    tokens = []
    last = u''
    for c in line:
        if c in u"'-" or c.isalpha():
            last += c
        else:
            if last != u'': tokens.append(last)
            last = u''
            if not c.isspace():
                tokens.append(c)
        if len(last) >= 2 and last[-2:] == u"''":
            last = last.rstrip("'")
            if last != u'': tokens.append(last)
            tokens.append(u"''")
            last = u''
            
    if last != u'': tokens.append(last)
    return u' '.join(tokens).encode('utf8')

if len(sys.argv) < 2:
    print 'Usage: python preprocess.py <in> <out>'
    exit(0)

if sys.argv[1] == sys.argv[2]:
    print 'in and out should be different paths'
    exit(0)

with open(sys.argv[1], 'r') as f_in, open(sys.argv[2], 'w') as f_out:
    while True:
        line = f_in.readline()
        if line == '': break
        f_out.write(preprocess(line) + '\n')