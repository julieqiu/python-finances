from finances.app.ingest.ingest_accounts import ingest_accounts
from finances.app.ingest.ingest_trips import ingest_trips
from finances.app.ingest.ingest_transactions import ingest_transactions
from finances.app.ingest.ingest_insurance_claims import ingest_insurance_claims
# from finances.app.ingest.ingest_travel_expenses import ingest_travel_expenses

from finances.database import db_session


TABLES = [
    'accounts',
    'insurance_claims',
    'transactions',
    'trip_transactions',
    'trips',
]


def main():
    with db_session() as session:
        print('TRUNCATING {}'.format(', '.join(t for t in TABLES)))
        session.execute('TRUNCATE {};'.format(', '.join(t for t in TABLES)))
        for t in TABLES:
            session.execute(
                'ALTER SEQUENCE {}_id_seq RESTART WITH 1;'.format(t)
            )

    ingest_accounts()
    print()
    ingest_trips()
    print()
    ingest_transactions()
    print()
    ingest_insurance_claims()


if __name__ == '__main__':
    main()
