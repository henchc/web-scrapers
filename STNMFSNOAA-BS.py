import requests
from bs4 import BeautifulSoup
import os
import time

# send payload to get list of species
payload = {'qwhocalled': 'monthly',
           'qcommon': '',
           'qreturn': 'Search',
           'qselect': 'List Empty, Do a Search to Fill'}
r = requests.get(
    'https://www.st.nmfs.noaa.gov/pls/webpls/FT_HELP.SPECIES',
    params=payload)

soup = BeautifulSoup(r.content, "lxml")
species = [x.text for x in soup.findAll("option")]

# iterate through species
for sp in species:

    if not os.path.exists(sp.replace(",", "").replace(
            " ", "-").replace("/", "_")):  # if need to restart script

        # make directory for species
        os.mkdir(sp.replace(",", "").replace(" ", "-").replace("/", "_"))

        # send payload to get different states and regions
        payload = {'qwhocalled': 'monthly',
                   'qcommon': '',
                   'qreturn': 'Return',
                   'qselect': sp}
        r = requests.get(
            'https://www.st.nmfs.noaa.gov/pls/webpls/FT_HELP.SPECIES',
            params=payload)

        soup = BeautifulSoup(r.content, "lxml")
        states = [
            x.text for x in soup.find(
                "select", {
                    "name": "qstate"}).findAll("option")]

        # iterate through different regions and states
        for st in states:

            payload = {'qspecies': sp,
                       'qreturn': 'Species Locator',
                       'qyearfrom': '1990',
                       'qyearto': '2015',
                       'qmonth': 'YEAR BY MONTH',
                       'qstate': st,
                       'qoutput_type': 'TABLE'}
            r = requests.get(
                'http://www.st.nmfs.noaa.gov/pls/webpls/MF_MONTHLY_LANDINGS.RESULTS',
                params=payload)

            # save html tables into folders
            with open(sp.replace(",", "").replace(" ", "-").replace("/", "_") + "/" + st + ".html", "w") as f:
                f.write(str(r.content))

            # don't overload server
            time.sleep(.1)

# get all species from main page
os.mkdir('ALL-SPECIES-COMBINED')

# iterate through different states and regions
for st in states:

    payload = {'qspecies': 'ALL SPECIES COMBINED',
               'qreturn': 'Species Locator',
               'qyearfrom': '1990',
               'qyearto': '2015',
               'qmonth': 'YEAR BY MONTH',
               'qstate': st,
               'qoutput_type': 'TABLE'}

    r = requests.get(
        'https://www.st.nmfs.noaa.gov/pls/webpls/MF_MONTHLY_LANDINGS.RESULTS',
        params=payload)

    with open('ALL-SPECIES-COMBINED' + "/" + st + ".html", "w") as f:
        f.write(str(r.content))
