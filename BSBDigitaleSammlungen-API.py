from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random
import requests
import re
import pickle
import numpy as np


# PART 1
# first collect bsb ids from search of years 700-1400
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])

driver.maximize_window()

driver.get("https://opacplus.bsb-muenchen.de/metaopac/start.do")
driver.find_element_by_css_selector(
    'input#searchRestrictionValue1_2.form-control').send_keys('700')
driver.find_element_by_css_selector(
    'input#searchRestrictionValue2_2.form-control').send_keys('1400')
driver.find_element_by_css_selector(
    'input#submitSearch.btn.btn-default.dbuttonb').click()
driver.find_element_by_css_selector(
    '#availableFacets > ul > li:nth-child(4) > ul > li:nth-child(5) > a > span.hidden-xs').click()

time.sleep(5)

print(driver.find_element_by_css_selector(
    '#speed_result_list_100 > div > div.nav.nav-tabs.box-header.navigation > div.col-xs-9.col-md-5 > h2').text)

bsbs = []
pattern = r'bsb[0-9]+'

for i in range(2000):

    print(i)

    soup = BeautifulSoup(driver.page_source, 'html5lib')

    rows = soup.find_all('td', {'class': 'resultscell'})

    for r in rows:
        links = r.find_all('a')
        for l in links:
            if re.search(pattern, l['href']):
                bsbs.append(re.search(pattern, l['href']).group())

    pickle.dump(bsbs, open('bsbs.pkl', 'wb'))

    driver.find_element_by_css_selector(
        '#speed_result_list_100 > div > div.nav.nav-tabs.box-header.navigation > div.hidden-xs.hidden-sm.col-xs-7.col-md-7.pull-right.pagination > div > ul > li:nth-child(8) > a').click()
    time.sleep(5)


# PART 2
# now read in list of bsb ids and collect API data


def get_dimensions(res):

    width = []
    height = []
    for p in res['sequences'][0]['canvases']:
        try:
            scale = p['service']['physicalScale']
            width.append(p['width'] * scale)
            height.append(p['height'] * scale)
        except:
            pass

    return (np.mean(height), np.mean(width))

bsbs = pickle.load(open('bsbs.pkl', 'rb'))
data_dicts = []

for bsb in bsbs:
    print(bsb)

    try:
        res = requests.get(
            'https://api.digitale-sammlungen.de/iiif/presentation/v2/{}/manifest'.format(bsb)).json()
        hs_dict = {}
        hs_dict['Thumbnail'] = res['thumbnail']['@id']
        hs_dict['Label'] = res['label']

        for m in res['metadata']:
            key = m['label'][1]['@value']
            value = m['value']

            if isinstance(value, list):
                value = value[-1]['@value']

            hs_dict[key.strip()] = value.strip()

        hs_dict['Height'], hs_dict['Width'] = get_dimensions(res)

        data_dicts.append(hs_dict)
        pickle.dump(data_dicts, open('data_dicts.pkl', 'wb'))

    except:
        pass

    time.sleep(3)
