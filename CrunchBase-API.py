import requests
import json
from __future__ import division
import math
import csv

# set key
key = "PUT_KEY_HERE"

# set base url
base_url = "https://api.crunchbase.com/v/3/organizations"

# set response format
response_format = ".json"

# set search parameters
search_params = {"name": "uber",
                 "user_key": key,
                 "page": "1"}

# make request
r = requests.get(base_url + response_format, params=search_params)
response_text = r.text

# Convert JSON response to a dictionary
data = json.loads(response_text)

print(data.keys())
