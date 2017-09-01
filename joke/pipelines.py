# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
import MySQLdb
import time
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class JokePipeline(object):
    def __init__(self):
        self.file = codecs.open('content.txt', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class JokePipelineToMYSQL(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        print dbparams
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    # SQL语句在这里
    def _conditional_insert(self, tx, item):
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = "insert into joke_detail(origin,type,title,content,url,ctime,grap_time) values(%s,%s,%s,%s,%s,%s,%s)"
        #print item
        #print item['type']
        #print sql
        params = (item['origin'],item['type'],item['title'],item['content'],item['url'],item['ctime'],now)
        tx.execute(sql,params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue
        #print "wrong"


