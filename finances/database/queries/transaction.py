from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from finances.database.models import DbTransaction, DbTripTransaction


def get_transactions(
        session: Session,
        joins: Optional[List] = None,
        filters: Optional[List] = None,
):
    # We don't want to use mutable values as defaults, so set joins/filters to
    # empty lists here if not passed
    if joins is None:
        joins = []
    if filters is None:
        filters = []

    transactions = session.query(DbTransaction)
    for j in joins:
        transactions = transactions.join(*j)

    return transactions.filter(*filters).order_by(DbTransaction.id).all()


def get_max_transaction_id(session):
    return session.query(func.max(DbTransaction.id)).first()[0]
