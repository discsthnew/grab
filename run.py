# -*- coding: UTF-8 -*-
__author__ = 'discsthnew'

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

site_doudou = {
              'start_urls': ['http://webstatic.doudou.com/'],
              'allow_domains': ['doudou.com']
            }
site_zuhao = {
             'start_urls': ['http://www.22zuhao.com/'],
             'allow_domains': ['22zuhao.com'],
             'cookies': {'cdntoken': 'ba598b6a3231ec3485da740386669144', 'cdnrand': '92f9db58e1a5339db0be9a895135e41d'}
            }

site_56va = {
             'start_urls': ['http://www.56va.cn/'],
             'allow_domains': ['56va.cn']
            }

site_kuaishou = {
                 'start_urls': ['http://www.kuaishou.com/'],
                 'allow_domains': ['kuaishou.com', 'yximgs.com']
                }

def setup_crawl(sites):
    process = CrawlerProcess(get_project_settings())
    for site in sites:
        process.crawl('base', **site)   # 'base' is spider's name
    # the script will block here until all crawling jobs are finished
    process.start()


if __name__ == '__main__':
    sites = [site_kuaishou]
    setup_crawl(sites)
