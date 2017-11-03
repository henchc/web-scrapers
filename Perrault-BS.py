import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

rows = []
for i in range(1, 12):

    url = 'http://www.pitt.edu/~dash/perrault{}.html'.format(
        str(i).zfill(2))

    soup = BeautifulSoup(requests.get(url).text, 'html5lib')

    title = soup.find('h1').text.strip()
    text = '\n'.join([p.text for p in soup.find_all('p')[:-1]])
    try:
        text += soup.find('blockquote').text
    except:
        pass

    bullets = soup.find_all('li')
    for b in bullets:
        if "aarne" in b.text.lower():
            at = ''.join([ch for ch in b.text if ch.isnumeric()])

    rows.append([title, at, text])

    time.sleep(1)

df = pd.DataFrame(rows, columns=['Title', 'Aarne-Thompson', 'Text'])
df.to_csv("perrault.csv", index=False)
