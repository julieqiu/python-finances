import datetime

from finances.app.classify.constants import CLASSIFICATION_TO_PHRASES


class Transaction:

    def __init__(self,
                 id,
                 date,
                 description,
                 amount,
                 account_id,
                 trip,
                 trip_category,
                 l1,
                 l2,
                 l3):

        self.id = id
        self.date = date
        self.description = description
        self.amount = amount
        self.account_id = account_id
        self.trip = trip
        self.trip_category = trip_category.name if trip_category else ''
        self.l1 = l1 if not trip else 'trip'
        self.l2 = l2 if not trip else 'trip'
        self.l3 = l3 if not trip else 'transaction'

    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year

    def is_valid(self):
        return self.date >= datetime.date(2018, 6, 6)

