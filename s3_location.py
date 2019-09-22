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

posts_data = sys.argv[1] ; print(post_csv)
df = pd.read_csv(posts_data, index_col=0)
df["loc_id"].unique()

lk = 'https://www.instagram.com/explore/locations/'+loc_id[i]+'/?hl=en'
page = urlopen(lk).read()
data=bs(page, 'html.parser')
body = data.find('body')
script = body.find('script')
raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
json_data=json.loads(raw)

# driver.get('https://www.instagram.com/explore/locations/'+user_or_tag_name+'/?hl=en')

# source = driver.page_source
# data=bs(source, 'html.parser')
# body = data.find('body')
# script = body.find('span')