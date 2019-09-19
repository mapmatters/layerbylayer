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
import pickle 
import pprint
pp = pprint.PrettyPrinter(indent=4)

with open ('links_list', 'rb') as fp:
    links = pickle.load(fp)

set_links = set(links)
links = list(set_links)
pp.pprint(links[0])

page = urlopen(links[0]).read()
data=bs(page, 'html.parser')
body = data.find('body')
script = body.find('script')
raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
json_data=json.loads(raw)
posts =json_data['entry_data']['PostPage'][0]['graphql']
posts= json.dumps(posts, ensure_ascii=False)
posts = json.loads(posts)

# basic information
links[0]
posts["shortcode_media"]["id"]
posts["shortcode_media"]["shortcode"]
posts["shortcode_media"]["display_url"]
posts["shortcode_media"]["tracking_token"]
posts["shortcode_media"]["taken_at_timestamp"]
posts["shortcode_media"]["is_video"]
# text , like count
text = posts["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
like = posts["shortcode_media"]["edge_media_preview_like"]["count"]
# location -> "https://www.instagram.com/explore/locations/"+loc_id
posts["shortcode_media"]["location"]
loc_id = posts["shortcode_media"]["location"]["id"]#["country_code"]
loc_name = posts["shortcode_media"]["location"]["name"]




pp.pprint(posts["shortcode_media"].keys())
json.dumps(posts, ensure_ascii=False)

edges = posts["shortcode_media"].keys()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
text = edges[i]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
x.columns =  x.columns.str.replace("shortcode_media.", "")