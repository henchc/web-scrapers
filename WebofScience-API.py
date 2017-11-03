from wos import WosClient
import wos.utils
import time

# must be on campus with access
with WosClient('') as client:
    journals = ["Science"]
    years = range(2000, 2001)
    for journal in journals:
        for year in years:

            rf = wos.utils.recordsFound(
                client, 'PY=' + str(year) + ' AND SO=' + journal)

            for num in range(1, rf, 100):

                info = wos.utils.query(
                    client,
                    'PY=' +
                    str(year) +
                    ' AND SO=' +
                    journal,
                    count=100,
                    frecord=num)

                with open("data/" + str(year) + '-' + journal + ' ' + str(num) + ".xml", "w") as f:
                    f.write(str(info.encode('utf-8')))

                time.sleep(2)

# http://ipscience-help.thomsonreuters.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/user_query/field_tags/WOSfieldTags.html
