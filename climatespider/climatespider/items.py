# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClimatespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area_id = scrapy.Field()
    area = scrapy.Field()
    the_date = scrapy.Field()
    the_time = scrapy.Field()
    qx_Condition = scrapy.Field()
    qx_DewPoint = scrapy.Field()
    qx_Events = scrapy.Field()
    qx_GustSpeed = scrapy.Field()
    qx_Humidity = scrapy.Field()
    qx_Precip = scrapy.Field()
    qx_Pressure = scrapy.Field()
    qx_Temp = scrapy.Field()
    qx_Visibility = scrapy.Field()
    qx_WindDir = scrapy.Field()
    qx_WindSpeed = scrapy.Field()
    qx_WindChill_HeatIndex = scrapy.Field()
