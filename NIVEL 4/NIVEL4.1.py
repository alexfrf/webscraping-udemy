# -*- coding: utf-8 -*-
"""
Created on Mon May 17 21:06:40 2021

@author: aleex
"""

# APIs - Extracción de Datos

import requests
import pandas as pd

headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    "referer": "https://www.udemy.com/courses/search/?src=ukw&q=python",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}

cursos_totales = []

for i in range(1,4):
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?fields[locale]=simple_english_title&src=ukw&q=python&skip_price=true&p={}'.format(i)
    response = requests.get(url_api,headers=headers)
    
    data = response.json()
    cursos = data['courses']
    
    for curso in cursos:
        print(curso['title'])
        print(curso['num_reviews'])
        print(curso['rating'])
        print('\n')
        cursos_totales.append(
            {
            "titulo":curso['title'],
            "num_reviews":curso['num_reviews'],
            "rating":curso['rating']
            }
            )
        
        
df = pd.DataFrame(cursos_totales)
df.to_csv('cursos_udemy.csv')