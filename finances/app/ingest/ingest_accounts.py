from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.db_errors import UniqueViolation, split_integrity_error
from finances.database.models import DbAccount


ACCOUNT_INFO = [
    ('CHASE SAPPHIRE RESERVE', 'CREDIT_CARD', 'CHASE', 2039, None),
    ('CHASE FREEDOM', 'CREDIT_CARD', 'CHASE', 4687, None),
    ('CHASE CHECKINGS', 'CHECKINGS', 'CHASE', 9986, None),
    ('CHASE SAVINGS', 'SAVINGS', 'CHASE', 2371, None),
    ('BANK OF AMERICA SAVINGS', 'SAVINGS', 'BANK_OF_AMERICA', 1, None),
    ('BANK OF AMERICA CHECKINGS', 'CHECKINGS', 'BANK_OF_AMERICA', 2, None),
    ('CHARLES SCHWAB', 'CHECKINGS', 'CHARLES_SCHWAB', 3, None),
    ('EMPIRE', 'INSURANCE', 'EMPIRE', 4, None),
    ('PAYPAL', 'PAYPAL', 'PAYPAL', 5, None),
]

def ingest_accounts():
    print('~~~ Adding ACCOUNTS to DB ~~~')
    for name, account_type, bank, number, routing in ACCOUNT_INFO:
        print(name, account_type, bank, number, routing)
        try:
            with db_session() as session, split_integrity_error() as err:
                values = {
                    'name': name,
                    'type': account_type,
                    'bank': bank,
                    'number': number,
                    'routing': routing,
                }

                upsert = insert(DbAccount).values(values).on_conflict_do_update(
                        index_elements=['name'],
                        set_=values
                    )
                session.execute(upsert)

        except UniqueViolation as err:
            print(err)
            continue
        except Exception as err:
            print(err)
            raise err


if __name__ == '__main__':
    ingest_accounts()
