# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class DseMarketSummaryPipeline(object):
    collection_name = 'DseMarketSummaryCollection'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name != "dsemarketsummary":
            return item
        self.db[self.collection_name].insert_one(dict(item))
        return item


class DayEndArchivePipeline(object):
    collection_name = 'DayEndArchiveCollection'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name != "dayendarchive":
            return item
        self.db[self.collection_name].insert_one(dict(item))
        return item


class TickerPipeline(object):
    collection_name = 'TickerCollection'
    collection_name_tracker = 'TickerCollectionTracker'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name != "ticker":
            return item

        cursor = self.db[self.collection_name_tracker].find({"trading_code": item['trading_code']}).limit(1)

        if cursor.count():
            val = cursor[0]
            if val["last_traded_price"] != item["last_traded_price"] or \
                    val["change"] != item["change"] or \
                    val["status"] != item["status"]:
                result = self.db[self.collection_name].insert_one(dict(item))

                val["last_traded_price"] = item["last_traded_price"]
                val["change"] = item["change"]
                val["status"] = item["status"]
                val['ticker_id'] = result.inserted_id

                self.db[self.collection_name_tracker].update({'_id': val['_id']}, {'$set': dict(val)})
        else:
            result = self.db[self.collection_name].insert_one(dict(item))
            temp = dict(item)
            temp['ticker_id'] = result.inserted_id
            self.db[self.collection_name_tracker].insert_one(temp)

        return item


class CategoryPipeline(object):
    collection_name = 'CategoryCollection'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name != "category":
            return item
        self.db[self.collection_name].insert_one(dict(item))
        return item
