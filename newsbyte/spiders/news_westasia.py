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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WestAsiaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_wa'
    region = 'West Asia'
    method = BaseNewsSpider.method
    start_urls = [
        ('http://www.almadapaper.net/rss/', 'parse_common', {'country': 'Iraq', 'language': 'Arabic', 'method': 'parse_almada', 'xpath': None}),  # Iraq
        ('http://feeds.iraqsun.com/rss/c31d0aaa23b24a75', 'parse_common', {'country': 'Iraq', 'language': 'English', 'method': method, 'xpath': '//div[@class="banner-text"]/p'}),  # Iraq
        ('http://www.aljoumhouria.com/news/rss', 'parse_common', {'country': 'Lebanon', 'language': 'Arabic', 'method': 'parse_aljoum', 'xpath': None}),  # Lebanon
        ('http://www.dailystar.com.lb/RSS.aspx?live=1', 'parse_common', {'country': 'Lebanon', 'language': 'English', 'method': 'parse_daily_star', 'xpath': None}),  # Lebanon
        ('http://alwatan.com/feed', 'parse_common', {'country': 'Oman', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Oman
        ('http://www.muscatdaily.com/rss/feed/Muscat_Daily_Oman_News', 'parse_common', {'country': 'Oman', 'language': 'English', 'method': 'parse_muscat', 'xpath': None}),  # Oman
        ('http://english.pnn.ps/feed/', 'parse_common', {'country': 'Palestine', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Palestine
        ('http://www.al-ayyam.ps/rss.php', 'parse_al_ayyam', {'country': 'Palestine', 'language': 'Arabic', 'method': method, 'xpath': '//div[@id="main_div"]/p'}),  # Palestine
        ('http://www.aljazeera.net/aljazeerarss/3c66e3fb-a5e0-4790-91be-ddb05ec17198/4e9f594a-03af-4696-ab98-880c58cd6718', 'parse_common', {'country': 'Saudi Arabia', 'language': 'Arabic', 'method': method, 'xpath': '//div[contains(@class,"article-body")]/p'}),  # Saudi Arabia
        ('http://www.arabnews.com/rss.xml', 'parse_common', {'country': 'Saudi Arabia', 'language': 'English', 'method': method, 'xpath': '//div[contains(@class,"entry-content")]/div[contains(@class,"show-for-small-only")]'}),  # Saudi Arabia
        ('http://www.arabnews.com/cat/1/rss.xml', 'parse_common', {'country': 'Saudi Arabia', 'language': 'English', 'method': method, 'xpath': '//div[contains(@class,"entry-content")]/div[contains(@class,"show-for-small-only")]'}),  # Saudi Arabia
        ('https://www.al-tagheer.com/rss.php?cat=1', 'parse_common', {'country': 'Yemen', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="story_text"]/p'}),  # Yemen
        ('http://www.saba.ye/en/rsscatfeed.php?category=14', 'parse_saba', {'country': 'Yemen', 'language': 'English', 'method': method, 'xpath': '//div[@class="mainText"]'}),  # Yemen
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

    def parse_daily_star(self, response):
        # Scrapes dynamic content of Daily Star news site
        item = response.meta['item']

        try:
            # Open new window and load article in it
            driver = webdriver.PhantomJS()
            driver.get(item['link'])

            # Wait until dynamically loaded element appears
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="divDetails"]')))

            # Start scraping article
            article = []

            for text in driver.find_elements_by_xpath('//div[@id="divDetails"]/p'):
                article.append(text.text)

            article = self.clean_html_tags(article)
            item['description'] = self.clean_description(item['description'])

            if item['description'] == '':
                item['description'] = article[0]

            item['article'] = self.newline_join_lst(article)
            if item['article'] == '':
                print "No article"
                driver.close()
                return None

            driver.close()
            return item
        except Exception as e:
            print '%s: %s' % (type(e), e)
            driver.close()

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

    def parse_al_ayyam(self, response):
        """
        This function uses feedparser to parse through rss feeds extracting the XML nodes important to present in news articles
         (i.e title of article, link, publication date, etc.) and populates the scrapy.Fields in the NewsbyteItem dictionary with said info.
        """
        feed = feedparser.parse(response.body)
        for entry in feed.entries:
            try:
                item = NewsbyteItem()
                item['source'] = response.url
                item['title'] = lxml.html.fromstring(entry.title).text
                pubdate = entry.published
                if not isinstance(pubdate, unicode):  # if pubdate is not unicode

                    # fix wrong dates
                    if pubdate.tm_year < 2000:
                        pubdate = time.localtime()
                    elif time.localtime().tm_yday - pubdate.tm_yday > 7:
                        continue
                    else:
                        item['pubdate'] = time.mktime(pubdate)
                else:
                    pubdate = parse(pubdate, fuzzy=True, dayfirst=True)
                    pubdate = time.mktime(pubdate.timetuple())

                item['pubdate'] = pubdate
                item['link'] = 'http://www.al-ayyam.ps/' + entry.link
                item['country'] = '#' if response.meta['country'] is None else response.meta['country']
                item['language'] = '#' if response.meta['language'] is None else response.meta['language']
                item['description'] = entry.description
                item['item_id'] = str(uuid4())
                item['region'] = self.region
                request = Request(
                    item['link'],
                    callback=getattr(self, response.meta['method']),
                    dont_filter=response.meta.get('dont_filter', False)
                )

                request.meta['item'] = item
                request.meta['entry'] = entry
                request.meta['xpath'] = response.meta['xpath']
                if 'thumb_xpath' in response.meta:
                    request.meta['thumb_xpath'] = response.meta['thumb_xpath']
                else:
                    item['thumbnail'] = ''

                yield request

            except Exception as e:
                print '%s: %s' % (type(e), e)
                print entry

    def parse_saba(self, response):
        """
        This function uses feedparser to parse through rss feeds extracting the XML nodes important to present in news articles
         (i.e title of article, link, publication date, etc.) and populates the scrapy.Fields in the NewsbyteItem dictionary with said info.
        """
        feed = feedparser.parse(response.body)
        for entry in feed.entries:
            try:
                item = NewsbyteItem()
                item['source'] = response.url
                item['title'] = lxml.html.fromstring(entry.title).text
                pubdate = entry.published
                if not isinstance(pubdate, unicode):  # if pubdate is not unicode

                    # fix wrong dates
                    if pubdate.tm_year < 2000:
                        pubdate = time.localtime()
                    elif time.localtime().tm_yday - pubdate.tm_yday > 7:
                        continue
                    else:
                        item['pubdate'] = time.mktime(pubdate)
                else:
                    pubdate = parse(pubdate, fuzzy=True, dayfirst=True)
                    pubdate = time.mktime(pubdate.timetuple())

                item['pubdate'] = pubdate
                item['link'] = re.sub('sab.ye', 'saba.ye', entry.link, flags=re.M | re.I)
                item['country'] = '#' if response.meta['country'] is None else response.meta['country']
                item['language'] = '#' if response.meta['language'] is None else response.meta['language']
                item['description'] = entry.description
                item['item_id'] = str(uuid4())
                item['region'] = self.region
                request = Request(
                    item['link'],
                    callback=getattr(self, response.meta['method']),
                    dont_filter=response.meta.get('dont_filter', False)
                )

                request.meta['item'] = item
                request.meta['entry'] = entry
                request.meta['xpath'] = response.meta['xpath']
                if 'thumb_xpath' in response.meta:
                    request.meta['thumb_xpath'] = response.meta['thumb_xpath']
                else:
                    item['thumbnail'] = ''

                yield request

            except Exception as e:
                print '%s: %s' % (type(e), e)
                print entry
