"""
OBJETIVO:  
    - Aprender a automatizar la ejecucion de extracciones en Selenium y requests.
    - Aprender a utilizar la libreria Schedule para agendar/automatizar procesos por intervalos.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 1 MAYO 2020
"""
import schedule # pip install schedule
import time
from selenium import webdriver

start_urls = [
    "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
]

def extraer_datos():
    driver = webdriver.Chrome("C:\\Users\\aleex\\chromedriver_win32/chromedriver.exe")

    # Por cada una de las URLs que quiero extraer...
    for url in start_urls:
        driver.get(url)
        try:
            time.sleep(5)
            but = driver.find_element_by_xpath('//button[@class="fc-button fc-cta-consent fc-primary-button"]//p[@class="fc-button-label"]')
            but.click()
        except:
            pass
        time.sleep(1)
        # Extraigo los datos
        ciudad = driver.find_element_by_xpath('//h1').text
        current = driver.find_element_by_xpath('//a[contains(@class, "cur-con-weather-card__panel")]//div[@class="temp"]').text
        real_feel = driver.find_element_by_xpath('//a[contains(@class, "cur-con-weather-card__panel")]//div[@class="real-feel"]').text

        # Limpieza de datos
        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        
        # Guardado de datos en un archivo
        f = open("./datos_clima_selenium.csv", "a")
        f.write(ciudad + "," + current + "," + real_feel + "\n")
        f.close()
        print(ciudad)
        print(current)
        print(real_feel)
        print()

    # Cierro el navegador
    driver.close()


# Logica de schedule (ver documentacion en recursos)
schedule.every(15).seconds.do(extraer_datos) # Cada 1 minuto ejecutar la funcion extraer_datos

# Reviso la cola de procesos cada segundo, para verificar si tengo que correr algun proceso pendiente
while True:
    schedule.run_pending() # Correr procesos que esten pendientes de ser ejecutados.
    time.sleep(1) # Para no saturar el CPU de mi maquina (por el while true), espero 1 segundo entre cada iteracion
