from collections import defaultdict


class ReportCategory:

    def __init__(self, name):
        self.name = name
        self.categories = defaultdict(dict)
        self.transactions = []
        self.total = 0


class Report:

    def __init__(self,
                start_date,
                end_date,
                transactions) -> None:

        self.start_date = start_date
        self.end_date = end_date
        self.transactions = [
            t for t in transactions
            if t.date >= self.start_date and
            t.date <= self.end_date
        ]

    @property
    def month(self) -> int:
        return self.start_date.month

    def to_dict(self) -> dict:
        if len(self.categorized_transactions.keys()) > 4:
            raise Exception('Unexpected keys in report: {}'.format(self.categorized_transactions.keys()))

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

    @property
    def categorized_transactions(self) -> {}:
        categorized_transactions = defaultdict(dict)
        for t in self.transactions:
            if not categorized_transactions.get(t.l1):
                categorized_transactions[t.l1] = ReportCategory(name=t.l1)

            if not categorized_transactions[t.l1].categories.get(t.l2):
                categorized_transactions[t.l1].categories[t.l2] = ReportCategory(name=t.l2)

            if not categorized_transactions[t.l1].categories[t.l2].categories.get(t.l3):
                categorized_transactions[t.l1].categories[t.l2].categories[t.l3] = ReportCategory(name=t.l3)

            categorized_transactions[t.l1].total += t.amount
            categorized_transactions[t.l1].categories[t.l2].total += t.amount
            categorized_transactions[t.l1].categories[t.l2].categories[t.l3].total += t.amount
            categorized_transactions[t.l1].categories[t.l2].categories[t.l3].transactions.append(t)
        return categorized_transactions

    def total_for(self, l1: str) -> float:
        if not self.categorized_transactions.get(l1):
            return 0
        return self.categorized_transactions[l1].total

    @property
    def total_earned(self):
        return self.total_for('INCOME')

    @property
    def total_spent(self):
        return self.total_fixed  + self.total_variable

    @property
    def total_fixed(self):
        return self.total_for('MONTHLY')

    @property
    def total_variable(self):
        return self.total_for('EXPENSES')

    @property
    def total_saved(self):
        return self.total_earned + self.total_spent
