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
import numpy as np
import math

#keys = [key for key in json_data]
#print("lenkey:", len(keys))
name = pd.read_csv('COOS_Keyword.csv')
nidx = pd.read_csv('cooskeyword.csv')
org = (pd.read_csv('cooskeyword_data.csv')).iloc[:].values.tolist()
name=(name.iloc[:,[1]]).values.tolist()
print("name : ", name)
nidx=(nidx.iloc[:,[1]]).values.tolist()
print("nidx : ", nidx)
idx_lst = []
for i in range(len(nidx)):
    if nidx[i] != name[i]:
        idx_lst.append(i)
print(idx_lst)
print(len(idx_lst))

keys = []
for j in idx_lst:
    keys.append(name[j])
keys = np.array(keys).flatten().tolist()
print(keys)

option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument('--dosavle--gpu')

URL = 'https://coos.kr/'
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
    while count_dict['count'] < len(keys):
        print(count_dict['count'])

        id= count*1+processnum
        idx = idx_lst[id]
        print("idx", idx)
        key = keys[id]
        print("key", key)
        count += 1
        count_dict['count'] += 1
        driver.get(url=URL)
        try: 
            #//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/i
            loading = driver.find_element("xpath", '//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div')
            search_box = driver.find_element('xpath', '//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/input')
            #//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/input
            search_box.send_keys(key.lower())
            while (loading.get_attribute('class')!='ui active visible big focus fluid search'):
                time.sleep(1)
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
                    url=driver.current_url
                    element.click()
                    print("click")
                    #주소가 바뀌었는지 확인하는 코드 필요
                    while(url==driver.current_url): 
                        time.sleep(0.5)
                    time.sleep(0.1)
                    url=driver.current_url
                    krName = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]').text
                    enName = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/div/div/div[2]/div[2]').text
                    isitinfo1 = " "
                    isitinfo2 = " "
                    isitinfo3 = " "
                    isitinfo4 = " "
                    try:
                        isitinfo1 = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/div/div[1]').text
                        isitinfo2 = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/div/div[2]').text
                        isitinfo3 = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/div/div[3]').text
                    except:
                        isitinfo4 = " None"
                    if isitinfo1[0] == "식":
                        info = isitinfo1
                    elif isitinfo2[0] == "식":
                        info = isitinfo2
                    elif isitinfo3[0] == "식":
                        info = isitinfo3
                    else:
                        info = isitinfo4
                        
                    '''infos = []
                    for i in info:
                        infos.append(i.text)'''
                    info = info[1:]
                    print(info)
                    name = {'kr': krName, 'en': enName}
                    print(name)
                    data.append([idx, key, krName, enName, info])
                    #ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/div[1]/p')
                    #ewg정보가 제공되는 지 확인하는 코드 
                    '''if(ewg.text=='SkinDeep 데이터가 제공되지 않는 성분입니다.'):
                        flag==0
                    else:
                        ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/div/button')
                        ewg.click()
                        ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/div/div')'''
                    count_dict['awscount'] += 1
                    break
            if(flag==0):
                count_dict['errcount'] += 1
                data.append([idx, key])
                #print("err:", count_dict['errcount'])
        except: 
            count_dict['errcount'] += 1
            data.append([idx, key])
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
    data=list(data)
    for i in range(len(data)):
        if org[data[i][0]][0] == data[i][0]:
            org[data[i][0]] = data[i]
    df = pd.DataFrame(org)
    print(df)
    df.to_csv("cooskeyword_data_again.csv", header=None, index=None, encoding='utf-8-sig')
    print(count_dict['count'], count_dict['errcount'])
    print(time.time()- start)
    
