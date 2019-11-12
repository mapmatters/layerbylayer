# https://data-newbie.tistory.com/206 영어전처리

import os
import glob
import pandas as pd
import re
import numpy as np
from datetime import date, datetime
from langdetect import detect
from langdetect import detect_langs

# pd.read_csv(sio, dtype={"user_id": int, "username": object})
# or --- https://codeday.me/ko/qa/20190403/188294.html
# headers = ['col1', 'col2', 'col3', 'col4']
# dtypes = ['datetime', 'datetime', 'str', 'float']
# pd.read_csv(file, sep='\t', header=None, names=headers, dtype=dtypes)

path='/home/yong_inline/files/post_info/'
files = glob.glob(path+"raw_files_2/post_info_*.csv") 
today = datetime.now().strftime("%Y%m%d")

df_list = []
for filename in sorted(files):
    df_list.append(pd.read_csv(filename))
df = pd.concat(df_list) ; len(df)
df = df[~df['text'].isna()] ; len(df)
df = df[df['is_ad']==False] ; len(df)
df = df.reset_index()

df.to_csv(path+'merge/posts_'+today+'_raw.csv', index=False)

try:
    df = df.drop(['index','Unnamed: 0','tracking_token'], axis=1)
except KeyError:
    df = df.drop(['index','Unnamed: 0'], axis=1)



def detect_func(lyrics):
    try:
        return detect(lyrics)
    except:
        return 'cannot_detect'

def text_munging(df):
    # raw text munging
    # 줄바꿈, 탭 제거
    df['text'] = df['text'].str.replace("\n", " ").replace("\t"," ")
    df['text'] = df['text'].apply(lambda x: x.strip())
    df['text_raw'] = df['text']
    df['text_len'] = df['text'].str.len()
    
    # 사람이 태깅된 단어 -> '@__usr__' 로 치환
    df['text'] = df['text'].str.replace('@([0-9a-zA-Z가-힣_]*)',"@__usr__")
    
    # language detection
    df['lang'] = df['text'].apply(detect_func) 

def hashtag_extract(df):    
    # hashtag 추출하기
    pattern = '#([0-9a-zA-Z가-힣_]*)' 
    hash_w = re.compile(pattern)
    df['hashtag'] = df['text'].apply(lambda x: hash_w.findall(str(x)))
    df['hashtag'] = df['hashtag'].apply(lambda x: [k for k in x if k]) #공백문자 제거
    df['hashtag_num'] = df['hashtag'].apply(lambda x: len(x))
    df_text = df[['loc_id','loc_name','text','text_len','hashtag','hashtag_num']]
    return df, df_text

text_munging(df)
# hashtag_extract(df)

df.to_csv(path+'merge/posts_'+today+'_munging.csv', index=False)
df = pd.read_csv(path+'merge/posts_'+today+'_munging.csv', encoding='utf-8', engine='python')

df_grp = df[['loc_name','text','lang']].groupby(['loc_name','lang']).count().sort_values('text', ascending=False)

# 장소별 갯수
pd.pivot_table(df, index=['loc_name','loc_id','lang'], aggfunc='count').text



# df[['loc_name','lang','text','hashtag']][10010:10011]

# df[['loc_name','index']].groupby('loc_name').count().sort_values('hashtag',ascending=False)

# df[['text_raw','tmp']].head(20)
# df.groupby('tmp').count().sort_values('index',ascending=False).head(10)
# df['tmp2'] = df['tmp'].apply(lambda x: x.detect_language())

# df2['hashtag'] = df2['hashtag'].apply(lambda x: np.array(x))
# type(df2['hashtag'])


# df2 = df_text[df_text['hashtag_num']>0]

# grouped = df2.groupby(df2['hashtag_num'])
# grouped.count()

import google.cloud.bigquery.magics
google.cloud.bigquery.magics.context.use_bqstorage_api = True
from google.cloud import bigquery
import pandas_gbq as gbq
from google.cloud.bigquery import Client, SchemaField
from google.oauth2 import service_account
import google.auth
credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

bqclient = bigquery.Client(
    credentials=credentials,
    project=your_project_id,
)
bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient(
    credentials=credentials
)

df.to_gbq('lbl.post_info_temp', 'supple-design-237807',if_exists='append')



credentials = ...  # From google-auth or pydata-google-auth library.

# Update the in-memory credentials cache (added in pandas-gbq 0.7.0).
pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "your-project-id"

# The credentials and project_id arguments can be omitted.
df = pandas_gbq.read_gbq("SELECT my_col FROM `my_dataset.my_table`")