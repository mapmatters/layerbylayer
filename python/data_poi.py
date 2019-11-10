# !pip3 install shapely #==1.5.17.post1
# !pip3 install geopandas #==0.2.1
# !pip3 install geojsonio #==0.0.3
# !pip install pyproj
# !pip install geojson
# !pip install geopy

from pandas.io.json import json_normalize
import folium
import json
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon
import geopandas as gpd
import geojsonio
from geopy.geocoders import Nominatim 
import requests
import urllib.request
from pyproj import Proj, transform
from geojson import Feature, FeatureCollection, Point
import subprocess
import pprint as pp
import time

# data load from google storage
project_id = 'supple-design-237807'
bucket_name = 'geodata_fs'

cmd1 = "gsutil cp gs://{}/seoul_bas_polygon.geojson /home/yong_inline/data/seoul_bas_polygon.geojson".format(bucket_name)
subprocess.call(cmd1, shell=True)

bas = gpd.read_file('/home/yong_inline/data/seoul_bas_polygon.geojson')
print(bas.head())

# --- get radius of each block, and save it then load it --- #
# centroid
bas['coord_x'] = bas['geometry'].centroid.x
bas['coord_y'] = bas['geometry'].centroid.y
# projection change
bas = bas.to_crs({'init': 'epsg:3857'})
# bounding box
bas['bbox'] = bas['geometry'].envelope
# max / min point in bounding box -> get distance with meter
bas['maxpt'] = gpd.points_from_xy(bas.geometry.bounds.maxx, bas.geometry.bounds.maxy)
bas['minpt'] = gpd.points_from_xy(bas.geometry.bounds.minx, bas.geometry.bounds.miny)
bas['dist_minmax'] = bas.apply(lambda r: r['maxpt'].distance(r['minpt']), axis=1)
# 다시 wgs84로 변환
bas = bas.to_crs({'init': 'epsg:4326'})
# file로 저장
bas.drop(['bbox','maxpt','minpt'], axis=1).to_file("/home/yong_inline/data/seoul_bas_polygon_modified.geojson", driver='GeoJSON')
cmd2 = "gsutil cp /home/yong_inline/data/seoul_bas_polygon_modified.geojson gs://{}/".format(bucket_name)
subprocess.call(cmd2, shell=True)
# 저장한 file 다시 불러오기
cmd3 = "gsutil cp gs://{}/seoul_bas_polygon_modified.geojson /home/yong_inline/data/seoul_bas_polygon_modified.geojson".format(bucket_name)
subprocess.call(cmd3, shell=True)
bas = gpd.read_file('/home/yong_inline/data/seoul_bas_polygon_modified.geojson')

# --- Foursquare 로부터 POI 정보 수집 --- #

# 강남구만 대상으로 테스트
CLIENT_ID = '30I5VMOG2YB4S1AL2CEPIEZOL2DRYSL1LBMVLEAOX1PXTAYB' # your Foursquare ID
CLIENT_SECRET = 'DK5XSRLY5HCGV0YUTCKFSKJIEYKHSIBWQNAXP1GEJLZICX0A' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 500

# 데이터 추출
url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    bas['coord_y'][20], 
    bas['coord_x'][20], 
    int(bas['dist_minmax'][0]/2), 
    LIMIT)
results = requests.get(url).json()
venues = results['response']['groups'][0]['items']
venues = json_normalize(venues)
colnms = list(venues.columns.values)

sig = list(bas.SIG_CD.unique())

# 구별 file 저장하기
for code in sig:
    print(code)
    print('\n')
    masterDF = pd.DataFrame(columns = colnms)
    df_t = bas[bas.SIG_CD == code].reset_index()
    for i in range(len(df_t)):
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
        CLIENT_ID, 
        CLIENT_SECRET, 
        VERSION, 
        df_t['coord_y'][i], 
        df_t['coord_x'][i], 
        int(df_t['dist_minmax'][i]/2), 
        LIMIT)
        try:
            results = requests.get(url).json()
        except JSONDecodeError:
            continue
        try:
            venues = results['response']['groups'][0]['items']
            tempDF = json_normalize(venues)
        except KeyError:
            continue

        masterDF = masterDF.append(tempDF,ignore_index=True, sort=False)

    # 파일 저장하기
    df = masterDF.drop_duplicates(['venue.id'], keep='last')
    df = df.fillna('') # NaN을 없애야 json으로 저장할 수 있음

    # category 정보 뽑아내기
    df['category_id'] = [x[0]['id'] for x in df['venue.categories']]
    df['category_name'] = [x[0]['name'] for x in df['venue.categories']]
    df['category_shortName'] = [x[0]['shortName'] for x in df['venue.categories']]

    # 필요한 컬럼만 남김
    df = df[['venue.id', 'venue.location.address','venue.location.cc', 'venue.location.lat', 'venue.location.lng', 'venue.name','category_id','category_name','category_shortName']]
    
    print(df.head())
    # geopandas 형태로 변환
    df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['venue.location.lng'], df['venue.location.lat']))
    df.to_file("/home/yong_inline/data/poi/seoul/points_sigcd_"+code+".geojson", driver='GeoJSON')
    time.sleep(10)


# 각 구별로 따로 돌리기

code = '11305'
masterDF = pd.DataFrame(columns = colnms)
df_t = bas[bas.SIG_CD == code].reset_index()
for i in range(len(df_t)):
    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    df_t['coord_y'][i], 
    df_t['coord_x'][i], 
    int(df_t['dist_minmax'][i]/2), 
    LIMIT)
    results = requests.get(url).json()
    # results = requests.get(url)
    # results = json.loads(response.content.decode('utf-8'))
    # try:
    #     results = requests.get(url).json()
    # except JSONDecodeError:
    #     continue
    try:
        venues = results['response']['groups'][0]['items']
        tempDF = json_normalize(venues)
    except KeyError:
        continue
    masterDF = masterDF.append(tempDF,ignore_index=True, sort=False)

# 파일 저장하기
df = masterDF.drop_duplicates(['venue.id'], keep='last')
df = df.fillna('') # NaN을 없애야 json으로 저장할 수 있음

# category 정보 뽑아내기
df['category_id'] = [x[0]['id'] for x in df['venue.categories']]
df['category_name'] = [x[0]['name'] for x in df['venue.categories']]
df['category_shortName'] = [x[0]['shortName'] for x in df['venue.categories']]

# 필요한 컬럼만 남김
df = df[['venue.id', 'venue.location.address','venue.location.cc', 'venue.location.lat', 'venue.location.lng', 'venue.name','category_id','category_name','category_shortName']]

print(df.head())
# geopandas 형태로 변환
df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['venue.location.lng'], df['venue.location.lat']))
df.to_file("/home/yong_inline/data/poi/seoul/points_sigcd_"+code+".geojson", driver='GeoJSON')

sig
code

