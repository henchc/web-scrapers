import requests
from bs4 import BeautifulSoup
import time

all_links = []
res = requests.get('http://default.sfplanning.org/meetingarchive/planning_dept/sf-planning.org/index.aspx-page=1000.html')
soup = BeautifulSoup(res.text, 'lxml')

# build date links
base = 'http://default.sfplanning.org/meetingarchive/planning_dept/sf-planning.org/'
links = [base + a['href'] for a in soup.find('div', {'id': 'ctl00_content_Screen'})('a')]

# collect nested links
for l in links:
    res = requests.get(l)
    soup = BeautifulSoup(res.text, 'lxml')

    links = [base + a['href'] for a in soup.find('div', {'id': 'ctl00_content_Screen'})('a')]
    all_links.extend(links)
    time.sleep(1)

# save HTML response for all links
for l in all_links:
    html = requests.get(l).text
    name = l.split('=')[-1]
    print(name)
    with open('sfplanning/' + name, 'w') as f:
        f.write(html)
    time.sleep(1)
