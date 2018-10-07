from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, String, Date, Text, ARRAY, Integer, ForeignKey, Numeric
from sqlalchemy import (
    ForeignKey, UniqueConstraint
)

from finances.database.models.base import Base
from finances.database.models.enums import TripTransactionCategory


class DbTripTransaction(Base):

    __tablename__ = 'trip_transactions'

    id = Column(Integer, primary_key=True)
    trip_id = Column(ForeignKey('trips.id'), nullable=False)
    transaction_id = Column(ForeignKey('transactions.id'), nullable=False)
    category = Column(Enum(TripTransactionCategory))
