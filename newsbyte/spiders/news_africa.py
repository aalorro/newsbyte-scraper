#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
import re
from uuid import uuid4
from dateutil.parser import parse
import time
import dateparser

from scrapy import Request

import newsbyte.tools as tools
from newsbyte.items import NewsbyteItem
from .basenews import BaseNewsSpider


class AfricaNewsSpider(BaseNewsSpider):
    """
    The various methods in this Spider outline how the text is extracted from the html document (of each link extracted
    from parse_common method in BaseNewsSpider) via xpath.
    """
    name = 'news_af'
    region = 'Africa'
    method = BaseNewsSpider.method

    start_urls = [
        ('http://www.echoroukonline.com/ara/feed/index.rss', 'parse_common', {'country': 'Algeria', 'language': 'Arabic', 'method': method, 'xpath': '//section[@class="article-contents"]/p'}),  # Algeria
        ('http://www.liberte-algerie.com/article/feed', 'parse_common', {'country': 'Algeria', 'language': 'French', 'method': method, 'xpath': '//div[@id="text_core"]/p'}),  # Algeria
        ('http://jornaldeangola.sapo.ao/feeds/articles/', 'parse_common', {'country': 'Angola', 'language': 'Portuguese', 'method': method, 'xpath': '//article/p'}),  # Angola
        ('http://allafrica.com/tools/headlines/rdf/angola/headlines.rdf', 'parse_common', {'country': 'Angola', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Angola
        ('http://www.mmegi.bw/2013_website/widgets/rss/rss.php?wid=1', 'parse_common', {'country': 'Botswana', 'language': 'Mixed', 'method': method, 'xpath': '//div[@class="text"]/p'}),  # Botswana
        ('http://allafrica.com/tools/headlines/rdf/burkinafaso/headlines.rdf', 'parse_common', {'country': 'Burkina Faso', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Burkina Faso
        ('http://www.lefaso.net/spip.php?page=backend', 'parse_common', {'country': 'Burkina Faso', 'language': 'French', 'method': method, 'xpath': '//div[@class="texte entry-content"]/p/text()'}),  # Burkina Faso
        ('http://www.cameroonjournal.com/feed/', 'parse_common', {'country': 'Cameroon', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry-content clearfix"]/p'}),  # Cameroon
        ('http://fr.allafrica.com/tools/headlines/rdf/cameroon/headlines.rdf', 'parse_common', {'country': 'Cameroon', 'language': 'French', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Cameroon
        ('http://www.asemana.publ.cv/spip.php?rubrique2&ak=1', 'parse_asemanalinks', {'country': 'Cape Verde', 'language': 'Portuguese', 'method': 'parse_asemanacontent', 'xpath': None}),  # Cape Verde
        ('http://acpcongo.com/acp/category/nation/feed/', 'parse_common', {'country': 'Congo-Kinshasa', 'language': 'French', 'method': method, 'xpath': '//div[@class="entry-content"]/p'}),  # Congo-Kinshasa
        ('http://groupelavenir.org/category/actualites/', 'parse_lavenirlinks', {'country': 'Congo-Kinshasa', 'language': 'French', 'method': 'parse_lavenircontent', 'xpath': None}),  # Congo-Kinshasa
        ('http://allafrica.com/tools/headlines/rdf/congo_kinshasa/headlines.rdf', 'parse_common', {'country': 'Congo-Kinshasa', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Congo-Kinshasa
        ('http://www.lanationdj.com/feed/', 'parse_common', {'country': 'Djibouti', 'language': 'French', 'method': method, 'xpath': '//div[@class="entry"]/p/text()'}),  # Djibouti
        ('http://www.egyptindependent.com/feed', 'parse_common', {'country': 'Egypt', 'language': 'English', 'method': method, 'xpath': '//div[@class="col-md-7 overflow-hidden"]/p'}),  # Egypt
        ('http://mubasher.aljazeera.net/Services/Rss/?K=MjAwODEwNTEyNTA1MzQyNTY4OUFDU0tFWTEyM0FqQ21zV2ViAA==', 'parse_common', {'country': 'Egypt', 'language': 'Arabic', 'method': 'parse_mubasher', 'xpath': None}),  # Egypt
        ('http://addisfortune.net/content/fortune-news/', 'parse_fortunelinks', {'country': 'Ethiopia', 'language': 'English', 'method': 'parse_fortunecontent', 'xpath': None}),  # Ethiopia
        ('http://allafrica.com/tools/headlines/rdf/ethiopia/headlines.rdf', 'parse_common', {'country': 'Ethiopia', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Ethiopia
        ('https://www.tesfanews.net/feed/', 'parse_common', {'country': 'Eritrea', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="entry-content"]/p'}),  # Eritrea
        ('http://www.farajat.net/ar/feed', 'parse_common', {'country': 'Eritrea', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="post"]/p'}),  # Eritrea
        ('http://www.gabonews.com/spip.php?page=backend&id_rubrique=1', 'parse_common', {'country': 'Gabon', 'language': 'French', 'method': 'parse_gabon', 'xpath': None}),  # Gabon
        ('http://www.gabonews.com/spip.php?page=backend&id_rubrique=2', 'parse_common', {'country': 'Gabon', 'language': 'English', 'method': 'parse_gabon', 'xpath': None}),  # Gabon
        ('http://allafrica.com/tools/headlines/rdf/gambia/headlines.rdf', 'parse_common', {'country': 'Gambia', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Gambia
        ('http://newsghana.com.gh/feed/', 'parse_common', {'country': 'Ghana', 'language': 'English', 'method': method, 'xpath': '//div[@class="td-post-content"]/p/text()'}),  # Ghana
        ('http://www.ghananewsagency.org/rss.php', 'parse_common', {'country': 'Ghana', 'language': 'English', 'method': method, 'xpath': '//div[@itemprop="articleBody"]/p/span/text()'}),  # Ghana
        ('http://allafrica.com/tools/headlines/rdf/guinea/headlines.rdf', 'parse_common', {'country': 'Guinea', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Guinea
        ('http://guineenews.org/feed/', 'parse_common', {'country': 'Guinea', 'language': 'French', 'method': method, 'xpath': '//div[@class="td-post-content"]/p'}),  # Guinea
        ('http://www.africaguinee.com/?q=rss.xml', 'parse_common', {'country': 'Guinea', 'language': 'French', 'method': method, 'xpath': '//div[@class="field-item even"]/p'}),  # Guinea
        ('http://www.nation.co.ke/rss', 'parse_common', {'country': 'Kenya', 'language': 'English', 'method': method, 'xpath': '//div/p[@class="MsoNormal"]'}),  # Kenya
        ('http://www.standardmedia.co.ke/rss/kenya.php', 'parse_common', {'country': 'Kenya', 'language': 'English', 'method': method, 'xpath': '//div[@class="main-article"]/p'}),  # Kenya
        ('http://allafrica.com/tools/headlines/rdf/liberia/headlines.rdf', 'parse_common', {'country': 'Liberia', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Liberia
        ('http://feeds.feedburner.com/MadagascarTribune?format=xml', 'parse_common', {'country': 'Madagascar', 'language': 'French', 'method': method, 'xpath': '//div[@id="content"]//p'}),  # Madagascar
        ('http://www.nyasatimes.com/feed/', 'parse_common', {'country': 'Malawi', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry-content"]//p/node()'}),  # Malawi
        ('http://malawi24.com/feed/', 'parse_common', {'country': 'Malawi', 'language': 'English', 'method': method, 'xpath': '//div[@class="left-col-content"]/p'}),  # Malawi
        ('http://allafrica.com/tools/headlines/rdf/mauritania/headlines.rdf', 'parse_common', {'country': 'Mauritania', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Mauritania
        ('http://www.alakhbar.info/news.feed?type=rss', 'parse_common', {'country': 'Mauritania', 'language': 'Arabic', 'method': method, 'xpath': '//div[@class="item-page"]/p'}),  # Mauritania
        ('http://www.leconomiste.com/rss-leconomiste', 'parse_common', {'country': 'Morocco', 'language': 'French', 'method': method, 'xpath': '//div[@property="content:encoded"]/p'}),  # Morroco
        ('http://www.ahdath.info/?feed=rss2', 'parse_common', {'country': 'Morocco', 'language': 'Arabic', 'method': method, 'xpath': '//article/p'}),  # Morroco
        ('http://allafrica.com/tools/headlines/rdf/mozambique/headlines.rdf', 'parse_common', {'country': 'Mozambique', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Mozambique
        ('http://www.verdade.co.mz/index.php?option=com_mediarss&feed_id=1&format=raw', 'parse_common', {'country': 'Mozambique', 'language': 'Portuguese', 'method': method, 'xpath': '//td[@valign="top"]/p/node()'}),  # Mozambique
        ('https://www.newera.com.na/feed/', 'parse_common', {'country': 'Namibia', 'language': 'Mixed', 'method': method, 'xpath': '//article/p'}),  # Namibia
        ('http://www.namibian.com.na/rssfeed.php', 'parse_common', {'country': 'Namibia', 'language': 'English', 'method': method, 'xpath': '//div[@class="info"]/article/p'}),  # Namibia
        ('http://allafrica.com/tools/headlines/rdf/niger/headlines.rdf', 'parse_common', {'country': 'Niger', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Niger
        ('http://www.tamtaminfo.com/feed/', 'parse_common', {'country': 'Niger', 'language': 'French', 'method': 'parse_tamtaminfo', 'xpath': None}),  # Niger
        ('http://www.thebreakingtimes.com/feed/', 'parse_common', {'country': 'Nigeria', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry-content"]/p'}),  # Nigeria
        ('http://feeds.feedburner.com/newsofrwanda', 'parse_common', {'country': 'Rwanda', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Rwanda
        ('http://www.rnanews.com/index.php?format=feed&type=rss', 'parse_common', {'country': 'Rwanda', 'language': 'Mixed', 'method': method, 'xpath': '//div[@class="article-content"]/p'}),  # Rwanda
        ('http://www.pressafrik.com/xml/syndication.rss', 'parse_common', {'country': 'Senegal', 'language': 'French', 'method': method, 'xpath': '//div[@class="access firstletter"]'}),  # Senegal
        ('http://allafrica.com/tools/headlines/rdf/senegal/headlines.rdf', 'parse_common', {'country': 'Senegal', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Senegal
        ('http://www.seychellesnewsagency.com/rss', 'parse_common', {'country': 'Seychelles', 'language': 'English', 'method': method, 'xpath': '//div[@id="textsize"]/p'}),  # Seychelles
        ('http://fr.allafrica.com/tools/headlines/rdf/seychelles/headlines.rdf', 'parse_common', {'country': 'Seychelles', 'language': 'French', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Seychelles
        ('http://www.heraldlive.co.za/feed/', 'parse_common', {'country': 'South Africa', 'language': 'English', 'method': 'parse_herald', 'xpath': None}),  # South Africa
        ('http://feeds.news24.com/articles/news24/SouthAfrica/rss', 'parse_common', {'country': 'South Africa', 'language': 'English', 'method': 'parse_news24', 'xpath': None}),  # South Africa
        ('http://www.southsudannation.com/feed/', 'parse_common', {'country': 'South Sudan', 'language': 'English', 'method': 'parse_southsudan', 'xpath': None}),  # South Sudan
        ('http://mzalendo.net/feed', 'parse_common', {'country': 'Tanzania', 'language': 'Swahili', 'method': method, 'xpath': '//div[@id="content"]/p'}),  # Tanzania
        ('http://24tanzania.com/feed/', 'parse_common', {'country': 'Tanzania', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry"]/p'}),  # Tanzania
        ('http://allafrica.com/tools/headlines/rdf/tanzania/headlines.rdf', 'parse_common', {'country': 'Tanzania', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Tanzania
        ('http://allafrica.com/tools/headlines/rdf/uganda/headlines.rdf', 'parse_common', {'country': 'Uganda', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Uganda
        ('http://zambiareports.com/feed/', 'parse_common', {'country': 'Zambia', 'language': 'English', 'method': method, 'xpath': '//div[@class="entry-content"]/p/node()'}),  # Zambia
        ('http://allafrica.com/tools/headlines/rdf/zambia/headlines.rdf', 'parse_common', {'country': 'Zambia', 'language': 'English', 'method': method, 'xpath': '//div[@class="story-body"]/p'}),  # Zambia
    ]

    def __init__(self, domain=None):
        super(AfricaNewsSpider, self).__init__()
        self.domain = domain

    def parse_asemanalinks(self, response):
        """
        Does not use an RSS Feed.
        """
        for link in response.xpath('//div[@class="articleRecente"]/dl/dd/a'):
            new_link = response.urljoin(''.join(link.xpath('./@href').extract()))
            title = ''.join(link.xpath('./text()').extract())

            item = NewsbyteItem()
            item['source'] = response.url
            item['link'] = new_link
            item['title'] = title
            item['country'] = '#' if response.meta['country'] is None else response.meta['country']
            item['item_id'] = str(uuid4())
            item['language'] = '#' if response.meta['language'] is None else response.meta['language']
            item['region'] = self.region
            # foreign language used in date
            request = Request(
                new_link,
                callback=getattr(self, response.meta['method']),
                dont_filter=response.meta.get('dont_filter', False)
            )

            request.meta['item'] = item

            yield request

    def parse_asemanacontent(self, response):
        item = response.meta['item']
        item['description'] = ''.join(response.xpath('//div[@id="article"]/h4/text()').extract())
        nodes = response.xpath('//div[@id="article"]/div/p').extract()
        date = ''.join(response.xpath('//span[@class="date"]/text()').extract())

        nodes = self.clean_html_tags(nodes)

        if item['description'] == '':
            item['description'] = nodes[1]
        # turn unicode string into a datetime object
        # convert the returned timetuple object into a unix timestamp
        item['pubdate'] = time.mktime(dateparser.parse(date).timetuple())
        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_lavenirlinks(self, response):
        """
        Does not use an RSS Feed.
        """
        for link in response.xpath('//div[@class="wpb_row row-fluid"]//h3[@class="entry-title"]/a'):
            new_link = ''.join(link.xpath('./@href').extract())
            title = ''.join(link.xpath('./@title').extract())

            item = NewsbyteItem()
            item['source'] = response.url
            item['link'] = new_link
            item['title'] = title
            item['country'] = '#' if response.meta['country'] is None else response.meta['country']
            item['item_id'] = str(uuid4())
            item['language'] = '#' if response.meta['language'] is None else response.meta['language']
            item['region'] = self.region

            request = Request(
                new_link,
                callback=getattr(self, response.meta['method']),
                dont_filter=response.meta.get('dont_filter', False)
            )

            request.meta['item'] = item

            yield request

    def parse_lavenircontent(self, response):
        item = response.meta['item']

        pubdate = ''.join(response.xpath('//header/div/time/@datetime').extract())
        # parse out extraneous part of date
        pubdate = pubdate[:pubdate.find('+')]
        # replace the 'T' in the string to a space to separate date from time
        pubdate = pubdate.replace('T', ' ')
        pubdate = parse(pubdate, yearfirst=True, fuzzy=True)
        item['pubdate'] = time.mktime(pubdate.timetuple())

        nodes = response.xpath('//div[@class="td-post-text-content"]/p').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        item['description'] = nodes[0]
        if item['article'] == '':
            return None

        return item

    def parse_mubasher(self, response):
        item = response.meta['item']
        print item

        try:
            nodes = response.xpath('//div[contains(@class, "field--name-field-ajmn-summary")]').extract()
            nodes = self.clean_html_tags(nodes)
            item['description'] = nodes[0]
            item['description'] = self.clean_description(item['description'])

            nodes = response.xpath('//div[contains(@class, "field--name-body")]/p').extract()
            nodes = self.clean_html_tags(nodes)
            nodes.insert(0, item['description'])

            item['article'] = self.newline_join_lst(nodes)
            if item['article'] == '':
                return None

            return item
        except Exception as e:
            print e

    def parse_albawab_arabic(self, response):
        item = response.meta['item']

        nodes = response.xpath('//div[@class="ni-content"]').extract()
        nodes = ''.join(nodes)

        nodes = tools.convert_div(nodes).strip()
        nodes = tools.strip_tags(tools.convert_br(nodes))

        description = re.search(r'(.*?)\n', nodes).group(0).strip()
        # Ignores articles that are just recipes
        if u'\u0627\u0644\u0645\u0643\u0648\u0646\u0627\u062a' in description:
            return None
        item['description'] = description
        item['article'] = nodes
        if item['article'] == '':
            return None

        return item

    def parse_fortunelinks(self, response):
        """
        Does not use an RSS Feed.
        """
        for link in response.xpath('//div[@class="span6"]/h3/a'):
            new_link = ''.join(link.xpath('./@href').extract())
            title = ''.join(link.xpath('./text()').extract())

            item = NewsbyteItem()
            item['source'] = response.url
            item['link'] = new_link
            item['title'] = title
            item['country'] = '#' if response.meta['country'] is None else response.meta['country']
            item['item_id'] = str(uuid4())
            item['language'] = '#' if response.meta['language'] is None else response.meta['language']
            item['region'] = item['region'] = self.region

            request = Request(
                new_link,
                callback=getattr(self, response.meta['method']),
                dont_filter=response.meta.get('dont_filter', False)
            )

            request.meta['item'] = item

            yield request

    def parse_fortunecontent(self, response):
        item = response.meta['item']

        description = ''.join(response.xpath('//div[@id="newsarticletext"]/h4').extract())
        item['description'] = tools.strip_tags(description).strip()

        pubdate = ''.join(response.xpath('//div[@id="author-line"]').extract())
        pubdate = tools.strip_tags(pubdate)
        pubdate = re.search(r'Published on .*?\d+,\d+', pubdate).group(0)
        pubdate = parse(pubdate, fuzzy=True)
        item['pubdate'] = time.mktime(pubdate.timetuple())

        nodes = response.xpath('//div[@id="newsarticletext"]/p').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_gabon(self, response):
        item = response.meta['item']
        item['description'] = ''.join(response.xpath('//div[@class="chapoArticle"]/p/text()').extract())
        nodes = response.xpath('//div[@class="texteArticle"]/p/text()').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_tamtaminfo(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@class="entry"]/p').extract()
        if not nodes:
            nodes = response.xpath('//div[@class="entry"]/div/p').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_herald(self, response):
        item = response.meta['item']
        item['description'] = tools.strip_tags(item['description'])
        nodes = response.xpath('//div[@id="testArtCol_a"]/p/node()').extract()
        nodes2 = response.xpath('//div[@id="testArtCol_b"]/p/node()').extract()
        if nodes2:
            for text in nodes2:
                nodes.append(text)

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_news24(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@id="article-body"]/p/node()').extract()
        if nodes == []:
            nodes = response.xpath('//article[@id="article-body"]/p/node()').extract()

        nodes = self.clean_html_tags(nodes)

        item['article'] = self.newline_join_lst(nodes)
        if item['article'] == '':
            return None

        return item

    def parse_southsudan(self, response):
        item = response.meta['item']
        nodes = response.xpath('//div[@class="entry"]/p').extract()

        lines = []
        for node in nodes:
            line = tools.strip_p(node).strip()
            line = re.sub(r'<!-- No token or token has expired. -->', '', line)  # take out extraneous line
            if line != '':
                lines.append(line)

        item['article'] = '\n\n'.join(lines)
        if item['article'] == '':
            return None

        return item
