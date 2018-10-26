from collections import defaultdict

from sqlalchemy import update

from finances.database.models import DbAccount, DbTransaction
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction, db_trip_to_domain_trip, db_account_to_domain_account


def all_accounts(account_id=None):
    with db_session() as session:
        if account_id:
            accounts = [
                db_account_to_domain_account(session.query(DbAccount).get(account_id))
            ]
        else:
            accounts = [
                db_account_to_domain_account(a)
                for a in session.query(DbAccount).all()
            ]

        type_to_accounts = defaultdict(list)
        for a in accounts:
            a.add_transactions([
                db_transaction_to_domain_transaction(t)
                for t in
                session.query(DbTransaction).filter_by(account_id=a.id).all()
            ])
            type_to_accounts[a.type].append(a)

        return type_to_accounts
