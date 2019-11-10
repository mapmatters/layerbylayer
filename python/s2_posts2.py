import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
import pandas as pd
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import pickle 
import csv
import pprint
import requests
import glob
from datetime import date, datetime
import os

# if not os.path.exists(dirname):
#             os.makedirs(dirname)

pp = pprint.PrettyPrinter(indent=4)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("disable-gpu")

chrome_path = '/usr/bin/chromedriver'

strart_i = int(sys.argv[1])
export_folder = sys.argv[2]

files_path = '../files/'
filenames = glob.glob(files_path + "post_urls/post_*.csv")
dfs = pd.DataFrame()
df_list = []
for filenm in filenames:
    df_each = pd.read_csv(filenm,index_col=None, header=0)
    df_list.append(df_each)

dfs = pd.concat(df_list)
dfs = dfs.reset_index()

cols = ['link','username', 'user_id', 'fullname', 'id', 'shortcode', 'display_url', 'taken_at_timestamp','is_video','is_ad','text', 'like_count', 'loc_id', 'loc_name']
df = pd.DataFrame(columns = cols)
driver = webdriver.Chrome(chrome_path, options=options)

today = datetime.now().strftime("%Y%m%d")
url_len = len(dfs.url)
for i in range(strart_i, url_len):
    lk = dfs.url[i]
    driver.get(lk)
    time.sleep(2)
    # 삭제된 게시물이면 skip
    if driver.find_element(By.CSS_SELECTOR, "body").get_attribute('class') == ' p-error dialog-404':
        continue
    page = driver.page_source
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
    res1 = [posts[i] for i in cols[4:10] if i in posts]
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
    df = df.append(res,ignore_index=True)
    # 마지막 게시물이면 저장
    if i == url_len-1:
        filenm = files_path+"post_info/"+export_folder+"/post_info_to__"+str(i)+"__"+today+".csv"
        df.to_csv(filenm, mode='w')
    # 10개가 차면 저장
    if i > 0 and 0 == i%10:
        print(df.tail(3))
        print(str(i)+'/'+str(url_len))
    # 100개 단위로 차면 chrome 재시작
    if i > 0 and 0 == i%200:
        filenm = files_path+"post_info/"+export_folder+"/post_info_to__"+str(i)+"__"+today+".csv"
        df.to_csv(filenm, mode='w')
        df.drop(df.index, inplace=True)
        driver.quit()
        time.sleep(61)
        driver = webdriver.Chrome(chrome_path, options=options)


driver.quit()

print(df.head())
print(df.tail())
print(len(df))
