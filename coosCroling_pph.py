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
        try:
            driver.get(url=URL) 
            #//*[@id="A-block"]/div/ul
            #//*[@id="B-block"]/div/ul/li[1]
            lista = driver.find_elements('xpath', '//*[@id=\"'+alpha+'-block\"]/div/ul/li')
            lista_cnt = len(lista)
            print(lista_cnt)
            count += lista_cnt
            xpath = '//*[@id=\"'+alpha+'-block\"]/div/ul/li'
            for num in range(lista_cnt):
                driver.get(url=URL)
                link = driver.find_element('xpath', xpath+'[' + str(num+1) + ']/span[1]/a')
                link = link.get_attribute('href')
                url=driver.current_url
                new=driver.get(url=link)
                while(url==driver.current_url):
                    url=driver.current_url
                    time.sleep(0.2)
                time.sleep(1)
                url=driver.current_url
                Name = driver.find_element('xpath', '//*[@id="wrapper"]/main/div/div/div[2]/div/div[1]/div[1]/div[1]/h1').text.replace('’', '\'')
                try:
                    atName = driver.find_element('xpath', '//*[@id="wrapper"]/main/div/div/div[2]/div/div[1]/div[1]/div[3]/p[2]').text.replace('’', '\'').replace('®', '')
                except:
                    atName = "None"
                info = driver.find_elements('xpath', '//*[@id="wrapper"]/main/div/div/div[2]/div/div[1]/div[1]/div[4]/p[3]')
                if len(info) != 0:
                    info = info[0].text.splitlines()
                else:
                    #//*[@id="wrapper"]/main/div/div/div[2]/div/div[1]/div[1]/div[5]/ul/li[1]
                    #off = driver.find_elements('xpath', '//*[@id="wrapper"]/main/div/div/div[2]/div/div[1]/div[1]/div[5]/ul/li')
                    elements = driver.find_elements('css selector','#wrapper > main > div > div > div.poison-content > div > div.poison-content-inner > div.poison-content-left > div.poison-description > ul>li')
                    infos = [i.text.replace('“', '"') for i in elements]
                    info = infos
                count_dict['awscount'] += 1
                print(Name, atName, 'info:',info)
                pair_data = {'Name': Name, 'alterName': atName, 'info': info}
                data.append(pair_data)
        except: 
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
    print(data)
    data=list(data)
    df = pd.DataFrame(data)
    df.to_csv("pph_data.csv", header=None, index=None)
    print(count_dict['count'], count_dict['errcount'])
    print(time.time()- start)
    
