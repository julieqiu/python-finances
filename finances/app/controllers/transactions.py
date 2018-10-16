from sqlalchemy import update

from finances.database.models import DbTransaction, DbTrip, DbTransactionClassification
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
            elif db_trans.l1 != 'SKIPPED':
                transactions.append(
                    db_transaction_to_domain_transaction(db_trans)
                )
    return transactions


def update_table_values(db_table: str, update_values: tuple, where_values: tuple, session):
    update_statement = """ UPDATE {table} \
        SET {update_col}='{update_val}' \
        WHERE {where_col}='{where_val}' \
        """.format(
            table=db_table,
            update_col=update_values[0],
            update_val=update_values[1],
            where_col=where_values[0],
            where_val=where_values[1],
    )
    session.execute(update_statement)


def all_trip_transactions():
    transactions = []
    with db_session() as session:
        db_trips = session.query(DbTrip).all()
        for db_trip in db_trips:
            trip = db_trip_to_domain_trip(db_trip)
            for trans in trip.transactions:
                transactions.append(trans)
    return transactions


def transactions_for_term(term: str):
    with db_session() as session:
        return session.query(DbTransaction).filter(
            DbTransaction.description.ilike('%{}%'.format(term))
        )

def trip_transaction_category_names():
    return [
        item.name for item in TripTransactionCategory
    ]


def trip_id_and_names():
    with db_session() as session:
        db_trips = session.query(DbTrip).all()

    return sorted([
        (trip.id, trip.name) for trip in db_trips
    ])


def transaction_classifications():
    with db_session() as session:
        return [(tc.l1, tc.l2, tc.l3) for tc in session.query(DbTransactionClassification).all()]
