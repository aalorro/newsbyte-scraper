#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from scrapy import Selector
from .basenews import BaseNewsSpider
import newsbyte.tools as tools
import re


class WestAsiaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_wa'
    region = 'West Asia'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://www.almadapaper.net/rss/', 'parse_common', {'country': 'Iraq', 'language': 'Arabic', 'method': 'parse_almada', 'xpath': 'West Asia'}),  # Iraq
        ('http://feeds.feedburner.com/IraqiDinarRevaluation', 'parse_common', {'country': 'Iraq', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Iraq
        ('http://www.aljoumhouria.com/news/rss', 'parse_common', {'country': 'Lebanon', 'language': 'Arabic', 'method': 'parse_aljoum', 'xpath': None}),  # Lebanon
        ('https://rss.mmedia.me/xml/latestnewsrss.aspx', 'parse_common', {'country': 'Lebanon', 'language': 'English', 'method': method, 'xpath': '//div[@class="article_txt"]/p'}),  # Lebanon
        ('http://alwatan.com/feed', 'parse_common', {'country': 'Oman', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Oman
        ('http://www.muscatdaily.com/rss/feed/Muscat_Daily_Oman_News', 'parse_common', {'country': 'Oman', 'language': 'English', 'method': 'parse_muscat', 'xpath': None}),  # Oman
        ('http://english.pnn.ps/feed/', 'parse_common', {'country': 'Palestine', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Palestinegit
        ('http://www.raya.ps/ar/rss/news', 'parse_common', {'country': 'Palestine', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="content_box"]/p/text()'}),  # Palestine
        ('http://www.aljazeera.net/aljazeerarss/3c66e3fb-a5e0-4790-91be-ddb05ec17198/4e9f594a-03af-4696-ab98-880c58cd6718', 'parse_common', {'country': 'Saudi Arabia', 'language': 'Arabic', 'method': method, 'xpath': '//div[@id="DynamicContentContainer"]/p'}),  # Saudi Arabia
        ('http://www.arabnews.com/rss.xml', 'parse_common', {'country': 'Saudi Arabia', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry-content wow fadeInUp"]/p'}),  # Saudi Arabia
        ('http://www.arabnews.com/cat/1/rss.xml', 'parse_common', {'country': 'Saudi Arabia', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry-content wow fadeInUp"]/p'}),  # Saudi Arabia
        ('http://www.elfagr.org/rss.aspx', 'parse_common', {'country': 'Yemen', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="ni-content"]'}),  # Yemen
    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(WestAsiaNewsSpider, self).__init__()

    def parse_almada(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@class="NewsDetails"]').extract()

        nodes = self.clean_html_tags(nodes)

        item['description'] = re.search(r'.*?\n', nodes[0]).group(0).strip()

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_aljoum(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@itemprop="articleBody"]/div[@id="cke_pastebin"]').extract()
        if nodes == []:
            nodes = response.xpath('//div[@itemprop="articleBody"]').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_muscat(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@class="attribute-desc-mct"]/p').extract()
        nodes2 = response.xpath('//div[@itemprop="articleBody"]/p').extract()

        # combine the two nodes
        for node in nodes2:
            nodes.append(node)

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item
