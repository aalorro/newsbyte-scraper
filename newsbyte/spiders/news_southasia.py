#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from basenews import BaseNewsSpider
import newsbyte.tools as tools
from uuid import uuid4
from newsbyte.items import NewsbyteItem
import time
from scrapy import Request
from dateutil.parser import parse
import pdb
from datetime import datetime


class SouthAsiaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_sa'
    region = 'South Asia'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://www.ittefaq.com.bd/rss.xml', 'parse_common', {'country': 'Bangladesh', 'language': 'Bengali', 'method': method, 'xpath': '//div[@class="details"]//span/text()'}),  # Bangladesh
        ('http://bdnews24.com/?widgetName=rssfeed&widgetId=1150&getXmlFeed=true', 'parse_common', {'country': 'Bangladesh', 'language': 'English', 'method': method, 'xpath': '//div[@class="custombody print-only"]/p'}),  # Bangladesh
        ('http://www.thedailystar.net/newspaper', 'parse_dailystarlinks', {'country': 'Bangladesh', 'language': 'English', 'method': 'parse_dailystarcontent', 'xpath': None}),  # Bangladesh
        ('http://www.dzkuensel.bt/', 'parse_kuensellinks', {'country': 'Bhutan', 'language': 'Dzongkha', 'method': method, 'xpath': '//article/p'}),  # Bhutan
        ('http://www.kuenselonline.com/feed/', 'parse_common', {'country': 'Bhutan', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Bhutan
        ('http://www.bhaskar.com/rss-feed/2322/', 'parse_common', {'country': 'India', 'language': 'Hindi', 'method': method, 'xpath': '//div[@class="ba_cntebt_text introFirst"]/div'}),  # India
        ('http://rss.jagran.com/rss/news/national.xml', 'parse_common', {'country': 'India', 'language': 'Hindi', 'method': method, 'xpath': '//div[@class="article-content"]/p'}),  # India
        ('http://indianexpress.com/section/india/feed/', 'parse_common', {'country': 'India', 'language': 'English', 'method': method, 'xpath': '//div[@class="full-details"]/p'}),  # India
        ('http://maldivesindependent.com/feed', 'parse_common', {'country': 'Maldives', 'language': 'English', 'method': method, 'xpath': '//div[@class="panel-content shortocde-content"]/p'}),  # Maldives
        ('https://mihaaru.com/', 'parse_mihaaru_links', {'country': 'Maldives', 'language': 'Dhivehi', 'method': 'parse_mihaaru_content', 'xpath': None}),  # Maldives
        ('http://www.onsnews.com/feed/', 'parse_common', {'country': 'Nepal', 'language': 'Nepali', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Nepal
        ('http://feeds.nepalnews.net/rss/7399985502eaed63', 'parse_common', {'country': 'Nepal', 'language': 'English', 'method': 'parse_nepalnews', 'xpath': None}),  # Nepal
        ('http://tribune.com.pk/pakistan/feed/', 'parse_common', {'country': 'Pakistan', 'language': 'English', 'method': method, 'xpath': '//div[@class="clearfix story-content read-full"]/p'}),  # Pakistan
        ('http://feeds.feedburner.com/dawn-news?format=xml', 'parse_common', {'country': 'Pakistan', 'language': 'English', 'method': 'parse_dawn', 'xpath': None}),  # Pakistan
        ('http://feeds.bbci.co.uk/urdu/rss.xml', 'parse_common', {'country': 'Pakistan', 'language': 'Urdu', 'method': method, 'xpath': '//div[@property="articleBody"]/p'}),  # Pakistan
        ('http://www.dailymirror.lk/RSS_Feeds/breaking-news', 'parse_common', {'country': 'Sri Lanka', 'language': 'English', 'method': method, 'xpath': '//div[@class="row inner-text"]/p'}),  # Sri Lanka
        ('http://www.lankadeepa.lk/rss/latest_news/1', 'parse_common', {'country': 'Sri Lanka', 'language': 'Sinhala', 'method': method, 'xpath': '//header[@class="post-content"]/p'}),  # Sri Lanka
    ]

    def __init__(self, domain=None):
        self.domain = domain
        super(SouthAsiaNewsSpider, self).__init__()

    def parse_dailystarlinks(self, response):
        """
        Does not use an RSS Feed.
        """
        links = response.xpath('//div[@class="three-33"]/ul[@class="list-border besides"]/li/a/@href').extract()
        frontpage_links = [link for link in links if 'frontpage' in link]

        for link in frontpage_links:
            item = NewsbyteItem()

            item['source'] = response.url
            item['link'] = response.urljoin(link)

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
            request.meta['xpath'] = response.meta['xpath']

            yield request

    def parse_dailystarcontent(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//div/h1/text()').extract_first()

        pubdate = response.xpath('//div[@class="small-text"]/text()').extract_first()

        # pubdate formatting to unix timestamp
        pubdate = pubdate.strip()
        pubdate = pubdate.split(' / ')[0]
        pubdate = parse(pubdate)
        pubdate = time.mktime(pubdate.timetuple())

        item['pubdate'] = pubdate

        nodes = response.xpath('//div[@class="field-body view-mode-teaser"]/p').extract()

        nodes = self.clean_html_tags(nodes)

        item['description'] = nodes[0]

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_kuensellinks(self, response):
        """
        Does not use an RSS Feed.
        """
        for article in response.xpath('//section/article'):
            item = NewsbyteItem()
            # extract the link from returned list
            link = ''.join(article.xpath('./h2/a/@href').extract())
            # extract the description from returned list
            description = ''.join(article.xpath('./p').extract())
            # extract the pubdate from returned list
            pubdate = ''.join(article.xpath('./div[@class="post-meta"]/span[@class="post-date"]/text()').extract())
            # convert from unicode to datetime object
            pubdate = parse(pubdate)
            # convert to unix timestamp
            pubdate = time.mktime(pubdate.timetuple())

            item['source'] = response.url
            item['link'] = link
            # extract article title from returned list and strip trailing whitespace
            item['title'] = ''.join(article.xpath('./h2/a/text()').extract()).strip()
            item['description'] = tools.strip_p(tools.strip_links2(description)).strip()
            item['pubdate'] = pubdate
            item['country'] = '#' if response.meta['country'] is None else response.meta['country']
            item['item_id'] = str(uuid4())
            item['language'] = '#' if response.meta['language'] is None else response.meta['language']
            item['region'] = self.region
            request = Request(
                link,
                callback=getattr(self, response.meta['method']),
                dont_filter=response.meta.get('dont_filter', False)
            )
            request.meta['item'] = item
            request.meta['xpath'] = response.meta['xpath']

            yield request

    def parse_mihaaru_links(self, response):
        """
        Does not use an RSS Feed.
        Scrapes site for links to articles.
        """
        links = response.xpath('//div[@class="main_news_size_2"]/a')

        for link in links:
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
            pubdate = time.localtime()  # if there is no pubdate the time it is scraped is used
            item['pubdate'] = time.mktime(pubdate)
            request = Request(
                item['link'],
                callback=getattr(self, response.meta['method']),
                dont_filter=response.meta.get('dont_filter', False)
            )
            request.meta['item'] = item

            yield request

    def parse_mihaaru_content(self, response):
        """
        Scrapes article content.
        """
        try:
            item = response.meta['item']

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

            nodes = response.xpath('//article/p').extract()
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

    def parse_nepalnews(self, response):
        item = response.meta['item']
        item['description'] = self.clean_description(item['description'])
        nodes = response.xpath('//div[@class="text"]/p').extract()

        nodes = self.clean_html_tags(nodes)

        if 'Read the full story' in nodes[-1]:  # avoid partial articles with links to another site
            return None

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            print "No article"
            return None

        return item

    def parse_dawn(self, response):
        item = response.meta['item']
        nodes = response.xpath('//article/div/p/text()').extract()
        item['description'] = nodes[0]

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item
