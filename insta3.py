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
browser = webdriver.Chrome('/Users/yongjae/Downloads/chromedriver') # 'type chromedriver' in cmd
browser.get('https://www.instagram.com/'+username+'/?hl=en')


Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight/1.5);")

links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('span')
for link in script.findAll('a'):
     if re.match("/p", link.get('href')):
        links.append('https://www.instagram.com'+link.get('href'))

# time.sleep(5)

# Pagelength = browser.execute_script("window.scrollTo(document.body.scrollHeight/1.5, document.body.scrollHeight/3.0);")

# source = browser.page_source
# data=bs(source, 'html.parser')
# body = data.find('body')
# script = body.find('span')
# for link in script.findAll('a'):
#      if re.match("/p", link.get('href')):
#         links.append('https://www.instagram.com'+link.get('href'))

with open('links_list', 'wb') as fp:
    pickle.dump(links, fp)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(links)



# page = urlopen(links[0]).read()

# result=pd.DataFrame()
# for i in range(len(links)):
#     try:
#         page = urlopen(links[i]).read()
#         data=bs(page, 'html.parser')
#         body = data.find('body')
#         script = body.find('script')
#         raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
#         json_data=json.loads(raw)
#         posts =json_data['entry_data']['PostPage'][0]['graphql']
#         posts= json.dumps(posts)
#         posts = json.loads(posts)
#         x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
#         x.columns =  x.columns.str.replace("shortcode_media.", "")
#         result=result.append(x)
       
#     except:
#         np.nan
# Just check for the duplicates
# result = result.drop_duplicates(subset = 'shortcode')
# result.index = range(len(result.index))
# pp.pprint(result)