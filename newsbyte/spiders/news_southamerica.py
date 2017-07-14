#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from .basenews import BaseNewsSpider
# import newsbyte.tools as tools
import re


class SouthAmericaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_sam'
    region = 'South America'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://www.ambito.com/rss/noticiasp.asp', 'parse_common', {'country': 'Argentina', 'language': 'Spanish', 'method': 'parse_ambito', 'xpath': None}),  # Argentina
        ('http://www.buenosairesherald.com/articles/rss.aspx', 'parse_common', {'country': 'Argentina', 'language': 'English', 'method': 'parse_buenosaires', 'xpath': None}),  # Argentina
        ('http://rss.eldiario.net/nacional.php', 'parse_common', {'country': 'Bolivia', 'language': 'Spanish', 'method': method, 'xpath': '//div[@class="nota_txt"]/p'}),  # Bolivia
        ('http://feeds.feedburner.com/TheRioTimes?format=xml', 'parse_common', {'country': 'Brazil', 'language': 'English', 'method': method, 'xpath': '//div[@class="td-post-content"]//p'}),  # Brazil
        ('http://www.huffpostbrasil.com/feeds/index.xml', 'parse_common', {'country': 'Brazil', 'language': 'Portuguese', 'method': method, 'xpath': '//div[contains(@class,"post-contents")]/p'}),  # Brazil
        ('http://www.elciudadano.cl/feed/', 'parse_common', {'country': 'Chile', 'language': 'Spanish', 'method': method, 'xpath': '//div[@class="the_content"]/p'}),  # Chile
        ('http://www.nuevodiario.co/feed/', 'parse_common', {'country': 'Colombia', 'language': 'Spanish', 'method': method, 'xpath': '//div[@class="td-post-content td-pb-padding-side"]/p'}),  # Colombia
        ('http://feeds.feedburner.com/thecitypaperbogota?format=xml', 'parse_common', {'country': 'Colombia', 'language': 'English', 'method': method, 'xpath': '//div[@class="td-post-content"]//p'}),  # Colombia
        ('http://peru.com/feed', 'parse_common', {'country': 'Peru', 'language': 'Spanish', 'method': method, 'xpath': '//div[@id="nota_body"]/p'}),  # Peru
        ('http://www.peruthisweek.com/rss', 'parse_common', {'country': 'Peru', 'language': 'English', 'method': method, 'xpath': '//article[@class="nota"]/p'}),  # Peru
    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(SouthAmericaNewsSpider, self).__init__()

    def parse_ambito(self, response):
        item = response.meta['item']
        nodes = response.xpath('//*[@id="textoDespliegue"]').extract()

        nodes = self.clean_html_tags(nodes)
        if item['description'] == '':
            item['description'] = re.search(r'.*?\n', nodes).group(0).strip()
        item['article'] = nodes
        if item['article'] == '':
            return None

        return item

    def parse_buenosaires(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@id="nota_despliegue"]//p').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['description'] == '':
            item['description'] = self.clean_description(nodes[0])
        if item['article'] == '':
            return None

        return item

