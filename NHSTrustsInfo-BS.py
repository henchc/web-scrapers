import requests
from bs4 import BeautifulSoup
import time
import csv


trust_url = 'https://www.nhs.uk/ServiceDirectories/Pages/NHSTrustListing.aspx'
res = requests.get(trust_url)
soup = BeautifulSoup(res.text, 'lxml')

all_trusts = [x for x in soup('a') if x['href'].startswith('/Services/Trusts/Overview/DefaultView.aspx?id=')]

all_items = []
for t in all_trusts:
    trust_name = t.text
    print(trust_name)
    trust_site = 'https://www.nhs.uk' + t['href'].replace('Overview', 'HospitalsAndClinics')
    res = requests.get(trust_site)
    soup = BeautifulSoup(res.text, 'lxml')
    items = [x for x in soup.find_all('div', {'class': 'panel-content'}) if 'Address' in str(x)]
    for i in items:
        item_name = i.find('h3')
        if item_name:
            item_name = item_name.text
        else:
            continue
            
        if not i.find('a'):
            continue
            
        if i.find('a')['href'].startswith('/Services'):
            url = 'https://www.nhs.uk' + i.find('a')['href']
            service_type = i.find('a')['href'].split('/')[2].title()
        else:
            url = i.find('a')['href']
            service_type = 'Other'

        properties = [x.text for x in i.find('dl').find_all('dt')]
        values = [BeautifulSoup(str(x).replace('<br/>', ', '), 'lxml').text for x in i.find('dl').find_all('dd')]

        info_dict = {'Name': item_name,
                     'URL': url,
                     'Type': service_type,
                     'Trust Name': trust_name}
        for i,k in enumerate(properties):
            if k in ['PostCode', 'Ext', 'Website']:
                continue
            info_dict[k.strip(':')] = values[i]

        all_items.append(info_dict)
        
    time.sleep(2)


keys = ['Name', 'Trust Name', 'Type', 'Tel', 'Address', 'Email', 'URL']
with open('nhs_sites.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_items)
