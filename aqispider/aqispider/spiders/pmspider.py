#-*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from aqispider.items import AqispiderItem
from scrapy.selector import Selector
import datetime
import re


class Pmspider(CrawlSpider):
    name = 'AQIspiders'
    allowed_domains = ['www.pm25.in']
    start_urls = ['http://www.pm25.in/rank']

    def parse(self, response):
        sel = Selector(response)
        update_time = (datetime.datetime.today()-datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H') + ':00'
        # update_time = datetime.datetime.today().strftime('%Y-%m-%d %H') + ':00'
        datas = sel.xpath('//div[@class="table"]/table/tbody/tr')
        for data in datas:
            item = AqispiderItem()
            item['datetime'] = update_time
            area_href = data.xpath('td[2]/a/@href').extract()[0]
            item['area'] = re.match(r'/(.*)', area_href).group(1)
            item['kq_aqi'] = data.xpath('td[3]/text()').extract()[0]
            item['kq_quality'] = data.xpath('td[4]/text()').extract()[0].encode('utf8')
            p_pollutant = data.xpath('td[5]/text()').extract()
            if len(p_pollutant) == 0:
                item['kq_primary_pollutant'] = ''
            elif len(p_pollutant) == 1:
                item['kq_primary_pollutant'] = p_pollutant[0].encode('utf8')
            else:
                item['kq_primary_pollutant'] = ('/').join(('').join(p_pollutant).split()).encode('utf8')
            item['kq_pm2_5'] = data.xpath('td[6]/text()').extract()[0]
            item['kq_pm10'] = data.xpath('td[7]/text()').extract()[0]
            item['kq_co'] = data.xpath('td[8]/text()').extract()[0]
            item['kq_no2'] = data.xpath('td[9]/text()').extract()[0]
            item['kq_o3'] = data.xpath('td[10]/text()').extract()[0]
            item['kq_o3_8h'] = data.xpath('td[11]/text()').extract()[0]
            item['kq_so2'] = data.xpath('td[12]/text()').extract()[0]
            yield item