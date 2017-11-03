from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random

driver = webdriver.PhantomJS()
next_page = "https://www.residentadvisor.net/reviews.aspx?format=single"

with open("resident-adv.csv", "a") as f:
    csv_w_interv = csv.writer(f)
    csv_w_interv.writerow(["title",
                           "artist",
                           "single",
                           "label",
                           "record",
                           "style",
                           "reviewed_date",
                           "release_date",
                           "comments",
                           "rating",
                           "description",
                           "URL"])


for i in range(10000):

    driver.get(next_page)

    soup = BeautifulSoup(driver.page_source, "html5lib")

    try:
	    next_page = "https://www.residentadvisor.net/" + \
	        soup.find("li", {"class": "but arrow-left bbox"}).find("a")['href']
	except:
		next_page = ""

    singles = soup.find(
        "div", {
            "id": "reviews"}).find_all(
        "article", {
            "class": "highlight-top"})

    review_links = [
        'https://www.residentadvisor.net' +
        x.find("a")['href'] for x in singles]

    if i == 0:
        review_links = review_links[25:]

    for l in review_links:
        driver.get(l)

        soup = BeautifulSoup(driver.page_source, 'html5lib')

        title = soup.find("div", {"id": "sectionHead"}).find("h1").text.strip()

        try:
            artist = title.split("-")[0].strip()

            single = title.split("-")[1].strip()
        except:
            artist = ''
            single = ''

        print(title)

        rating = soup.find("span", {"class": "rating"}).text.split("/")[0]
        reviewed_date = soup.find("span", {"itemprop": "dtreviewed"})[
            'datetime'].strip()

        meta_list = soup.find("ul", {"class": "clearfix"}).find_all("li")

        style = meta_list[2].text.split('\n')[4]
        label = str(meta_list[0]).split(
            '<br/>')[0].split('">')[-1].split('</')[0].strip()
        record = str(meta_list[0]).split('<br/>')[-1].split("</")[0].strip()
        release_date = meta_list[1].text.split('\n')[4]
        comments = meta_list[3].text.split('\n')[4].split("/")[0].strip()
        description = soup.find("span",
                                {"itemprop": "description"}).text.strip()

        with open("resident-adv.csv", "a") as f:
            csv_w_interv = csv.writer(f)
            csv_w_interv.writerow([title,
                                   artist,
                                   single,
                                   label,
                                   record,
                                   style,
                                   reviewed_date,
                                   release_date,
                                   comments,
                                   rating,
                                   description,
                                   l])

        time.sleep(random.randint(1, 3))

    time.sleep(random.randint(1, 3))
