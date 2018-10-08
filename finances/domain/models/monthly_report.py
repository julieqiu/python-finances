from collections import defaultdict

from finances.domain.models.report import Report


class MonthlyReportCategory:

    def __init__(self, name):
        self.name = name
        self.categories = defaultdict(dict)
        self.transactions = []
        self.total = 0


class MonthlyReport(Report):

    @property
    def name(self) -> str:
        return self.month_name

    @property
    def transactions(self) -> list:
        return sorted([
            t for t in self._transactions
            if t.month == self.month
        ], key=lambda t: t.date, reverse=True)

    @property
    def reports(self):
        return [
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

    @property
    def categorized_transactions(self) -> {}:
        categorized_transactions = defaultdict(dict)
        for t in self.transactions:
            if not categorized_transactions.get(t.l1):
                categorized_transactions[t.l1] = MonthlyReportCategory(name=t.l1)

            if not categorized_transactions[t.l1].categories.get(t.l2):
                categorized_transactions[t.l1].categories[t.l2] = MonthlyReportCategory(name=t.l2)

            if not categorized_transactions[t.l1].categories[t.l2].categories.get(t.l3):
                categorized_transactions[t.l1].categories[t.l2].categories[t.l3] = MonthlyReportCategory(name=t.l3)

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
