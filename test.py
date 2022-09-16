import encodings
from encodings.utf_8 import encode
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = ['driver'+str(i) for i in range(100)]
for i in range(100):
    driver[i] = webdriver.Chrome(executable_path='./chromedriver')