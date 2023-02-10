#!/usr/bin/env python
# coding: utf-8

# In[4]:


def crawlerapp(name_class):
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
        'FEED_FORMAT':'csv',
        'FEED URI':'{}.csv'.format(name_class.name)
    })

    process.crawl(name_class)
    return process.start()

