from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random
import requests
import time as time_lib

driver = webdriver.Chrome()
next_page = "http://www.boardgamecapital.com/board-game-rules.htm"
driver.get(next_page)

soup = BeautifulSoup(driver.page_source, 'html5lib')
game_cells = soup.find('tbody').find('tbody').find_all('td')[:-1]

game_dict = {}

for g in game_cells:
    game_dict[g.text] = {}
    game_dict[g.text]['link'] = 'http://www.boardgamecapital.com/' + \
        g.find('a')['href']

for k in game_dict.keys():
    print(k)
    driver.get(game_dict[k]['link'])

    soup = BeautifulSoup(driver.page_source, 'html5lib')

    gstats1 = [x.split(':') for x in soup.find(
        'div', {'class': 'gstats1'}).text.split('\n')]
    price = gstats1[0][1].strip()[1:]
    time = gstats1[1][1].strip()

    gstats2 = [x.split(':') for x in soup.find(
        'div', {'class': 'gstats2'}).text.split('\n')]
    age = gstats2[0][1].strip()
    players = gstats2[1][1].strip()

    text = soup.find('div', {'class', 'mainbody'}).text

    pdf_links = [
        a for a in soup.find(
            'div', {
                'class', 'mainbody'}).find_all('a') if 'Game Rules' in a.text]

    paths = []
    for url in pdf_links:
        path = 'pdfs/{}.pdf'.format(url.text)
        with open(path, 'wb') as f:
            f.write(requests.get(url['href']).content)

        paths.append(path)

    paths = ';'.join(paths)

    game_dict[k]['price'] = price
    game_dict[k]['time'] = time
    game_dict[k]['age'] = age
    game_dict[k]['players'] = players
    game_dict[k]['paths'] = paths
    game_dict[k]['web_text'] = text

    time_lib.sleep(1)
