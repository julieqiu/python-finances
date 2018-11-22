from finances.database.models import DbAccount, DbTransaction, DbTrip, DbInsuranceClaim
from finances.domain.models import Account, Transaction, Trip, InsuranceClaim


def db_transaction_to_domain_transaction(db_transaction: DbTransaction,
                                         db_trip: Trip=None,
                                         trip_category=None):
    domain_trip = None
    if db_trip:
        domain_trip = db_trip_to_domain_trip(db_trip)

    description = db_transaction.description_edited
    if not description:
        description = db_transaction.description

    return Transaction(
        id=db_transaction.id,
        date=db_transaction.date,
        description=description,
        amount=db_transaction.amount,
        account_id=db_transaction.account_id,
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


def db_account_to_domain_account(db_account: DbAccount):
    return Account(
        id=db_account.id,
        name=db_account.name,
        account_type=db_account.type,
        bank=db_account.bank,
        number=db_account.number,
        routing=db_account.routing,
    )


def db_insurance_claim_to_domain_insurance_claim(db_insurance_claim: DbInsuranceClaim):
    return InsuranceClaim(
        id=db_insurance_claim.id,
        service_date=db_insurance_claim.service_date,
        claim_type=db_insurance_claim.type,
        claim_id=db_insurance_claim.claim_id,
        patient=db_insurance_claim.patient,
        provider=db_insurance_claim.provider,
        billed=db_insurance_claim.billed,
        allowed_amount=db_insurance_claim.allowed_amount,
        paid=db_insurance_claim.paid,
        deductible=db_insurance_claim.deductible,
        coinsurance=db_insurance_claim.coinsurance,
        copay=db_insurance_claim.copay,
        not_covered=db_insurance_claim.not_covered,
        personal_cost=db_insurance_claim.personal_cost,
        status=db_insurance_claim.status,
    )
