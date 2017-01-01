#-*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from RealtimeClim.items import RealtimeclimItem
from scrapy.selector import Selector
from datetime import datetime

class Spider(CrawlSpider):
    name = "AO_spider"
    allowed_domains = ['tianqi.2345.com']
    start_urls = [
        'https://tianqi.2345.com/today-60728.htm',
        'https://tianqi.2345.com/today-54511.htm',
        'https://tianqi.2345.com/today-60273.htm',
        'https://tianqi.2345.com/today-54527.htm',
        'https://tianqi.2345.com/today-53772.htm',
        'https://tianqi.2345.com/today-58362.htm',
        'https://tianqi.2345.com/today-50884.htm',
        'https://tianqi.2345.com/today-60735.htm',
        'https://tianqi.2345.com/today-50953.htm',
        'https://tianqi.2345.com/today-50842.htm',
        'https://tianqi.2345.com/today-58321.htm',
        'https://tianqi.2345.com/today-57036.htm',
        'https://tianqi.2345.com/today-54602.htm',
        'https://tianqi.2345.com/today-59488.htm',
        'https://tianqi.2345.com/today-54401.htm',
        'https://tianqi.2345.com/today-58502.htm',
        'https://tianqi.2345.com/today-57687.htm',
        'https://tianqi.2345.com/today-58457.htm',
        'https://tianqi.2345.com/today-57494.htm',
        'https://tianqi.2345.com/today-58606.htm',
        'https://tianqi.2345.com/today-59288.htm',
        'https://tianqi.2345.com/today-59493.htm',
        'https://tianqi.2345.com/today-53798.htm',
        'https://tianqi.2345.com/today-54662.htm',
        'https://tianqi.2345.com/today-56294.htm',
        'https://tianqi.2345.com/today-50774.htm',
        'https://tianqi.2345.com/today-58357.htm'
    ]

    def parse(self, response):
        sel = Selector(response)
        parameter = sel.xpath('//ul[@class="parameter"]')
        item = RealtimeclimItem()
        datetimestr = datetime.today().strftime('%Y-%m-%d %H') + ':00'
        areaid = response.url.split('-')[1].split('.')[0]
        temp = parameter.xpath('li[2]/i/text()').extract()[0][:-1]
        humidity = float(parameter.xpath('li[5]/i/text()').extract()[0][:-1])/100
        pressure = parameter.xpath('li[6]/i/text()').extract()[0].split()[0]

        item['area'] = areaid
        item['datetime'] = datetimestr
        item['qx_temp'] = temp
        item['qx_humidity'] = humidity
        item['qx_pressure'] = pressure
        yield item