import datetime
from collections import defaultdict

from finances.domain.models.report import Report


class InsuranceReport(Report):

    def __init__(self, year, transactions, insurance_claims):
        super(InsuranceReport, self).__init__(
            start_date=datetime.date(year, 1, 1),
            end_date=datetime.date(year, 12, 31),
            transactions=transactions,
        )
        self._insurance_claims = insurance_claims

    @property
    def name(self) -> str:
        return 'Insurance Claims'

    def total_for(self, category) -> float:
        total = 0
        if category.lower() == 'payments':
            for t in self.payments:
                total += t.amount
            return total

        if category.lower() == 'reimbursements':
            for t in self.reimbursements:
                total += t.amount
            return total

        for ic in self.insurance_claims:
            if category.lower() == 'billed':
                total += ic.billed
            elif category.lower() == 'paid':
                total += ic.paid
            elif category.lower() == 'deductible':
                total += ic.deductible
            elif category.lower() == 'coinsurance':
                total += ic.coinsurance
            elif category.lower() == 'personal_cost':
                total += ic.personal_cost
            elif category.lower() == 'not_covered':
                total += ic.not_covered
        return total


    @property
    def insurance_claims(self) -> list:
        return sorted([
            ic for ic in self._insurance_claims
            if ic.date.year == self.year
            and ic.personal_cost > 0
            and 'not available' not in ic.provider
            and ic.status == 'Approved'
        ], key=lambda t: t.date, reverse=True)

    @property
    def transactions(self) -> list:
        return sorted([
            t for t in self._transactions
            if t.l2 == 'HEALTH'
        ], key=lambda t: t.date, reverse=True)

    @property
    def payments(self) -> list:
        return sorted([
            t for t in self._transactions
            if t.l3 != 'REIMBURSEMENTS'
        ], key=lambda t: t.date, reverse=True)

    @property
    def reimbursements(self) -> list:
        return sorted([
            t for t in self._transactions
            if t.l3 == 'REIMBURSEMENTS'
        ], key=lambda t: t.date, reverse=True)
