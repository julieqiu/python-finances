from collections import defaultdict


class Account:

    def __init__(self,
                id,
                name: str,
                account_type: str,
                bank: str,
                number: int,
                routing: int,
                starting_balance: int=0,
                transactions: list=[],
                ):

        self.id= id
        self.name = name
        self.type = account_type
        self.bank = bank
        self.number = number
        self.routing = routing
        self.starting_balance = starting_balance
        self._transactions = [t for t in transactions if t.account_id == self.account_id]

    @property
    def balance(self):
        total = self.starting_balance
        for t in self.transactions:
            total += t.amount
        return total

    @property
    def transactions(self):
        return sorted([
            t for t in self._transactions
            if t.account_id == self.id
        ], key=lambda t: t.date, reverse=True)

    def add_transactions(self, transactions: list):
        for t in transactions:
            if t.account_id == self.id:
                self._transactions.append(t)

