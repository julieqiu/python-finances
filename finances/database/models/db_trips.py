from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, Text, ARRAY, Integer, ForeignKey, Numeric
from sqlalchemy import (
    ForeignKey, UniqueConstraint
)

from finances.database.models.base import Base


class DbTrip(Base):

    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
