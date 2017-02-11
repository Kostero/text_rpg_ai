import BeautifulSoup as bs
import mechanize
from time import sleep
import re


brackets = re.compile(r'\([^)]*\)')
leftbracket = re.compile(r'[^)]*\)')
rightbracket = re.compile(r'\([^)]*')


def downloadCommands(site):
    result = []
    number = site.split("/")[2]
    url = 'https://solutionarchive.com/index.php?page=file&args=force,true/'\
        + number + '/mode,file/'
    print(url)
    err = 0
    ok = 0
    response = mechanize.urlopen(url)
    html = response.read()
    for line in html.split("\n"):
        line = re.sub(brackets, "", line)
        line = re.sub(leftbracket, "", line)
        line = re.sub(rightbracket, "", line)
        commands = re.split(r';|\,|\.|\>| \band\b | \bor\b | \bthen\b', line)
        for command in commands:
            if re.match(r'^[a-zA-Z0-9\;\,\.\-\*\:\'\"\/\s]{1,80}$', command) \
                    and re.search(r'[a-zA-Z]', command):
                result.append(command.strip())
                ok += 1
            else:
                err += 1
            if (ok+err) > 20 and ok < 0.2 * (ok+err):
                print(ok, err)
                return
    f = open("downloadedCommands.txt", 'a')
    for command in result:
        f.write(command+"\n")
    f.close()


def downloadSolution(site):
    response = mechanize.urlopen('https://solutionarchive.com'+site)
    html = response.read()
    soup = bs.BeautifulSoup(html)
    links = soup.findAll('a')
    for link in links:
        if "solution" in link.getText().lower():
            try:
                downloadCommands(link['href'])
            except Exception as e:
                print "ERR downloading solution ", link['href'], e.message


def main():
    f = open("downloadedCommands.txt", 'w')
    f.close()
    for page in range(1, 145):
        print "P", page
        response = mechanize.urlopen(
            'https://solutionarchive.com/list/p,'+str(page))
        html = response.read()
        soup = bs.BeautifulSoup(html)
        table = soup.find('table', {'class': 'gameslist'})
        rows = table.findAll('tr')
        for row in rows[1:]:
            cells = row.findAll('td')
            language = cells[3].getText()
            if language.lower() != "english":
                continue
            if "solution" in cells[4].getText().lower():
                href = cells[0].find('a')['href']
                try:
                    downloadSolution(href)
                except Exception as e:
                    print "ERR downloading game ", href, e.message


if __name__ == "__main__":
    main()
