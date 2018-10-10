from finances.database.models import DbTransaction, DbTrip
from finances.database.models.enums import TripTransactionCategory
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction, db_trip_to_domain_trip


def all_transactions(trips=False):
    transactions = []
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        for db_trans in db_transactions:
            if trips and db_trans.trip_id:
                    db_trip = session.query(DbTrip).get(db_trans.trip_id)
                    transactions.append(
                        db_transaction_to_domain_transaction(db_trans, db_trip)
                    )
            else:
                transactions.append(
                    db_transaction_to_domain_transaction(db_trans)
                )
    return transactions


def all_trip_transactions():
    transactions = []
    with db_session() as session:
        db_trips = session.query(DbTrip).all()
        for db_trip in db_trips:
            trip = db_trip_to_domain_trip(db_trip)
            for trans in trip.transactions:
                transactions.append(trans)
    return transactions


def all_trip_categories():
    return [
        item.name for item in TripTransactionCategory
    ]


def all_trips():
    with db_session() as session:
        db_trips = session.query(DbTrip).all()

    return sorted([
        '{} - {}'.format(trip.start_date, trip.name) for trip in db_trips
    ])


def transactions_for_term(term: str):
    with db_session() as session:
        return session.query(DbTransaction).filter(
            DbTransaction.description.ilike('%{}%'.format(term))
        )
