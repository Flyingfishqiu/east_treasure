# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter,JsonItemExporter

import pymongo


class TreasurePipeline(object):
    def open_spider(self, spider):
        self.file = open('treasure.csv', 'wb')
        self.write = CsvItemExporter(self.file)
        self.write.start_exporting()

    def process_item(self, item, spider):
        self.write.export_item(item)
        return item


    def close_spider(self, spider):
        self.file.close()
        self.write.finish_exporting()


class TreasureJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('treasure.json', 'wb')
        self.write = JsonItemExporter(self.file)
        self.write.start_exporting()

    def process_item(self, item, spider):
        self.write.export_item(item)
        return item


    def close_spider(self, spider):
        self.file.close()
        self.write.finish_exporting()

class TreasureMongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['AQI_Mongo']
        self.collection = self.db['aqi']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


    def close_spider(self, spider):
        self.client.close()
