# -*- coding: UTF-8 -*-
__author__ = 'walker'

import re
import os
import urlparse


def convert_url(response, url):
    normal_url = re.compile(r'(?P<schema>http|https)://(?P<host>[^/]+)/(?P<uri>.*)')
    relative_path_url = re.compile(r'[^http].*/+.*')

    if normal_url.match(url, re.I):
        return url

    if relative_path_url.match(url, re.I):
        refer_url = response.request.url
        m = normal_url.match(refer_url)
        if not m:
            raise ValueError('error refer_url:', refer_url)
        host = m.groupdict()['host']
        path = os.path.dirname()


def convert_url_agian(response, url):
    """

    :param response: scrapy Response obj
    :param url: str
    :return: url: str

    sometimes the url may not agree with specification, such as 'javascirpt:viod(0)', '//www.exmaple.com/index.html'， 'css/public.css'.
    if url use relative path, such as 'css/public.css', in that case, we have to complete it.
    if the url you visited is 'http://www.example.com/aaa/bbb/index.html, and the css source is 'css/public.css'.
    then it's absolute path will be /aaa/bbb/css/public.css, so we could use `os` lib to achieve this function.
    """
    schema, netloc, path, params, query, fragment = urlparse.urlparse(url)
    refer_schema, refer_netloc, refer_path, refer_parmas, refer_query, refer_frag = urlparse.urlparse(response.request.url)
    if not schema:
        # //www.example.com/aaa/bbb
        if not netloc:
            # css/public.css
            if not path:
                raise ValueError('illegal url path: ', url)
            abs_path = os.path.join(os.path.dirname(refer_path), path)
            return urlparse.urlunparse((refer_schema, refer_netloc, abs_path, params, query, fragment))
        else:
            return urlparse.urlunparse((refer_schema, netloc, path, params, query, fragment))
    else:
        if schema not in ['http', 'https']:
            raise ValueError('illegal url schema: ', url)
        return url


def filter_url_list(allow_domain, urls, visited_urls):
    """

    :param allow_domain: set
    :param urls: list
    :param visited_urls: list
    :return: new_urls: list

    filter url in urls which host not in allowd_domain set and has been added into visited_urls list.
    """
    normal_url = re.compile(r'(?P<schema>http|https)://(?P<host>[^/]+)/(?P<uri>.*)')
    new_urls = set()
    for url in urls:
        m = normal_url.match(url)
        # if not m:
        #     raise ValueError('Illegal url:', url)
        if not m:
            print 'Illegal url: ', url
            continue
        host = m.groupdict()['host'].split(':')[0]
        base_domain = '.'.join(host.split('.')[-2:])
        if base_domain in allow_domain:
            if visited_urls:
                if url in visited_urls:
                    continue
            new_urls.add(url)
    return new_urls




