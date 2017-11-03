import json
from urllib.request import Request, urlopen


def getJson(func, apikey, params):
    url = 'http://www.opensecrets.org/api/?method=%s&output=json&%s&apikey=%s' % \
          (func, params, apikey)

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    response = urlopen(req).read().decode('utf-8')
    responseJson = json.loads(response)

    return responseJson

func = "getOrgs"
apikey = ""
params = "org=Exxon"

info = getJson(func, apikey, params)

print(info)

orgid = info.get("response").get("organization")[
    0].get("@attributes").get("orgid")

func = "orgSummary"
params = "id=" + orgid
summary = getJson(func, apikey, params)

print(summary)
