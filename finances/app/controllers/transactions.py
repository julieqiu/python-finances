from sqlalchemy import update

from finances.database.models import DbTransaction, DbTrip, DbTripTransaction, DbTransactionClassification
from finances.database.models.enums import TripTransactionCategory
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction, db_trip_to_domain_trip


def all_transactions(l1: str, l2: str, l3: str):
    transactions = {}
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        for t in db_transactions:
            if t.l1 == 'SKIPPED':
                continue
            transactions[t.id] = db_transaction_to_domain_transaction(t)

        db_trip_transactions = session.query(DbTripTransaction).all()
        for db_tt in db_trip_transactions:
            t = db_transaction_to_domain_transaction(
                db_tt.transaction, db_tt.trip, db_tt.category
            )
            transactions[t.id] = t

    return sorted(transactions.values(), key=lambda t: t.date, reverse=True)


def convert_for_type(val):
    if val.isnumeric() == int:
        return int(update_val)
    elif item.isalpha():
        return "'{}'".format(item)
    return val


def update_table_values(db_table: str, update_values: tuple, where_values: tuple, session):
    update_col = update_values[0]
    update_val = update_values[1]
    where_col = where_values[0]
    where_val = where_values[1]

    if update_values[1] == '':
        update_val = 'OTHER'

    insert_statement = """ INSERT INTO {table} \
        ({update_col}, {where_col}) \
        VALUES({update_val}, {where_val}) \
        """.format(
            table=db_table,
            update_col=update_col,
            update_val=update_val,
            where_col=where_col,
            where_val=where_val,
        )

    update_statement = """ UPDATE {table} \
        SET {update_col}='{update_val}' \
        WHERE {where_col}='{where_val}' \
        """.format(
            table=db_table,
            update_col=update_col,
            update_val=update_val,
            where_col=where_col,
            where_val=where_val,
        )
    if not update_values[1] and update_values[0] != 'category' and db_table == 'trip_transactions':
        delete_statement = """ DELETE FROM {table} \
                WHERE {where_col}={where_val}
            """.format(
                table=db_table,
                where_col=where_col,
                where_val=where_val,
            )
        print(delete_statement)
        session.execute(delete_statement)
    else:
        try:
            print(insert_statement)
            session.execute(insert_statement)
        except Exception as err:
            print(err)
            session.rollback()
            print(update_statement)
            session.execute(update_statement)


def all_trip_transactions(trip_id: int, trip_category: str):
    transactions = []
    print(trip_id, trip_category)
    with db_session() as session:
        if not trip_id:
            db_trips = session.query(DbTrip).all()
        else:
            db_trips = session.query(DbTrip).filter_by(id=trip_id).all()

        print('num trips', len(db_trips))
        for db_trip in db_trips:
            trip = db_trip_to_domain_trip(db_trip)
            for tt in db_trip.trip_transactions:
                if trip_category and not tt.category:
                    continue
                elif trip_category and tt.category.name != trip_category.upper():
                    continue

                transactions.append(
                    db_transaction_to_domain_transaction(
                        tt.transaction,
                        db_trip,
                        tt.category)
                )


    print('num transactions', len(transactions))
    return sorted(transactions, key=lambda t: t.date, reverse=True)


def transactions_for_term(term: str):
    transactions = {}
    with db_session() as session:
        db_transactions = session.query(DbTransaction).filter(
            DbTransaction.description.ilike('%{}%'.format(term))
        )
        db_trip_transactions = session.query(DbTripTransaction).filter(
            DbTripTransaction.transaction_id.in_([t.id for t in db_transactions])
        )

        for t in db_transactions:
            transactions[t.id] = db_transaction_to_domain_transaction(t)
        for tt in db_trip_transactions:
            transactions[tt.transaction_id] = db_transaction_to_domain_transaction(
                tt.transaction,
                tt.trip,
                tt.category,
            )

    return transactions.values()

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
