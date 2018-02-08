# -*- coding: UTF-8 -*-
__author__ = 'walker'

import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector
from grab.items import Resource

from utils import convert_url_agian, filter_url_list


visited_urls = set()


class ResourceSpider(scrapy.Spider):
    global visited_urls
    name = 'xiazaiba'
    allowed_domain = ["doudou.com", '123bo.com']
    start_urls = [
        "http://www.doudou.com/",
    ]

    # def start_requests(self):
    #     return

    def parse(self, response):
        html_urls = set()
        other_urls = set()

        unfiltered_html_urls = response.xpath('//a/@href').re('^[^#]+')
        unfiltered_img_urls = response.xpath('//img/@src').re('^[^#]+')
        unfiltered_css_urls = response.xpath('//link/@href').re('^[^#]+')
        unfiltered_js_urls = response.xpath('//script/@src').re('^[^#]+')

        print unfiltered_html_urls

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
        print html_urls
        for url in html_urls:
            try:
                print url
            except Exception, e:
                print e
                continue
        print '-----------------img url---------------------------'
        for url in img_urls:
            try:
                print url
            except Exception, e:
                print e
                continue
        print '------------------css url--------------------------'
        for url in img_urls:
            try:
                print url
            except Exception, e:
                print e
                continue
        print '------------------css url--------------------------'
        for url in css_urls:
            try:
                print url
            except Exception, e:
                print e
                continue
        print '------------------js url---------------------------'
        for url in js_urls:
            try:
                print url
            except Exception, e:
                print e
                continue
        return


    def myparse(self, response):
        resource = Resource()
        headers = response.headers
        resource.url = response.url
        resource.content_length = int(headers['Content-Length'])
        resource.content_type = headers['Content-Type']
        # if resource.content_type > 1024 * 1024:
        #     resource.type = 'small'
        # else:
        #     resource.type = 'big'
        yield resource



        print '------------------js url---------------------------'
        print js_urls
        return


    def myparse(self, response):
        resource = Resource()
        headers = response.headers
        resource.url = response.url
        resource.content_length = int(headers['Content-Length'])
        resource.content_type = headers['Content-Type']
        # if resource.content_type > 1024 * 1024:
        #     resource.type = 'small'
        # else:
        #     resource.type = 'big'
        yield resource




