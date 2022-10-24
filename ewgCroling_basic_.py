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
import math
process_num=1


#with open('kqcData.json', 'r', encoding='utf-8') as f:
    #json_data = json.load(f)

#keys = [key for key in json_data]
#print("lenkey:", len(\keys))
name = pd.read_csv('COOS_Keyword.csv')
name=(name.iloc[:,[1]]).values.tolist()
keys = []
for i in name:
    keys.append(i[0])
print(keys)

option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument('--dosavle--gpu')

URL = 'https://www.ewg.org/skindeep/'
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



def croling(data, count_dict, processnum):
    
    count=0
    print('driver start')
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)
    driver.get(url=URL)
    while count_dict['count'] < len(keys):
        time.sleep(1)
        print(count_dict['count'])
        idx= count*process_num+processnum
        key = keys[idx]
        count += 1
        count_dict['count'] += 1
        driver.get(url=URL)
        try: 
            #//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/i
            search_box = driver.find_element('xpath', '//*[@id="open-search"]')
            search_box.click()
            search_box = driver.find_element('xpath', '//*[@id="search"]')

            search_box.send_keys(key.lower())
            search_list = driver.find_element('xpath', '//*[@id="eac-container-search"]/ul')
       
            style=search_list.is_displayed()
            search_time=0
            while(style==False and search_time<3) : 
                style=search_list.is_displayed()
                search_time += 0.4
                time.sleep(0.4)
            ingredients = driver.find_elements('xpath', '//*[@id="eac-container-search"]/ul/li')
            ingredientcount = len(ingredients)
            xpath = '//*[@id="eac-container-search"]/ul/li'
            #//*[@id="eac-container-search"]/ul/li[1]/div/a
            i_list=[idx, key]
            for ingredient in range(ingredientcount):
                flag=0
                t = driver.find_element('xpath', xpath+'[' + str(ingredient+1) + ']/div/a')
                search_url = t.get_attribute('href').split('/')
                search_type = search_url[-2]
                print(search_type)
                k = key.lower().replace('-', '').replace(' ','').replace(',','').replace('(','').replace(')','')
                t = t.text.replace('-', '').replace(' ','').replace(',','').lower()
                try: t_idx1=t.index('(')
                except: t_idx1=len(t)
                try: t_idx2=t.index(')')+1
                except: t_idx2=len(t)
                print(t_idx1, t_idx2)
                text = t[:t_idx1]+t[t_idx2:]
                if(search_type=='ingredients'): print(text, k)
                if(t==k):
                    flag=1
                    element = driver.find_element('xpath', xpath+'[' + str(ingredient+1) + ']/div')
                    url=driver.current_url
                    element.click()
                    print("click")
                    while(url==driver.current_url): 
                        time.sleep(0.5)
                    time.sleep(0.1)
                    url=driver.current_url
                    enName = driver.find_element('xpath', '//*[@id="chemical"]/div[1]/div[3]/div[1]/div[2]/h2').text
                    img = driver.find_element('xpath', '//*[@id="chemical"]/div[1]/div[3]/div[1]/div[1]/a/img')
                    img_src = img.get_attribute('src')
                    ewg_level = img_src[img_src.find('?')+1:].split('&')
                    ewg_level = (ewg_level[1][-1], ewg_level[0][-1])
                    if ewg_level[0] == ewg_level[1]:
                        ewg_level = ewg_level[0]
                    else:
                        ewg_level = ewg_level[0]+','+ewg_level[1]
                    data_level = (driver.find_element('xpath', '//*[@id="chemical"]/div[1]/div[3]/div[1]/div[1]/p').text)[6:]
                    name = {'en': enName}

                    print(name)
                    print(ewg_level)
                    print(data_level)
                    
                    data.append([idx, key, enName, ewg_level, data_level])
                    #ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/div[1]/p')
                    
                    '''if(ewg.text=='SkinDeep '):
                        flag==0
                    else:
                        ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/div/button')
                        ewg.click()
                        ewg = driver.find_element('xpath', '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[3]/td[2]/div/div')'''
                    count_dict['awscount'] += 1
                    break
        except:
        #if(0): 
            count_dict['errcount'] += 1
            #i_list[1]='err'
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

    # while count<ln(keys):
    for i in range(process_num):
        p = multiprocessing.Process(target = croling, args = (data, count_dict, i))
        process.append(p)
        p.start()

    for p in process:
        p.join()
    print(data)
    data=list(data)
    df = pd.DataFrame(data)
    df.to_csv("ewg_data_test1.csv", header=None, index=None)
    print(count_dict['count'], count_dict['errcount'])
    print(time.time()- start)
    
