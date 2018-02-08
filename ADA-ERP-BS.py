import requests
from bs4 import BeautifulSoup
import re
import time
import pickle
import csv


def get_pages(soup):
    '''
    gets links to any subsequent pages
    '''
    base = 'https://professional.diabetes.org'
    try:
        page_links = soup.find('ul', {'class': 'pagination'}).find_all('a')
        links = [base + a['href'] for a in page_links]
        return set(links)
    except:
        return None


def get_org_dicts(soup):
    '''
    turn any listed organizations on page to dictionaries
    '''

    orgs = soup.find_all('div', {'class': 'col col-sm-4'})

    org_dicts = []

    for o in orgs:
        meta = o.find_all('div')
        org_dict = {}

        # up to colon is key after is value
        pattern = re.compile('(.*?):(.*)')
        for m in meta:
            try:
                groups = re.search(pattern, m.text).groups()
                title = groups[0].strip()
                value = groups[1].strip()
                org_dict[title] = value
            except:
                pass

        org_dicts.append(org_dict)

    return org_dicts


if __name__ == "__main__":
    # get list of states from sample URL
    init = 'https://professional.diabetes.org/erp_list?field_erp_state_value=NY'
    res = requests.get(init)
    soup = BeautifulSoup(res.text, 'html5lib')
    options = soup.find(
        'select', {'id': 'edit-field-erp-state-value'}).find_all('option')
    states = [x['value'] for x in options]

    # start iteration through state URLS
    all_dicts = []
    for s in states:
        print(s)
        state_link = 'https://professional.diabetes.org/erp_list?field_erp_state_value={}'.format(
            s)
        res = requests.get(state_link)
        soup = BeautifulSoup(res.text, 'html5lib')

        # get dicts
        all_dicts.extend(get_org_dicts(soup))
        pickle.dump(all_dicts, open('all-dicts.pkl', 'wb'))

        # get extra pages
        pages = get_pages(soup)

        # cycle through subsequent pages
        if pages != None:
            for p in pages:
                res = requests.get(p)
                soup = BeautifulSoup(res.text, 'html5lib')
                all_dicts.extend(get_org_dicts(soup))
                time.sleep(1)
                pickle.dump(all_dicts, open('all-dicts.pkl', 'wb'))
        time.sleep(1)

    # dump csv
    with open('erp.csv', 'w') as csvfile:
        fieldnames = list(all_dicts[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_dicts)
