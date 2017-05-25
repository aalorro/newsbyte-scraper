#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from .basenews import BaseNewsSpider


class EastAsiaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_ea'
    region = 'East Asia'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://www.sonin.mn/feed', 'parse_common', {'country': 'Mongolia', 'language': 'Mongolian', 'method': method, 'xpath': '//div[@id="text-show"]/div[@style="text-align: justify;"]'}),  # Mongolia
        ('http://mongolia.gogo.mn/feed', 'parse_common', {'country': 'Mongolia', 'language': 'English', 'method': method, 'xpath': '//div[@class="newscontent-container"]/p/span'}),  # Mongolia

    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(EastAsiaNewsSpider, self).__init__()


