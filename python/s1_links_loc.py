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
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("disable-gpu")


files_path = '../../files/'
email = sys.argv[1]
password = sys.argv[2]
location_path = files_path+'location_info/'+sys.argv[3] 
output_filenm = sys.argv[4] # 'location_info.csv'

location_ids = pd.read_csv(location_path)
location_ids['loc_id'] = location_ids['loc_id'].astype('str')

chrome_path = '/usr/bin/chromedriver'

driver = webdriver.Chrome(chrome_path, chrome_options=options)
driver.get('https://www.instagram.com/explore/locations/486650968033082/?hl=en')

time.sleep(10)

emailInput = driver.find_elements_by_css_selector('form input')[0]
passwordInput = driver.find_elements_by_css_selector('form input')[1]

emailInput.send_keys(email)
passwordInput.send_keys(password)
passwordInput.send_keys(Keys.ENTER)

time.sleep(10)

# location information
cols_loc = ['loc_id', 'name', 'lat', 'lng']
df_loc = pd.DataFrame(columns=cols_loc)

# post
cols_url = ['loc_id','url']
df_url = pd.DataFrame(columns=cols_url)


def get_location_info(loc_id):
    global df_loc
    # get location meta information
    lk = 'https://www.instagram.com/explore/locations/'+loc_id+'/?hl=en'
    driver.get(lk)
    time.sleep(5)
    source = driver.page_source
    data = bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('script')
    raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
    json_data=json.loads(raw)

    location = json_data['entry_data']['LocationsPage'][0]['graphql']['location']

    loc_id = location['id']
    name = location['name']
    lat = location['lat']
    lng = location['lng']

    loc_info = json_normalize(dict(zip(cols_loc, [loc_id, name, lat, lng])))
    df_loc = df_loc.append(loc_info, ignore_index=True)
    time.sleep(5)


def get_post_link(num_of_links, loc_id):
    global df_url
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
                url = 'https://www.instagram.com'+link.get('href')
                post_url = json_normalize(dict(zip(cols_url, [loc_id, url])))
                df_url = df_url.append(post_url, ignore_index=True)

        # how many links are collected
        len_links = len(set(df_url.url))
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


for item in list(location_ids['loc_id']):
    get_location_info(item)
    get_post_link(3000, item)
    
    df_url = df_url.drop_duplicates()
    print(len(df_url['url']))
    path = files_path+'post_urls/'
    filenm = 'post_'+item
    df_url.to_csv(path+filenm+'.csv')
    
    df_url.drop(df_url.index, inplace=True)

path = files_path+'location_info/'
df_loc.to_csv(path+output_filenm)

driver.quit()


