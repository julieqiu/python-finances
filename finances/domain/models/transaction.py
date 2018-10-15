from finances.app.classify.constants import CLASSIFICATION_TO_PHRASES


class Transaction:

    def __init__(self,
                 id,
                 date,
                 description,
                 amount,
                 account,
                 trip,
                 trip_category,
                 l1,
                 l2,
                 l3):

        self.id = id
        self.date = date
        self.description = description
        self.amount = amount
        self.account = account
        self.trip = trip
        self.trip_category = trip_category.name if trip_category else None
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year
