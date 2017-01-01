from scrapy import cmdline
from dateutil.parser import parse
import datetime

print('城市拼音（beijing）：')
location = input()
print('起始日期（2016/1/1）：')
begindate = input()
def getyesterday(d):
    return (parse(d)-datetime.timedelta(days=1)).strftime('%Y/%m/%d')
locdict = {
    'beijing': 'airport/ZBAA/',
    'hejian': 'station/54618/',
    'tianjin': 'airport/ZBTJ/',
    'taiyuan': 'airport/ZBYN/',
    'shanghai': 'airport/ZSSS/', 
    'shuangyashan': 'station/50888/',
    'mohe': 'station/50136/',
    'haerbin': 'airport/ZYHB/',
    'daqing': 'station/50854/',
    'hefei': 'airport/ZSOF/',
    'xian': 'airport/ZLXY/',
    'baoding': 'station/54602/',
    'zhuhai': 'airport/VMMC/',
    'zhangjiakou': 'station/54401/',
    'jiujiang': 'station/58506/',
    'changsha': 'airport/ZGHA/',
    'hangzhou': 'airport/ZSHC/',
    'wuhan': 'airport/ZHHH/',
    'nanchang': 'station/58606/',
    'foshan': 'airport/ZGGG/',
    'shenzhen': 'airport/ZGSZ/',
    'xingtai': 'station/53798/',
    'dalian': 'airport/ZYTL/',
    'chengdu':'airport/ZUUU/',
    'yichunshi': 'station/50774/',
    'qianguozhen': 'station/50949/',
    'zhengzhou': 'airport/ZHCC/'
}
cmdline.execute('scrapy crawl WUGCrawlSpider_OC -a target={0}'.format(locdict[location]+getyesterday(begindate)).split())