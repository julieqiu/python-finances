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

    @property
    def housing_transactions(self):
        pass

    @property
    def travel_transactions(self):
        pass

    @property
    def food_transactions(self):
        pass

    @property
    def entertainment_transactions(self):
        pass

    @property
    def local_transportation_transactions(self):
        pass

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
