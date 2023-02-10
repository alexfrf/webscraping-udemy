# -*- coding: utf-8 -*-
"""
Created on Thu May 20 00:19:01 2021

@author: aleex
"""

# SCRAPY - Automatización de Extracción de Datos

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess

class ExtractorClima(Spider):
    name = "MiCrawlerDeClima"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'LOG_ENABLED': True # Elimina los miles de logs que salen al ejecutar Scrapy en terminal
    }

    # Start URLs puede ser un arreglo de muchas URLs. Al no haber reglas, cada una de
    # estas URLs va a ejecutar la funcion parse una vez que se haga el requerimiento y
    # se obtenga una respuesta
    start_urls = [
        "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
        "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
        "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
    ]

    def parse(self, response):
        ciudad = response.xpath('//h1/text()').get()
        current = response.xpath('//div[contains(@class, "cur-con-weather-card__panel")]//div[@class="temp"]/text()').get()
        real_feel = response.xpath('//div[contains(@class, "cur-con-weather-card__panel")]//div[@class="real-feel"]/text()').get()

        # Limpieza de datos
        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        
        # Guardado de datos en un archivo
        f = open("./datos_clima_scrapy.csv", "a")
        f.write(ciudad + "," + current + "," + real_feel + "\n")
        f.close()
        print(ciudad)
        print(current)
        print(real_feel)
        print()
        
# EXTRACCIÓN NORMAL
        
process = CrawlerProcess()
process.crawl(ExtractorClima)
process.start()

# EXTRACCIÓN PERIÓDICA
        
# runner = CrawlerRunner()
# task = LoopingCall(lambda: runner.crawl(ExtractorClima))
# task.start(20)
# reactor.run()
