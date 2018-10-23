from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, JSON, Integer, Column, String, Text, Boolean, ForeignKey, Numeric, UniqueConstraint

from finances.database.models.base import Base


class DbTransactionClassification(Base):

    __tablename__ = 'transaction_classifications'
    __table_args__ = (UniqueConstraint('l1', 'l2', 'l3'),)

    id = Column(Integer, primary_key=True)
    l1 = Column(String, nullable=False)
    l2 = Column(String, nullable=False)
    l3 = Column(String, nullable=False)
    phrases = Column(ARRAY(Text), nullable=False)
