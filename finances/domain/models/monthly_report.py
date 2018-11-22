from collections import defaultdict

from finances.domain.models.report import Report


class MonthlyReportNode:

    def __init__(self, name):
        self.name = name
        self.children = defaultdict(dict)
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
            if t.month == self.month and t.is_valid()
        ], key=lambda t: t.date, reverse=True)

    @property
    def data(self):
        """
        ~~~ Structure of Dictionary ~~~

        "Income": MonthlyReportNode(Income)
            name: Income
            total: xx
            children:
                "Income":
                    name: Income
                    total: xx
                    children:
                        "Income":
                            name: Income
                            total: xx
                            children:
                            transactions:
        Skipped:
            Skipped:
                Skipped;
                    list
        Subscriptions:
            Monthly:
                Monthly
                    list
            Annual
                Annual
                    list
        "Expenses":
            Food:
                total
                Groceries:
                    total
                    list
                Eating Out:
                    total
                    list
        """
        return self.categorized_transactions

    @property
    def categorized_transactions(self) -> dict:
        categorized_transactions = defaultdict(dict)
        for t in self.transactions:
            if not categorized_transactions.get(t.l1):
                categorized_transactions[t.l1] = MonthlyReportNode(name=t.l1)

            if not categorized_transactions[t.l1].children.get(t.l2):
                categorized_transactions[t.l1].children[t.l2] = MonthlyReportNode(name=t.l2)

            if not categorized_transactions[t.l1].children[t.l2].children.get(t.l3):
                categorized_transactions[t.l1].children[t.l2].children[t.l3] = MonthlyReportNode(name=t.l3)

            categorized_transactions[t.l1].total += t.amount
            categorized_transactions[t.l1].children[t.l2].total += t.amount
            categorized_transactions[t.l1].children[t.l2].children[t.l3].total += t.amount
            categorized_transactions[t.l1].children[t.l2].children[t.l3].transactions.append(t)
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
        return self.total_for('SUBSCRIPTIONS')

    @property
    def total_variable(self):
        return self.total_for('EXPENSES')

    @property
    def total_saved(self):
        return self.total_earned + self.total_spent
