from database.models.base import Base
from database.models.mixins import MysqlPrimaryKeyMixin, MysqlTimestampsMixin
from sqlalchemy import String, Column, JSON, Text, BIGINT, TIMESTAMP

str_768 = 768

class Company(Base, MysqlPrimaryKeyMixin, MysqlTimestampsMixin):
    __tablename__ = 'companies'

    business_id = Column(String(str_768), nullable=False, unique=True)
    url = Column(String(str_768), nullable=False)
    name = Column(String(1024), nullable=False)
    category = Column(String(str_768), nullable=False)
    address = Column(Text, nullable=False)
    country = Column(String(6), nullable=False)
    state = Column(String(2), nullable=False)
    city = Column(String(40), nullable=False)
    street = Column(String(str_768), nullable=True)
    postal_code = Column(String(10), nullable=False)
    website = Column(String(str_768), nullable=True)
    image_url = Column(String(768), nullable=True)
    phone = Column(String(20), nullable=True)
    fax = Column(String(20), nullable=True)
    work_hours = Column(JSON, nullable=True)
    user_score = Column(String(5), nullable=True)
    reviews_quantity = Column(BIGINT, nullable=True)
    accredited_score = Column(String(2), nullable=False)
    accredited_date = Column(TIMESTAMP, nullable=True)
    foundation_date = Column(TIMESTAMP, nullable=True)
    years_old = Column(BIGINT, nullable=True)
    instagram = Column(String(str_768), nullable=True)
    facebook = Column(String(str_768), nullable=True)
    twitter = Column(String(str_768), nullable=True)
    management = Column(JSON, nullable=True)
    contact = Column(JSON, nullable=True)
    sent_to_customer = Column("sent_to_customer", TIMESTAMP, nullable=True, server_default=None)


    def __repr__(self) -> str:
        return f'{self.url} {self.name}'