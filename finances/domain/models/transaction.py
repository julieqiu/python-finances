from finances.app.classify.constants import CLASSIFICATION_TO_PHRASES


class Transaction:

    def __init__(self,
                 id,
                 date,
                 description,
                 amount,
                 account,
                 trip,
                 trip_category):

        self.id = id
        self.date = date
        self.description = description
        self.amount = amount
        self.account = account
        self.trip = trip
        self.trip_category = trip_category.name if trip_category else None

    @property
    def _classification(self):
        for l1, l1_dict in CLASSIFICATION_TO_PHRASES.items():
            for l2, l2_dict in l1_dict.items():
                for l3, phrases in l2_dict.items():
                    for phrase in phrases:
                        if phrase.lower() in self.description.lower():
                            return (l1, l2, l3)
        return ('EXPENSES', 'Other', 'Other')

    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year

    @property
    def l1(self):
        return self._classification[0]

    @property
    def l2(self):
        return self._classification[1]

    @property
    def l3(self):
        return self._classification[2]
