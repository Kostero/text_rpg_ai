import urllib2
import urllib
import re
import subprocess
import os.path
import wget
import sys
from BeautifulSoup import BeautifulSoup

url = 'https://www.bookrix.com'
count = 1
while os.path.exists('data/' + str(count) + '.epub'):
    count += 1

def get_download_link(page):
    response = urllib2.urlopen(url + page)
    bs = BeautifulSoup(response.read())
    button = bs.find('a', {'class': 'button blue withIcon download download-book '})
    if button is None:
        return None
    page = button.get('data-download')
    response = urllib2.urlopen(url + page)
    bs = BeautifulSoup(response.read())
    for link in bs.findAll('a'):
        if link.text == 'Download ePub File':
            return url + link.get('href')

def scrap(page):
    print 'openning', page
    if not page.startswith('http'):
        page = url + page
    response = urllib2.urlopen(page)
    bs = BeautifulSoup(response.read())
    print 'done'
    for book in bs.findAll('a', {'class': 'word-break'}):
        try:
            link = get_download_link(book.get('href'))
            if link: 
                global count
                path = 'data/' + str(count)
                filename = wget.download(link, out=path + '.epub')
                subprocess.call(['ebook-convert', path + '.epub', path + '.txt'])
                print
                print 'Downloaded', book.text
                count += 1
        except KeyboardInterrupt:
            return
        except:
            pass
    print 'page finished'
    next = bs.find('li', {'class': 'next'})
    next_link = next.find('a')
    if next_link:
        scrap(next_link.get('href'))

if __name__ == '__main__':
    scrap(sys.argv[1])