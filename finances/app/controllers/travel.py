import datetime

from finances.database.models import DbTransaction, DbTrip
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction, db_trip_to_domain_trip
from finances.domain.models import TripReport, Transaction


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
            trips[t.trip.name] = TripReport(t.trip, [])
        trips[t.trip.name].add_transaction(t)

    x = sorted([v for _, v in trips.items()], key=lambda v: v.trip.start_date, reverse=True)
    print(x)
    return x
