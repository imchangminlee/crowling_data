import encodings
from encodings.utf_8 import encode
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import multiprocessing
import os

with open('kqcData.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

keys = [key for key in json_data]
print("lenkey:", len(keys))


URL = 'https://coos.kr/'
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url=URL)
login = driver.find_element('xpath', '//*[@id="__next"]/div/div/div[1]/div[1]/div/div/div[2]/div[4]/div')
login.click()
id = driver.find_element('xpath','//*[@id="__next"]/div/div/main/div/div/div/form/div[1]/input')
id.send_keys('hso@klapoo.com')
pw = id = driver.find_element('xpath','//*[@id="__next"]/div/div/main/div/div/div/form/div[2]/input')
pw.send_keys('@winhk0416')
time.sleep(3)
pw.send_keys(Keys.RETURN)

#전체데이터 저장
data={}
errcount=0
aswcount=0
for key in keys:
    driver.get(url=URL)
    try: 
        search_box = driver.find_element('xpath', '//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/input')
        search_box.send_keys(key.lower())
        time.sleep(2.5)
        ingredients = driver.find_elements('xpath', '//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div')
        ingredientcount = len(ingredients)
        xpath = '//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div'
        for ingredient in range(ingredientcount):
            flag=0
            t = driver.find_element('xpath', xpath+'[' + str(ingredient+1) + ']/div/div[2]')
            k = driver.find_element('xpath', xpath+'[' + str(ingredient+1) + ']/div/div[1]')
            if(t.text.lower()==key.lower() or k.text.lower()==key.lower()):
                flag=1
                element = driver.find_element('xpath', xpath+'[' + str(ingredient+1) + ']/div')
                element.click()
                time.sleep(3)

                krName = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]').text
                enName = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/div/div/div[2]/div[2]').text
                name = {'kr': krName, 'en': enName}

                print(name)
                ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/div[1]/p')
                #ewg정보가 제공되는 지 확인하는 코드 
                '''if(ewg.text=='SkinDeep 데이터가 제공되지 않는 성분입니다.'):
                    flag==0
                else:
                    ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/div/button')
                    ewg.click()
                    ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/div/div')'''
                aswcount += 1
                break
        if(flag==0):
            errcount += 1
    except: errcount += 1
    print('ingredientcount: ',ingredientcount,'aswcount:', aswcount,'errcount: ', errcount)
