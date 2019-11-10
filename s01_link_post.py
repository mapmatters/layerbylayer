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

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

link_type=sys.argv[1] ; print(link_type)
user_or_tag_name=sys.argv[2] ; print(user_or_tag_name)

driver = webdriver.Chrome('/usr/bin/chromedriver', options=options) # 'type chromedriver' in cmd

if link_type=='user':
    driver.get('https://www.instagram.com/'+user_or_tag_name+'/?hl=en')
elif link_type=='tag':
    # driver = webdriver.Chrome('/usr/bin/chromedriver') # 'type chromedriver' in cmd
    driver.get('https://www.instagram.com/explore/tags/'+user_or_tag_name+'/?hl=en')
else:
    print("type first arg as 'user' or 'tag'. (ex. python3 s1_links.py user choiza11)")
    sys.exit(0)

links=[]

#  scroll height ì°¸ì¡°:
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

links_list = filenm

with open (links_list, 'rb') as fp:
    links = pickle.load(fp)

cols = ['link','username', 'user_id', 'fullname', 'id', 'shortcode', 'display_url', 'tracking_token', 'taken_at_timestamp','is_video','is_ad','text', 'like_count', 'loc_id', 'loc_name']
df = pd.DataFrame(columns = cols)
# for i in range(0, 8):
for i in range(0, len(links)):
    lk = links[i]
    page = urlopen(lk).read()
    # try:
    #     page = urlopen(lk).read()
    # except ConnectionResetError as e:
    #     if e.errno != errno.ECONNRESET:
    #         raise # Not error we are looking for
    #     pass # Handle error here.
    page = urlopen(lk).read()
    data=bs(page, 'html.parser')
    body = data.find('body')
    script = body.find('script')
    raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
    json_data=json.loads(raw)
    posts =json_data['entry_data']['PostPage'][0]['graphql']
    posts= json.dumps(posts, ensure_ascii=False)
    posts = json.loads(posts)
    posts = posts["shortcode_media"]
    res0 = [lk, posts['owner']['username'],posts['owner']['id'],posts['owner']['full_name']]
    res1 = [posts[i] for i in cols[4:11] if i in posts]
    try: 
        res2 = [posts["edge_media_to_caption"]["edges"][0]["node"]["text"], posts["edge_media_preview_like"]["count"]]
    except IndexError:
        res2 = ['', posts["edge_media_preview_like"]["count"]]
    try:
        res3 = [posts["location"]["id"], posts["location"]["name"]]
    except TypeError:
        res3 = ['','']
    res = res0 + res1 + res2 + res3
    res = json_normalize(dict(zip(cols, res)))
    df = df.append(res,ignore_index=True, sort=False)
    print(df.tail(5))
    time.sleep(5+uniform(-0.2,0.2))

today = datetime.now().strftime("%Y%m%d")
filenm = user_or_tag_name+"_post_info_"+today+".csv"
df.to_csv(filenm, mode='w')
df = pd.read_csv(filenm, index_col=0)
print(df.head())
print(df.tail())
print(len(df))