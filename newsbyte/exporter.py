#! /usr/env/bin/python
import sys
sys.dont_write_bytecode = True
from scrapy.exporters import XmlItemExporter, JsonItemExporter
import time


class NewsXmlItemExporter(XmlItemExporter):

    def __init__(self, file, **kwargs):
        super(NewsXmlItemExporter, self).__init__(file, root_element='news', item_element='item', **kwargs)

    def start_exporting(self):
        self.xg.startDocument()
        self.xg.startElement(self.root_element, {'version': str(int(time.time()))})
        self.xg._write(u'\n')

    def export_item(self, item):
        if item.get('description', '') == ''or item.get('article', '') == '':
            return None

        self.xg._write(u'\t')
        self.xg.startElement(self.item_element, {})
        for name, value in self._get_serialized_fields(item, default_value=''):
            self.xg._write(u'\n\t\t')
            self._export_xml_field(name, value)
        self.xg._write(u'\n\t')
        self.xg.endElement(self.item_element)
        self.xg._write(u'\n')


class NewsJsonItemExporter(JsonItemExporter):
    def __init__(self, file, **kwargs):
        super(NewsJsonItemExporter, self).__init__(file, **kwargs)

    def export_item(self, item):
        if item.get('description', '') == '' or item.get('article', '') == '':
            print "No description or content"
            return None

        if self.first_item:
            self.first_item = False
        else:
            self.file.write(',\n')
        itemdict = dict(self._get_serialized_fields(item))
        self.file.write(self.encoder.encode(itemdict))
