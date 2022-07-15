from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class University(Base):
    __tablename__ = "university"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    avg_rate_free = Column(Integer)
    avg_rate_paid = Column(Integer)
    count_free_place = Column(Integer)
    count_paid_place = Column(Integer)
    city = Column(String(128))


