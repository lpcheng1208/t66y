# -*- coding: utf-8 -*-

import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class T66YPipeline(object):
    # def __init__(self):
    #     self.file = open('t66y.txt', 'a+', encoding='utf-8')
    #
    # def process_item(self, item, spider):
    #     obj = dict(item)
    #     str = json.dumps(obj, ensure_ascii=False)
    #     self.file.write(str + "\n")
    #     return item
    #
    # def close_spider(self, spider):
    #     self.file.close()

    video_name = 'video'
    quotesInsert = '''insert into goods_video(video_name,video_url)
                        values('{video_name}','{video_url}')'''

    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):
        print(item)
        if spider.name == "1024":
            sqltext = self.quotesInsert.format(
                video_name=pymysql.escape_string(item['name']),
                video_url=pymysql.escape_string(item['video_url']),)
            # spider.log(sqltext)
            self.cursor.execute(sqltext)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
