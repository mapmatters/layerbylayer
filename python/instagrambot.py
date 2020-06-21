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

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("disable-gpu")


class InstagramBot():
    def __init__(self, email, password):
        self.driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
        self.email = email
        self.password = password

    def signIn(self):
        self.driver.get('https://www.instagram.com/accounts/login/?hl=en')
        time.sleep(2)
        emailInput = self.driver.find_elements_by_css_selector('form input')[0]
        passwordInput = self.driver.find_elements_by_css_selector('form input')[1]
        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def collectItems(self, link_type, user_or_tag_or_loc, num_of_links):
        if link_type=='user':
            self.driver.get('https://www.instagram.com/'+user_or_tag_or_loc+'/?hl=en')
        elif link_type=='tag':
            self.driver.get('https://www.instagram.com/explore/tags/'+user_or_tag_or_loc+'/?hl=en')
        elif link_type=='loc':
            self.driver.get('https://www.instagram.com/explore/locations/'+user_or_tag_or_loc+'/?hl=en')
            # 486650968033082 신촌
        else:
            print("type first arg as 'user' or 'tag'. (ex. python3 s1_links.py user choiza11)")
            sys.exit(0)
        links=[]
        # num_of_post = self.driver.find_element(By.CLASS_NAME, "g47SY").text.replace(",","")
        time.sleep(5)
        cols = ['post_link','img_alt','img_link']
        df = pd.DataFrame(columns = cols)
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            post_list = self.driver.find_elements_by_css_selector('article a')
            for post in post_list:
                href = post.get_attribute("href")
                imgs = post.find_elements_by_css_selector('img')
                for img in imgs:
                    imgalt = img.get_attribute("alt")
                    srcset = img.get_attribute("srcset")
                    res = [href, imgalt, srcset]
                    print(img.get_attribute("alt"), "\n")
                    res = json_normalize(dict(zip(cols, res)))
                    df = df.append(res,ignore_index=True, sort=False)
                    df = df.drop_duplicates()
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            len_links = len(df.post_link.unique())
            if new_height == last_height:
                break
            last_height = new_height
            if len_links > int(num_of_links):
                break

        print(len_links)

        today = datetime.now().strftime("%Y%m%d")
        filenm = link_type+"_"+user_or_tag_or_loc+"_posts_links_imgalt_src_"+today+".csv"
        df.to_csv(filenm, mode='w')

    def collectPostInfo(self, fileload, foldernm, num_of_i):
        links = pd.read_csv(fileload)
        links = links.post_link.unique()
        cols = ['link','username', 'user_id', 'fullname', 'id', 'shortcode', 'display_url', 'tracking_token', 'taken_at_timestamp','is_video','is_ad','text', 'like_count', 'loc_id', 'loc_name']
        df = pd.DataFrame(columns = cols)
        for i in range(int(num_of_i), len(links)):
            lk = links[i]
            self.driver.get(lk)
            time.sleep(2)
            if self.driver.find_element(By.CSS_SELECTOR, "body").get_attribute('class') == ' p-error dialog-404':
                today = datetime.now().strftime("%Y%m%d")
                filenm = foldernm+"/post_info_to__"+str(i)+"__"+today+".csv"
                df.to_csv(filenm, mode='w')
                df.drop(df.index, inplace=True)
                continue
            page = self.driver.page_source
            # page = urlopen(lk).read()
            data = bs(page, 'html.parser')
            body = data.find('body')
            script = body.find('script')
            raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
            json_data = json.loads(raw)
            posts = json_data['entry_data']['PostPage'][0]['graphql']
            posts = json.dumps(posts, ensure_ascii=False)
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
            print(i, 0 < i and 0 == i%10)
            if 0 < i and 0 == i%10:
                today = datetime.now().strftime("%Y%m%d")
                filenm = foldernm+"/post_info_to__"+str(i)+"__"+today+".csv"
                df.to_csv(filenm, mode='w')
                df.drop(df.index, inplace=True)
                time.sleep(20)


    def closeBrowser(self):
        self.driver.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()

bot = InstagramBot(sys.argv[1], sys.argv[2])
bot.collectItems(sys.argv[3], sys.argv[4], sys.argv[5])
bot.closeBrowser()

# 예시
bot = InstagramBot('matmatters', 'password')
bot.signIn()
bot.collectItems('loc', '486650968033082', '1000')
bot.closeBrowser()
