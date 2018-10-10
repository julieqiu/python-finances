from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, Numeric, Enum
from finances.database.models.base import Base
from finances.database.models.enums import AccountType, AccountBank


class DbAccount(Base):

    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    bank = Column(Enum(AccountBank), nullable=False)
    number = Column(Integer)
    routing = Column(Integer)
