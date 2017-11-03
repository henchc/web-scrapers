from selenium import webdriver  # powers the browser interaction
from selenium.webdriver.support.ui import Select  # selects menu options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup  # to parse HTML
import csv  # to write CSV
import pandas as pd  # to see CSV
import time
import os
import random


header = ['Prof_Name',
          'Title',
          'School',
          'Overall_Quality',
          'Overall_Take_Again',
          'Overall_Difficulty',
          'Overall_Hot',
          'Comment_Date',
          'Rating_Type',
          'Course',
          'Quality',
          'Difficulty',
          'Credit',
          'Attendance',
          'Textbook',
          'Take_Again',
          'Grade',
          'Comment',
          'Helpful',
          'Not_Helpful',
          'URL']

with open("rmp.csv", "a") as f:
    csv_w = csv.writer(f)
    csv_w.writerow(header)

base_url = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='

driver = webdriver.PhantomJS()
driver.get(base_url + str(random.randint(1, 500000)))
driver.find_element_by_css_selector('a.btn.close-this').click()

for i in range(500000):
    url = base_url + str(random.randint(1, 500000))
    driver.get(url)

    try:
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        comment_table = soup.find('table', {'class': 'tftable'})
        comments = comment_table.find_all('tr')[1:]
    except:
        continue

    prof_name = ' '.join(
        soup.find(
            'h1', {
                'class': 'profname'}).text.strip().split())
    print(prof_name)
    school = soup.find('a', {'class': 'school'}).text.strip()
    title = ' '.join(
        soup.find(
            'div', {
                'class': 'result-title'}).text.strip().split()).split(' are you')[0]

    overall = soup.find_all('div', {'class': 'grade'})[:3]
    o_quality, o_take_again, o_difficulty = [x.text.strip() for x in overall]
    o_hot = soup.find_all('div', {'class': 'grade'})[3].find('img')[
        'src'].split('/')[-1].split('.')[0]

    all_rows = []
    for c in comments:
        try:
            date = c.find('div', {'class': 'date'}).text.strip()
            rating_type = c.find('span', {'class': 'rating-type'}).text.strip()
            course = c.find('span', {'class': 'name'}).text.strip()
            credit = c.find('span', {'class': 'credit'}
                            ).text.strip().split(':')[1].strip()
            attendance = c.find(
                'span', {
                    'class': 'attendance'}).text.strip().split(':')[1].strip()
            textbook = c.find(
                'span', {
                    'class': 'textbook-used'}).text.strip().split(':')[1].strip()
            take_again = c.find(
                'span', {
                    'class': 'would-take-again'}).text.strip().split(':')[1].strip()
            grade = c.find('span', {'class': 'grade'}
                           ).text.strip().split(':')[1].strip()

            brkdown = c.find(
                'div', {
                    'class': 'breakdown'}).find_all(
                'div', {
                    'class': 'descriptor-container'})
            quality, difficulty = [x.text.strip().split()[0] for x in brkdown]

            helpful = c.find('a', {'class': 'helpful'}).find(
                'span', {'class': 'count'}).text.strip()
            not_helpful = c.find(
                'a', {
                    'class': 'nothelpful'}).find(
                'span', {
                    'class': 'count'}).text.strip()

            comment = c.find('p', {'class': 'commentsParagraph'}).text

            row = [prof_name,
                   title,
                   school,
                   o_quality,
                   o_take_again,
                   o_difficulty,
                   o_hot,
                   date,
                   rating_type,
                   course,
                   quality,
                   difficulty,
                   credit,
                   attendance,
                   textbook,
                   take_again,
                   grade,
                   comment,
                   helpful,
                   not_helpful,
                   url]

            all_rows.append(row)

        except:
            pass

    with open("rmp.csv", "a") as f:
        csv_w = csv.writer(f)
        csv_w.writerows(all_rows)

    time.sleep(random.randint(1, 3))
