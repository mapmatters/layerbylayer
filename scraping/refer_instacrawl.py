# https://gist.github.com/JosephMata/7c3bac580234a17102c2d3ba19822cd2

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

# add chrome option
options = webdriver.ChromeOptions()
# options.
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("disable-gpu")

#starting a new driver session
# driver = webdriver.Chrome('/Users/yongjae/Downloads/chromedriver', chrome_options=options) # 'type chromedriver' in cmd
driver = webdriver.Chrome('/usr/bin/chromedriver', options=options) # 'type chromedriver' in cmd

driver.get('https://www.instagram.com/?hl=en')
driver.set_window_size(1920, 1080)

# make sure the driver stays open for 5sec
sleep(3)

#clean exit


# #find Log in link
login_elem = driver.find_element_by_xpath(
	'//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')

#clicks log in
login_elem.click()

sleep(3)

driver.find_elements_by_name("username")[0].send_keys("yongjae__park")
element_password = driver.find_elements_by_name("password")[0]
element_password.send_keys("qkrtjqkd132!")
element_password.submit()
print("login success")
sleep(5)

# Not now click
# driver.find_element_by_xpath('//button[text()="Not Now"]').click()
WebDriverWait(driver, 10).\
until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Not Now"]'))).click()
print("")
# driver.find_element_by_xpath("/div[2]/div/div/div[2]/button[1]").click()
# driver.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']").click()

# sleep(5)
# driver.quit()
# # find form inputs and enter data
# inputs = driver.find_elements_by_xpath(
# 	'//*[@id="react-root"]/section/main/article/div[1]/div[1]/div/form/div[2]/div/label/input')

# print(inputs)

# inputs2 = driver.find_elements_by_xpath(
# 	'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')

# ActionChains(driver)\
#     .move_to_element(inputs[0]).click()\
#     .send_keys('yongjae__park')\
#     .move_to_element(inputs2[0]).click()\
#     .send_keys('qkrtjqkd132!')\
#     .perform()

sleep(5)

# # find the log in button and click it
# login_button = driver.find_element_by_xpath(
# 	'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button')

# #could have been part of the above actionchain
# ActionChains(driver)\
# .move_to_element(login_button)\
# .click().perform()
    
# search = driver.find_element_by_css_selector(
# 	'#react-root > section > nav > div._s4gw0._1arg4 > div > div > div._5ayw3._ohiyl > input')

# ActionChains(driver)\
# .move_to_element(search).click()\
# .send_keys('dylanwerneryoga')\
# .perform()

# name = driver.find_element_by_xpath(
# 	'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div')

# ActionChains(driver)\
# .move_to_element(name)\
# .click().perform()


# sleep(5)
# post = driver.find_element_by_class_name('_si7dy')
# post.click()




# load= driver.find_element_by_xpath(
# 	'/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a')

# while True:
# 	try:
# 		button = WebDriverWait(load, 5).until(EC.visibility_of_element_located((By.XPATH, 
#         	"/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a")))
# 	except TimeoutException:
# 		break  # no more wines
# 	button.click()  # load more comments



# csv_file = open('insta2.csv', 'wb')
# writer = csv.writer(csv_file)
# writer.writerow(['hashtag'])


# hash_dict = {}



# tag = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[4]/span").text
# hash_dict["hashtag"] = tag
# writer.writerow(hash_dict.values()) 


# driver.back()


	


# sleep(5)

# search = driver.find_element_by_css_selector(
# 	'#react-root > section > nav > div._s4gw0._1arg4 > div > div > div._5ayw3._ohiyl > input')

# ActionChains(driver)\
# .move_to_element(search).click()\
# .send_keys('laurasykora')\
# .perform()

# name = driver.find_element_by_xpath(
# 	'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div')

# ActionChains(driver)\
# .move_to_element(name)\
# .click().perform()



# sleep(5)
# post = driver.find_element_by_class_name('_si7dy')
# post.click()




# load= driver.find_element_by_xpath(
# 	'/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a')

# while True:
# 	try:
# 		button = WebDriverWait(load, 5).until(EC.visibility_of_element_located((By.XPATH, 
#         	"/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a")))
# 	except TimeoutException:
# 		break  # no more wines
# 	button.click()  # load more comments






# tag = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]").text
# hash_dict["hashtag"] = tag
# writer.writerow(hash_dict.values())



# driver.back()


# #############################



# sleep(5)

# search = driver.find_element_by_css_selector(
# 	'#react-root > section > nav > div._s4gw0._1arg4 > div > div > div._5ayw3._ohiyl > input')

# ActionChains(driver)\
# .move_to_element(search).click()\
# .send_keys('laurasykora')\
# .perform()

# name = driver.find_element_by_xpath(
# 	'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div')

# ActionChains(driver)\
# .move_to_element(name)\
# .click().perform()



# sleep(5)
# post = driver.find_element_by_class_name('_si7dy')
# post.click()




# load= driver.find_element_by_xpath(
# 	'/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a')

# while True:
# 	try:
# 		button = WebDriverWait(load, 5).until(EC.visibility_of_element_located((By.XPATH, 
#         	"/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a")))
# 	except TimeoutException:
# 		break  # no more wines
# 	button.click()  # load more comments



# tag = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]").text
# hash_dict["hashtag"] = tag
# writer.writerow(hash_dict.values())



# driver.back()


	
# csv_file.close()