import datetime

from finances.database.models import DbTransaction, DbTrip
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction, db_trip_to_domain_trip
from finances.domain.models import Report, Trip, Transaction


INT_TO_MONTH = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}


def travel_reports():
    trips = {}
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        transactions = []
        for db_trans in db_transactions:
            if db_trans.trip_id:
                db_trip = session.query(DbTrip).get(db_trans.trip_id)
                transactions.append(
                    db_transaction_to_domain_transaction(db_trans, db_trip)
                )

        for t in transactions:
            if not t.trip:
                print('not a trip transaction')
                continue

            if not trips.get(t.trip.name):
                trips[t.trip.name] = {}
                trips[t.trip.name]['start_date'] = t.trip.start_date
                trips[t.trip.name]['end_date'] = t.trip.end_date
                trips[t.trip.name]['transactions'] = []
            trips[t.trip.name]['transactions'].append(t)

    return trips
