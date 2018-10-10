from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean, Column, String, Date, Text, ARRAY, Integer, ForeignKey, Numeric, Enum,
    ForeignKey, UniqueConstraint
)

from finances.database.models.base import Base
from finances.database.models.enums import TripTransactionCategory


class DbTripTransaction(Base):

    __tablename__ = 'trip_transactions'

    id = Column(Integer, primary_key=True)
    trip_id = Column(ForeignKey('trips.id'), nullable=False)
    transaction_id = Column(ForeignKey('transactions.id'), nullable=False, unique=True)
    category = Column(Enum(TripTransactionCategory), nullable=True)

    transaction = relationship('DbTransaction', lazy='joined')
    trip = relationship('DbTrip', lazy='joined')
