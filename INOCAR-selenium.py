import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    driver.get("http://www.inocar.mil.ec/mareas/pagina_mareas.php")
    # a = driver.wait.until(EC.presence_of_element_located((By.NAME,
    # "id_puerto")))
    driver.find_element_by_xpath(
        "//select[@name='id_puerto']/option[@value='378']").click()
    driver.find_element_by_xpath(
        "//select[@name='dias']/option[@value='1']").click()
    driver.find_element_by_xpath(
        "//select[@name='mes']/option[@value='1']").click()
    driver.find_element_by_xpath(
        "//select[@name='anio']/option[@value='2015']").click()
    driver.find_element_by_name("Submit").click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    a = soup.findAll("div")
    print(a)

if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "Selenium")
    time.sleep(5)
    driver.quit()
