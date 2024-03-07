from database.models.base import Base
from database.models.mixins import MysqlPrimaryKeyMixin, MysqlStatusMixin
from sqlalchemy import String, Column, Enum
from sqlalchemy.dialects.mysql import ENUM
from rmq.utils import TaskStatusCodes

class Url(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin):
    __tablename__ = 'urls'

    url = Column(String(768), nullable=False)

    def __repr__(self) -> str:
        return f'{self.url}'