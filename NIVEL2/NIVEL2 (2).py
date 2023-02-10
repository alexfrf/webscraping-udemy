#!/usr/bin/env python
# coding: utf-8

# ## Webscrapping NIVEL 2 - Extracción Vertical + Horizontal

# In[1]:


import numpy as np
import pandas as pd
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


# ### 2.2.- Extracción Vertical + Horizontal con Scrapy en MercadoLibre

# In[2]:


class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()
    
class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }

    # Utilizamos 2 dominios permitidos, ya que los articulos utilizan un dominio diferente
    allowed_domains = ['articulo.mercadolibre.com.ec', 'listado.mercadolibre.com.ec']

    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros/']

    download_delay = 1

    # Tupla de reglas
    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/_Desde_\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule( # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/MEC-' 
            ), follow=True, callback='parse_items'), # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )
    
    def limpiarTexto(self,texto):
        nuevotexto = texto.replace('\n',' ').replace('\r',' ').replace('\t',' ').strip()
        return nuevotexto
    
    def parse_items(self,response):
        item = ItemLoader(Articulo(),response)
        item.add_xpath('titulo','//h1/text()',MapCompose(self.limpiarTexto))
        item.add_xpath('descripcion','//div[@class="ui-pdp-description"]/p/text()',MapCompose(self.limpiarTexto))
        item.add_xpath('precio','//span[@class="price-tag-fraction"]/text()')
        
        yield item.load_item()
    


# In[3]:


from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess

if __name__ == "__main__": # Código que se va a ejecutar al dar clic en RUN
        process = CrawlerProcess()
        process.crawl(MercadoLibreCrawler) # Nombre de la clase de mi Spider
        process.start()

