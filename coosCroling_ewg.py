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

with open('kqcData.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

#keys = [key for key in json_data]
#print("lenkey:", len(keys))
name = pd.read_csv('new_name_merge.csv')
name=(name.iloc[:,[0]]).values.tolist()
keys = []
for i in name:
    keys.append(i[0])
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

        idx= count*8+processnum
        key = keys[idx]
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
                    info = driver.find_elements('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/div/div')
                    infos = []
                    for i in info:
                        infos.append(i.text)
                    print(infos)
                    name = {'kr': krName, 'en': enName}

                    print(name)
                    data.append([idx, key])
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
                data.append([idx])
                #print("err:", count_dict['errcount'])
        except: 
            count_dict['errcount'] += 1
            data.append([idx])
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
    for i in range(8):
        p = multiprocessing.Process(target = croling, args = (data, count_dict, i))
        process.append(p)
        p.start()

    for p in process:
        p.join()
    print(data)
    data=list(data)
    df = pd.DataFrame(data)
    df.to_csv("coos_data.csv", header=None, index=None)
    print(count_dict['count'], count_dict['errcount'])
    print(time.time()- start)
    
