from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()

class Zooshop(Base):
    __tablename__ = 'zooshops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    on_page_order_number = Column(Integer, nullable=False)
    shop_name = Column(String(100))
    description = Column(String(100))
    phone = Column(String(30))
    website = Column(String(30))
    address = Column(String(100))
    how_to_get = Column(String(300))

    page_number = Column(Integer, nullable=False)
    db_added = Column(DateTime, nullable=False, default=datetime.utcnow)


