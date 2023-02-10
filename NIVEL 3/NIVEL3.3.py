# -*- coding: utf-8 -*-
"""
Created on Mon May 17 17:04:23 2021

@author: aleex
"""

# SELENIUM // SCROLLING Y MANEJO DE TABS - GOOGLE PLACES

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait

scrollingScript = """ 
  document.getElementsByClassName('section-layout section-scrollbox scrollable-y scrollable-show')[0].scroll(0, 50000)
"""

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome("C:\\Users\\aleex\\chromedriver_win32/chromedriver.exe",options=opts)

driver.get('https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423706!4d-3.6850768!9m1!1b1')
sleep(random.uniform(4.0, 5.0))

# COOKIES DISCLAIMER
try:
    disclaimer = driver.find_element(By.XPATH, '//div[@class="VfPpkd-RLmnJb"]')
    disclaimer.click() # lo obtenemos y le damos click
except Exception as e:
    print (e) 
    None
    
sleep(random.uniform(4.0,5.0))

scrolls = 0
while (scrolls != 3):
    driver.execute_script(scrollingScript)
    sleep(random.uniform(4.0,5.0))
    scrolls+=1
    
reviews_restaurante = driver.find_elements(By.XPATH,'//div[contains(@class,"section-review ripple-container")]')

for review in reviews_restaurante:
    userlink = review.find_element(By.XPATH,'.//div[@class="section-review-title"]')
    try:
        userlink.click()
        driver.switch_to.window(driver.window_handles[1]) #cambiar a la pestaña 1 del navegador
        but = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//button[@class="section-tab-bar-tab ripple-container section-tab-bar-tab-unselected')))
        but.click()
        
        user_reviews = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class="section-layout section-scrollbox scrollable-y scrollable-show'))
            )
        
        user_scrolls = 0
        while(user_scrolls!=3):
            driver.execute_script(sccrollingScript)
            sleep(random.uniform(5,6))
            user_scrolls+=1
            
        user_reviews = driver.find_elements(By.XPATH,'//div[contains(@class,"section-review ripple-container")]')
        
        for i in user_reviews:
            texto = i.find_element(By.XPATH,'.//span[@class="section-review-text"]').text
            rating = i.find_element(By.XPATH,'.//span[@class="section-review-stars"]').get_attribute('aria-label')
            print(texto)
            print(rating)
            
        driver.close()
        
    except Exception as e:
        print(e)
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    