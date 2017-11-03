from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random


driver = webdriver.PhantomJS()
next_page = "https://www.ctsnet.org/surgeons/surgeons-advanced-search?ln=&fn=&subspecialty=adult_cardiac_surgery&city=&country=gb&province=&o"

with open("IT-cardi.csv", "a") as f:
    csv_w_interv = csv.writer(f)
    csv_w_interv.writerow(["Name",
                           "Hospital",
                           "Phone",
                           "Interests",
                           "Practice-Areas",
                           "City-Region",
                           "Country",
                           "Street", "URL"])


for i in range(1000):

    driver.get(next_page)

    soup = BeautifulSoup(driver.page_source, "html5lib")

    try:
        next_page = "https://www.ctsnet.org" + \
            soup.find('a', {'title': 'Go to next page'})['href']
    except:
        next_page = ""

    td_a = soup.find_all(
        "td", {"class": "views-field views-field-field-contact-last-name"})

    if i == 0:
        links = ["https://www.ctsnet.org" +
                 x.find("a")['href'] for x in td_a[48:]]
    else:
        links = ["https://www.ctsnet.org" + x.find("a")['href'] for x in td_a]

    for l in links:

        driver.get(l)
        soup = BeautifulSoup(driver.page_source, "html5lib")

        try:
            name = soup.find('h1', {"class": 'page-title'}).text.strip()
            print(name)
        except:
            continue

        try:
            hospital = soup.find(
                'div', {
                    "class": 'contact-institution'}).text.strip()
        except:
            continue

        try:
            country = soup.find('div',
                                {"class": 'contact-country'}).text.strip()

        except:
            country = ''

        try:
            street = soup.find('div', {"class": 'contact-street'}).text.strip()
        except:
            street = ''

        try:
            city = soup.find(
                'div', {
                    "class": 'contact-city-province-code'}).text.strip()

        except:
            city = ''

        try:
            phone = soup.find('div', {"class": 'contact-numbers'}).text.strip()
        except:
            continue

        try:
            fields = soup.find(
                'div', {
                    "class": 'views-field views-field-field-contact-subspecialty'}).text.strip().replace(
                '\n', '; ')
        except:
            fields = ''

        try:

            interests = soup.find(
                'div', {
                    "class": 'field field--name-field-contact-interest field--type-text-long field--label-hidden'}).text.strip().replace(
                '\n', '; ')
        except:
            interests = ''

        if len(phone) > 0:

            with open("IT-cardi.csv", "a") as f:
                csv_w_interv = csv.writer(f)
                csv_w_interv.writerow(
                    [name, hospital, phone, interests, fields, city, country, street, l])

        time.sleep(random.randint(1, 3))
    time.sleep(random.randint(1, 3))
