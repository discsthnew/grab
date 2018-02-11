# -*- coding: UTF-8 -*-
# author: discsthnew

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import MYSQL

engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' %
                       (MYSQL['user'],
                        MYSQL['password'],
                        MYSQL['host'],
                        MYSQL['port'],
                        MYSQL['db']),
                       encoding='utf-8')

DBSession = sessionmaker(bind=engine, expire_on_commit=False)



