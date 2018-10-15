from finances.database import db_session
from finances.database.db_errors import UniqueViolation, split_integrity_error
from finances.database.models import DbTrip, DbTransaction, DbTripTransaction
from finances.domain.constructors import db_transaction_to_domain_transaction


def write_to_db(trip_id: int, transaction_id: int):
    try:
        with db_session() as session, split_integrity_error() as err:
            session.add(DbTripTransaction(
                trip_id=trip_id,
                transaction_id=transaction_id,
            ))
            session.commit()
    except UniqueViolation as err:
        print(err)


def ingest_trip_transactions():
    domain_transactions = []
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        db_trips = session.query(DbTrip).all()
        for trip in db_trips:
            trip_transaction_ids = set([tt.id for tt in trip.trip_transactions])

            for t in db_transactions:
                if t in trip_transaction_ids:
                    print('Skipping - already in table')
                    continue
                elif trip.start_date <= t.date <= trip.end_date:
                    domain_transactions.append(
                        db_transaction_to_domain_transaction(t, trip)
                    )

    for domain_trans in domain_transactions:
        if (domain_trans.l1 == 'EXPENSES' and
            domain_trans.l2 not in ['Health', 'Shopping'] and
            domain_trans.l3 not in ['venmo']):
            print('Writing: ', t.description)

            write_to_db(domain_trans.trip.id, domain_trans.id)


if __name__ == '__main__':
    ingest_trip_transactions()
