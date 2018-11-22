from finances.database.models import DbTransaction, DbInsuranceClaim
from finances.database import db_session
from finances.domain.constructors import (
    db_transaction_to_domain_transaction,
    db_insurance_claim_to_domain_insurance_claim,
)
from finances.domain.models import MonthlyReport, InsuranceReport


def insurance_report(year=2018, provider=None):
    insurance_claims, transactions = get_insurance_claims_and_transactions()
    if provider:
        insurance_claims = [
            ic for ic in insurance_claims
            if provider.upper() in ic.provider.upper()
        ]

        transactions = [
            t for t in transactions
            if provider.upper() in t.description.upper()
        ]

    return InsuranceReport(
        year=year,
        transactions=transactions,
        insurance_claims=insurance_claims,
    )


def get_insurance_claims_and_transactions():
    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        transactions = [
            db_transaction_to_domain_transaction(t)
            for t in db_transactions
            if t.l2 == 'HEALTH'
        ]

        db_insurance_claims = session.query(DbInsuranceClaim).all()
        insurance_claims = [
            db_insurance_claim_to_domain_insurance_claim(ic)
            for ic in db_insurance_claims
        ]

    return insurance_claims, transactions
