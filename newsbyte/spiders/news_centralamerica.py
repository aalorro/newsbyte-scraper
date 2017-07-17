#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from scrapy import Selector, Request
from .basenews import BaseNewsSpider
import newsbyte.tools as tools
import re
import feedparser
import time
import lxml
from uuid import uuid4
from dateutil.parser import parse
from newsbyte.items import NewsbyteItem


class CentralAmericaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_cam'
    region = 'Central America'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://www.listindiario.com/rss/portada/', 'parse_common', {'country': 'Dominican Republic', 'language': 'Spanish', 'method': method, 'xpath': '//div[@id="ArticleBody"]/p'}),  # Dominican Republic
        ('https://dominicantoday.com/dr/local/', 'parse_dominican_today_links', {'country': 'Dominican Republic', 'language': 'English', 'method': 'parse_dominican_today_content', 'xpath': None}),  # Dominican Republic
        ('http://www.elsalvadornoticias.net/feed/', 'parse_common', {'country': 'El Salvador', 'language': 'Spanish', 'method': 'parse_elsalvador', 'xpath': None}),  # El Salvador
        ('http://www.prensalibre.com/smartTV/nacionales.xml', 'parse_common', {'country': 'Guatemala', 'language': 'Spanish', 'method': 'parse_prensalibre', 'xpath': None}),  # Guatemala
        ('http://www.haitilibre.com/rss-flash-en.xml', 'parse_common', {'country': 'Haiti', 'language': 'English', 'method': method, 'xpath': '//td[@width="100%"]/text()[not(ancestor::span)]'}),  # Haiti
        ('https://www.haitilibre.com/rss-flash.xml', 'parse_common', {'country': 'Haiti', 'language': 'French', 'method': method, 'xpath': '//td[@width="100%"]/text()[not(ancestor::span)]'}),  # Haiti
        ('http://www.jamaicaobserver.com/rss/news/', 'parse_common', {'country': 'Jamaica', 'language': 'English', 'method': method, 'xpath': '//div[@id="story"]/p'}),  # Jamaica
        ('http://www.jamaica-gleaner.com/feed/rss.xml', 'parse_common', {'country': 'Jamaica', 'language': 'English', 'method': method, 'xpath': '//div[@property="content:encoded"]//text()'}),  # Jamaica
        ('http://www.20minutos.com.mx/rss/', 'parse_common', {'country': 'Mexico', 'language': 'Spanish', 'method': method, 'xpath': '//div[@class="article-content"]/p'}),  # Mexico
        ('http://www.mundodehoy.com/index.php/feed/index.rss', 'parse_common', {'country': 'Mexico', 'language': 'Spanish', 'method': method, 'xpath': '//div[@id="article_body"]/p'}),  # Mexico
        ('http://www.elnuevodiario.com.ni/rss/', 'parse_common', {'country': 'Nicaragua', 'language': 'Spanish', 'method': 'parse_nuevo', 'xpath': None}),  # Nicaragua
        ('http://www.diariolibre.com/rss/portada.xml', 'parse_common', {'country': 'Panama', 'language': 'Spanish', 'method': method, 'xpath': '//div[@class="text"]/p/text()'}),  # Panama
        ('http://feeds.feedburner.com/newsroompanama?format=xml', 'parse_common', {'country': 'Panama', 'language': 'English', 'method': 'parse_newsroompanama', 'xpath': None}),  # Panama

    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(CentralAmericaNewsSpider, self).__init__()

    def parse_dominican_today_links(self, response):
        """
        Does not use an RSS Feed.
        Scrapes site for links to articles.
        Only gets news categorized under "Local"
        """
        links = response.xpath('//div[contains(@class, "noticias2-category")]/h2/a')

        for link in links:
            try:
                item = NewsbyteItem()
                item['source'] = response.url
                url = link.xpath('@href').extract()
                item['link'] = url[0]
                title = link.xpath('text()').extract()
                item['title'] = title[0]
                item['country'] = '#' if response.meta['country'] is None else response.meta['country']
                item['item_id'] = str(uuid4())
                item['language'] = '#' if response.meta['language'] is None else response.meta['language']
                item['region'] = self.region
                request = Request(
                    item['link'],
                    callback=getattr(self, response.meta['method']),
                    dont_filter=response.meta.get('dont_filter', False)
                )
                request.meta['item'] = item

                yield request
            except Exception as e:
                print e

    def parse_dominican_today_content(self, response):
        """
        Scrapes article content.
        """
        try:
            item = response.meta['item']

            date = response.xpath('//span[@class="fecha"]/text()').extract()
            date = re.sub(r'\| ', '', date[0])
            date = parse(date, fuzzy=True)
            item['pubdate'] = time.mktime(date.timetuple())

            if 'thumb_xpath' in response.meta:
                thumb_xpath = response.meta['thumb_xpath']
                try:
                    thumb_nodes = response.xpath(thumb_xpath).extract()
                    thumb_nodes = self.get_images(thumb_nodes)
                    item['thumbnail'] = thumb_nodes[0]
                except:
                    item['thumbnail'] = ''
            else:
                item['thumbnail'] = ''

            nodes = response.xpath('//div[@class="article-body-text"]/span/p').extract()
            nodes = self.clean_html_tags(nodes)

            description = nodes[0]
            item['description'] = (description[:512] + '...') if len(description) > 512 else description

            item['article'] = self.newline_join_lst(nodes)
            if item['article'] == '':
                print "No article"
                return None

            return item
        except Exception as e:
            print e

    def parse_elsalvador(self, response):
        item = response.meta['item']
        item['description'] = tools.strip_tags(item['description'])
        nodes = response.xpath('//div[@id="content-area"]/p').extract()
        # get rid of extraneous html comments in the first and last elements of the list
        nodes = nodes[1:-1]

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_lenouvelliste(self, response):
        item = response.meta['item']

        nodes = ''.join(response.xpath('//div[@class="bodytextarticle"]/p').extract())
        nodes = tools.strip_p(nodes).strip()

        #  convert the returned list from the xpath method into a string and strip any trailing whitespace
        # from the string
        description = ''.join(response.xpath('//div[@class="entry-content"]/p/em/text()').extract()).strip()

        # if description is an empty string, take the first line of the article as the description
        if description == '':
            description = re.search(r'.*?\n\n', nodes).group(0).strip()

        item['description'] = description
        item['article'] = nodes

        if item['article'] == '':
            return None

        return item

    def parse_prensalibre(self, response):
        item = response.meta['item']
        item['description'] = self.clean_description(item['description'])
        nodes = response.xpath('//div[@class="sart-content"]/*/text()').extract()

        nodes = self.clean_html_tags(nodes)
        nodes = [node for node in nodes if 'CDATA' not in node]

        item['article'] = self.newline_join_lst(nodes[1:])

        if item['article'] == '':
            return None

        return item

    def parse_nuevo(self, response):
        item = response.meta['item']
        nodes = ''.join(response.xpath('//div[@itemprop="articleBody"]').extract())

        nodes = tools.strip_div(tools.convert_p(nodes)).strip()

        item['article'] = nodes
        item['description'] = re.search(r'.*?\n\n', nodes).group(0).strip()
        if item['article'] == '':
            return None

        return item

    def parse_newsroompanama(self, response):
        item = response.meta['item']

        nodes = response.xpath('//div[@class="entry clearfix"]/p').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        item['description'] = nodes[0]
        if item['article'] == '':
            return None

        return item
