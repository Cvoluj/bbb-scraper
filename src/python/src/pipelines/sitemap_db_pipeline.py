import scrapy
import logging
from twisted.internet import reactor
from database.connection import get_db
from database.models import Url
from items.urls_item import UrlsItem
from rmq.utils.sql_expressions import compile_expression, stringify_expression
from twisted.internet import defer
from sqlalchemy import insert
from twisted.internet import reactor



class UrlDatabasePipeline():
    
    def open_spider(self, spider):
        self.conn = get_db()

    @defer.inlineCallbacks
    def process_item(self, item: UrlsItem, spider):
        try:
            query = insert(Url).prefix_with('IGNORE').values(url=item['url'])
            yield self.conn.runQuery(*compile_expression(query))
        except Exception as e:
            logging.error("Error inserting item: %s", e)
    

    def close_spider(self, spider):
        self.conn.close()