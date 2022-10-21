import encodings
from encodings.utf_8 import encode
from itertools import count
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import multiprocessing
import os
from selenium.webdriver.common.by import By


option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument('--dosavle--gpu')

URL = 'https://www.aspca.org/pet-care/animal-poison-control/dogs-plant-list'
'''driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url=URL)
login = driver.find_element('xpath', '//*[@id="__next"]/div/div/div[1]/div[1]/div/div/div[2]/div[4]/div')
login.click()
id = driver.find_element('xpath','//*[@id="__next"]/div/div/main/div/div/div/form/div[1]/input')
id.send_keys('hso@klapoo.com')
pw = id = driver.find_element('xpath','//*[@id="__next"]/div/div/main/div/div/div/form/div[2]/input')
pw.send_keys('@winhk0416')
time.sleep(3)
pw.send_keys(Keys.RETURN)'''

#전체데이터 저장

def croling(data, count_dict, processnum):
    
    count=0
    print('driver start')
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)
    driver.get(url=URL)
    ingredients = driver.find_elements('xpath', '//*[@id="content"]/div[2]/div/div/div/div/div[2]/div')
    #ingredients = driver.find_element('xpath', '//*[@id="site-name"]/a')
    
    print(len(ingredients))
    ingredientcount = len(ingredients)
    try: 
        xpath = '//*[@id="content"]/div[2]/div/div/div/div/div[2]/div'
        for ingredient in range(ingredientcount):
            flag=0
            Name = driver.find_element('xpath', xpath+'['+str(ingredient+1)+']/div/span/a').text.replace('’', '\'')
            sName = driver.find_element('xpath', xpath+'['+str(ingredient+1)+']/div/span/i').text.replace('’', '\'')
            pair_data = {'normal': Name, 'scientific': sName}
            data.append(pair_data)
            count_dict['awscount'] += 1
        if(flag==0):
            count_dict['errcount'] += 1
            #print("err:", count_dict['errcount'])
    except: 
        count_dict['errcount'] += 1
        #print("err:", count_dict['errcount'])
    print('aswcount:', count_dict['awscount'],'errcount: ', count_dict['errcount'])
    
if __name__ == '__main__':
    start = time.time()
    data = multiprocessing.Manager().list()
    count_dict = multiprocessing.Manager().dict()
    count_dict['count'] = 0
    count_dict['errcount'] = 0
    count_dict['awscount'] = 0
#     errcount = 0
#
#     count = 0

    process = []

    # while count<len(keys):
    for i in range(1):
        p = multiprocessing.Process(target = croling, args = (data, count_dict, i))
        process.append(p)
        p.start()

    for p in process:
        p.join()
    print(data)
    data=list(data)
    df = pd.DataFrame(data)
    df.to_csv("aspca_toxic_data.csv", header=None, index=None)
    print(count_dict['count'], count_dict['errcount'])
    print(time.time()- start)
    
