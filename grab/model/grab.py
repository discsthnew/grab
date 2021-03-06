# -*- coding: UTF-8 -*-
# author: discsthnew

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, text

import db_config

Base = declarative_base()


class Resource(Base):
    __tablename__ = 'resource_test'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    url = Column(String(512), nullable=False)
    content_type = Column(String(64), nullable=True, server_default='text/html')
    content_length = Column(Integer(), nullable=False)
    cache_control = Column(String(128), nullable=True)
    host = Column(String(64), nullable=True)
    date = Column(DateTime(), server_default=text('CURRENT_TIMESTAMP'))


Base.metadata.create_all(db_config.engine)

