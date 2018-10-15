from typing import List

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, Text, ARRAY, Integer, ForeignKey, Numeric
from sqlalchemy import (
    ForeignKey, UniqueConstraint
)

from finances.database.models.base import Base
from finances.database.models.db_transaction import DbTransaction
from finances.database.models.db_trip_transaction import DbTripTransaction


class DbTrip(Base):

    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    trip_transactions = relationship(
        DbTripTransaction, primaryjoin='DbTripTransaction.trip_id == DbTrip.id', backref='trip_transactions'
    )

    @property
    def transactions(self) -> List[DbTransaction]:
        return [tt.transaction for tt in self.trip_transactions]
