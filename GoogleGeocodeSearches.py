import requests
import urllib
import time

searches = ['UC Berkeley', 'University of Minnesota', 'Middlebury College']

latitude = []
longitude = []
for s in searches:
    search = urllib.parse.quote(s)

    print(s)

    try:
        json_res = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(search)).json()
        coordinates = json_res['results'][0]['geometry']['location']
        latitude.append(coordinates['lat'])
        longitude.append(coordinates['lng'])
    except:
        latitude.append(None)
        longitude.append(None)

    time.sleep(.5)

print(list(zip(latitude, longitude)))
