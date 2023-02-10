# -*- coding: utf-8 -*-
"""
Created on Mon May 17 22:29:09 2021

@author: aleex
"""

# Requests - EXTRACCIÓN DE DATOS DE SCRIPTS

import requests
import pandas as pd
from lxml import html
import json

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

for i in range(1, 5):

    url = "https://www.gob.pe/busquedas?reason=sheet&sheet=" + str(i)
    
    
    respuesta = requests.get(url,headers=headers)
    respuesta.encoding = 'UTF-8'
    parser = html.fromstring(respuesta.text)
    # EXTRACCION SOLO DEL TEXTO QUE DICE INGLES
    datos = parser.xpath("//script[contains(text(), 'window.initialData')]")
    datos = datos[0].text_content()
    indice = datos.find('{')
    datos = datos[indice:]
    
    obj = json.loads(datos)
    
    output = obj['data']['attributes']['results']
    for i in output:
        try:
            print(output['content'])
        except:
            pass
