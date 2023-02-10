# -*- coding: utf-8 -*-
"""
Created on Sat May 15 21:21:07 2021

@author: aleex
"""

# SELENIUM / WEBSCRAPPING HORIZONTAL - Olx

# import random
# from time import sleep
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome("C:\\Users\\aleex\\chromedriver_win32/chromedriver.exe")
driver.get('https://www.olx.com.ec/autos_c378')

but = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')

for i in range(3):
    try:
        but = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//button[@data-aut-id="btnLoadMore"]'))
            )
        #but = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
        but.click()
        WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.XPATH,'//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
            )
    except:
        break
    
autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

for i in autos:
    try:
        precio = i.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
        print(precio)
        descripcion = i.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
        print(descripcion)
    except:
        pass
