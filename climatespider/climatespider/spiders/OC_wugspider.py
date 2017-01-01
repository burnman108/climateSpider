#-*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from climatespider.items import ClimatespiderItem
from scrapy.selector import Selector
from dateutil.parser import parse
import re
from datetime import datetime
#from scrapy.exceptions import CloseSpider


class wugSpider(CrawlSpider):
    name = "WUGCrawlSpider_OC"
    current = ''
    close_down = False
    allowed_domains = ['www.wunderground.com']
    # start_urls = ['https://www.wunderground.com/history/airport/ZLXY/2015/12/31/DailyHistory.html']
    # rules =(
    #     Rule(LinkExtractor(allow=('/history/.*?',), restrict_xpaths=('//div[@class="next-link"]')),
    #          callback='parse_item', follow=True),
    # )
            
    def __init__(self, target = None):
        if self.current is not '':
            target = self.current
        if target is not None:
            self.current = target
        self.start_urls = [
            'https://www.wunderground.com/history/{0}/DailyHistory.html'.format(target)
        ]
        self.rules = (
            Rule(
                LinkExtractor(allow=('/history/.*?',), restrict_xpaths=('//div[@class="next-link"]'), deny=('.*/{d.year}/{d.month}/{d.day}/DailyHistory.html'.format(d=datetime.now()))),
                callback='parse_item', follow=True
            ),
        )
        super(wugSpider, self).__init__()


    def parse_item(self, response):
        sel = Selector(response)
        indexlist = list(map(lambda x: x.replace(' ','').replace('.',''),sel.xpath('//table[@id="obsTable"]/thead/tr/th/text()').extract()))
        date = re.match(r'.*(\d{4}\/\d{1,2}\/\d{1,2}).*', response.url).group(1)
        datatable = sel.xpath('//tr[@class="no-metars"]')
        # items = []
        for each in datatable:
            item = ClimatespiderItem()
            item['area'] = re.match(r'.*history/(.*)/2\d{3}/.*', response.url).group(1)
            # item['date'] = date
            if len(indexlist) == 13:
                item['the_date'] = date
                item['the_time'] = parse(each.xpath('td[1]/text()').extract()[0]).strftime('%H:%M')
                item['qx_Humidity'] = each.xpath('td[5]/text()').extract()[0]
                item['qx_WindDir'] = each.xpath('td[8]/text()').extract()[0]
                item['qx_Precip'] = each.xpath('td[11]/text()').extract()[0]
                item['qx_Events'] = each.xpath('td[12]/text()').extract()[0].strip()
                try:
                    item['qx_Condition'] = each.xpath('td[13]/text()').extract()[0]
                except Exception as e:
                    item['qx_Condition'] = ''
                try:
                    item['qx_Temp'] = each.xpath('td[2]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_Temp'] = each.xpath('td[2]/text()').extract()[0].strip().replace('-','')
                try:
                    item['qx_WindChill_HeatIndex'] = each.xpath('td[3]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_WindChill_HeatIndex'] = each.xpath('td[3]/text()').extract()[0].strip().replace('-','')
                try:
                    item['qx_DewPoint'] = each.xpath('td[4]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_DewPoint'] = each.xpath('td[4]/text()').extract()[0].strip().replace('-','')
                try:
                    item['qx_Pressure'] = each.xpath('td[6]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_Pressure'] = each.xpath('td[6]/text()').extract()[0].strip().replace('-','')
                try:
                    item['qx_Visibility'] = each.xpath('td[7]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_Visibility'] = each.xpath('td[7]/text()').extract()[0].strip().replace('-','')
                try:
                    item['qx_WindSpeed'] = each.xpath('td[9]/span[1]/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_WindSpeed'] = each.xpath('td[9]/text()').extract()[0].strip().replace('-','')
                try:
                    item['qx_GustSpeed'] = each.xpath('td[10]/span[1]/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_GustSpeed'] = each.xpath('td[10]/text()').extract()[0].strip().replace('-','')
                yield item
            else:
                item['the_date'] = date
                item['the_time'] = parse(each.xpath('td[1]/text()').extract()[0]).strftime('%H:%M')
                item['qx_Humidity'] = each.xpath('td[4]/text()').extract()[0]
                item['qx_WindDir'] = each.xpath('td[7]/text()').extract()[0]
                item['qx_Precip'] = each.xpath('td[10]/text()').extract()[0]
                item['qx_Events'] = each.xpath('td[11]/text()').extract()[0].strip()
                try:
                    item['qx_Condition'] = each.xpath('td[12]/text()').extract()[0]
                except Exception as e:
                    item['qx_Condition'] = ''
                try:
                    item['qx_Temp'] = each.xpath('td[2]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_Temp'] = each.xpath('td[2]/text()').extract()[0].strip().replace('-','')
                # try:
                #     item['WindChill_HeatIndex'] = each.xpath('td[3]/span/span[@class="wx-value"]/text()').extract()[0]
                # except Exception as e:
                #     item['WindChill_HeatIndex'] = each.xpath('td[3]/text()').extract()[0].strip().replace('-', '')
                try:
                    item['qx_DewPoint'] = each.xpath('td[3]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_DewPoint'] = each.xpath('td[3]/text()').extract()[0].strip().replace('-', '')
                try:
                    item['qx_Pressure'] = each.xpath('td[5]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_Pressure'] = each.xpath('td[5]/text()').extract()[0].strip().replace('-', '')
                try:
                    item['qx_Visibility'] = each.xpath('td[6]/span/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_Visibility'] = each.xpath('td[6]/text()').extract()[0].strip().replace('-', '')
                try:
                    item['qx_WindSpeed'] = each.xpath('td[8]/span[1]/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_WindSpeed'] = each.xpath('td[8]/text()').extract()[0].strip().replace('-', '')
                try:
                    item['qx_GustSpeed'] = each.xpath('td[9]/span[1]/span[@class="wx-value"]/text()').extract()[0]
                except Exception as e:
                    item['qx_GustSpeed'] = each.xpath('td[9]/text()').extract()[0].strip().replace('-', '')
                yield item
            # for index in range(len(indexlist)):


        #if (self.close_down == True):
        #    print(u"-----------数据爬取完毕，closespider------------")
        #    raise CloseSpider(reason="to the end")

