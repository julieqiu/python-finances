class Food:

    def __init__(self):
        self.groceries = 0
        self.coffee = 0
        self.alcohol = 0


class Income:

    def __init__(self):
        self.income = 0
        self.reimbursed = 0
        self.bonus = 0


class MonthlyInfo:

    def __init__(self):
        self.food = Food()
        self.income = Income()

