import requests
from bs4 import BeautifulSoup
import time
import pickle
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
artworks = []
for i in range(0, 7200, 100):
    print(i)
    url = 'https://www.fbi.gov/investigate/violent-crime/art-theft/national-stolen-art-file?b_start:int=' + \
        str(i)
    res = requests.get(url, headers)
    soup = BeautifulSoup(res.text, 'html5lib')

    for i in soup.find_all('li', {'class': 'grid-item'}):

        art = {}
        art['title'] = i.find('h3').text
        art['description'] = i.find('p').text

        try:
            art['image_link'] = i.find('img')['src']
        except:
            art['image_link'] = 'None'

        keys = [x.text for x in i.find_all('b')]
        values = [x.text for x in i.find_all('span')]

        for t in list(zip(keys, values)):
            art[t[0]] = t[1]

        artworks.append(art)

    pickle.dump(artworks, open('artworks.pkl', 'wb'))
    time.sleep(5)

pd.DataFrame(artworks).to_csv('artworks.csv', index=False)
