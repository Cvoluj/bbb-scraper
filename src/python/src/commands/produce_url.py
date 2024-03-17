from rmq.utils import TaskStatusCodes
from rmq.commands import Producer

from sqlalchemy import select, update
from database.models import Url
from commands.base import BaseCommand

class ProduceUrlToQueue(Producer):
    def init(self):
        pass

    def build_task_query_stmt(self, chunk_size):
        """This method must returns sqlalchemy Executable or string that represents valid raw SQL select query

        stmt = select([DBModel]).where(
            DBModel.status == TaskStatusCodes.NOT_PROCESSED.value,
        ).order_by(DBModel.id.asc()).limit(chunk_size)
        return stmt
        """
        stmt = select(Url).where(
            Url.status == TaskStatusCodes.NOT_PROCESSED.value,
        ).order_by(Url.id.asc()).limit(chunk_size)
        return stmt
    
    def build_task_update_stmt(self, db_task, status):
        """This method must returns sqlalchemy Executable or string that represents valid raw SQL update query

        return update(DBModel).where(DBModel.id == db_task['id']).values({'status': status})
        """
        return update(Url).where(Url.id == db_task['id']).values({'status': status})
