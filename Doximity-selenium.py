from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random


header = [
    'Name',
    'Title',
    'Hospital',
    'Phone',
    'State',
    'Tags',
    'Summary',
    'Skills',
    'City',
    'Address']

with open("cardi.csv", "a") as f:
    csv_w_electro = csv.writer(f)
    csv_w_electro.writerow(header)

driver = webdriver.PhantomJS()
next_page = "https://www.doximity.com/directory/md/specialty/thoracic-surgery?from_slug=pub%2Fmichael-peter-kaye-md"

for i in range(1000):

    driver.get(next_page)

    try:
        next_page = BeautifulSoup(
            driver.page_source, "html5lib").find(
            "a", {
                "class": "next_page"})['href']
        next_page = "https://www.doximity.com" + next_page
    except:
        next_page = ""

    links = [a.get_attribute(
        'href') for a in driver.find_elements_by_css_selector("ul.list-4-col a")]
    links = random.sample(links, 15)

    for l in links:

        driver.get(l)
        soup = BeautifulSoup(driver.page_source, "html5lib")

        try:
            name = soup.find("span", {"id": "user_full_name"}).text.strip()
            print(name)
        except:
            name = ""

        try:
            title = soup.find("p", {"itemprop": "jobTitle"}).text.strip()
        except:
            title = ""

        try:
            city = soup.find(
                "span", {
                    "itemprop": "addressLocality"}).text.strip()
        except:
            city = ""

        try:
            state = soup.find("span",
                              {"itemprop": "addressRegion"}).text.strip()
        except:
            state = ""

        try:
            address = soup.find("div", {"class": "col-1-2"}).text.strip()
        except:
            address = ""

        try:
            hospital = soup.find("section",
                                 {"class": "section hospital-info"}).findAll("span",
                                                                             {"itemprop": "name"})
            hospitals = '; '.join([x.text.strip() for x in hospital])
        except:
            hospitals = ""

        try:
            phone = soup.find("span", {"itemprop": "telephone"}).text.strip()
        except:
            phone = ""

        try:
            summary = soup.find(
                "section", {
                    "class": "section summary-info"}).find("ul").text.strip()
        except:
            summary = ""

        try:
            skills = soup.find(
                "div", {
                    "class": "section skills-info"}).find("ul").text.strip()
        except:
            skills = ""

        try:
            tags = soup.find("div", {"class": "section"}).find(
                "p").text.strip()

            if len(phone) > 0:
                if "cardi" in tags.lower():
                    with open("cardi.csv", "a") as f:
                        csv_w_electro = csv.writer(f)
                        csv_w_electro.writerow(
                            [name, title, hospitals, phone, state, tags, summary, skills, city, address])

        except:
            pass

        time.sleep(random.randint(1, 3))

    time.sleep(random.randint(1, 3))
