
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from .basenews import BaseNewsSpider


class EastEuropeNewsSpider(BaseNewsSpider):
    name = 'news_ee'
    region = 'East Europe'
    method = BaseNewsSpider.method

    start_urls = [
        ('http://eng.belta.by/rss', 'parse_common', {'country': 'Belarus', 'language': 'English', 'method': method, 'xpath': '//p'}),  # Belarus
        ('http://www.belta.by/rss', 'parse_common', {'country': 'Belarus', 'language': 'Russian', 'method': method, 'xpath': '//p'}),
    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(EastEuropeNewsSpider, self).__init__()
