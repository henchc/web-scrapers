from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random
import requests

next_page = 'http://www.start.umd.edu/baad/database'
base_url = 'http://www.start.umd.edu'

all_rows = []
all_rows.append(['ID',
                 'Group Name',
                 'Country',
                 'Lethality',
                 'Number of Allies',
                 'Number of Rivals',
                 'Founded',
                 'Fatalities',
                 'Fatality Years',
                 'Ideologies',
                 'Strength',
                 'Territorial Control',
                 'Funding through Drug Trafficking',
                 'Record Year'])

for i in range(1, 6):
    res = requests.get(next_page).text

    soup = BeautifulSoup(res, 'html5lib')

    rows = soup.find('table', {'class', 'sticky-enabled'}).find_all('tr')
    rows = rows[1:]

    for r in rows:
        cells = r.find_all('td')
        cell_text = [x.text.strip() for x in cells]
        link = base_url + cells[0].find('a')['href']

        res = requests.get(link).text
        soup = BeautifulSoup(res, 'html5lib')

        year_bullets = soup.find('div', {'class': 'item-list'}).find_all('li')
        year_urls = [(base_url + x.find('a')['href'],
                      x.find('a').text.strip()) for x in year_bullets]
        for u in year_urls:
            record_year = u[1]
            res = requests.get(u[0]).text
            soup = BeautifulSoup(res, 'html5lib')

            founded = soup.find(
                'div', {'class', 'quick-view-founded'}).text.split(':')[-1].strip()
            fatalities, fatality_years = soup.find(
                'div', {'class', 'quick-view-lethality'}).text.split(':')[-1].strip().split(' ', maxsplit=1)
            ideology = soup.find(
                'div', {'class', 'quick-view-ideology'}).text.split(':')[-1].strip()
            strength = soup.find(
                'div', {'class', 'quick-view-strength'}).text.split(':')[-1].strip()
            terrcnt = soup.find(
                'div', {'class', 'quick-view-terrcnt'}).text.split(':')[-1].strip()
            drugs = soup.find(
                'div', {'class', 'quick-view-drug-funding'}).text.split(':')[-1].strip()

            data_row = [
                cell_text[0] + '-' + record_year] + cell_text + [
                founded,
                fatalities,
                fatality_years,
                ideology,
                strength,
                terrcnt,
                drugs,
                record_year]
            print(data_row)
            all_rows.append(data_row)

            time.sleep(1)

        time.sleep(1)

    next_page = 'http://www.start.umd.edu/baad/database?page={}'.format(str(i))
    time.sleep(1)


with open("baad.csv", "w") as f:
    csv_w = csv.writer(f)
    csv_w.writerows(all_rows)
