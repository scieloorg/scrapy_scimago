# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JournalItem(scrapy.Item):
    # define the fields for your item here like:
    issn = scrapy.Field()
    scimago_id = scrapy.Field()
