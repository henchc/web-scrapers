from bs4 import BeautifulSoup
import json
import csv
import sys

# read in html source of chart
html_path = sys.argv[1]
with open(html_path, "r") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

# find line of JSON data
raw_data = str(soup)[
    str(soup).find("var doc = ") +
    len("var doc = "):str(soup).find(";\n    doc.Document.state = doc.Document.state")]

figure_data = json.loads(raw_data)

# get states JSON
states = json.loads(figure_data["Document"]['state'])


def find_corr_text(thread_id, soup):
    '''
    find the text from a ThreadId
    '''
    item_id = states['Threads'][thread_id]["ItemId"]
    loc = str(soup).find(item_id)
    end = str(soup)[loc:].find("}}")
    raw = str(soup)[loc + len(item_id) + 3:][:end - \
              len(item_id) - 1].replace("\\", "")

    try:
        props = json.loads(raw)
        text = props["Properties"]["Text"]['t']
    except:
        return None

    return text

# cycle through comments and add text
rows = []
for k in states['Comments'].keys():
    states['Comments'][k]['text'] = find_corr_text(
        states['Comments'][k]['ThreadId'], soup)
    rows.append(states['Comments'][k])

# write csv
with open('lucidchart-comments.csv', 'w') as f:
    w = csv.DictWriter(f, list(set(list(rows[0].keys()) + ['Type'])))
    w.writeheader()
    w.writerows(rows)
