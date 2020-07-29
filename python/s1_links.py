
import sys
import csv
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import pickle 
import pprint
import requests
from datetime import date, datetime
from random import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

pp = pprint.PrettyPrinter(indent=4)

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("disable-gpu")


link_type=sys.argv[1] ; print(link_type)
_id_=sys.argv[2] ; print(_id_)
email=sys.argv[3]
password=sys.argv[4]
num_of_links = int(sys.argv[5])

chrome_path = '/usr/bin/chromedriver'

driver = webdriver.Chrome(chrome_path, chrome_options=options)
driver.get('https://www.instagram.com/explore/locations/'+_id_+'/?hl=en')

time.sleep(10)

emailInput = driver.find_elements_by_css_selector('form input')[0]
passwordInput = driver.find_elements_by_css_selector('form input')[1]

emailInput.send_keys(email)
passwordInput.send_keys(password)
passwordInput.send_keys(Keys.ENTER)

time.sleep(10)


# driver = webdriver.Chrome(chrome_path, options=options) # 'type chromedriver' in cmd


if link_type=='user':
    driver.get('https://www.instagram.com/'+_id_+'/?hl=en')
elif link_type=='tag':
    driver.get('https://www.instagram.com/explore/tags/'+_id_+'/?hl=en')
elif link_type=='loc':
    pass
    # driver.get('https://www.instagram.com/explore/locations/'+_id_+'/?hl=en')
    # 486650968033082 신촌
else:
    print("type first arg as 'user' or 'tag'. (ex. python3 s1_links.py user choiza11)")
    sys.exit(0)

links=[]

#  scroll height 참조:
# https://cnpnote.tistory.com/entry/PYTHON-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-selenium-webdriver%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A5%BC-%EC%8A%A4%ED%81%AC%EB%A1%A4%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95%EC%9D%80-%EB%AC%B4%EC%97%87%EC%9E%85%EB%8B%88%EA%B9%8C

time.sleep(10)
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # extract information
    source = driver.page_source
    data=bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
        if re.match("/p", link.get('href')):
            links.append('https://www.instagram.com'+link.get('href'))
    
    # how many links are collected
    len_links = len(set(links))
    print(f'the number of distinct links: {len_links}')
    
    # Wait to load page
    time.sleep(5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    if len_links > int(num_of_links):
        break



driver.quit()

set_links = set(links)
links = list(set_links)
print(len(links))

today = datetime.now().strftime("%Y%m%d")
filenm = link_type+"_"+_id_+"_links_list_"+today

with open(filenm, 'wb') as fp:
    pickle.dump(links, fp)

