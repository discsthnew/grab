# -*- coding: UTF-8 -*-
__author__ = 'walker'


import os
import urlparse

import scrapy
from scrapy.http import Request
from grab.items import Resource
from scrapy.utils.url import urljoin_rfc
from scrapy import log

from utils import convert_url_agian, filter_url_list


visited_urls = set()


class ResourceSpider(scrapy.Spider):
    global visited_urls
    name = 'base'
    allowed_domain = ["doudou.com", '123bo.com', '22zuhao.com']
    start_urls = [
        "http://webstatic.doudou.com/",
    ]

    # "http://webstatic.doudou.com/",
    # def start_requests(self):
    #     return

    def parse(self, response):
        unfiltered_html_urls = response.xpath('//a/@href').re('^[^#]+')
        unfiltered_img_urls = response.xpath('//img/@src').re('^[^#]+')
        unfiltered_css_urls = response.xpath('//link/@href').re('^[^#]+')
        unfiltered_js_urls = response.xpath('//script/@src').re('^[^#]+')

        print unfiltered_js_urls

        html_urls = filter_url_list(allow_domain=self.allowed_domain,
                                    urls=[convert_url_agian(response, url) for url in unfiltered_html_urls],
                                    visited_urls=visited_urls)
        img_urls = filter_url_list(allow_domain=self.allowed_domain,
                                   urls=[convert_url_agian(response, url) for url in unfiltered_img_urls],
                                   visited_urls=visited_urls)
        css_urls = filter_url_list(allow_domain=self.allowed_domain,
                                   urls=[convert_url_agian(response, url) for url in unfiltered_css_urls],
                                   visited_urls=visited_urls)
        js_urls = filter_url_list(allow_domain=self.allowed_domain,
                                  urls=[convert_url_agian(response, url) for url in unfiltered_js_urls],
                                  visited_urls=visited_urls)

        print '-----------------html url-------------------------'
        for url in html_urls:
            try:
                self.log(url)
            except Exception, e:
                self.log(e)
                continue
        print '-----------------img url---------------------------'
        for url in img_urls:
            try:
                self.log(url)
            except Exception, e:
                self.log(e)
                continue
        print '------------------css url--------------------------'
        for url in css_urls:
            try:
                self.log(url)
            except Exception, e:
                print e
                continue
        print '------------------js url---------------------------'
        for url in js_urls:
            try:
                self.log(url)
            except Exception, e:
                print e
                continue
        if html_urls:
            visited_urls.add(url)
            for url in html_urls:
                patterns = urlparse.urlparse(url)
                suffix = os.path.splitext(os.path.basename(patterns[2]))[1]
                if not suffix or suffix in ['.html', '.htm', '.php', '.jsp', '.aspx']:
                    if response.headers.has_key('Content-Length'):
                        length = response.header['Content-Length']
                    else:
                        length = len(response.body)
                    try:
                        yield Resource(
                            url=response.url,
                            content_type=response.headers['Content-Type'],
                            content_length=length,
                            host=urlparse.urlparse(response.url)[1]
                        )
                    except KeyError, e:
                        self.log('url: %s, error: %s' % (url, str(e)))
                    yield Request(url, callback=self.parse, method='GET')
                else:
                    yield Request(url, callback=self.myparse, method='HEAD')
        for urls in [img_urls, css_urls, js_urls]:
            if urls:
                visited_urls.add(url)
                for url in urls:
                    yield Request(url, callback=self.myparse, method='HEAD')

    def myparse(self, response):
        # if resource.content_type > 1024 * 1024:
        #     resource.type = 'small'
        # else:
        #     resource.type = 'big'
        try:
            yield Resource(
                url=response.url,
                content_type=response.headers['Content-Type'],
                content_length=response.headers['Content-Length'],
                host=urlparse.urlparse(response.url)[1]
            )
        except KeyError, e:
            print response.url+' error: ' + str(e)


class ZuhaoSpider(scrapy.Spider):
    global visited_urls
    name = '22zuhao'
    allowed_domain = ['22zuhao.com']
    start_urls = [
        "http://www.22zuhao.com/",
    ]

    cookies = {'cdntoken': 'ba598b6a3231ec3485da740386669144', 'cdnrand': '92f9db58e1a5339db0be9a895135e41d'}

    def parse(self, response):
        # record item
        if response.url not in visited_urls:
            visited_urls.add(response.url)
            if response.headers.has_key('Content-Length'):
                length = response.header['Content-Length']
            else:
                length = len(response.body)
            try:
                yield Resource(
                    url=response.url,
                    content_type=response.headers['Content-Type'],
                    content_length=length,
                    host=urlparse.urlparse(response.url)[1]
                )
            except KeyError, e:
                print response.url, e

        # get url from web page
        unfiltered_html_urls = response.xpath('//a/@href').re('^[^#]+')
        unfiltered_img_urls = response.xpath('//img/@src').re('^[^#]+')
        unfiltered_css_urls = response.xpath('//link/@href').re('^[^#]+')
        unfiltered_js_urls = response.xpath('//script/@src').re('^[^#]+')

        # do filter
        html_urls = filter_url_list(allow_domain=self.allowed_domain,
                                    urls=[convert_url_agian(response, url) for url in unfiltered_html_urls],
                                    visited_urls=visited_urls)
        img_urls = filter_url_list(allow_domain=self.allowed_domain,
                                   urls=[convert_url_agian(response, url) for url in unfiltered_img_urls],
                                   visited_urls=visited_urls)
        css_urls = filter_url_list(allow_domain=self.allowed_domain,
                                   urls=[convert_url_agian(response, url) for url in unfiltered_css_urls],
                                   visited_urls=visited_urls)
        js_urls = filter_url_list(allow_domain=self.allowed_domain,
                                  urls=[convert_url_agian(response, url) for url in unfiltered_js_urls],
                                  visited_urls=visited_urls)

        self.log('-----------------html url-------------------------', level=log.INFO)
        for url in html_urls:
            try:
                # self.log(url, level=log.INFO)
                print url
            except Exception, e:
                print e
                continue
        # return

        # return a Request iteration while the given url is pointed to a webpage, otherwise, return a Item iteration
        if html_urls:
            for url in html_urls:
                if url in visited_urls:
                    continue
                patterns = urlparse.urlparse(url)
                suffix = os.path.splitext(os.path.basename(patterns[2]))[1]
                if not suffix or suffix in ['.html', '.htm', '.php', '.jsp', '.aspx']:
                    yield Request(url, callback=self.parse, method='GET',
                                  cookies=self.cookies)
                else:
                    yield Request(url, callback=self.myparse, method='HEAD', cookies=self.cookies)
                    visited_urls.add(url)
                # add into visited url list

        for urls in [img_urls, css_urls, js_urls]:
            if urls:
                if url in visited_urls:
                    continue
                for url in urls:
                    yield Request(url, callback=self.myparse, method='HEAD', cookies=self.cookies)
                    visited_urls.add(url)

    def myparse(self, response):
        try:
            yield Resource(
                url=response.url,
                content_type=response.headers['Content-Type'],
                content_length=int(response.headers['Content-Length']),
                host=urlparse.urlparse(response.url)[1]
            )
        except KeyError, e:
            print response.url+' error: ' + str(e)



