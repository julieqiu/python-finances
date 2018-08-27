from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, Text, ARRAY, Integer, ForeignKey, Numeric

from finances.models.base import Base


class Transaction(Base):

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric)
    account_id = Column(ForeignKey('accounts.id'), nullable=False)
