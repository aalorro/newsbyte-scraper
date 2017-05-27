#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
import re
import newsbyte.tools as tools
from .basenews import BaseNewsSpider


class CentralAsiaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_ca'
    region = 'Central Asia'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://inform.kz/rss/rus.xml', 'parse_common', {'country': 'Kazakhstan', 'language': 'Russian', 'method': method, 'xpath': '//div[@class="article_body"]/p'}),  # Kazakhstan
        ('http://astanatimes.com/feed/', 'parse_common', {'country': 'Kazakhstan', 'language': 'English', 'method': method, 'xpath': '//div[@class="post"]/p'}),  # Kazakhstan
        ('http://www.vb.kg/?rss', 'parse_common', {'country': 'Kyrgyzstan', 'language': 'Russian', 'method': method, 'xpath': '//div[@class="topic-text"]/p/text()'}),  # Kyrgyzstan
        ('http://www.ca-news.org/rss/canews.rss', 'parse_common', {'country': 'Kyrgyzstan', 'language': 'Russian', 'method': method, 'xpath': '//div[@class="newstext"]/p/node()'}),  # Kyrgyzstan
        ('http://kabar.kg/eng/rss', 'parse_common', {'country': 'Kyrgyzstan', 'language': 'English', 'method': 'parse_kabar', 'xpath': None}),  # Kyrgyzstan
        ('http://khovar.tj/eng/feed/', 'parse_common', {'country': 'Tajikistan', 'language': 'English', 'method': method, 'xpath': '//div[@class="column9"]/p'}),  # Tajikistan
        ('http://www.fergananews.com/rss.php', 'parse_common', {'country': 'Tajikistan', 'language': 'Tajik', 'method': 'parse_fergananews', 'xpath': None}),  # Tajikistan
        ('http://www.anons.uz/rss/allcat/latest/', 'parse_common', {'country': 'Uzbekistan', 'language': 'Mixed', 'method': method, 'xpath': '//div[@class="article_text"]/div'}),  # Uzbekistan
        ('http://www.uz24.uz/rss.php?lang=uz', 'parse_common', {'country': 'Uzbekistan', 'language': 'Mixed', 'method': method, 'xpath': '//div[@class="inner_in"]/p'}),  # Uzbekistan
        ('https://www.uzdaily.com/rss.htm', 'parse_common', {'country': 'Uzbekistan', 'language': 'English', 'method': method, 'xpath': '//div[@class="fulltext"]'}),  # Uzbekistan
    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(CentralAsiaNewsSpider, self).__init__()

    def parse_kabar(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@class="post-content clearfix"]/p/node()').extract()
        item['description'] = nodes[0]

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_fergananews(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@id="text"]/p').extract()
        # the description is the whole article therefore we change
        # the description to the first sentence of the article
        description = re.search(r'.*?\.', tools.strip_tags(item['description']))
        item['description'] = description.group(0)

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item
