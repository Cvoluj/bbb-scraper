import logging
from database.connection import get_db
from database.models import Company
from items import CompanyItem
from rmq.utils.sql_expressions import compile_expression
from twisted.internet import defer
from sqlalchemy import insert
from twisted.internet import reactor


class CompanyDatabasePipeline():

    def open_spider(self, spider):
        print('JASHDJHAJSDHJASHJDHJ')
        self.conn = get_db()

    @defer.inlineCallbacks
    def process_item(self, item: CompanyItem, spider):
        try:
            query = insert(Company).prefix_with('IGNORE').values(**item)
            yield self.conn.runQuery(*compile_expression(query))
        except Exception as e:
            logging.error("Error inserting item: %s", e)
    

    def close_spider(self, spider):
        self.conn.close()
