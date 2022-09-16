import encodings
from encodings.utf_8 import encode
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import multiprocessing
import os

option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument('--dosavle--gpu')
# processnum=3
# drivers = ['driver'+str(i) for i in range(processnum)]
# driver= [webdriver.Chrome(executable_path='./chromedriver', chrome_options=option) for i in range(processnum)]
# print('open')



URL = 'https://www.ewg.org/skindeep/'
with open('kqcData.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
keys = [key for key in json_data]

def croling(data_dict, count_dict):
    print('driver start')
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)
    while count_dict['count'] < len(keys):
        print('croling', count_dict['count'])
        key = keys[count_dict['count']]
        count_dict['count'] += 1
        driver.get(url=URL)
        search_box = driver.find_elements('xpath','//INPUT[@id="search"]')[2]
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
            post_data['score'] = score1
            data_dict[key]=post_data
            print("success")

        except:
            count_dict['errcount'] += 1
            print("err:", count_dict['errcount'])
        time.sleep(2)


if __name__ == '__main__':
    start = time.time()
    data = multiprocessing.Manager().dict()
    count_dict = multiprocessing.Manager().dict()
    count_dict['count'] = 0
    count_dict['errcount'] = 0
#     errcount = 0
#
#     count = 0

    process = []

    # while count<len(keys):
    for i in range(16):
        p = multiprocessing.Process(target = croling, args = (data, count_dict))
        process.append(p)
        p.start()

    for p in process:
        p.join()

    print(count_dict['count'], count_dict['errcount'])
    print(time.time()- start)







