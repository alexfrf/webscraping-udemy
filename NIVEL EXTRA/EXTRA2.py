# -*- coding: utf-8 -*-
"""
Created on Thu May 20 01:18:15 2021

@author: aleex
"""

# SELENIUM - Automatización de Extracción de Datos

from selenium import webdriver
import schedule
import time

start_urls = [
    "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
] 

def extraer_datos():
    driver = webdriver.Chrome("C:\\Users\\aleex\\chromedriver_win32/chromedriver.exe")
    for url in start_urls:
        driver.get(url)
        try:
            time.sleep(5)
            but = driver.find_element_by_xpath('//button[@class="fc-button fc-cta-consent fc-primary-button"]//p[@class="fc-button-label"]')
            but.click()
        except:
            pass
        time.sleep(1)
        ciudad = driver.find_element_by_xpath('//h1').text
        current = driver.find_element_by_xpath('//div[contains(@class, "temp-container")]//div[@class="temp"]').text
        real_feel = driver.find_element_by_xpath('//div[contains(@class, "temp-container")]//div[@class="real-feel"]').text
        
        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').replace('C','').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        
        # Guardado de datos en un archivo
        f = open("./datos_clima_selenium.csv", "a")
        f.write(ciudad + "," + current + "," + real_feel + "\n")
        f.close()
        print(ciudad)
        print(current)
        print(real_feel)
        print()
        
    driver.close()
    
# Logica de schedule (ver documentacion en recursos)
schedule.every(1).minutes.do(extraer_datos) # Cada 1 minuto ejecutar la funcion extraer_datos

while True:
    schedule.run_pending()
    time.sleep(1) #seconds
        