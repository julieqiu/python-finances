from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Date, Text, ARRAY, Integer, ForeignKey, Numeric

from finances.database.models.base import Base


class DbInsuranceClaim(Base):

    __tablename__ = 'insurance_claims'

    id = Column(Integer, primary_key=True)
    service_date = Column(Date, nullable=False)
    type = Column(String, nullable=True)
    claim_number = Column(String, nullable=True)
    patient = Column(String, nullable=True)
    provider = Column(String, nullable=False)
    billed = Column(Numeric, default=0)
    allowed_amount = Column(Numeric, default=0)
    paid = Column(Numeric, default=0)
    deductible = Column(Numeric, default=0)
    coinsurance = Column(Numeric, default=0)
    copay = Column(Numeric, default=0)
    not_covered = Column(Numeric, default=0)
    personal_cost = Column(Numeric, default=0)
    status = Column(String)
    account_id = Column(ForeignKey('accounts.id'), nullable=False)
