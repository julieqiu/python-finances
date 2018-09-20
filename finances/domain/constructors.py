from finances.database.models import DbTransaction
from finances.domain.transaction import Transaction


def db_transaction_to_domain_transaction(db_transaction: DbTransaction):
    return Transaction(
        db_transaction.date = date,
        db_transaction.description = description,
        db_transaction.amount = amount,
        db_transaction.account = account,
    )
