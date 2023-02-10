# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:57:57 2021

@author: aleex
"""
# SELENIUM / WEBSCRAPPING HORTIZONTAL + VERTICAL - Mercado Libre

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome("C:\\Users\\aleex\\chromedriver_win32/chromedriver.exe",options=opts)
driver.get('https://listado.mercadolibre.com.ec/repuestos-autos-camionetas-bujias')

PAGINACION_MAX = 10
PAGINACION_ACTUAL = 1

# COOKIES DISCLAIMER
try:
    disclaimer = driver.find_element(By.XPATH, '//button[@id="cookieDisclaimerButton"]')
    disclaimer.click() # lo obtenemos y le damos click
except Exception as e:
    print (e) 
    None
    

while PAGINACION_MAX > PAGINACION_ACTUAL: # infinitas iteraciones mientras se cumpla esa condición

    artic = driver.find_elements(By.XPATH,'//a[@class="ui-search-item__group__element ui-search-link"]')
    links=[]
    for a in artic:
        links.append(a.get_attribute('href'))
        
    for link in links:
        try:
            driver.get(link)
            titulo = driver.find_element_by_xpath('//h1').text
            precio = driver.find_element(By.XPATH, '//span[@class="price-tag-amount"]').text
            print (titulo)
            print (precio.replace('\n', '').replace('\t', ''))

            driver.back()
        except Exception as e:
            driver.back()
            print(e)
            
    
    try:
        but = driver.find_element(By.XPATH,'//span[text()="Siguiente"]')
        but.click()
    except:
        break # rompe todo el loop del while
        print('Error')