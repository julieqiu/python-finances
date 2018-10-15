from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, JSON, Integer, Column, String, Text, Boolean, ForeignKey, Numeric

from finances.database.models.base import Base


class DbTransactionClassification(Base):

    __tablename__ = 'transaction_classifications'

    id = Column(Integer, primary_key=True)
    l1 = Column(String, nullable=False)
    l2 = Column(String, nullable=True)
    l3 = Column(String, nullable=True)
    phrases = Column(ARRAY(Text), nullable=False)
