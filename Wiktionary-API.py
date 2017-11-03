'''This script scrapes wiktionary to get MHG lemmas of NHG lemmas.'''

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from string import punctuation
import urllib.parse
import treetaggerwrapper
import json
import time
from random import randint
import os
import pyprind


# get words from freq list and translations
with open("top10000.txt", "r") as f:
    words = f.read().split()

with open("NHG.txt", "r") as f:
    more_words = f.read().split()

all_words = set(words + more_words)

# turn words to set of lemmas
tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')

lemmas = []
for w in all_words:
    lemm = tagger.tag_text(w)[0].split("\t")[-1]
    lemmas.append(lemm)

lemmas = set(lemmas)

# start scraping here
base = "https://de.wiktionary.org/w/api.php?format=xml&action=query&titles="
branch = "&rvprop=content&prop=revisions&redirects=1"

if os.path.isfile("cognate_dict.json"):
    cognate_dict = json.load(open("cognate_dict.json", "r"))
else:
    cognate_dict = {}

bar = pyprind.ProgBar(len(lemmas), monitor=True, bar_char="#")
for w in lemmas:

    if w not in cognate_dict:

        # for UTF-8 URL parsing
        url = base + w + branch
        url_word = urllib.parse.quote(w)
        url = base + url_word + branch

        html = urlopen(url)
        bsObj = BeautifulSoup(html.read(), "lxml")
        text = bsObj.get_text()

        if "mittelhochdeutsch" in text:
            ind = text.index("mittelhochdeutsch")
            cognates = text[ind:].split("''")

            if len(cognates) > 1:
                cognates = cognates[1].split()
                for i, c in enumerate(cognates):
                    if "|" in c:
                        cognates[i] = c.split("|")[-1]

                for char in punctuation:
                    cognates = [c.replace(char, "") for c in cognates]

                cognates = [c for c in cognates if len(c) > 0 and c[
                    0].isalpha()]

                cognate_dict[w] = cognates

                with open("cognate_dict.json", "w") as f:
                    json.dump(cognate_dict, f)

                time.sleep(randint(1, 3))

            else:
                cognate_dict[w] = None

                with open("cognate_dict.json", "w") as f:
                    json.dump(cognate_dict, f)

        else:

            cognate_dict[w] = None

            with open("cognate_dict.json", "w") as f:
                json.dump(cognate_dict, f)

    bar.update()

print("Done!")
