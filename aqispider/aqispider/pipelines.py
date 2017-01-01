# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymysql

def dbconn():
    conn = pymysql.connect(
        host=settings['MYSQL_HOST'],
        user=settings['MYSQL_USER'],
        passwd=settings['MYSQL_PASS'],
        db=settings['MYSQL_DATABASE'],
        port=settings['MONGODB_PORT'],
        charset=settings['CHARSET']
    )
    return conn

class AqispiderPipeline(object):
    def __init__(self):
        self.currents_seen = set()
    def process_item(self, item, spider):
        dbObject = dbconn()
        cursor = dbObject.cursor()
        data_create = "create table if not exists `aqi_cli_data`\
                            ( \
                            `id`                      int                 not null auto_increment comment '主键id',\
                            `datetime`                datetime            not null comment '日期',\
                            `qx_Humidity`             float               null default null comment '湿度',\
                            `qx_Pressure`             varchar(60)         null default null comment '气压',\
                            `qx_Temp`                 varchar(60)         null default null comment '温度',\
                            `kq_aqi`                  varchar(60)         null default null comment 'AQI',\
                            `kq_quality`              varchar(60)         null default null comment '空气质量指数类别',\
                            `kq_primary_pollutant`    varchar(60)         null default null comment '首要污染物',\
                            `kq_pm2_5`                varchar(60)         null default null comment 'PM2.5细颗粒物',\
                            `kq_pm10`                 varchar(60)         null default null comment 'PM10可吸入颗粒物',\
                            `kq_co`                   varchar(60)         null default null comment '一氧化碳',\
                            `kq_no2`                  varchar(60)         null default null comment '二氧化氮',\
                            `kq_o3`                   varchar(60)         null default null comment '臭氧1小时平均',\
                            `kq_o3_8h`                varchar(60)         null default null comment '臭氧8小时平均',\
                            `kq_so2`                  varchar(60)         null default null comment '二氧化硫',\
                            `area_id`                 int                 not null comment '外键地区id',\
                            primary key (id)\
                            ) engine=InnoDB comment='气象与空气质量资料列表';"
        area_create = "create table if not exists `areas_data`\
                            ( \
                            `area_id`                 int                 not null auto_increment comment '主键id',\
                            `area_name`               varchar(60)         not null comment '地区名称',\
                            `station_name`            varchar(60)         null default null comment '气象资料来源',\
                            primary key (area_id)\
                            ) engine=InnoDB comment='地区列表';"

        cursor.execute(data_create)
        cursor.execute(area_create)
        area_insert = "insert into `areas_data`(`area_name`) values(%s)"

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

        if item['area'] in self.currents_seen:
            pass
        else:
            cursor.execute(area_insert, (item['area']))
            self.currents_seen.add(item['area'])
        dbObject.commit()



        try:
            area_id_search = "select `area_id` from `areas_data` where `area_name`=%s and station_name is not null"
            cursor.execute(area_id_search, item['area'])
            result = cursor.fetchone()
            data_update = "update `aqi_cli_data` set `kq_aqi`=%s, `kq_quality`=%s, `kq_primary_pollutant`=%s, \
                          `kq_pm2_5`=%s, `kq_pm10`=%s, `kq_co`=%s, `kq_no2`=%s, `kq_o3`=%s, `kq_o3_8h`=%s,  \
                          `kq_so2`=%s where `datetime`=%s and `area_id`=%s"
            cursor.execute(data_update, (item['kq_aqi'], item['kq_quality'], item['kq_primary_pollutant'],
                                         item['kq_pm2_5'], item['kq_pm10'], item['kq_co'], item['kq_no2'],
                                         item['kq_o3'], item['kq_o3_8h'], item['kq_so2'], item['datetime'],
                                         str(result[0])))
        except Exception as e:
            area_id_search = "select `area_id` from `areas_data` where `area_name`=%s"
            cursor.execute(area_id_search, item['area'])
            result = cursor.fetchone()
            data_insert = "insert into `aqi_cli_data` (`datetime`, `kq_aqi`, `kq_quality`, `kq_primary_pollutant`,  \
                          `kq_pm2_5`, `kq_pm10`, `kq_co`, `kq_no2`, `kq_o3`, `kq_o3_8h`, `kq_so2`, `area_id`) values  \
                          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(data_insert, (item['datetime'], item['kq_aqi'], item['kq_quality'], item['kq_primary_pollutant'],
                                         item['kq_pm2_5'], item['kq_pm10'], item['kq_co'], item['kq_no2'], item['kq_o3'],
                                         item['kq_o3_8h'], item['kq_so2'], str(result[0])))
        dbObject.commit()