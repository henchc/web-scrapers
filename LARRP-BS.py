from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random
import requests


def dl_pages(base_url, books, pres):
    os.mkdir(pres)
    for i1, b in enumerate(books):
        next_page = b
        res = requests.get(next_page).text
        soup = BeautifulSoup(res, 'html5lib')
        book_title = soup.find('h3').text

        os.mkdir(pres + '/' + book_title + '-' + str(i1))

        try:
            for i in range(1, 10000):
                res = requests.get(next_page).text

                soup = BeautifulSoup(res, 'html5lib')

                if 'Discurso al proclamarse su candidatura' in book_title:
                    next_page = base_url + \
                        soup.find('center').find_all('a')[1]['href']
                else:
                    next_page = base_url + \
                        soup.find('center').find_all('a')[2]['href']

                tif_link = base_url + \
                    [x['href'] for x in soup.find_all('a') if 'tif' in x['href']][0]

                res = requests.get(tif_link).content

                with open(pres + '/' + book_title + '-' + str(i1) + '/page-' + str(i) + '.tif', 'wb') as f:
                    f.write(res)

                time.sleep(1)
        except:
            continue


books = [
    'http://lanic.utexas.edu/larrp/pm/sample2/argentin/yrigoyen/180002t.html',
    'http://lanic.utexas.edu/larrp/pm/sample2/argentin/yrigoyen/190117t.html',
    'http://lanic.utexas.edu/larrp/pm/sample2/argentin/yrigoyen/200253t.html',
    'http://lanic.utexas.edu/larrp/pm/sample2/argentin/yrigoyen/210286t.html',
    'http://lanic.utexas.edu/larrp/pm/sample2/argentin/yrigoyen/170347.html']

base_url = 'http://lanic.utexas.edu/larrp/pm/sample2/argentin/yrigoyen/'

dl_pages(base_url, books, 'yrigoyen')


res = requests.get(
    'http://lanic.utexas.edu/larrp/pm/sample2/argentin/peron/index.html').text

soup = BeautifulSoup(res, 'html5lib')

books = []
base_url = 'http://lanic.utexas.edu/larrp/pm/sample2/argentin/peron/'
for li in soup.find('ul').find_all('li'):
    link = [x for x in li.find_all('a') if 'idx' not in x['href']][0]

    if not link.text.strip().startswith('I'):
        books.append(base_url + link['href'])


dl_pages(base_url, books, 'peron')
