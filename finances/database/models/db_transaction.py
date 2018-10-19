from sqlalchemy import (
    Boolean, Column, String, Date, Text, ARRAY, Integer, ForeignKey, Numeric,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship

from finances.database.models.base import Base
from finances.database.models.db_transaction_classification import DbTransactionClassification


class DbTransaction(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        UniqueConstraint('date', 'description', 'amount'),
    )

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    description_edited = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    reimbursable = Column(Boolean, nullable=True)
    reimbursement = Column(Boolean, nullable=True)
    account_id = Column(ForeignKey('accounts.id'), nullable=True)
    classification_id = Column(ForeignKey('transaction_classifications.id'), nullable=True)

    classification = relationship(
        DbTransactionClassification,
        primaryjoin='DbTransactionClassification.id == DbTransaction.classification_id',
        backref='transaction_classifications'
    )


    @property
    def l1(self) -> str:
        if self.classification:
            return self.classification.l1
        return ''

    @property
    def l2(self) -> str:
        if self.classification:
            return self.classification.l2
        return ''

    @property
    def l3(self) -> str:
        if self.classification:
            return self.classification.l3
        return ''
