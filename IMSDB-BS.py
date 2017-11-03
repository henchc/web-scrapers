import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import time
import urllib
import pickle

res = requests.get('http://www.imsdb.com/all%20scripts/').text

soup = BeautifulSoup(res, 'html5lib')

movies = soup.find_all('td', {'valign': 'top'})[2].find_all('p')

base_url = 'http://www.imsdb.com'
movie_urls = [
    base_url +
    urllib.parse.quote(
        m.find('a')['href']) for m in movies]

all_meta = []
# all_meta = pickle.load(open('meta_dicts.pkl', 'rb'))
for i, url in enumerate(movie_urls[:3]):
    print(i)
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html5lib')

    script_details = soup.find('table', {'class': 'script-details'})

    title = script_details.find('h1').text.strip()

    split_details = script_details.find_all('td')[2]

    meta_data = {'title': title}
    for t in split_details.find_all('b'):

        sibling_data = ''
        for s in t.next_siblings:
            if isinstance(s, NavigableString):
                if len(str(s).strip()) > 1:
                    sibling_data += str(s).strip()
                    break
            elif isinstance(s, Tag):
                try:
                    if s.name == 'a':
                        sibling_data += s.text + ';'
                except:
                    pass

                if s.name == 'b':
                    break

        meta_data[t.text] = sibling_data

    all_meta.append(meta_data)

    if "Read" in script_details.find_all('a')[-1].text:

        script_link = base_url + \
            urllib.parse.quote(script_details.find_all('a')[-1]['href'])

        script_path = "scripts/" + title + '.html'
        with open(script_path, 'w') as f:
            f.write(requests.get(script_link).text)

    else:
        script_path = "NA"

    meta_data['script_path'] = script_path

    pickle.dump(all_meta, open('meta_dicts.pkl', 'wb'))

    time.sleep(1)
