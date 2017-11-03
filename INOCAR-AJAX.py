import json
import requests
from bs4 import BeautifulSoup
import re
import csv
import time
from random import randint
import pickle
import os.path

id_dict = {"61": "San Lorenzo", "377": "Esmeraldes"}
days = [str(x) for x in list(range(1, 32))]
months = [str(x) for x in list(range(1, 13))]
years = [str(x) for x in list(range(2003, 2016))]

if os.path.isfile("already_scraped.pkl"):
    already_scraped = pickle.load(open("already_scraped.pkl", "rb"))
else:
    already_scraped = []

for l in id_dict.keys():
    for y in years:
        for m in months:
            for d in days:
                date = d + "/" + m + "/" + y
                if (l, date) not in already_scraped:
                    payload = {
                        "id_puerto": l,
                        "dias": d,
                        "mes": m,
                        "anio": y,
                        "task": "generate",
                        "tipocon": "form_",
                        "Submit": "Ver",
                    }

                    r = requests.post(
                        url='http://www.inocar.mil.ec/mareas/consulta.php',
                        data=payload
                    )

                    soup = BeautifulSoup(r.text, "lxml")

                    r1 = soup.findAll("tr", {"class": "row_1"})[2:4]
                    r2 = soup.findAll("tr", {"class": "row_2"})[2:4]
                    rows = [tuple(r1[0].get_text().split('\n')),
                            tuple(r2[0].get_text().split('\n')),
                            tuple(r1[1].get_text().split('\n')),
                            tuple(r2[1].get_text().split('\n'))]

                    with open('data.csv', 'a') as f:
                        a = csv.writer(f)
                        for r in rows:
                            row = (id_dict[l], date) + r
                            a.writerow(row)

                    already_scraped.append((l, date))
                    pickle.dump(
                        already_scraped, open(
                            "already_scraped.pkl", "wb"))
                    time.sleep(randint(1, 3))
