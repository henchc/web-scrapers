import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

soup = BeautifulSoup(requests.get(
    "https://www.cs.cmu.edu/~spok/grimmtmp/").text, 'html5lib')

titles = [x.text.strip() for x in soup.find_all("li")]

base = 'https://www.cs.cmu.edu/~spok/grimmtmp/'
rows = []

for i in range(1, 210):

    url = 'https://www.cs.cmu.edu/~spok/grimmtmp/{}.txt'.format(
        str(i).zfill(3))

    text = requests.get(url).text.strip()

    rows.append([titles[i - 1], text])

    time.sleep(1)

df = pd.DataFrame(rows, columns=['Title', 'Text'])
df.to_csv("grimm.csv", index=False)
