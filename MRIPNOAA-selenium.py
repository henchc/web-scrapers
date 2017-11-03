import re
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import Request, urlopen
import time


driver = webdriver.Chrome()  # needs chromedriver in PATH

# iframed into
# http://www.st.nmfs.noaa.gov/recreational-fisheries/MRIP/mrip-project
driver.get("https://www.st.nmfs.noaa.gov/pims/#view=public_page&program_id=1")

time.sleep(15)

for i in range(11):

    projects = []

    for i in driver.find_elements_by_class_name("dijitTitlePaneTextNode"):
        os.mkdir("MRIP/" + i.text)
        projects.append(i.text)

    content_pane = driver.find_elements_by_class_name("dijitContentPane")[0]
    links = content_pane.find_elements_by_class_name("docLink")
    if len(links) > 0:
        project_ct = -1
        for l in links:
            if l.text == "Proposal":  # begins each new project
                project_ct += 1
                with open("MRIP/" + projects[project_ct] + "/" + "source.html", 'w') as f:
                    f.write(str(driver.page_source))

            res = urlopen(Request(l.get_attribute("href")))
            with open("MRIP/" + projects[project_ct] + "/" + l.text + ".pdf", 'wb') as pdf:
                pdf.write(res.read())

            time.sleep(1)

    driver.find_element_by_id("dijit_form_Button_4_label").click()
    time.sleep(1)
