from scrapy import cmdline
from dateutil.parser import parse
import datetime


print('起始日期（2016/1/1）：')
begindate = input()
def getyesterday(d):
    return (parse(d)-datetime.timedelta(days=1)).strftime('%Y/%m/%d')

cmdline.execute('scrapy crawl WUGCrawlSpider_AC -a target={0}'.format(getyesterday(begindate)).split())