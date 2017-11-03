from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random
import requests

driver = webdriver.Chrome()
driver.get("http://careers.historians.org/jobs/?page=1")

base_url = 'http://careers.historians.org'
all_rows = []
pages = ["http://careers.historians.org/jobs/?page=1",
         "http://careers.historians.org/jobs/?page=2"]

for p in pages:
    driver.get(p)
    soup = BeautifulSoup(driver.page_source, 'html5lib')

    rows = soup.find_all('div', {'class': 'bti-ui-job-detail-container'})
    for r in rows:
        title = r.find('a').text.strip()
        link = base_url + r.find('a')['href']
        employer = r.find(
            'div', {
                'class': 'bti-ui-job-result-detail-employer'}).text.strip()
        location = r.find(
            'div', {
                'class': 'bti-ui-job-result-detail-location'}).text.strip()
        date_posted = r.find(
            'div', {
                'class': 'bti-ui-job-result-detail-age'}).text.strip()

        driver.get(link)

        soup = BeautifulSoup(driver.page_source, 'html5lib')

        try:
            job_description = soup.find(
                'div', {'class': 'bti-jd-description'}).text.strip()

            details = soup.find('div', {'class': 'bti-jd-details-container'})

            details_titles = [
                x.text.replace(
                    ':', '').lower().strip() for x in details.find_all(
                    'div', {
                        'class': 'bti-jd-detail-title'})]
            details_text = [
                x.text.strip() for x in details.find_all(
                    'div', {
                        'class': 'bti-jd-detail-text'})]

            details_dict = {}

            for i in range(len(details_titles)):
                t = details_titles[i]
                if 'categories' in t:
                    t = 'category'
                elif 'required' in t:
                    t = 'preferred education'
                details_dict[t] = details_text[i]

            details_dict['title'] = title
            details_dict['link'] = link
            details_dict['employer'] = employer
            details_dict['location'] = location
            details_dict['date_posted'] = date_posted
            details_dict['job_description'] = job_description

            try:
                details_dict['employer_about'] = soup.find(
                    'div', {'class': 'bti-jd-employer-info'}).text.strip()
            except:
                details_dict['employer_about'] = ''

            all_rows.append(details_dict)

        except:
            pass

        time.sleep(1)

header = ["title",
          "employer",
          "location",
          "posted",
          "date_posted",
          "primary field",
          "category",
          "preferred education",
          "salary",
          "type",
          "employment type",
          "job_description",
          "employer_about",
          "link"
          ]


with open('AHA-data.csv', 'w') as f:
    w = csv.DictWriter(f, header)
    w.writeheader()
    w.writerows(all_rows)
