from enum import Enum


class AccountType(Enum):
    CHECKINGS = 'checkings'
    SAVINGS = 'savings'
    CREDIT_CARD = 'credit-card'
    INSURANCE = 'insurance'
    PAYPAL = 'paypal'
