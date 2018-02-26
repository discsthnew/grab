# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from model.grab import Resource
from model.db_config import DBSession


class GrabPipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        resource = Resource(
            url=item['url'],
            content_type=item['content_type'],
            content_length=item['content_length'],
            cache_control=item['cache_control'],
            host=item['host']
        )

        if self.session.query(Resource).filter(Resource.url==item['url']).scalar():
            pass
        else:
            self.session.add(resource)
            try:
                self.session.commit()
            except Exception:
                self.session.rollback()
        return item

    def close_spider(self, spider):
        self.session.close()
