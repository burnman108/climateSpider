# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealtimeclimItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area = scrapy.Field()
    datetime = scrapy.Field()
    qx_temp = scrapy.Field()
    qx_humidity = scrapy.Field()
    qx_pressure = scrapy.Field()


