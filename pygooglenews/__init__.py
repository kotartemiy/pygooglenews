import time
import feedparser
from bs4 import BeautifulSoup
import urllib
from dateparser import parse as parse_date
import requests
from datetime import datetime
from datetime import timedelta
from time import mktime
import types

from typing import List


class GoogleNews:
    def __init__(self, lang='en', country='US'):
        self.lang = lang.lower()
        self.country = country.upper()
        self.BASE_URL = 'https://news.google.com/rss'

    def __top_news_parser(self, text):
        """Return subarticles from the main and topic feeds"""
        try:
            bs4_html = BeautifulSoup(text, "html.parser")
            # find all li tags
            lis = bs4_html.find_all('li')
            sub_articles = []
            for li in lis:
                try:
                    sub_articles.append({"url": li.a['href'],
                                         "title": li.a.text,
                                         "publisher": li.font.text})
                except:
                    pass
            return sub_articles
        except:
            return text

    def __ceid(self):
        """Compile correct country-lang parameters for Google News RSS URL"""
        return '?ceid={}:{}&hl={}&gl={}'.format(self.country, self.lang, self.lang, self.country)

    def __add_sub_articles(self, entries):
        for i, val in enumerate(entries):
            if 'summary' in entries[i].keys():
                entries[i]['sub_articles'] = self.__top_news_parser(entries[i]['summary'])
            else:
                entries[i]['sub_articles'] = None
        return entries

    def __scaping_bee_request(self, api_key, url):
        response = requests.get(
            url="https://app.scrapingbee.com/api/v1/",
            params={
                "api_key": api_key,
                "url": url,
                "render_js": "false"
            }
        )
        if response.status_code == 200:
            return response
        if response.status_code != 200:
            raise Exception("ScrapingBee status_code: " + str(response.status_code) + " " + response.text)

    def __parse_feed(self, feed_url, proxies=None, scraping_bee=None):

        if scraping_bee and proxies:
            raise Exception("Pick either ScrapingBee or proxies. Not both!")

        if proxies:
            r = requests.get(feed_url, proxies=proxies)
        else:
            r = requests.get(feed_url)

        if scraping_bee:
            r = self.__scaping_bee_request(url=feed_url, api_key=scraping_bee)
        else:
            r = requests.get(feed_url)

        if 'https://news.google.com/rss/unsupported' in r.url:
            raise Exception('This feed is not available: ' + r.url)

        d = feedparser.parse(r.text)

        if not scraping_bee and not proxies and len(d['entries']) == 0:
            d = feedparser.parse(feed_url)

        return dict((k, d[k]) for k in ('feed', 'entries'))

    def __search_helper(self, query):
        return urllib.parse.quote_plus(query)

    def __from_to_helper(self, validate=None):
        try:
            validate = parse_date(validate).strftime('%Y-%m-%d')
            return str(validate)
        except:
            raise Exception('Could not parse your date')

    def top_news(self, proxies=None, scraping_bee=None):
        """Return a list of all articles from the main page of Google News
        given a country and a language"""
        d = self.__parse_feed(self.BASE_URL + self.__ceid(), proxies=proxies, scraping_bee=scraping_bee)
        d['entries'] = self.__add_sub_articles(d['entries'])
        return d

    def topic_headlines(self, topic: str, proxies=None, time_span: timedelta = None, sort_by_publish_date: bool = True,
                        scraping_bee=None):
        """Return a list of all articles from the topic page of Google News
        given a country and a language"""
        # topic = topic.upper()
        d = {'entries': []}
        if topic.upper() in ['WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SCIENCE', 'SPORTS',
                             'HEALTH']:
            t = self.__parse_feed(
                self.BASE_URL + '/headlines/section/topic/{}'.format(topic.upper()) + self.__ceid(),
                proxies=proxies, scraping_bee=scraping_bee)
        else:
            t = self.__parse_feed(self.BASE_URL + '/topics/{}'.format(topic) + self.__ceid(), proxies=proxies,
                                  scraping_bee=scraping_bee)
        d['feed'] = t['feed']
        if time_span is not None:
            d['entries'] += [ta for ta in t['entries'] if
                             datetime.now() - time_span <= datetime.fromtimestamp(
                                 mktime(ta['published_parsed']))]
        else:
            d['entries'] += t['entries']

        d['entries'] = self.__add_sub_articles(d['entries'])

        if sort_by_publish_date:
            d['entries'] = sorted(d['entries'],
                                  key=lambda p: datetime.fromtimestamp(mktime(p['published_parsed'])).timestamp(),
                                  reverse=True)

        if len(d['entries']) > 0:
            return d
        else:
            raise Exception('unsupported topic')

    def topic_multiple_headlines(self, topic_list: List[str], time_span: timedelta = None, sort_by_publish_date: bool = True,
                                 proxies=None, scraping_bee=None):
        """Return a list of all articles from the list of topic page of Google News
        given a country and a language"""

        d = {'entries': []}
        for topic in topic_list:
            try:
                if topic.upper() in ['WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SCIENCE', 'SPORTS',
                                     'HEALTH']:
                    t = self.__parse_feed(
                        self.BASE_URL + '/headlines/section/topic/{}'.format(topic.upper()) + self.__ceid(),
                        proxies=proxies, scraping_bee=scraping_bee)
                else:
                    t = self.__parse_feed(self.BASE_URL + '/topics/{}'.format(topic) + self.__ceid(), proxies=proxies,
                                          scraping_bee=scraping_bee)
                d['feed'] = t['feed']
                if time_span is not None:
                    d['entries'] += [ta for ta in t['entries'] if
                                     datetime.now() - time_span <= datetime.fromtimestamp(
                                         mktime(ta['published_parsed']))]
                else:
                    d['entries'] += t['entries']
            except Exception as e:
                pass

        d['entries'] = self.__add_sub_articles(d['entries'])
        if sort_by_publish_date:
            d['entries'] = sorted(d['entries'],
                                  key=lambda p: datetime.fromtimestamp(mktime(p['published_parsed'])).timestamp(),
                                  reverse=True)

        if len(d['entries']) > 0:
            return d
        else:
            raise Exception('unsupported topic')

    def geo_headlines(self, geo: str, proxies=None, scraping_bee=None, time_span: timedelta = None,
                      sort_by_publish_date: bool = True):
        """Return a list of all articles about a specific geolocation
        given a country and a language"""
        d = {'entries': []}
        t = self.__parse_feed(self.BASE_URL + '/headlines/section/geo/{}'.format(geo) + self.__ceid(),
                              proxies=proxies, scraping_bee=scraping_bee)
        d['feed'] = t['feed']
        if time_span is not None:
            d['entries'] += [ta for ta in t['entries'] if
                             datetime.now() - time_span <= datetime.fromtimestamp(
                                 mktime(ta['published_parsed']))]
        else:
            d['entries'] += t['entries']

        d['entries'] = self.__add_sub_articles(d['entries'])
        if sort_by_publish_date:
            d['entries'] = sorted(d['entries'],
                                  key=lambda p: datetime.fromtimestamp(mktime(p['published_parsed'])).timestamp(),
                                  reverse=True)
        return d

    def geo_multiple_headlines(self, geo: List[str], time_span: timedelta = None, sort_by_publish_date: bool = True,
                               proxies=None, scraping_bee=None):
        """Return a list of all articles about a list of geolocation
        given a country and a language"""

        d = {'entries': []}
        for n in geo:
            try:
                t = self.__parse_feed(self.BASE_URL + '/headlines/section/geo/{}'.format(n) + self.__ceid(),
                                      proxies=proxies, scraping_bee=scraping_bee)
                d['feed'] = t['feed']
                if time_span is not None:
                    d['entries'] += [ta for ta in t['entries'] if
                                     datetime.now() - time_span <= datetime.fromtimestamp(
                                         mktime(ta['published_parsed']))]
                else:
                    d['entries'] += t['entries']
            except Exception as e:
                pass

        d['entries'] = self.__add_sub_articles(d['entries'])

        if sort_by_publish_date:
            d['entries'] = sorted(d['entries'],
                                  key=lambda p: datetime.fromtimestamp(mktime(p['published_parsed'])).timestamp(),
                                  reverse=True)

        # Remove multiple news
        res = []
        for da in d['entries']:
            if da['title'] not in [re['title'] for re in res]:
                res += [da]
        d['entries'] = res
        return d

    def search(self, query: str, helper=True, when=None, from_=None, to_=None, proxies=None, scraping_bee=None):
        """
        Return a list of all articles given a full-text search parameter,
        a country and a language

        :param bool helper: When True helps with URL quoting
        :param str when: Sets a time range for the artiles that can be found
        """

        if when:
            query += ' when:' + when

        if from_ and not when:
            from_ = self.__from_to_helper(validate=from_)
            query += ' after:' + from_

        if to_ and not when:
            to_ = self.__from_to_helper(validate=to_)
            query += ' before:' + to_

        if helper == True:
            query = self.__search_helper(query)

        search_ceid = self.__ceid()
        search_ceid = search_ceid.replace('?', '&')

        d = self.__parse_feed(self.BASE_URL + '/search?q={}'.format(query) + search_ceid, proxies=proxies,
                              scraping_bee=scraping_bee)

        d['entries'] = self.__add_sub_articles(d['entries'])
        return d
