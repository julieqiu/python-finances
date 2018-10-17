from finances.database.models import DbTransaction, DbTrip
from finances.domain.models import Transaction, Trip


def db_transaction_to_domain_transaction(db_transaction: DbTransaction,
                                         db_trip: Trip=None,
                                         trip_category=None):
    domain_trip = None
    if db_trip:
        domain_trip = db_trip_to_domain_trip(db_trip)
    return Transaction(
        id=db_transaction.id,
        date=db_transaction.date,
        description=db_transaction.description,
        amount=db_transaction.amount,
        account=db_transaction.account_id,
        trip=domain_trip,
        trip_category=trip_category,
        l1=db_transaction.l1,
        l2=db_transaction.l2,
        l3=db_transaction.l3,
    )


def db_trip_to_domain_trip(db_trip: DbTrip):
    return Trip(
        id=db_trip.id,
        name=db_trip.name,
        start_date=db_trip.start_date,
        end_date=db_trip.end_date,
    )
