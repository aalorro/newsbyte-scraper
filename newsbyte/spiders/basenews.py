#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
from scrapy import Spider, Request
import feedparser
import time
import lxml
from uuid import uuid4
from dateutil.parser import parse
from newsbyte.items import NewsbyteItem
from urlparse import urlparse
import newsbyte.tools as tools


class BaseNewsSpider(Spider):

    region = "Default"
    method = 'parse_body'

    """
     All Newsbyte spiders inherit this class to reduce code redundancy.
    """
    def start_requests(self):
        """
        Modified the start_requests method to include the additional elements in the start_urls list
        """
        for url, method, meta in self.start_urls:
            if self.domain is None or urlparse(url).netloc == self.domain:
                yield Request(
                    url,
                    callback=getattr(self, method),
                    meta=meta
                )

#####################
### Helper Functions ###
#####################

    def clean_html_tags(self, lst):
        # parse out all html tags unrelated to font styles
        lst = [tools.strip_div(tools.strip_p(tools.strip_links2(tools.strip_span(tools.convert_br(element))))).strip() for element in lst if element]
        # parse out javascript
        lst = [tools.strip_javascript(element) for element in lst if element]
        # parse out iframe and img tags
        lst = [tools.strip_iframe(tools.strip_img(element)) for element in lst if element]
        # parse out empty elements
        lst = [element for element in lst if element]
        return lst

    def newline_join_lst(self, lst):
        return '\n\n'.join(lst)

    def clean_description(self, text):
        return tools.html_unescape(tools.strip_tags(text)).strip()

    def get_images(self, lst):
        # get src attribute from img tag
        lst = [tools.get_src_attr(element).strip() for element in lst if element]
        # parse out empty elements
        lst = [element for element in lst if element]
        return lst

####################
#### RSS parser ####
####################

    def parse_common(self, response):
        """
        This function uses feedparser to parse through rss feeds extracting the XML nodes important to present in news articles
         (i.e title of article, link, publication date, etc.) and populates the scrapy.Fields in the NewsbyteItem dictionary with said info.
        """
        feed = feedparser.parse(response.body)
        for entry in feed.entries:
            try:
                item = NewsbyteItem()

                attributes = entry.keys()
                if 'published_parsed' in attributes:
                    pubdate = entry.published_parsed
                else:
                    pubdate = None
                if pubdate is None and 'updated_parsed' in attributes:
                    pubdate = entry.updated_parsed
                elif pubdate is None and 'published' in attributes:
                    pubdate = entry.published
                if pubdate is None:
                    pubdate = time.localtime()  # if there is no pubdate the time it is scraped is used
                if not isinstance(pubdate, unicode):  # if pubdate is not unicode
                    # fix wrong dates
                    if pubdate.tm_year < 2000:
                        pubdate = time.localtime()
                    elif time.localtime().tm_yday - pubdate.tm_yday > 7:
                        continue
                    else:
                        item['pubdate'] = time.mktime(pubdate)
                else:
                    if response.url == 'http://mubasher.aljazeera.net/rss.xml' or \
                        response.url == 'http://www.almadapaper.net/rss/':
                        pubdate = parse(pubdate, fuzzy=True, dayfirst=False)
                    else:
                        pubdate = parse(pubdate, fuzzy=True, dayfirst=True)
                    pubdate = time.mktime(pubdate.timetuple())
                    item['pubdate'] = pubdate

                item['item_id'] = str(uuid4())
                item['source'] = response.url
                item['link'] = entry.link
                item['country'] = '#' if response.meta['country'] is None else response.meta['country']
                item['language'] = '#' if response.meta['language'] is None else response.meta['language']
                item['title'] = lxml.html.fromstring(entry.title).text
                item['description'] = entry.description
                item['region'] = self.region
                request = Request(
                    entry.link,
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

    def parse_body(self, response):
        try:
            item = response.meta['item']
            content_xpath = response.meta['xpath']

            nodes = response.xpath(content_xpath).extract()
            nodes = self.clean_html_tags(nodes)
            item['description'] = self.clean_description(item['description'])

            if item['description'] == '':
                item['description'] = nodes[0]

            item['article'] = self.newline_join_lst(nodes)
            if item['article'] == '':
                print "No article"
                return None

            if 'thumb_xpath' in response.meta:
                thumb_xpath = response.meta['thumb_xpath']
                try:
                    thumb_nodes = response.xpath(thumb_xpath).extract()
                    thumb_nodes = self.get_images(thumb_nodes)
                    item['thumbnail'] = thumb_nodes[0]
                except:
                    print 'No thumbnail'
                    item['thumbnail'] = ''
            else:
                item['thumbnail'] = ''

            return item
        except Exception as e:
            print '%s: %s' % (type(e), e)
