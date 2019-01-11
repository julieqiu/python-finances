from sqlalchemy import update, or_, and_

from finances.database.models import DbTransaction, DbTrip, DbTripTransaction, DbTransactionClassification
from finances.database.models.enums import TripTransactionCategory
from finances.database.queries.transaction import get_transactions
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction, db_trip_to_domain_trip


FILTER_DIR = '/Users/julie/Code/github.com/finances/finances/app/classify/filters/'
L3_TO_FILE = {
    'ALCOHOL': 'alcohol.txt',
    'COFFEE': 'coffee.txt',
    'ENTERTAINMENT': 'entertainment.txt',
    'FOOD': 'food.txt',
    'SHOPPING': 'shopping.txt',
}


def all_transactions(l1: str=None, l2: str=None, l3: str=None, month: int=None, year: int=2018):
    transactions = {}
    with db_session() as session:
        db_transactions = get_transactions(
            session=session
        )
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

    if month:
        transactions = {
                k:v for k, v in transactions.items()
                if v.date.month == month and v.date.year == year
        }

    if l3:
        transactions = [t for t in transactions.values() if t.l3 == l3.upper()]
    elif l2:
        transactions = [t for t in transactions.values() if t.l2 == l2.upper()]
    elif l1:
        transactions = [t for t in transactions.values() if t.l1 == l1.upper()]
    else:
        transactions = [t for t in transactions.values()]

    return sorted([t for t in transactions], key=lambda t: t.date, reverse=True)


def convert_for_type(val):
    if val.isnumeric() == int:
        return int(update_val)
    elif item.isalpha():
        return "'{}'".format(item)
    return val


def update_table_values(db_table: str, update_values: tuple, where_values: tuple):
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
        with db_session() as session:
            session.execute(delete_statement)
    else:
        with db_session() as session:
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
    return sorted([t for t in transactions if t.is_valid()], key=lambda t: t.date, reverse=True)


def transactions_for_term(term: str):
    transactions = {}
    with db_session() as session:
        db_trip_transactions = session.query(DbTripTransaction).all()
        db_transactions = session.query(DbTransaction).filter(
                or_(
                    and_(
                        DbTransaction.description.ilike('%{}%'.format(term)),
                        DbTransaction.description_edited.is_(None)
                    ),
                    DbTransaction.description_edited.ilike('%{}%'.format(term)),
                )
            )

        for t in db_transactions:
            transactions[t.id] = db_transaction_to_domain_transaction(t)

        for tt in db_trip_transactions:
            if tt.transaction_id in transactions:
                transactions[tt.transaction_id] = db_transaction_to_domain_transaction(
                    tt.transaction, tt.trip, tt.category
                )

    return sorted([t for t in transactions.values()], key=lambda t: t.date, reverse=True)



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
        return [(tc.id, tc.l1, tc.l2, tc.l3) for tc in session.query(DbTransactionClassification).all()]


def transactions(request):
    if request.method == 'POST':
        for key, value in request.form.items():
            if value:
                db_table = key.split('-')[0]
                db_col = key.split('-')[1]
                db_val = key.split('-')[2]
                if len(key.split('-')) == 4:
                    # for description_edited
                    db_col2 = key.split('-')[3]
                    db_val2 = value
                elif len(value.split('-')) == 2:
                    db_col2 = value.split('-')[0]
                    db_val2 = value.split('-')[1]

                # TODO: send description over the wire and write to disk
                update_table_values(
                    db_table,
                    update_values=(db_col2, db_val2),
                    where_values=(db_col, db_val),
                )

    if 'trips' in request.args.keys():
        trip_id = request.args.get('id')
        if trip_id and trip_id.isnumeric():
            trip_id = int(trip_id)

        category = request.args.get('category')
        transactions = all_trip_transactions(trip_id, category)

    elif 'month' in request.args.keys():
        month = int(request.args.get('month'))
        year = int(request.args.get('year', 2018))
        transactions = all_transactions(month=month, year=year)

    elif 'amount' in request.args.keys():
        term = request.args.get('term')
        transactions = transactions_for_amount(amount)

    elif 'term' in request.args.keys():
        term = request.args.get('term')
        transactions = transactions_for_term(term)

    else:
        l1 = request.args.get('l1')
        l2 = request.args.get('l2')
        l3 = request.args.get('l3')
        transactions = all_transactions(l1=l1, l2=l2, l3=l3)

    if 'classify' in request.args.keys():
        transactions = [
            t for t in transactions if t.l3 == 'OTHER'
        ]

    return transactions
