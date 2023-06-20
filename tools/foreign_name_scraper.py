from selenium import webdriver
from typing import List
import io

def parse():
    driver = _openForeignNameSite()
    links = _getNameLinks(driver)
    names = set()
    for link in links:
        linkNames = _getNames(driver, link)
        names.update(linkNames)
    # warning: Need to clean some rows manually. takes about 20 minutes.
    # if you're ok with that, uncomment and run code
    # _saveNames(list(names))




def _openForeignNameSite():
    driver = webdriver.Chrome()
    driver.get("https://name.ichiran.info/")
    return driver

def _getNameLinks(driver: webdriver.Chrome):
    tableLinks = driver.find_elements_by_xpath ("//*[@class= 'ie5']/table/tbody/tr/td/a")
    return [link.get_attribute('href') for link in tableLinks]

def _getNames(driver: webdriver.Chrome, link: str):
    driver.get(link)
    tableNames = driver.find_elements_by_xpath ("//*[@class= 'ie5']/table/tbody/tr/td[3]/strong")
    extractedNames = [name.text for name in tableNames]
    names = []
    for name in extractedNames:
        names += name.split('、')
    return names

def _saveNames(names: List[str]):
    with io.open('data/foreign_names.txt', mode='w', encoding='utf-8') as file:
        for name in names:
            file.write(name)
            file.write('\n')

        file.close()

parse()