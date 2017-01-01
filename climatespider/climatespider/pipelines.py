# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
#import pymongo
import pymysql
#from datetime import datetime
#from dateutil.parser import parse


def dbconn():
    conn = pymysql.connect(
        host = settings['MYSQL_HOST'],
        user = settings['MYSQL_USER'],
        passwd = settings['MYSQL_PASS'],
        db = settings['MYSQL_DATABASE'],
        port = settings['MONGODB_PORT'],
        charset = settings['CHARSET'],
        )
    return conn
class ClimatespiderPipeline(object):
    def __init__(self):
        self.currents_seen = set()
    def process_item(self, item, spider):
        locationdict = {
            'airport/ZBAA': 'beijing',
            'station/54618': 'hejian', #cangzhou,botou
            'airport/ZBTJ': 'tianjin',
            'airport/ZBYN': 'taiyuan',
            'airport/ZSSS': 'shanghai', #suzhou
            'station/50888': 'shuangyashan',
            'station/50136': 'mohe',
            'airport/ZYHB': 'haerbin',
            'station/50854': 'daqing',
            'airport/ZSOF': 'hefei',
            'airport/ZLXY': 'xian',
            'station/54602': 'baoding',
            'airport/VMMC': 'zhuhai',
            'station/54401': 'zhangjiakou',
            'station/58506': 'jiujiang',
            'airport/ZGHA': 'changsha',
            'airport/ZSHC': 'hangzhou',
            'airport/ZHHH': 'wuhan',
            'station/58606': 'nanchang',
            'airport/ZGGG': 'foshan',
            'airport/ZGSZ': 'shenzhen',
            'station/53798': 'xingtai',
            'airport/ZYTL': 'dalian',
            'airport/ZUUU': 'chengdu',
            'station/50774': 'yichunshi',
            'station/50949': 'qianguozhen',
            'airport/ZHCC': 'zhengzhou'
        }

        dbObject = dbconn()
        cursor = dbObject.cursor()
        data_create = "create table if not exists wh_qx_data\
                    ( \
                    id                   int             not null auto_increment comment '主键id',\
                    the_date                date            not null comment '日期',\
                    the_time                time            not null comment '时间',\
                    qx_Condition            varchar(60)        null comment '状况',\
                    qx_DewPoint             varchar(60)        null comment '露点',\
                    qx_Events               varchar(60)        null comment '活动',\
                    qx_GustSpeed            varchar(60)        null comment '瞬时风速',\
                    qx_Humidity             varchar(60)        null comment '湿度',\
                    qx_Precip               varchar(60)        null comment '冰雹',\
                    qx_Pressure             varchar(60)        null comment '气压',\
                    qx_Temp                 varchar(60)        not null comment '温度',\
                    qx_Visibility           varchar(60)        null comment '能见度',\
                    qx_WindDir              varchar(60)        null comment '风向',\
                    qx_WindSpeed            varchar(60)        null comment '风速',\
                    qx_WindChill_HeatIndex  varchar(60)        null comment '风冷温_热指数',\
                    area_id                 int             not null comment '外键地区id',\
                    primary key (id)\
                    ) engine=InnoDB comment='气象资料列表';"   # the_date可以通过split('/')进行拆分成年月日
        area_create = "create table if not exists areas_data\
                    ( \
                    area_id                 int             not null auto_increment comment '主键id',\
                    area_name               varchar(60)        not null comment '地区名称',\
                    station_name            varchar(60)        not null default 0 comment '资料来源',\
                    primary key (area_id)\
                    ) engine=InnoDB comment='地区列表';"

        cursor.execute(data_create)
        cursor.execute(area_create)
        area_insert = "insert into `areas_data`(`station_name`, `area_name`) values(%s,%s)"
        area_update = "update `areas_data` set `station_name` = %s where `area_name` = %s"
        #去重
        try:
            '''
            判断数据库中是否有wh_qx_area表的存在，如果存在的话，将字段
            area_name的值提取出来并赋值到currents_seen中用于之后的去重,
            如果不存在，则pass掉错误提示。
            '''
            area_name_search = "select `area_name` from `areas_data`"
            cursor.execute(area_name_search)
            area_name = cursor.fetchall()
            self.currents_seen = set(str(x[0]) for x in area_name)
        except Exception as e:
            pass

        if locationdict[item['area']] in self.currents_seen:
            cursor.execute(area_update, (item['area'], locationdict[item['area']]))
        else:
            cursor.execute(area_insert, (item['area'], locationdict[item['area']]))
            self.currents_seen.add(item['area'])
        dbObject.commit()

        #查询地区id并插入气象资料数据表
        area_id_search = "select `area_id` from `areas_data` where `station_name`=%s"
        cursor.execute(area_id_search, item['area'])
        result = cursor.fetchone()

        if len(item) == 15:
            data_insert = "insert into wh_qx_data(`the_date`, `the_time`, `qx_Condition`, `qx_DewPoint`, `qx_Events`, `qx_GustSpeed`, `qx_Humidity`, `qx_Precip`, `qx_Pressure`, `qx_Temp`, `qx_Visibility`, `qx_WindDir`, `qx_WindSpeed`, `qx_WindChill_HeatIndex`, `area_id`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(data_insert,(item['the_date'], item['the_time'], item['qx_Condition'], item['qx_DewPoint'], item['qx_Events'], item['qx_GustSpeed'], item['qx_Humidity'], item['qx_Precip'], \
                item['qx_Pressure'], item['qx_Temp'], item['qx_Visibility'], item['qx_WindDir'], item['qx_WindSpeed'], item['qx_WindChill_HeatIndex'], str(result[0])))
                dbObject.commit()
            except Exception as e:
                print(e)
                dbObject.rollback()
        else:
            data_insert = "insert into wh_qx_data(`the_date`, `the_time`, `qx_Condition`, `qx_DewPoint`, `qx_Events`, `qx_GustSpeed`, `qx_Humidity`, `qx_Precip`, `qx_Pressure`, `qx_Temp`, `qx_Visibility`, `qx_WindDir`, `qx_WindSpeed`, `area_id`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(data_insert,(item['the_date'], item['the_time'], item['qx_Condition'], item['qx_DewPoint'], item['qx_Events'], item['qx_GustSpeed'], item['qx_Humidity'], item['qx_Precip'], \
                item['qx_Pressure'], item['qx_Temp'], item['qx_Visibility'], item['qx_WindDir'], item['qx_WindSpeed'], str(result[0])))
                dbObject.commit()
            except Exception as e:
                print(e)
                dbObject.rollback()









