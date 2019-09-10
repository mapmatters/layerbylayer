import requests
import time
import json

arr = []
end_cursor = '' # empty for the 1st page
tag = 'choiza11' # your tag
page_count = 5 # desired number of pages

url = "https://www.instagram.com/{0}/?__a=1&max_id={1}".format(tag, end_cursor)
r = requests.get(url)
data = json.loads(r.text)
# print(data)
# print(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)[:20000])

var1 = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
i = 1
post = var1[i]["node"]
text = var1[i]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
location = var1[i]["node"]["location"]["id"]
# print(json.dumps(var1[3], ensure_ascii=False, sort_keys=True, indent=4))
print(len(var1)) # 게시물 갯수
print(json.dumps(post,ensure_ascii=False, sort_keys=True, indent=4))
print(text)
print(location)
# 문자열
# key가 json_string인 문자열 가져오기
# json_string = data["logging_page_id"]
# print(json_string)

# 숫자
# key가 json_number인 숫자 가져오기
# json_string2 = json_string["user"]
# print(json_string2)
# print(str(json_number)) # 숫자이기 때문에 str()함수를 이용

# # 배열
# # key가 json_array인 배열 가져오기
# json_array = json_data["json_array"]
# print(json_array)

# # 객체
# # key가 json_object인 객체 가져와서 만들기
# # json object의 경우에 python ojbect로 바꿀때는 따로 처리를 해줘야합니다.
# # 기본형은 dictionary입니다.
# json_object = json_data["json_object"]
# print(json_object)

# # bool형
# # key가 json_bool인 bool형 자료 가져오기
# json_bool = json_data["json_bool"]
# print(json_bool)
