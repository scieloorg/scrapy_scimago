# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from lxml import etree


class MongoDBPipeline(object):

    collection_name = 'journals'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.scimago_ids = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'node1-mongodb.scielo.org:27000'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'articlemeta')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        root = etree.Element('SCIMAGOLIST')

        for key, value in self.scimago_ids.items():
            item = etree.Element('title')
            item.set('ISSN', key.replace('-', ''))
            item.set('SCIMAGO_ID', value)
            root.append(item)

        with open('scimago_ids.xml', 'wb') as xml:
            xml.write(etree.tostring(
                root,
                encoding='utf-8',
                method='xml',
                pretty_print=True,
                xml_declaration=True)
            )

        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update(
            {'code': item.get('issn')},
            {'$set': {'scimago_id': item.get('scimago_id')}}
        )

        self.scimago_ids[item.get('issn')] = item.get('scimago_id')

        return item
