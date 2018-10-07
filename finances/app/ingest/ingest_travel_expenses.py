from finances.database import db_session
from finances.database.models import DbTrip, DbTransaction
from finances.domain.constructors import db_transaction_to_domain_transaction


def write_to_db(session, transaction: DbTransaction, trip: DbTrip) -> None:
    transaction.trip_id = trip.id
    session.add(transaction)
    session.commit()


def match_transactions_with_trip():
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        db_trips = session.query(DbTrip).all()
        for trip in db_trips:
            for t in db_transactions:
                if t.trip_id is not None:
                    print('Skipping, has trip id')
                    continue
                if trip.start_date <= t.date <= trip.end_date:
                    domain_trans = db_transaction_to_domain_transaction(t)
                    if (domain_trans.l1 == 'EXPENSES' and
                        domain_trans.l2 not in ['Health', 'Shopping'] and
                        domain_trans.l3 not in ['venmo']):
                        print('Writing: ', t.description)
                        write_to_db(session, t, trip)


def main():
    match_transactions_with_trip()


if __name__ == '__main__':
    main()
