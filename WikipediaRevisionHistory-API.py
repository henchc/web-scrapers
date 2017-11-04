import requests
import re
import time
import re
from bs4 import BeautifulSoup
import json
import pickle


def get_revisions(page_title, num_rev):
    url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvprop=ids|flags|timestamp|comment|user|content|tags|flags&rvlimit=1&rvdiffto=prev&titles=" + page_title
    revisions = []
    next_request = ''  # information for the next request

    # while True:
    for i in range(num_rev):
        response = json.loads(
            requests.get(
                url +
                next_request).text)  # web request

        page_id = list(response['query']['pages'].keys())[0]
        revisions.append(
            response['query']['pages'][
                str(page_id)]['revisions'][0])

        cont = response['continue']['rvcontinue']
        if not cont:  # break the loop if 'continue' element missing
            break

        # gets the revision Id from which to start the next request
        next_request = "&rvcontinue=" + cont

        time.sleep(1)

    return revisions


page_names = pickle.load(open('page_names.pkl', 'rb'))

for p in page_names:
    print(p)
    results = get_revisions(p, 200)
    pickle.dump(results, open('pickles/' + p + '.pkl', 'wb'))
