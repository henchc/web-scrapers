import pandas as pd
import urllib.parse
from bs4 import BeautifulSoup
import requests
import json
import time

df = pd.read_csv('game_data.csv')
game_names = set([x.replace(' Rules', '') for x in df['Title']])
print(len(game_names))

all_dicts = []
for g in game_names:
    game = {'Title': g}

    enc = urllib.parse.quote_plus(g)
    search_url = 'https://boardgamegeek.com/geeksearch.php?action=search&objecttype=boardgame&q={}&B1=Go'.format(
        enc)

    print(search_url)

    res = requests.get(search_url).text
    soup = BeautifulSoup(res, 'html5lib')

    first_result = soup.find('tr', {'id': 'row_'})

    try:
        metadata = [
            x.text.strip().replace(
                '\n',
                ' ').replace(
                '\t',
                '').replace(
                '  ',
                ' ') for x in first_result.find_all('td')]
        game['rank'], game['name'], game['geek_rating'], game[
            'avg_rating'], game['voters'] = [metadata[0]] + metadata[2:-1]
        sub_url = 'https://boardgamegeek.com' + \
            first_result.find_all('td')[2].find('a')['href']

        for l in requests.get(sub_url).text.split('\n'):
            if l.strip().startswith('GEEK.geekitemPreload'):
                data = json.loads(l.strip()[23:-1])
                game = {**game, **data['item']['stats']}

        all_dicts.append(game)
        json.dump(all_dicts, open('all_dicts.json', 'w'))
        time.sleep(1)

    except:
        all_dicts.append(game)
        json.dump(all_dicts, open('all_dicts.json', 'w'))
        time.sleep(1)

df2 = pd.DataFrame(all_dicts)

match = []
for t in df2['Title']:
    for o in df['Title']:
        if o.startswith(t):
            match.append(o)
            break

df2['Title'] = match
df.merge(df2, on=('Title')).to_csv('game_data_with_bgg.csv', index=False)
