from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random
import requests
import pickle


driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
driver.get('http://riograndegames.com/search.html?category%5B%5D=5&category%5B%5D=10&category%5B%5D=14&category%5B%5D=1&category%5B%5D=2&category%5B%5D=12&category%5B%5D=3&category%5B%5D=6&category%5B%5D=8&category%5B%5D=9&category%5B%5D=4&category%5B%5D=13&category%5B%5D=22&category%5B%5D=16&category%5B%5D=11&category%5B%5D=7&category%5B%5D=17&category%5B%5D=18&category%5B%5D=15&language=0&min_players=0&length=0&min_age=0&term=')
search_results = driver.find_element_by_css_selector(
    'div#search_results.isotope').find_elements_by_css_selector('div.search_item.isotope-item')

games_dicts = []
attributes = [
    'data-title',
    'data-orig',
    'data-length',
    'data-date',
    'data-age',
    'data-players',
    'data-msrp']

for s in search_results:
    game = {}
    for a in attributes:
        game[a] = s.get_attribute(a)

    game['page_link'] = s.find_element_by_css_selector(
        'a').get_attribute('href')

    games_dicts.append(game)


final_games_dicts = []
for g in games_dicts:
    print(g['data-title'])
    driver.get(g['page_link'])
    cats = driver.find_elements_by_css_selector('span.game_cat')
    cats = [c.text.replace(',', '') for c in cats]
    g['game_category'] = ';'.join(cats)

    # unfold and download
    driver.find_element_by_css_selector('span.button2').click()

    asset_links = driver.find_elements_by_css_selector('p.asset_list a')

    for a in asset_links:
        images = a.find_elements_by_css_selector("img")
        for i in images:
            if "rules" in i.get_attribute('title').lower():
                download = a.get_attribute('href')
                session = requests.Session()
                cookies = driver.get_cookies()

                for cookie in cookies:
                    session.cookies.set(cookie['name'], cookie['value'])
                response = session.get(download)

                dl_path = 'pdfs/' + g['data-title'] + '.pdf'

                with open(dl_path, 'wb') as f:
                    f.write(response.content)

                g['pdf_path'] = dl_path
                final_games_dicts.append(g)
                pickle.dump(final_games_dicts, open('game_dicts.pkl', 'wb'))

                time.sleep(1)
                break
        break

    time.sleep(1)
