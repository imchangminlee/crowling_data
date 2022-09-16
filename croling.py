import encodings
from encodings.utf_8 import encode
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


with open('kqcData.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

keys = [key for key in json_data]
print("lenkey:", len(keys))


URL = 'https://www.ewg.org/skindeep/'
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url=URL)
#전체데이터 저장
data={}
errcount=0

for idx ,key in enumerate(keys[:]):
    search_box = driver.find_elements('xpath','//INPUT[@id="search"]')[2]
    print(key, "전체", idx)
    search_box.clear()
    search_box.send_keys(key)
    search_box.send_keys(Keys.RETURN)
    try:
        post = driver.find_elements('xpath','//*[@class="product-listings content-max-width"]/div[1]/div[2]/div/a')
        post[0].click()
        
        posts = driver.find_elements('xpath', '//*[@id="chemical"]/div[1]/div[3]/section/section/ul/li')
        post_data={}
        #common concerns
        danger=posts[0].find_elements('xpath', '//*[@class="concern"]/div[1]')
        type_danger=posts[0].find_elements('xpath', '//*[@class="concern"]/div[2]')
        for i in range(len(danger)):
            post_data[type_danger[i].text]=danger[i].text
        #data:limited
        post = driver.find_element('xpath', '//*[@id="chemical"]/div[1]/div[3]/div[1]/div[1]/p')
        post_data['data']=post.text.split(': ')[1]
        #image
        post = driver.find_element('xpath', '//*[@id="chemical"]/div[1]/div[3]/div[1]/div[1]/a/img')
        src = post.get_attribute('src')
        score = src.split('=')[1].split('&')[0]
        scoremin = src.split('=')[2]
        if(score==scoremin):
            score1=score
        else:
            score1 = scoremin + '-' + score
        print(score1)
        post_data['score'] = score1
        data[key]=post_data
        driver.get(url=URL)

    except: 
        driver.get(url=URL)
        errcount=errcount+1
        print("err:", errcount)
    time.sleep(2)

file_path='./kqcData1.json'
with open(file_path, 'w') as outfile:
    json.dump(data, outfile)
print(errcount, '/', len(keys))

