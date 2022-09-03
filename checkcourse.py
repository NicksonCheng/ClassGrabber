from ast import Try
from lib2to3.pgen2 import driver
from multiprocessing.sharedctypes import Value
from optparse import Option
from os import link
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# the module of webdriver wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DRIVER_PATH = "/usr/local/bin/chromedriver"

# document
# element.get_attribute
# if element is not displayed, please use javascript executer to trigger the event


def searchCourse(driver):
    # elems = driver.find_elements(By.XPATH, "//a[@href]")
    # for elem in elems:
    #     print(elem.get_attribute("innerHTML"))
    selectors = driver.find_elements(by=By.CLASS_NAME, value="dropdown")
    for selector in selectors:
        link = selector.find_element(by=By.TAG_NAME, value="a")
        if ("Catalog" in link.get_attribute("innerHTML")):
            driver.execute_script("arguments[0].click();", link)
            break
    sleep(3)
    driver.quit()
    return


if __name__ == '__main__':
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()))
    driver.get("https://course.ncku.edu.tw/")

    timeout = 3
    try:
        element_present = EC.presence_of_all_elements_located(
            (By.ID, "header"))
        res = WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Time out for loading page")
    finally:
        print("Page loaded")
    searchCourse(driver)
