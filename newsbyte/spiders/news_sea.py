#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from scrapy import Selector, Request
from .basenews import BaseNewsSpider
import feedparser
import time
from uuid import uuid4
from dateutil.parser import parse
import newsbyte.tools as tools
from newsbyte.items import NewsbyteItem


class SEANewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_sea'
    region = 'South East Asia'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://kohsantepheapdaily.com.kh/rss', 'parse_common', {'country': 'Cambodia', 'language': 'Khmer', 'method': method, 'xpath': '//div[@id="fullArticle"]/p'}),  # Cambodia
        ('http://vodhotnews.com/rss', 'parse_common', {'country': 'Cambodia', 'language': 'Khmer', 'method': method, 'xpath': '//article/p'}),  # Cambodia
        ('http://feeds.thecambodianews.net/rss/c7e1014a94f7e43b', 'parse_common', {'country': 'Cambodia', 'language': 'English', 'method': method, 'xpath': '//div[@class="text"]/p'}),  # Cambodia
        ('http://www.tribunnews.com/rss', 'parse_common', {'country': 'Indonesia', 'language': 'Indonesian', 'method': method, 'xpath': '//div[@class="side-article txt-article"]/p'}),  # Indonesia
        ('http://www.merdeka.com/feed/', 'parse_common', {'country': 'Indonesia', 'language': 'Indonesian', 'method': method, 'xpath': '//div[@id="mdk-body-newsarea"]/p'}),  # Indonesia
        ('http://jakartaglobe.beritasatu.com/rss/news/', 'parse_common', {'country': 'Indonesia', 'language': 'English', 'method': 'parse_jakartaglobe', 'xpath': None}),  # Indonesia
        ('http://feeds.laosnews.net/rss/a6670896145a3ae3', 'parse_common', {'country': 'Laos', 'language': 'English', 'method': 'parse_laosnews', 'xpath': None}),  # Laos
        ('http://vientianemai.net/site/column/1.html', 'parse_vienlinks', {'country': 'Laos', 'language': 'Lao', 'method': 'parse_viencontent', 'xpath': None}),  # Laos
        ('https://www.kuanjailao.com/feed', 'parse_common', {'country': 'Laos', 'language': 'Lao', 'method': method, 'xpath': '//div[@class="entry"]/p'}), # Laos
        ('http://lao.voanews.com/api/', 'parse_common', {'country': 'Laos', 'language': 'Lao', 'method': method, 'xpath': '//div[@class="wsw"]/p'}), # Laos
        ('http://www.bharian.com.my/terkini.xml', 'parse_common', {'country': 'Malaysia', 'language': 'Malay', 'method': method, 'xpath': '//div[@class="field-item even"]/p'}),  # Malaysia
        ('http://www.thestar.com.my/rss/news/nation/', 'parse_common', {'country': 'Malaysia', 'language': 'English', 'method': method, 'xpath': '//div[@class="story"]/p'}),  # Malaysia
        ('http://www.irrawaddy.org/feed', 'parse_common', {'country': 'Myanmar', 'language': 'English', 'method': method, 'xpath': '//div[@class="article-entry pad"]/p'}),  # Myanmar
        ('http://feeds.bbci.co.uk/burmese/rss.xml', 'parse_common', {'country': 'Myanmar', 'language': 'Burmese', 'method': method, 'xpath': '//div[@property="articleBody"]/p'}),  # Myanmar
        ('http://www.balita.net.ph/feed', 'parse_common', {'country': 'Philippines', 'language': 'Tagalog', 'method': method, 'xpath': '//div[@id="container"]/div[1]/p', 'thumb_xpath': '//p/a/img/@src'}),  # Philippines
        ('https://www.abante.com.ph/news', 'parse_abante_links', {'country': 'Philippines', 'language': 'Tagalog', 'method': 'parse_abante_content', 'xpath': None}),  # Philippines
        ('https://www.abante.com.ph/ent', 'parse_abante_links', {'country': 'Philippines', 'language': 'Tagalog', 'method': 'parse_abante_content', 'xpath': None}),  # Philippines
        ('https://www.abante.com.ph/sports3', 'parse_abante_links', {'country': 'Philippines', 'language': 'Tagalog', 'method': 'parse_abante_content', 'xpath': None}),  # Philippines
        ('http://www.tempo.com.ph/feed', 'parse_common', {'country': 'Philippines', 'language': 'English', 'method': method, 'xpath': '//div[contains(@class, "entry")]/p', 'thumb_xpath': '//p/a/img/@src'}),  # Philippines
        ('http://www.abs-cbnnews.com/nation/feed', 'parse_common', {'country': 'Philippines', 'language': 'English', 'method': method, 'xpath': '//div[@class="article-content"]/p', 'thumb_xpath': '//figure/img/@src'}),  # Philippines
        ('http://www.abs-cbnnews.com/entertainment/feed', 'parse_common', {'country': 'Philippines', 'language': 'English', 'method': method, 'xpath': '//div[@class="article-content"]/p', 'thumb_xpath': '//figure/img/@src'}),  # Philippines
        ('http://www.abs-cbnnews.com/sports/feed', 'parse_common', {'country': 'Philippines', 'language': 'English', 'method': method, 'xpath': '//div[@class="article-content"]/p', 'thumb_xpath': '//figure/img/@src'}),  # Philippines
        ('http://www.bangkokpost.com/rss/data/most-recent.xml', 'parse_common', {'country': 'Thailand', 'language': 'English', 'method': method, 'xpath': '//div[@class="articleContents"]/p/node()'}),  # Thailand
        ('http://www.thairath.co.th/rss/news', 'parse_common', {'country': 'Thailand', 'language': 'Thai', 'method': method, 'xpath': '//article/p'}),  # Thailand
        ('http://e.vnexpress.net/rss/home.rss', 'parse_common', {'country': 'Vietnam', 'language': 'English', 'method': method, 'xpath': '//div//p'}),  # Vietnam
        ('http://vnexpress.net/rss/thoi-su.rss', 'parse_common', {'country': 'Vietnam', 'language': 'Vietnamese', 'method': method, 'xpath': '//div//p'}),  # Vietnam
    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(SEANewsSpider, self).__init__()

    def parse_cambodianews(self, response):
        item = response.meta['item']
        item['description'] = self.clean_description(item['description'])
        nodes = response.xpath('//div[@class="article_text"]/p').extract()

        nodes = self.clean_html_tags(nodes)

        if 'Read the full story' in nodes[-1]:  # avoid partial articles with links to another site
            return None

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_jakartaglobe(self, response):
        item = response.meta['item']
        article = response.xpath('//div[@class="content"]')

        nodes = article.xpath('./p').extract()
        nodes_2 = article.xpath('./div/div[@class="more-content"]/p').extract()

        for node in nodes_2:
            nodes.append(node)

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)

        if item['article'] == '':
            return None

        return item

    def parse_laosnews(self, response):
        item = response.meta['item']
        item['description'] = self.clean_description(item['description'])
        nodes = response.xpath('//div[@class="text"]/p').extract()

        nodes = self.clean_html_tags(nodes)

        if 'Read the full story' in nodes[-1]:  # avoid partial articles with links to another site
            return None

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_vienlinks(self, response):
        """
        There's an issue regarding date published... currently using the date when it's scraped.
        Does not use an RSS Feed.
        """
        for link in response.xpath('//div[@class="list-view"]//a/@href'):
            full_link = response.urljoin(link.extract())
            item = NewsbyteItem()
            item['source'] = response.url
            item['link'] = full_link
            item['country'] = '#' if response.meta['country'] is None else response.meta['country']
            item['item_id'] = str(uuid4())
            item['language'] = '#' if response.meta['language'] is None else response.meta['language']
            item['region'] = self.region
            pubdate = time.localtime()
            item['pubdate'] = time.mktime(pubdate)
            request = Request(
                full_link,
                callback=getattr(self, response.meta['method']),
                dont_filter=response.meta.get('dont_filter', False)
            )
            request.meta['item'] = item

            yield request

    def parse_viencontent(self, response):
        item = response.meta['item']
        item['title'] = ''.join(response.xpath('//div[@class="col-lg-12"]/h1/text()').extract())  # extract title from returned list

        nodes = response.xpath('//div[@class="col-lg-9"]/p').extract()

        nodes = self.clean_html_tags(nodes)
        item['description'] = self.clean_description(nodes[0])
        item['article'] = self.newline_join_lst(nodes)

        if item['article'] == '':
            return None

        return item

    def parse_abante_links(self, response):
        """
        Does not use an RSS Feed.
        Scrapes site for links to articles.
        """

        # Gets links
        links = response.xpath('//div[contains(@class,"td-animation")]')
        for link in links:
            try:
                item = NewsbyteItem()
                item['source'] = response.url
                url = link.xpath('div[@class="item-details"]/h3/a/@href').extract()
                item['link'] = url[0]
                title = link.xpath('div[@class="item-details"]/h3/a/@title').extract()
                item['title'] = title[0]
                item['country'] = '#' if response.meta['country'] is None else response.meta['country']
                item['item_id'] = str(uuid4())
                item['language'] = '#' if response.meta['language'] is None else response.meta['language']
                item['region'] = self.region
                pubdate = link.xpath('div[@class="item-details"]/div/span/time/@datetime').extract()
                pubdate = parse(pubdate[0], fuzzy=True, dayfirst=False)
                item['pubdate'] = time.mktime(pubdate.timetuple())
                description = link.xpath('div[@class="item-details"]/div[@class="td-excerpt"]').extract()
                item['description'] = description[0]
                thumbnail = link.xpath('div[@class="td-module-thumb"]/a/img/@src').extract()
                item['thumbnail'] = thumbnail[0]
                request = Request(
                    item['link'],
                    callback=getattr(self, response.meta['method']),
                    dont_filter=response.meta.get('dont_filter', False)
                )
                request.meta['item'] = item

                yield request
            except Exception as e:
                print e

    def parse_abante_content(self, response):
        """
        Scrapes article content.
        """
        try:
            item = response.meta['item']

            nodes = response.xpath('//div[@class="td-post-content"]/p').extract()
            nodes = self.clean_html_tags(nodes)
            item['description'] = self.clean_description(item['description'])

            if item['description'] == '':
                description = nodes[0]
                item['description'] = (description[:512] + '...') if len(description) > 512 else description

            item['article'] = self.newline_join_lst(nodes)
            if item['article'] == '':
                print "No article"
                return None

            return item
        except Exception as e:
            print e

    def parse_komchad(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@class="newsDetail"]/div/node()').extract()
        if not nodes:
            nodes = response.xpath('//div[@class="newsDetail"]/p/node()').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)

        if item['article'] == '':
            return None

        return item
