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


links_list = sys.argv[1] ; print(links_list)

with open (links_list, 'rb') as fp:
    links = pickle.load(fp)

cols = ['link','username', 'user_id', 'fullname', 'id', 'shortcode', 'display_url', 'tracking_token', 'taken_at_timestamp','is_video','is_ad','text', 'like_count', 'loc_id', 'loc_name']
df = pd.DataFrame(columns = cols)
# for i in range(0, 8):
for i in range(0, len(links)):
    lk = links[i]
    page = urlopen(lk).read()
    data = bs(page, 'html.parser')
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
    time.sleep(2+uniform(-0.2,0.2))

today = datetime.now().strftime("%Y%m%d")
filenm = links_list+"_post_info_"+today+".csv"
df.to_csv(filenm, mode='w')
df = pd.read_csv(filenm, index_col=0)
print(df.head())
print(df.tail())
print(len(df))
# cols = ['link','username', 'user_id', 'fullname', 'id', 'shortcode', 'display_url', 'tracking_token', 'taken_at_timestamp','is_video','is_ad','text', 'like_count', 'loc_id', 'loc_name']
# df = pd.DataFrame(columns = cols)

# lk = links[1]
# page = urlopen(lk).read()
# data=bs(page, 'html.parser')
# body = data.find('body')
# script = body.find('script')
# raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
# json_data=json.loads(raw)
# posts =json_data['entry_data']['PostPage'][0]['graphql']
# posts= json.dumps(posts, ensure_ascii=False)
# posts = json.loads(posts)
# posts = posts["shortcode_media"]
# res0 = [lk, posts['owner']['username'],posts['owner']['id'],posts['owner']['full_name']]
# res1 = [posts[i] for i in cols[4:11] if i in posts]
# try: 
#     res2 = [posts["edge_media_to_caption"]["edges"][0]["node"]["text"], posts["edge_media_preview_like"]["count"]]
# except IndexError:
#     res2 = ['', posts["edge_media_preview_like"]["count"]]
# try:
#     res3 = [posts["location"]["id"], posts["location"]["name"]]
# except TypeError:
#     res3 = ['','']
# res = res0 + res1 + res2 + res3

# res = json_normalize(dict(zip(cols, res)))
# df = df.append(res,ignore_index=True, sort=False)


# print(df)
