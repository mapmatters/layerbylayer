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
import os
import datetime
import shutil
import glob

pp = pprint.PrettyPrinter(indent=4)

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('window-size=1000x500')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
#options.add_argument("disable-gpu")

class campinginfo(object):
    def __init__(self):
#         self.df = df
#         self.kwe_col = kwd_col
        self.chrome_path = '/usr/local/bin/chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('window-size=1000x500')
        self.options.add_argument("start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("disable-gpu")
        
        self.path1 = "../file/campsite_list_raw.csv"
        self.path2 = "../file/campsite_list_modify.csv"
        self.url_1 = 'https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=2500&searchKrwd=&listOrdrTrget=last_updusr_pnttm&pageIndex=1'
        

    def get_siteinfo(self):
        driver = webdriver.Chrome(self.chrome_path, options=self.options)
        driver.get(self.url_1) 

        time.sleep(10)
        source = driver.page_source 
        data = bs(source, 'html.parser')
        cont = data.findAll("div",{"class":"camp_cont"})

        cols = ['name','url','addr']
        df = pd.DataFrame(columns=cols)
        prefix = 'https://www.gocamping.or.kr'
        for i in range(len(cont)):
            name = cont[i].h2.a.get_text().split("]")[1]
            url_t = cont[i].h2.a['href'].split("&")[0]
            url = ''.join([prefix,url_t])
            addr = cont[i].ul(class_="addr")[0].get_text()

            info = [name, url, addr]
            dict1 = dict(zip(cols, info))
            df = df.append(dict1, ignore_index=True)

        df['name'] = df.name.str.strip()
        driver.quit()
        return df

        
    def get_sitexy(self):
        limit_ = 1000
        driver = webdriver.Chrome(self.chrome_path, options=self.options)
        cols = ['name','addr', 'call_num','coord_x','coord_y']
        df = pd.DataFrame(columns=cols)

        for i in range(1,4):
            url_2 = 'https://www.gocamping.or.kr/bsite/camp/info/list.do?listTy=MAP&pageUnit={limit}&searchKrwd=&listOrdrTrget=last_updusr_pnttm&pageIndex={page}'.format(limit=limit_, page=i)
            driver.get(url_2) 
            time.sleep(3)
            source = driver.page_source 
            data = bs(source, 'html.parser')
            cont = data.findAll("div", {"class":"map_list"})[0]
            ul = cont.ul.select("li[onclick]")

            for j in range(len(ul)):
                camp = ul[j]
                xy = camp['onclick']
                x = re.findall('[0-9]*[0-9]\.[0/-9]*[0-9]', xy)[1]
                y = re.findall('[0-9]*[0-9]\.[0/-9]*[0-9]', xy)[0]
                name = camp.h2.text.split(']')[1].strip()
                addr = camp.find("li", {"class":"addr"}).get_text()
                call_num = camp.find("li", {"class":"call_num"}).get_text() if camp.find("li", {"class":"call_num"}) else ""
                val_list = [name, addr, call_num, x, y]
                result = dict(zip(cols, val_list))
                df = df.append(result, ignore_index=True)
            print(df.tail(2))
        df.to_csv(self.path1)
        driver.quit()
        return df
    
    def modify_table(self, df):
        def name_for_tag(x):
            if x=="Najost Camp": return "나조스트캠핑장"
            elif x=="iFA캠프운악": return "캠프운악"
            elif x=="Black tree": return "블랙트리캠핑장"
            elif x=="영천 구룡산 오토&펜션": return "영천구룡산오토캠핑장"
            elif x=="(주)자연에너지-드림랜드오토캠핑장": return "드림랜드오토캠핑장"
            elif x=="소회산리멍우리협곡관광농원(캠핑장)": return "멍우리협곡캠핑장"
            elif x=="춘천Believing(빌리빙)캠핑장": return "춘천빌리빙캠핑장"
            elif x=="변산반도국립공원 고사포 야영장 (임시)": return "고사포야영장"
            elif x=="A&J오토캠핑장": return "AJ오토캠핑장"
            elif x=="Camp 1950 by 민들레울": return "camp1950"
            elif x=="(주)자연인": return "자연인글램핑"
            elif x=="(주)수동자연마을 힐링별밤수목원캠핑장": return "힐링별밤수목원캠핑장"
            elif x=="stay714": return "스테이714"
            elif x=="선녀와나무꾼": return "선녀와나무꾼캠핑장"
            elif x=="블루스카이": return "블루스카이캠핑장"
            elif x=="CLUB 596": return "클럽596"
            elif x=="비토애": return "비토애글램핑"
            elif x=="(주)연합진흥 경도 글램핑파크": return "경도글램핑파크"
            elif x=="(주)태평소금 천일염 힐링캠프": return "천일염힐링캠프"
            elif x=="누룽지": return "누룽지캠핑장"
            elif x=="포시즌": return "포시즌캠핑장"
            elif x=="마이웨이 리조트 관광": return "마이웨이리조트"
            elif x=="바오바오": return "바오바오글램핑" 
            elif x=="블루마운틴": return "팔공산블루마운틴" 
            elif x=="별헤는 밤": return "별헤는밤캠핑장"
            elif x=="선녀와 나무꾼": return "선녀와나무꾼캠핑장"
            elif x=="테르메덴": return "테르메덴카라반"
            elif x=="캠프통 아일랜드": return "캠프통아일랜드글램핑"
            elif x=="포세이돈": return "포세이돈카라반"# 2266	(주)포세이돈	20904
            elif x=="노을캠핑장": return "강화노을캠핑장"# 1005	노을캠핑장	18276

            elif "&" in x: return re.sub("&","앤", x)
            elif re.search("\(.*\)", x): return re.sub("\(.*\)","", x)
            else: return x
        df["hashtag"] = df["name"].apply(name_for_tag)
        df["hashtag"] = df["hashtag"].apply(name_for_tag)
        df["hashtag"] = df["hashtag"].apply(lambda x: x.replace(" ","").strip())
        to_drop = ['산책','선인장','부에노스아이레스','가온','캐빈','숲속의 작은집','생각속의 집', '풍경']
        df = df[~df.name.isin(to_drop)]
        df.reset_index(drop=True, inplace=True)
        df.to_csv(self.path2)
        return df
    
#     def append_csv(file_name, dict_):
#         with open(file_name, 'r+b') as f:
#             header = next(csv.reader(f))
#             dict_writer = csv.DictWriter(f, header, -999)
#             dict_writer.writerow(dict_)
        
    def get_postnum(self, df, k=0):
        def append_csv(file_name, dict_):
            with open(file_name, 'r+t') as f:
                header = next(csv.reader(f))
                dict_writer = csv.DictWriter(f, header, -999)
                dict_writer.writerow(dict_)
            
        cols = list(df.columns) + ['num_index', 'search_order', 'search_rslt', 'url','text','dt']
        df_out = pd.DataFrame(columns=cols)
        today_ymd = datetime.datetime.today() .strftime('%Y%m%d')
        filepath = '../file/camping_' + today_ymd + '_' + str(k) +'.csv'
        df_out.to_csv(filepath, index=False)

        driver = webdriver.Chrome(self.chrome_path, options=self.options)
        url = 'https://www.instagram.com/explore/tags/'+'캠프운악'
        driver.get(url) 

        time.sleep(3)

        t = driver.find_elements_by_css_selector("input[placeholder='Search']")[0]

        for i in range(k,len(df)):
            print(i, end=" ")
            t.send_keys(df.iloc[i]['hashtag'])
            time.sleep(1.5)
            t2 = driver.find_elements_by_class_name("yCE8d")
            if len(t2)>0:
                for j in range(len(t2)):
                    ref = t2[j].get_attribute('href')
                    title = t2[j].text.split("\n")[0]
                    txt = t2[j].find_elements_by_class_name("Fy4o8")[0].text
                    info = list(df.iloc[i,:]) + [i, j, title, ref, txt, today_ymd]
                    dict1 = dict(zip(cols, info))
                    append_csv(filepath, dict1)
#                     df_out = df_out.append(dict1, ignore_index=True)
            else:
                pass
            t.clear()
            if i>0 and i%100 == 0:
                print()
                print(df_out.tail(2))
                time.sleep(3)
        driver.quit()
        df_out.head(20)

#         df_out.to_csv('../file/camping_' + today_ymd + '.csv', index=False)
        return df_out
    
a = campinginfo()
campxy = a.get_sitexy()
campxy = a.modify_table(campxy)
time.sleep(3)
camp_post = a.get_postnum(campxy)