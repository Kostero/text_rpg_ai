import BeautifulSoup as bs
import urllib2


def parseCommands(site):
    response = urllib2.urlopen(site)
    html = response.read()
    soup = bs.BeautifulSoup(html)
    commands = soup.findAll('p', {'class': 'in'})
    commandsList = []
    for command in commands:
        try:
            textCommands = command.find('kbd').getText().split(".")
            for textCommand in textCommands:
                commandsList.append(textCommand.strip())
        except:
            if True:
                textCommands = command.getText().replace("&gt;", "").split(".")
                for textCommand in textCommands:
                    if len(textCommand) > 0 and \
                            textCommand[0] != '(' and textCommand[-1] != ')':
                        commandsList.append(textCommand.strip())
            else:
                print(command)
    return commandsList


def main():
    for letter in "qwertyuiopasdfghjklzcvbnm":
        print "L", letter
        response = urllib2.urlopen('http://plover.net/~davidw/sol/'+letter)
        html = response.read()
        soup = bs.BeautifulSoup(html)
        links = soup.findAll('a')
        for link in links:
            text = link['href']
            if ".html" in text:
                site = 'http://plover.net/~davidw/sol/'+letter+'/'+text
                commands = parseCommands(site)
                f = open('downloadedCommands.txt', 'a')
                for command in commands:
                    if command != "":
                        f.write(command + "\n")
                f.close()


if __name__ == "__main__":
    main()
