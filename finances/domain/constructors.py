from finances.database.models import DbTransaction, DbTrip
from finances.domain.models import Transaction, Trip


def db_transaction_to_domain_transaction(db_transaction: DbTransaction, db_trip: DbTrip=None):
    trip = None
    if db_trip:
        trip = db_trip_to_domain_trip(db_trip)

    return Transaction(
        date=db_transaction.date,
        description=db_transaction.description,
        amount=db_transaction.amount,
        account=db_transaction.account_id,
        trip=trip,
    )


def db_trip_to_domain_trip(db_trip: DbTrip):
    return Trip(
        name=db_trip.name,
        start_date=db_trip.start_date,
        end_date=db_trip.end_date,
    )
