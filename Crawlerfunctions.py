#!/usr/bin/env python
# coding: utf-8

# In[2]:


def crawlerapp(name_class,name_file):
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
        'FEED_FORMAT':'csv',
        'FEED URI':'{}.csv'.format(name_file)
    })

    process.crawl(name_class)
    return process.start()

