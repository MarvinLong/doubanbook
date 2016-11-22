# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from doubanbook import settings

class DoubanbookPipeline(object):

    def __init__(self):
        self.client = MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        self.db = self.client.douban
        # self.collection = settings['MONGODB_COLLECTION']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db.doubanbook.update({'_id':item['book_name']},{'$set':dict(item)},upsert=True)
        return item

    def printitem(self, item):
        for i in item:
            print i.encode('gbk')
