from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.db_errors import UniqueViolation, split_integrity_error
from finances.database.models import DbTrip, DbTransaction, DbTripTransaction
from finances.database.models.enums import TripTransactionCategory
from finances.domain.constructors import db_transaction_to_domain_transaction

MAX_ID = 1232

CATEGORY_TO_PHRASES = {
    TripTransactionCategory.ENTERTAINMENT: ['TOURS'],
    TripTransactionCategory.FOOD: [],
    TripTransactionCategory.HOUSING: ['HOTEL', 'AIRBNB', 'BOOKING', 'INN'],
    TripTransactionCategory.LOCAL_TRANSPORTATION: [
        'LYFT',
        'METRO',
        'TAXI',
        'UBER',
    ],
    TripTransactionCategory.TRAVEL: [
        'AIRLINE',
        'AMERICAN',
        'CHASE TRAVEL',
        'DELTA',
        'RYANAIR',
        'UNITED',
        'VUELING',
        'IBERIA',
        'AERLING',
        'FRONTIER',
        'NORWEGIAN',
    ],
}


def write_to_db(trip_id: int, transaction_id: int, category: TripTransactionCategory):
    try:
        values = dict(
                trip_id=trip_id,
                transaction_id=transaction_id,
                category=category,
                )
        with db_session() as session, split_integrity_error() as err:
            upsert = insert(DbTripTransaction).values(values).on_conflict_do_update(
                    index_elements=['transaction_id'],
                    set_=values
                )
            session.execute(upsert)
    except UniqueViolation as err:
        print(err)


def categorize_trip_transaction(domain_trans: DbTransaction) -> str:
    for category, phrases in CATEGORY_TO_PHRASES.items():
        if any(phrase
               for phrase in phrases
               if phrase in domain_trans.description.upper()):
            return category

    if domain_trans.l2 in [k.name for k in CATEGORY_TO_PHRASES.keys()]:
        return domain_trans.l2
    return 'FOOD'


def should_categorize(domain_trans) -> bool:
    if not domain_trans.l1:
        return True

    if domain_trans.l1.upper() in ['MONTHLY', 'SKIPPED', 'INCOME']:
        return False

    if domain_trans.l2.upper() in ['HEALTH', 'SHOPPING']:
        return False

    if domain_trans.l3.upper() in ['VENMO']:
        return False

    return True



def ingest_trip_transactions():
    with db_session() as session:
        trip_transaction_ids = {
            tt.transaction_id for tt in
            session.query(DbTripTransaction).all()
        }
        print(len(trip_transaction_ids))
        domain_transactions = []
        for trip in session.query(DbTrip).all():
            for t in session.query(DbTransaction).filter(DbTransaction.id > MAX_ID):
                if t.id in trip_transaction_ids:
                    print('Skipping - already in table and categorized')
                    continue
                elif trip.start_date <= t.date <= trip.end_date:
                    domain_transactions.append(
                        db_transaction_to_domain_transaction(t, trip)
                    )

    for domain_trans in domain_transactions:
        if not should_categorize(domain_trans):
            continue

        print('Writing [{}]: {}'.format(domain_trans.id, domain_trans.description))
        category = categorize_trip_transaction(domain_trans)
        write_to_db(
            trip_id=domain_trans.trip.id,
            transaction_id=domain_trans.id,
            category=category,
        )

    print('Make sure to update the max id in this script to the latest max id in transactions')
    print('SELECT MAX(id) FROM transactions;')


if __name__ == '__main__':
    ingest_trip_transactions()
