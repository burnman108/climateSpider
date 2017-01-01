# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    datetime = scrapy.Field()
    area = scrapy.Field()
    kq_aqi = scrapy.Field()
    kq_quality = scrapy.Field()
    kq_primary_pollutant = scrapy.Field()
    kq_pm2_5 = scrapy.Field()
    kq_pm10 = scrapy.Field()
    kq_co = scrapy.Field()
    kq_no2 = scrapy.Field()
    kq_o3 = scrapy.Field()
    kq_o3_8h = scrapy.Field()
    kq_so2 = scrapy.Field()