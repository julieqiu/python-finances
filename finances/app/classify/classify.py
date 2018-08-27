import csv
from os import listdir
from os.path import isfile, join

from sqlalchemy.dialects.postgresql import insert

from finances.models import Transaction, Account
from finances.database import db_session

KEYWORD_TO_CATEGORY = {
    '35339 SPRING': 'INCOME',
    'ATM CHECK DEPOSIT': 'DEPOSIT',
    'ATM WITHDRAWAL': 'ATM WITHDRAWAL',
    'BKOFAMERICA': 'DEPOSIT',
    'CHASE CREDIT CRD': 'CREDIT CARD PAYMENT',
    'CHASE DES:EPAY': 'DEPOSIT',
    'CHECK': 'CHECK',
    'EQUINOX': 'EQUINOX',
    'EXPENSIFY': 'REIMBURSEMENT',
    'INTEREST PAYMENT': 'INTEREST',
    'INTEREST': 'INTEREST',
    'LYFT': 'LYFT',
    'MTA': 'MTA',
    'PAYMENT TO CHASE CARD': 'CREDIT CARD PAYMENT',
    'PAYPAL': 'PAYPAL',
    'RECOVERY PHYSICAL THERAPY': 'PHYSICAL THERAPY',
    'REMOTE ONLINE DEPOSIT': 'REIMBURSEMENT',
    'SHOPSPRING': 'INCOME',
    'SPRING NYC DIR DEP': 'INCOME',
    'SQ *': 'FOOD',
    'STUYVESANT': 'RENT',
    'TAXI': 'TAXI',
    'TRANSFER': 'DEPOSIT',
    'TST*': 'FOOD',
    'UBER': 'UBER',
    'VENMO': 'VENMO',
    'WEIGHTWATCHERS.COM': 'WEIGHTWATCHERS',
    'WITHDRAW': 'ATM WITHDRAWAL',
    'METRO-NORTH': 'METRO-NORTH',
    'DELI': 'DELI',
    'ZOLA': 'WEDDING',
    'SWEETGREEN': 'FOOD',
    'JELLO LABS': 'INCOME',
    'MCDONALD': 'FOOD',
    'DUMPLING': 'FOOD',
    'WALGREENS': 'SHOPPING',
    'AMAZON': 'SHOPPING',
    'NAILS': 'NAILS',
    'SUSHI': 'FOOD',
    'BURGER': 'FOOD',
    'PIZZA': 'FOOD',
    'EAT': 'FOOD',
    'TACO': 'FOOD',
    'FOOD': 'FOOD',
    'CAVA': 'FOOD',
    'CAFE': 'FOOD',
    'AUDIBLE': 'AUDIBLE',
    'YELP': 'FOOD',
}

def classify_trans(description: str) -> str:
    for keyword, category in KEYWORD_TO_CATEGORY.items():
        if keyword in description.upper():
            return category

    return None


def classify_transactions():
    x = set()
    with db_session() as session:
        transactions = session.query(Transaction).all()
        for t in transactions:
            if not classify_trans(t.description):
                x.add(t.description)

    stuff = list(x)
    for item in sorted(stuff):
        print(item)



if __name__ == '__main__':
    classify_transactions()
