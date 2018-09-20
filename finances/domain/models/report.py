class Report:

    def __init__(self
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

    @property
    def transactions_by_classification(self) -> {}:
        classified_transactions = {}
        for t in self.transactions:
            if classified_transactions.get(t.l1) is None:
                classified_transactions[t.l1]['TOTAL'] = 0

            if classified_transactions[t.l1].get(t.l2) is None:
                classified_transactions[t.l1][t.l2] = {}
                classified_transactions[t.l1][t.l2]['TOTAL'] = 0

            if classified_transactions[t.l1][t.l2].get(t.l3) is not None:
                classified_transactions[t.l1][t.l2][t.l3] = {}
                classified_transactions[t.l1][t.l2][t.l3]['TRANSACTIONS'] = []
                classified_transactions[t.l1][t.l2][t.l3]['TOTAL'] = 0

            classified_transactions[t.l1][t.l2][t.l3]['TRANSACTIONS'].append(t)

            classified_transactions[t.l1]['TOTAL'] += t
            classified_transactions[t.l1][t.l2]['TOTAL'] += t
            classified_transactions[t.l1][t.l2][t.l3]['TOTAL'] += t

        return classified_transactions

    @property
    def total_earned(self):
        return self.transactions_by_classification['income']['TOTAL']

    @property
    def total_spent(self):
        total = 0
        for l1, value in self.transactions_by_classification.items():
            if l1 != 'income':
                total += self.transactions_by_classification[l1]['TOTAL']
        return total

    @property
    def total_save(self):
        return self.total_earned - self.total_saved
