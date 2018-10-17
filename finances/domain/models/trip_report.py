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
    def transactions(self):
        return sorted([
            t for t in self._transactions
            if t.trip and t.trip.name == self.trip.name
        ], key=lambda t: t.date, reverse=True)


    def _transactions_for_category(self, category):
        return [
            t for t in self.transactions
            if t.trip_category == category
        ]

    @property
    def housing_transactions(self):
        return self._transactions_for_category(TripTransactionCategory.HOUSING.name)

    @property
    def travel_transactions(self):
        return self._transactions_for_category(TripTransactionCategory.TRAVEL.name)

    @property
    def food_transactions(self):
        return self._transactions_for_category(TripTransactionCategory.FOOD.name)

    @property
    def entertainment_transactions(self):
        return self._transactions_for_category(TripTransactionCategory.ENTERTAINMENT.name)

    @property
    def local_transportation_transactions(self):
        return self._transactions_for_category(TripTransactionCategory.LOCAL_TRANSPORTATION.name)

    @property
    def other_transportation_transactions(self):
        return [
            t for t in self.transactions
            if not t.trip_category
        ]

    def to_dict(self) -> dict:
        if not self.transactions:
            return {}

        return {
            'total_earned': self.total_earned,
            'total_spent': self.total_spent,
            'total_saved': self.total_saved,
            'reports': [
                {
                    'header': 'Income',
                    'data': self.categorized_transactions.get('INCOME', {}),
                    'color': 'green',
                },
                {
                    'header': 'Monthly',
                    'data': self.categorized_transactions.get('MONTHLY', {}),
                    'color': 'red',
                },
                {
                    'header': 'Expenses',
                    'data': self.categorized_transactions.get('EXPENSES', {}),
                    'color': 'red',
                },
                {
                    'header': 'Skipped',
                    'data': self.categorized_transactions.get('SKIPPED', {}),
                    'color': 'gray',
                },
            ]
        }
