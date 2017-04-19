import os

def parse(path):
    file = open(path, mode='r')
    answer = []
    try:
        for line in file.readlines():
            if line == '': continue
            if line[0] == '\\':
                key = line[1:].strip()
                answer.append((key, ''))
            else:
                last = answer[-1]
                answer[-1] = (last[0], last[1] + line)
    except:
        return None
    return answer

def parse_all(path):
    answer = []
    files = 0
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        if os.path.isfile(file) and os.path.splitext(file)[1] == '.log':
            files += 1
            parsed = parse(file)
            if parsed:
                answer.append(parsed)
    print('Read successfully {0} out of {1} files'.format(len(answer), files))
    return answer