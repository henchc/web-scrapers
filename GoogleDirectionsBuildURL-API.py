import requests

base = "https://www.google.com/maps/dir/"

locs = [
    "305 Harrison St, seattle, WA 98109, USA",
    "san francisco airport",
    "UC berkeley",
    "stanford university"]

# API STUFF HERE

ordered_locs = []

final_url = base

for l in locs:
    final_url += '+'.join(l.split()) + "/"

print(final_url)
