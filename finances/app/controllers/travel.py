import datetime

from finances.database.models import DbTransaction, DbTrip
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction, db_trip_to_domain_trip
from finances.domain.models import TripReport, Transaction


def travel_reports(trip_id=None):
    trips = {}

    transactions = []
    with db_session() as session:
        if not trip_id:
            db_trips = session.query(DbTrip).all()
        else:
            db_trips = session.query(DbTrip).filter_by(id=trip_id).all()
        for db_trip in db_trips:
            for db_trip_transaction in db_trip.trip_transactions:
                transactions.append(
                    db_transaction_to_domain_transaction(
                        db_trip_transaction.transaction,
                        db_trip,
                        db_trip_transaction.category,
                    )
                )

    for t in transactions:
        if not t.trip:
            continue

        if not trips.get(t.trip.name):
            trips[t.trip.name] = TripReport(t.trip, [])
        trips[t.trip.name].add_transaction(t)

    return sorted([v for _, v in trips.items()], key=lambda v: v.trip.start_date, reverse=True)
