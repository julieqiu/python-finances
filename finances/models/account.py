from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, Numeric
from recipes.models.base import Base


class Account(Base):

    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    balance = Column(Numeric)
