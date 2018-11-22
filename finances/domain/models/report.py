import abc
from collections import defaultdict


class Report:

    def __init__(self, start_date, end_date, transactions, year=2018):
        self.start_date = start_date
        self.end_date = end_date
        self._transactions = [t for t in transactions if t.year == year]

    def add_transaction(self, transaction):
        self._transactions.append(transaction)
        self._transactions.sort(key=lambda t: t.date, reverse=True)

    @abc.abstractmethod
    def name(self) -> str:
        return 'NOT IMPLEMENTED'

    @property
    def month(self) -> int:
        return self.start_date.month

    @property
    def year(self) -> int:
        return self.start_date.year

    @property
    def month_name(self) -> str:
        return {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December',
        }[self.month]
