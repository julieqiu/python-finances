from collections import defaultdict


class Trip:

    def __init__(self, name, start_date, end_date, transactions):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.transactions = transactions
