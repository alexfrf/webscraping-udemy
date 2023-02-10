#!/usr/bin/env python
# coding: utf-8

# ## 1.- Webscrapping estático (NIVEL 1)

# ### 1.1.- Extracción de info de WIKIPEDIA mediante requests y lxml

# In[1]:


import pandas as pd
import numpy as np


# **1.1.1.- Hacer requerimientos con requests**

# In[2]:


import requests # empleada para hacer requerimientos a las webs


# In[3]:


headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36"}
url = 'https://www.wikipedia.org/'
requerimiento = requests.get(url,headers=headers)
print(requerimiento.text)


# **1.1.2.- Parsear la extracción con lxml**
#Valor copiado y pegado de wikipedia. Extraemos el id, que nos servirá para parsear y leer así lo correspondiente a este código html
"""
<a id="js-link-box-en" href="//en.wikipedia.org/" title="English — Wikipedia — The Free Encyclopedia" class="link-box" data-slogan="The Free Encyclopedia">
<strong>English</strong>
<small><bdi dir="ltr">6&nbsp;207&nbsp;000+</bdi> <span>articles</span></small>
</a>

"""
# **Método 1: parser.get_element_by_id('id').text_content()**

# In[4]:


from lxml import html
idx="js-link-box-en" # el id del código html pegado arriba. Es un código único para cada url
parser = html.fromstring(requerimiento.text)
english = parser.get_element_by_id(idx)
english


# In[5]:


print(english.text_content())


# <a id="js-link-box-en" href="//en.wikipedia.org/" title="English — Wikipedia — The Free Encyclopedia" class="link-box" data-slogan="The Free Encyclopedia">
# <strong>English</strong>
# <small><bdi dir="ltr">6&nbsp;207&nbsp;000+</bdi> <span>articles</span></small>
# </a>

# **Método 2: parser.xpath()**

# In[6]:


english= parser.xpath("//a[@id='js-link-box-en']/strong/text()")
print(english)


# <img src='c1.PNG'>

# In[7]:


# obteniendo el listado de idiomas
idiomas=parser.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()") 
# buscamos todas las líneas que contengan el parámetro marcado dentro de un div class y que vayan dentro de strong (negrita)
print(idiomas)


# In[8]:


for i in idiomas:
    print(i)


# **Método 3: parser.find_class(class).text_content()**

# In[9]:


idiomas = parser.find_class('central-featured-lang')
for i in idiomas:
    print(i.text_content())


# ### 1.2.- Requests y beautiful soup - Extracción de Stackoverflow

# In[10]:


import requests
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36"}
url = 'https://stackoverflow.com/questions'
requerimiento = requests.get(url,headers=headers)


# **1.2.1.- Parsear la extracción con BeautifulSoup**

# In[11]:


from bs4 import BeautifulSoup
soup= BeautifulSoup(requerimiento.text)


# <img src='c2.PNG'>

# <img src='c4.PNG'>

# In[12]:


# Obtener todas las preguntas de stackoverflow
questions = soup.find(id="questions")
questions_list = questions.find_all('div',class_='question-summary') 
# no es necesario el 'div', pero debemos asegurarnos por si existen dos clases iguales. ç
# Nos devuelve todo el cod html desde ese id

for i in questions_list:
    #OPCION 1
    titulo_pregunta=i.find('h3').text  #.text = .text_content en lxml
    # me devuelve las preguntas
    descripcion_pregunta = (i.find(class_='excerpt').text).replace('\n','').replace('\r','').strip()
    # me devuelve las descripciones o subtitulos
    # retiro los espacios de las descripciones y con strip() retiro las sangrías
    
    print(titulo_pregunta)
    print(descripcion_pregunta)
    
    #OPCION 2
    #elemento = i.find('h3')
    #elemento_pregunta = elemento.text #devuelve las preguntas
    #elemento_descripcion_pregunta = elemento.find_next_sibling('div').text.replace('\n','').replace('\r','').strip()
    
    #print(elemento_pregunta)
    #print(elemento_descripcion_pregunta)
    
    #Misma solución en ambos procesos. La diferencia es que para el segundo no hace falta saber el nombre de class del cod html.
    
    print()


# <img src='c3.PNG'>

# ### 1.3.- Extracción de datos con Scrapy

# **Si se emplea Scrapy no es necesario recurrir a librerías como lxml o beautifulsoup para parsear, ya que Scracpy dispone de la función Parse como mecanismo para llevarlo a cabo. El proceso a nivel mecánico tiene una estructura similar a esta:**

# <img src='c5.PNG'>

# #### 1.3.1.- Webscrapping con Scrapy - Extracción de Stackoverflow

# In[13]:


from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from scrapy.crawler import CrawlerProcess

# *Antes de comenzar con el puro proceso debemos siempre determinar, en la extracción que queremos realizar, qué es el item y qué son las propiedades. En este caso, el item es el título de la pregunta y las propiedades son las descripciones de cada una. Tras ello, hemos de definirlo mediante clases (object-oriented programming), del siguiente modo:*

# In[19]:


class Pregunta(Item):
    id = Field()
    pregunta = Field()
    #descripcion = Field()
# el objetivo del proceso será rellenar el campo pregunta con todas las preguntas y el campo descripción con las descripciones

class StackOverflow(Spider): # Spider se emplea para extracciones estáticas, de una sola página
    name = 'MiprimerSpider'
    custom_settings = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36"}
    start_urls = ['https://stackoverflow.com/questions'] # en este caso es una lista de len()=1, en vez de un str
    # El requerimiento se hace simplemente con lo que hemos hecho ya, sin recesidad de la herramienta requests. Falta Parsear
    
    #DEFINIMOS LAS REGLAS
    def parse(self,response):
        sel = Selector(response) # la función Selector() realiza las consultas a la página, tomando el requerimiento previo
        questions = sel.xpath("//div[@id='questions']//div[@class='question-summary']")
        # el resultado, dado que hay varias líneas con question-summary, será una lista con todos los elementos que son preguntas
        for x in questions: # iteramos cada elemento para reproducir su texto
            item = ItemLoader(Pregunta(),x)
            item.add_xpath('pregunta','.//h3/a/text()')
            # el campo pregunta se rellenará con el segundo elemento, que es la ruta xpath en la que se localiza el contenido
            #item.add_xpath('descripcion',".//div[@class='excerpt']/text()")
            item.add_value('id',1) # se añade un valor concreto, en lugar de un campo xpath, a una propiedad definida antes
            
            yield item.load_item() # similar a return en las funciones
            
if __name__ == "__main__": # Código que se va a ejecutar al dar clic en RUN
    process = CrawlerProcess()
    process.crawl(StackOverflow) # Nombre de la clase de mi Spider
    process.start()


# La ejecución de scripts con scrapy también es diferente a lo "normal", dado que debe hacerse desde una terminal y no del modo convencional.
