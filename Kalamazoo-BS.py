from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

urls = []
for i in range(1035, 1053):
    urls.append(
        "http://scholarworks.wmich.edu/cgi/viewcontent.cgi?article=" +
        str(i) +
        "&context=medieval_cong_archive")

for i, url in enumerate(urls):
    res = urlopen(Request(url))
    pdf = open(("kzoo/kalamazoo_" + str(i) + ".pdf"), 'wb')
    pdf.write(res.read())
    pdf.close()
