#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import sys
sys.dont_write_bytecode = True
import scrapy


class NewsbyteItem(scrapy.Item):
    source = scrapy.Field()
    link = scrapy.Field()
    pubdate = scrapy.Field()
    country = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    article = scrapy.Field()
    item_id = scrapy.Field()
    language = scrapy.Field()
    region = scrapy.Field()
    thumbnail = scrapy.Field()
