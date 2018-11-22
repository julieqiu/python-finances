from finances.app.ingest.ingest_accounts import ingest_accounts
from finances.app.ingest.ingest_insurance_claims import ingest_insurance_claims
from finances.app.ingest.ingest_transaction_classifications import ingest_transaction_classifications
from finances.app.ingest.ingest_transactions import ingest_transactions
from finances.app.ingest.ingest_trip_transactions import ingest_trip_transactions
from finances.app.ingest.ingest_trips import ingest_trips

from finances.database import db_session


TABLES = [
    'accounts',
    'insurance_claims',
    'transactions',
    'transaction_classifications',
    'trip_transactions',
    'trips',
]


def main():
    with db_session() as session:
        for t in TABLES:
            result = session.execute('SELECT MAX(id) FROM {};'.format(t)).first()
            if not result[0]:
                max_id = 1
            else:
                max_id = result[0] + 1
            session.execute(
                'ALTER SEQUENCE {}_id_seq RESTART WITH {};'.format(t, max_id)
            )
            print('SET max_id of {} to {}'.format(t, max_id))



if __name__ == '__main__':
    main()
