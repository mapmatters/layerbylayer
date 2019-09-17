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

with open ('links_list', 'rb') as fp:
    links = pickle.load(fp)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(links)

page = urlopen(links[0]).read()
data=bs(page, 'html.parser')
body = data.find('body')
script = body.find('script')
raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
json_data=json.loads(raw)
posts =json_data['entry_data']['PostPage'][0]['graphql']
posts= json.dumps(posts)
posts = json.loads(posts)
x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
x.columns =  x.columns.str.replace("shortcode_media.", "")
pp.pprint(posts) 