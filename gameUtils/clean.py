import sys

if len(sys.argv) < 3:
    sys.stderr.write("usage: clean.py <empty> <input>\n")
    exit(1)
empty = open(sys.argv[1], "r")
inp = open(sys.argv[2], "r")

emptyLines = list(empty.readlines())
inputLines = list(inp.readlines())
empty.close()
inp.close()

def removePrefix(a, b):
    i = 0
    while i < len(a):
        if a[i] != b[i]:
            break
        i += 1
    return b[i:]


def removeSufix(a, b):
    a = list(reversed(a))
    b = list(reversed(b))
    return list(reversed(removePrefix(a, b)))


inputLines = removePrefix(emptyLines, inputLines)
inputLines = removeSufix(emptyLines, inputLines)
for line in inputLines[1:]:
    sys.stdout.write(line)
