import os

log_file = None

def open_log(path, filename):
    global log_file
    i = 0
    while True:
        newpath = path + 'logs/' + os.path.splitext(filename)[0] + '_' + str(i) + '.log'
        if not os.path.exists(newpath):
            break
        i += 1
    log_file = open(newpath, 'w')

def log(header, text):
    log_file.write('\\' + header + '\n')
    log_file.write(text.replace('\\', '_') + '\n')