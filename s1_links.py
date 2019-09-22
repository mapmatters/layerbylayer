import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import pickle 
import csv
import pprint
import requests
from datetime import date, datetime
from random import *
pp = pprint.PrettyPrinter(indent=4)

link_type=sys.argv[1] ; print(link_type)
user_or_tag_name=sys.argv[2] ; print(user_or_tag_name)

if link_type=='user':
    driver = webdriver.Chrome('/Users/yongjae/Downloads/chromedriver') # 'type chromedriver' in cmd
    driver.get('https://www.instagram.com/'+user_or_tag_name+'/?hl=en')
elif link_type=='tag':
    driver = webdriver.Chrome('/Users/yongjae/Downloads/chromedriver') # 'type chromedriver' in cmd
    driver.get('https://www.instagram.com/explore/tags/'+user_or_tag_name+'/?hl=en')
else:
    print("type first arg as 'user' or 'tag'. (ex. python3 s1_links.py user choiza11)")
    sys.exit(0)

links=[]

#  scroll height 참조:
# https://cnpnote.tistory.com/entry/PYTHON-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-selenium-webdriver%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EC%9B%B9-%ED%8E%98%EC%9D%B4%EC%A7%80%EB%A5%BC-%EC%8A%A4%ED%81%AC%EB%A1%A4%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95%EC%9D%80-%EB%AC%B4%EC%97%87%EC%9E%85%EB%8B%88%EA%B9%8C


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


driver.quit()

set_links = set(links)
links = list(set_links)
print(len(links))

today = datetime.now().strftime("%Y%m%d")
filenm = link_type+"_"+user_or_tag_name+"_links_list_"+today

with open(filenm, 'wb') as fp:
    pickle.dump(links, fp)


# with open(filenm, "w", newline='') as output:
#     wr = csv.writer(links, lineterminator='\n')
#     for val in links:
#         wr.writerow([val])    

