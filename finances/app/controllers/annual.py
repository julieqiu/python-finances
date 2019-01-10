import datetime

from finances.database.models import DbTransaction
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction
from finances.domain.models import AnnualReport


def annual_report(year=2018):
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        transactions = [
            db_transaction_to_domain_transaction(t)
            for t in db_transactions
            if t.date.year == 2018
        ]

    return AnnualReport(
        datetime.date(2018, 6, 1),
        datetime.date(2018, 12, 31),
        transactions,
    )
