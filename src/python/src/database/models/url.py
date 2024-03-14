from database.models.base import Base
from database.models.mixins import MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlExceptionMixin
from sqlalchemy import String, Column


class Url(Base, MysqlPrimaryKeyMixin, MysqlStatusMixin, MysqlExceptionMixin):
    __tablename__ = 'urls'

    url = Column(String(768), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f'{self.url}'