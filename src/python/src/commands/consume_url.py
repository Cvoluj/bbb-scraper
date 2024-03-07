from rmq.utils import TaskStatusCodes
from rmq.commands import Consumer

from sqlalchemy import select, update
from sqlalchemy.dialects.mysql import insert, Insert
from database.models import Url
from commands.base import BaseCommand


class ConsumeUrlFromQueue(BaseCommand, Consumer):
    def init(self):
        pass

    def build_message_store_stmt(self, message_body):
        """If processing message task requires several queries to db or single query has extreme difficulty
        then this self.process_message method could be overridden.
        In this case using of self.build_message_store_stmt method is not required
        and could be overridden with pass statement

        Example:
        message_body['status'] = TaskStatusCodes.SUCCESS.value
        del message_body['created_at']
        del message_body['updated_at']
        stmt = insert(SearchEngineQuery)
        stmt = stmt.on_duplicate_key_update({
            'status': stmt.inserted.status
        }).values(message_body)
        return stmt
        """
        message_body['status'] = TaskStatusCodes.SUCCESS.value
        stmt: Insert = insert(Url)
        stmt = stmt.on_duplicate_key_update({
            'status': stmt.inserted.status
        }).values(message_body)

        return stmt