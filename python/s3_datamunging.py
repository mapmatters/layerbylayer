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

path='/home/yong_inline/frint/files/post_info/'
files = glob.glob(path+"raw_files/post_info_*.csv") 
df_list = []
for filename in sorted(files):
    df_list.append(pd.read_csv(filename))
df = pd.concat(df_list)
df = df[~df['text'].isna()]
df = df.reset_index()
df = df.drop(['index','Unnamed: 0'], axis=1)

today = datetime.now().strftime("%Y%m%d")

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

df.to_csv(path+'merge/posts_'+today+'.csv', index=False)
df = pd.read_csv(path+'merge/posts_'+today+'.csv')

df[['loc_name','lang','text','hashtag']][10010:10011]

df[['loc_name','index']].groupby('loc_name').count().sort_values('hashtag',ascending=False)

df[['text_raw','tmp']].head(20)
df.groupby('tmp').count().sort_values('index',ascending=False).head(10)
df['tmp2'] = df['tmp'].apply(lambda x: x.detect_language())

df2['hashtag'] = df2['hashtag'].apply(lambda x: np.array(x))
type(df2['hashtag'])


df2 = df_text[df_text['hashtag_num']>0]

grouped = df2.groupby(df2['hashtag_num'])
grouped.count()