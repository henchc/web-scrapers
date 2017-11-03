from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


html = urlopen("http://www.federalreserve.gov/monetarypolicy/discountrate.htm")
bsObj = BeautifulSoup(html.read(), "lxml")
d1 = bsObj.findAll("option")

urls = []
for item in d1:
    if "PDF" in str(item.get_text()):
        prefix = "http://www.federalreserve.gov"
        url = prefix + str(item['value'])
        urls.append((url, str(item.get_text())))

urls = urls[:3]

print(len(urls))

for url in urls:
    res = urlopen(Request(url[0]))
    pdf = open((url[1] + ".pdf"), 'wb')
    pdf.write(res.read())
    pdf.close()
