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
        self._l1 = l1
        self._l2 = l2
        self._l3 = l3

    @property
    def l1(self):
        if self.trip or not self._l1:
            return 'EXPENSES'
        return self._l1

    @property
    def l2(self):
        if self.trip:
            return 'TRIP'
        if not self._l2:
            return 'OTHER'
        return self._l2

    @property
    def l3(self):
        if self.trip:
            return self.trip.name
        if not self._l3:
            return 'OTHER'
        return self._l3


    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year

    def is_valid(self):
        return self.date >= datetime.date(2018, 6, 6)
