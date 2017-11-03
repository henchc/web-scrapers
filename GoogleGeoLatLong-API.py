import json
from urllib.request import Request, urlopen
import time
import csv


def getJson(lat, longi):
    url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=true' % \
          (lat, longi)

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    response = urlopen(req).read().decode('utf-8')
    responseJson = json.loads(response)['results']

    return responseJson

latlong = [(18.6, -
            100.566667), (19.6, -
                          100.566667), (19.6, -
                                        101.566667), (17.6, -
                                                      100.566667), (27.121381, -
                                                                    107.200644), (37.586630, -
                                                                                  123.233372), (25.267348, -
                                                                                                120.087235), (19.6, -
                                                                                                              96.566667), (17.6, -
                                                                                                                           98.566667), (37.882042, -
                                                                                                                                        122.277562)]

municps = []
for coord in latlong:
    switch = 0
    info = getJson(coord[0], coord[1])
    # municps.append(info.get("results")[1].get("address_components")[0].get("long_name"))
    # #if certain data is there
    for result in info:  # to avoid errors if incorrect data
        for address_component in result['address_components']:
            if address_component['types'] == [
                    "administrative_area_level_2", "political"]:
                municps.append(address_component['long_name'])
                switch = 1
                break
            break

    if switch == 1:
        continue
    else:
        municps.append("None")

    time.sleep(.11)


latlongname = list(zip(latlong, municps))

with open('data.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['lat-long', 'name'])
    for row in latlongname:
        csv_out.writerow(row)
