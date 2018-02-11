# -*- coding: UTF-8 -*-
__author__ = 'discsthnew'

import re
import os
import urlparse


def convert_url(response, url):
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
            # urljoin('http://example.com/', '../css/a.css') retrun 'http://exmaple.com/../css/a.css
            # that would be wrong, so let's remove `..` after 'http://exmaple.com/`
            # Notice:
            #    use urljoin() method will lose it's query str.
            tmp_url = urlparse.urljoin(response.request.url, path)
            tmp_url_with_right_path = re.sub(r'\.\./', '', tmp_url, count=1)
            tmp_url_patterns = urlparse.urlparse(tmp_url_with_right_path)
            real_url = urlparse.urlunparse((refer_schema, refer_netloc, tmp_url_patterns[2], params, query, fragment))
            return real_url
        else:
            return urlparse.urlunparse((refer_schema, netloc, path, params, query, fragment))
    else:
        # if schema not in ['http', 'https']:
        #     raise ValueError('illegal url schema: ', url)
        return url


def filter_url_list(allow_domains, urls, visited_urls):
    """ filter url list

    :param allow_domains: set
    :param urls: list
    :param visited_urls: list
    :return: new_urls: list

    filter url in urls which host not in allowd_domain set and has been added into visited_urls list.
    """
    normal_url = re.compile(r'(?P<schema>http|https)://(?P<host>[^/]+)(?P<uri>.*)')
    new_urls = set()
    for url in urls:
        if visited_urls:
            if url in visited_urls:
                continue
        m = normal_url.match(url)
        # if not m:
        #     raise ValueError('Illegal url:', url)
        if not m:
            if isinstance(url, str):
                print 'Illegal url: ', url
            continue
        # the host may perform as `domain:port`, such as 'example.com:8080'.
        host = m.groupdict()['host'].split(':')[0]
        # host = urlparse.urlparse(url)[1]
        base_domain = '.'.join(host.split('.')[-2:])
        if base_domain in allow_domains:
            new_urls.add(url)
    return new_urls




