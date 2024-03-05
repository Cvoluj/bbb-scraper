from sqlalchemy import String, Column
from database.models.base import Base


class Url(Base):
    __tablename__ = 'urls'
    url = Column(String(768), primary_key = True)

    def __repr__(self) -> str:
        return f'{self.url}'