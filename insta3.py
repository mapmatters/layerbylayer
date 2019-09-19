from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import pprint
import pickle


username='choiza11'
driver = webdriver.Chrome('/Users/yongjae/Downloads/chromedriver') # 'type chromedriver' in cmd
driver.get('https://www.instagram.com/'+username+'/?hl=en')

page_count = 10
links=[]

#  scroll height 참조:
# https://cnpnote.tistory.com/entry/PYTHON-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-selenium-webdriver%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A5%BC-%EC%8A%A4%ED%81%AC%EB%A1%A4%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95%EC%9D%80-%EB%AC%B4%EC%97%87%EC%9E%85%EB%8B%88%EA%B9%8C

SCROLL_PAUSE_TIME = 0.5

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
    
    # Wait to load page
    time.sleep(5)
    # time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# def collect_links(h0, dvd_num):
#     Pagelength = driver.execute_script("window.scrollTo("+h0+",document.body.scrollHeight/"+dvd_num+");")
#     source = driver.page_source
#     data=bs(source, 'html.parser')
#     body = data.find('body')
#     script = body.find('span')
#     for link in script.findAll('a'):
#         if re.match("/p", link.get('href')):
#             links.append('https://www.instagram.com'+link.get('href'))
#     time.sleep(5)

# h0 = '0'
# for i in range(1, page_count):
#     collect_links(h0, str(1*page_count))
#     h0 = 'document.body.scrollHeight/{0}'.format(1*page_count)

driver.quit()

with open('links_list', 'wb') as fp:
    pickle.dump(links, fp)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(links)
set_links = set(links)
print(len(links))
print(len(set_links))