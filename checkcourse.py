from ast import Try
from lib2to3.pgen2 import driver
from multiprocessing.sharedctypes import Value
from optparse import Option
from os import link
import selectors
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# the module of webdriver wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DRIVER_PATH = "/usr/local/bin/chromedriver"

# document
# element.get_attribute
# if element is not displayed, please use javascript executer to trigger the event

course_infor = {"course": "網路管理", "ta": "楊竹星",
                "college": "電機資訊學院", "dep": "電機所"}


def waitLoading(element, type, name, timeout=3):
    find_type = {"class": By.CLASS_NAME, "id": By.ID, "tag": By.TAG_NAME}
    # wait for page loading
    try:
        element_present = EC.presence_of_all_elements_located(
            (find_type[type], name))
        res = WebDriverWait(element, timeout).until(element_present)
    except TimeoutException:
        print("Time out for loading page")
    finally:
        pass
    return


def updateDriver(driver):
    new_url = driver.window_handles[0]
    driver.switch_to.window(new_url)
    return driver


def searchCoruse(driver):

    course_input = driver.find_element(by=By.ID, value="cosname")
    teacher_input = driver.find_element(by=By.ID, value="teaname")
    course_input.send_keys(course_infor["course"])
    teacher_input.send_keys(course_infor["ta"])
    sel_col = Select(driver.find_element(by=By.ID, value="sel_col"))
    sel_col.select_by_visible_text(course_infor["college"])
    dep_element = driver.find_element(by=By.ID, value="sel_dept")
    sel_dep = Select(dep_element)
    sel_dep.select_by_visible_text(course_infor["dep"])

    #btns = driver.find_elements(by=By.CLASS_NAME, value="btn-primary")
    search_btn = driver.find_element(
        by=By.XPATH, value="//*[contains(text(), '查詢') and contains(@class,'btn-primary')]")
    search_btn.click()
    sleep(10)
    driver.quit()
    return


def courseAdvanceSearch(driver):

    # change to chinese page
    drowdowns = driver.find_elements(by=By.CLASS_NAME, value="dropdown")
    for drowdown in drowdowns:
        link = drowdown.find_element(by=By.TAG_NAME, value="a")
        if ("中文" in link.get_attribute("innerHTML")):
            driver.execute_script("arguments[0].click();", link)
            waitLoading(driver, "class", "dropdown", 3)
            break
    drowdowns = driver.find_elements(by=By.CLASS_NAME, value="dropdown")
    for drowdown in drowdowns:
        link = drowdown.find_element(by=By.TAG_NAME, value="a")
        if ("課程資訊" in link.get_attribute("innerHTML")):
            print("find it")
            sub_drowdowns = drowdown.find_elements(
                By.CLASS_NAME, value="eng_span")
            break

    # access the course information
    for sub_drowdown in sub_drowdowns:
        span = sub_drowdown.find_element(by=By.TAG_NAME, value="span")
        if ("進階課程查詢" in span.get_attribute("innerHTML")):
            link = sub_drowdown.find_element(by=By.TAG_NAME, value="a")
            driver.execute_script("arguments[0].click();", link)
            break
    waitLoading(driver, "class", "form-control", 3)
    driver = updateDriver(driver)
    searchCoruse(driver)
    return


def jumpPage(driver):
    # access the course catalog
    drowdowns = driver.find_elements(by=By.CLASS_NAME, value="dropdown")
    for drowdown in drowdowns:
        link = drowdown.find_element(by=By.TAG_NAME, value="a")
        if ("Catalog" in link.get_attribute("innerHTML")):
            driver.execute_script("arguments[0].click();", link)
            break

    # find course in specific course

    driver = updateDriver(driver)
    courses = driver.find_element(by=By.CLASS_NAME, value="btn_menu_main")
    courses.click()

    timeout = 3
    try:
        element_present = EC.element_to_be_clickable(
            (By.ID, "btn_all_dept"))
        res = WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Time out for loading page")
    finally:
        pass
    driver = updateDriver(driver)
    btns = driver.find_elements(by=By.CLASS_NAME, value="btn_menu")
    for btn in btns:
        if ("Advance" in btn.get_attribute("innerHTML")):
            btn.click()

    # start to search course

    try:
        element_present = EC.presence_of_all_elements_located((
            By.ID, "cosname"))
        res = WebDriverWait(driver, timeout).until(element_present)
    except:
        print("Time out for loading page")
    finally:
        pass

    driver = updateDriver(driver)
    searchCoruse(driver)
    return


if __name__ == '__main__':
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()))
    driver.get("https://course.ncku.edu.tw/")

    # wait for page loading
    waitLoading(driver, "id", "header", 3)
    courseAdvanceSearch(driver)
