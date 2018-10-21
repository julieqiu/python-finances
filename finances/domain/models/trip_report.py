from finances.database.models.enums import TripTransactionCategory
from . import Report


class TripReport(Report):

    def __init__(self, trip, transactions):
        super(TripReport, self).__init__(
            trip.start_date,
            trip.end_date,
            transactions,
        )
        self.trip = trip

    @property
    def name(self) -> str:
        return self.trip.name

    @property
    def total(self) -> float:
        total = 0
        for t in self.transactions:
            total += t.amount
        print(self.name, ': ', total)
        return total

    @property
    def transactions(self):
        return sorted([
            t for t in self._transactions
            if t.trip and t.trip.name == self.trip.name
            and t.is_valid()
        ], key=lambda t: t.date, reverse=True)

    def _total_for(self, category: str) -> float:
        total = 0
        for t in self._transactions_for_category(category):
            total += t.amount
        return total

    def _transactions_for_category(self, category):
        return [
            t for t in self.transactions
            if t.trip_category == category
        ]

    def section_for_category(self, category):
        return {
            'name': ' '.join(category.split('_')).title(),
            'total': self._total_for(category),
            'transactions': self._transactions_for_category(category),
        }

    def trip_transaction_categories(self):
        return [
            ttc.name for ttc in TripTransactionCategory
        ]
