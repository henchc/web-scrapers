# https://pypi.python.org/pypi/glassdoor
# http://stackoverflow.com/questions/30956891/rest-glassdoor-api-requires-user-agent-in-header
import urllib.request as request
import requests
import json
from collections import OrderedDict

# authentication information & other request parameters
params_gd = OrderedDict({
    "v": "1",
    "format": "json",
    "t.p": "",
    "t.k": "",
    "action": "employers",
    "employerID": "11111",
    # programmatically get the IP of the machine
    "userip": json.loads(request.urlopen("http://ip.jsontest.com/").read().decode('utf-8'))['ip'],
    "useragent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"
})

# construct the URL from parameters
basepath_gd = 'http://api.glassdoor.com/api/api.htm'

# request the API
response_gd = requests.get(
    basepath_gd, params=params_gd, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"})

# check the response code (should be 200)  & the content
response_gd
data = json.loads(response_gd.text)

print(data["response"]["employers"][0].keys())
