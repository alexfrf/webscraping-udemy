#!/usr/bin/env python
# coding: utf-8

# ## Webscrapping NIVEL 2 - Extracción Vertical

# In[1]:


import numpy as np
import pandas as pd


# ### 2.1.- Extracción Vertical + Crawling en TripAdvisor con Scrapy

# In[2]:


from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


# In[3]:


class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()
    
class TripAdvisor(CrawlSpider):
    name = "Hoteles"
    custom_settings={
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36",
            "CLOSESPIDER_PAGECOUNT":50 
        }
    start_urls = ["https://www.tripadvisor.es/Hotels-g187514-Madrid-Hotels.html"]
    download_delay = 2 # se statea para evitar baneos
    
    # Debemos definir las reglas de extracción vertical: a dónde tiene que navegar la herramienta para extraer info.
    # Para ello, debemos averiguar y definir un patrón que coincida con todas las sub urls que queremos trabajar.
    
    rules = (
        Rule(
            LinkExtractor(
                allow = r'/Hotel_Review-' # se toma de la url
            ), follow =True, callback = "parse_item" # para las url que cumplan con la variable allow se aplicrá la función de abajo
        ),
    )
    
    #MAPCOMPOSE preprocesa la información extraida -limpiar y modificar los datos parseados- antes de guardarla en un archivo.
    #En la función de abajo tomamos el texto definido abajo y le aplicamos QUITARSIMBOLO, que quita el símbolo que aparece
    #en la extracción entre el precio y el símbolo del €.
    
    def quitarsimbolo(self,texto):
        nuevoTexto = texto.replace('\xa0','')
        nuevoTexto = nuevoTexto.replace('\n','').replace('\r','')
        return nuevoTexto
    
    def parse_item(self,response):
        sel = Selector(response)
        item = ItemLoader(Hotel(),sel)
        
        item.add_xpath('nombre','//h1[@id="HEADING"]/text()')
        item.add_xpath('precio','//div[@class="CEf5oHnZ"]/text()',
                      MapCompose(self.quitarsimbolo)) 
        # añadimos self. porque la función quitarsimbolo está fuera de esta función pero está dentro de la clase TripAdvisor
        
        item.add_xpath('descripcion','//div[contains(@class,"_2f_ruteS _1bona3Pu _2-hMril5")]/div[1]/text()')
        item.add_xpath('amenities','//div[contains(@class,"_2rdvbNSg")]/text()')
        
        yield item.load_item()


# In[4]:


from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess

if __name__ == "__main__": # Código que se va a ejecutar al dar clic en RUN
        process = CrawlerProcess()
        process.crawl(TripAdvisor) # Nombre de la clase de mi Spider
        process.start()


# <img src='c1.PNG'>
