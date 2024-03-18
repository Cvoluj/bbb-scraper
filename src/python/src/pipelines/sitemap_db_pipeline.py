import logging
from database.connection import get_db
from database.models import Url
from items.url_item import UrlItem
from rmq.utils.sql_expressions import compile_expression
from twisted.internet import defer
from sqlalchemy import insert


class UrlDatabasePipeline():
    
    def open_spider(self, spider):
        self.conn = get_db()

    @defer.inlineCallbacks
    def process_item(self, item: UrlItem, spider):
        try:
            query = insert(Url).prefix_with('IGNORE').values(url=item['url'])
            yield self.conn.runQuery(*compile_expression(query))
        except Exception as e:
            logging.error("Error inserting item: %s", e)
    

    def close_spider(self, spider):
        self.conn.close()