import requests
import json
import time

status = ["funded", "expired"]

all_loans = []

for s in status:
    for i in range(1, 2):  # change range to 10000
        # set base url
        base_url = "http://api.kivaws.org/v1/loans/search"

        # set response format
        response_format = ".json"

        # set search parameters
        search_params = {"status": s,
                         "sort_by": "newest",
                         "page": i}

        # make request
        r = requests.get(base_url + response_format, params=search_params)
        time.sleep(1.1)
        response_text = r.text

        # Convert JSON response to a dictionary
        data = json.loads(response_text)

        last_date = data["loans"][-1]["posted_date"]

        if "2016" in last_date[:4]:
            for l in data["loans"]:
                l_id = str(l["id"])

                # set base url
                base_url = "http://api.kivaws.org/v1/loans/"

                # set response format
                response_format = ".json"

                # make request
                r = requests.get(base_url + l_id + response_format)
                time.sleep(1.1)
                response_text = r.text

                # Convert JSON response to a dictionary
                detailed_data = json.loads(response_text)
                final_data = detailed_data["loans"][0]

                r = requests.get(base_url + l_id + "/teams" + response_format)
                time.sleep(1.1)
                response_text = r.text
                team_data = json.loads(response_text)
                final_data["team_count"] = len(team_data["teams"])

                all_loans.append(final_data)

        else:
            break

json.dump(all_loans, open("kiva_data.json", "w"))
