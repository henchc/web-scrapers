import dryscrape
import sys
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time


urls = ["http://www.glorecords.blm.gov"]
ext = "/ConvertedImages/CV_Patent_0123-207.PDF"

for url in urls:
    # set up a web scraping session
    sess = dryscrape.Session(base_url=url)

    # we don't need images
    sess.set_attribute('auto_load_images', True)

    # visit homepage and search for a term
    sess.visit(ext)
    time.sleep(15)
    # sess.render('sshot.png')

    res = urlopen(Request(url + ext))
    pdf = open((url[1] + ".pdf"), 'wb')
    pdf.write(res.read())
    pdf.close()
