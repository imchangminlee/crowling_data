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

URL = 'https://www.petpoisonhelpline.com/poisons/'
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
    alpha_lst = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z", "5"]
    for alpha in alpha_lst:
        print(alpha)
        if True:
            driver.get(url=URL)
            lista = driver.find_elements('xpath', '//*[@id="'+alpha+'-block"]/div/ul/li')
            lista_cnt = len(lista)
            count += lista_cnt
            
            for num in range(lista_cnt):
                driver.get(url=URL)
                xpath = '//*[@id="'+alpha+'-block"]/div/ul/li'
                link = driver.find_element('xpath', xpath+'[' + str(num+1) + ']/span[1]/a')
                link = link.get_attribute('href')
                
                new=driver.get(url=link)
                listm = driver.find_elements('xpath', '//*[@id="wrapper"]/main/div/div/div[2]/div/div[2]/ul/li')
                listm_cnt = len(listm)
                print(listm_cnt)
                xpath = '//*[@id="wrapper"]/main/div/div/div[2]/div/div[2]/ul/li'

                animal_lt = []
                for anum in range(listm_cnt):
                    try:
                        animal_lst = driver.find_element('xpath', xpath+'[' + str(anum+1) + ']/a').text
                        animal_lt.append(animal_lst)
                    except:
                        animal_lt.append("None")
                count_dict['awscount'] += 1
                data.append(animal_lt)
        else: 
            print("stop")
            count_dict['errcount'] += 1
    print('aswcount:', count_dict['awscount'],'errcount: ', count_dict['errcount'])
    print('whole count:', count)
    
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
    result = []
    for elm in data:
        semi = [False, False, False, False, False]
        for i in range(len(elm)):
            #['DOGS', 'CATS', 'COWS', 'HORSES', 'BIRDS']
            if elm[i] == "DOGS":
                semi[0] = True
            elif elm[i] == "CATS":
                semi[1] = True
            elif elm[i] == "COWS":
                semi[2] = True
            elif elm[i] == "HORSES":
                semi[3] = True
            elif elm[i] == "BIRDS":
                semi[4] = True
            else:
                semi = semi
        if semi == [False, False, False, False, False]:
            semi = [None, None, None, None, None]
        result.append(semi)
    data = result

    print(data)
    data=list(data)
    df = pd.DataFrame(data)
    df.to_csv("pph_animal_data.csv", header=None, index=None)
    print(count_dict['count'], count_dict['errcount'])
    print(time.time()- start)
    
