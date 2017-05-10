#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
sys.dont_write_bytecode = True


class NewsbytePipeline(object):
    def process_item(self, item, spider):
        return item
