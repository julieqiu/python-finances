from finances.database.models import DbTransaction
from finances.domain.models import Transaction


def db_transaction_to_domain_transaction(db_transaction: DbTransaction):
    return Transaction(
        date=db_transaction.date,
        description=db_transaction.description,
        amount=db_transaction.amount,
        account=db_transaction.account_id,
    )
