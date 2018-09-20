from finances.app.classify.constants import CLASSIFICATION_TO_PHRASES


class Transaction:

    def __init__(self,
                 date,
                 description,
                 amount,
                 account):
        self.date = date
        self.description = description
        self.amount = amount
        self.account = account

    def _classification_for_transaction(self):
        for l1, l1_dict in CLASSIFICATION_TO_PHRASES.items():
            for l2, l2_dict in l1_dict.items():
                for l3, phrases in l2_dict.items():
                    for phrase in phrases:
                        if phrase in self.description:
                            return (l1, l2, l3)
        return (None, None, None)

    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year

    @property
    def l1(self):
        return self._classification_for_transaction[0]

    @property
    def l2(self):
        return self._classification_for_transaction[1]

    @property
    def l3(self):
        return self._classification_for_transaction[2]
