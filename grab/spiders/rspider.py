# -*- coding: UTF-8 -*-
__author__ = 'discsthnew'


import os
import urlparse

import scrapy
from scrapy.http import Request
from grab.items import Resource

from utils import convert_url, filter_url_list

visited_urls = set()


class ResourceSpider(scrapy.Spider):
    global visited_urls
    name = 'base'

    def __init__(self, **kwargs):
        super(ResourceSpider, self).__init__(**kwargs)
        self.allowed_domains = kwargs.get('allow_domains') or ()
        self.start_urls = kwargs.get('start_urls') or ()
        self.cookies = kwargs.get('cookies') or {}

    # allowed_domain = ['22zuhao.com', '56va.cn']
    # start_urls = [
    #     "http://www.56va.cn/",
    #     "http://22zuhao.com/"
    # ]

    # cookies = {'cdntoken': 'ba598b6a3231ec3485da740386669144', 'cdnrand': '92f9db58e1a5339db0be9a895135e41d'}
    # cookies = {'cdntoken': 'a76dc7539a1fcc09063a2b5cf606ea54', 'cdnrand': '6be3a36229f65e1568d0641cd6a2cb2d'}

    def parse(self, response):
        headers = response.headers
        # record item
        if response.url not in visited_urls:
            visited_urls.add(response.url)

        cache_control = headers['Cache-Control'] if headers.has_key('Cache-Control') else ''

        if response.request.method == 'HEAD':
            try:
                yield Resource(
                    url=response.url,
                    content_type=headers['Content-Type'],
                    content_length=int(headers['Content-Length']),
                    cache_control=cache_control,
                    host=urlparse.urlparse(response.url)[1]
                )
            except KeyError, e:
                print response.url+' error: ' + str(e)

        elif response.request.method == 'GET':
            # if headers.has_key('Content-Length'):
            #     length = headers['Content-Length']
            # else:
            #     length = len(response.body)
            length = headers['Content-Length'] if headers.has_key('Content-Length') else len(response.body)
            try:
                yield Resource(
                    url=response.url,
                    content_type=response.headers['Content-Type'].split(';')[0],
                    content_length=length,
                    cache_control=cache_control,
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
            html_urls = filter_url_list(allow_domains=self.allowed_domains,
                                        urls=[convert_url(response, url) for url in unfiltered_html_urls],
                                        visited_urls=visited_urls)
            img_urls = filter_url_list(allow_domains=self.allowed_domains,
                                       urls=[convert_url(response, url) for url in unfiltered_img_urls],
                                       visited_urls=visited_urls)
            css_urls = filter_url_list(allow_domains=self.allowed_domains,
                                       urls=[convert_url(response, url) for url in unfiltered_css_urls],
                                       visited_urls=visited_urls)
            js_urls = filter_url_list(allow_domains=self.allowed_domains,
                                      urls=[convert_url(response, url) for url in unfiltered_js_urls],
                                      visited_urls=visited_urls)

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
                        yield Request(url, callback=self.parse, method='HEAD', cookies=self.cookies)
                    # add into visited url list
                    visited_urls.add(url)

            for urls in [img_urls, css_urls, js_urls]:
                if urls:
                    if url in visited_urls:
                        continue
                    for url in urls:
                        yield Request(url, callback=self.parse, method='HEAD', cookies=self.cookies)
                        visited_urls.add(url)



