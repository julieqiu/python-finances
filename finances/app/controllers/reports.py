import datetime
from typing import List

from finances.database.models import DbTransaction, DbTripTransaction
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction
from finances.domain.models import Report, Transaction


def get_transactions_between_dates(start_date: datetime.datetime, end_date: datetime.datetime):
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        transactions = {
            t.id: db_transaction_to_domain_transaction(t)
            for t in db_transactions
            if start_date <= t.date <= end_date
        }

        for tt in session.query(DbTripTransaction).all():
            if start_date <= tt.transaction.date <= end_date:
                transactions[tt.transaction.id] = db_transaction_to_domain_transaction(
                    tt.transaction, tt.trip, tt.category)

    return transactions.values()


def generate_report(start_date: datetime.datetime, end_date: datetime.datetime):
    transactions = get_transactions_between_dates(start_date, end_date)
    return group_transactions(transactions)
