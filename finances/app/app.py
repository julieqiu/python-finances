import datetime

from flask import Flask, render_template

from finances.database import db_session
from finances.database.models import DbTransaction
from finances.app.controllers.monthly import monthly_reports

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    now = datetime.datetime.now()
    return render_template(
        'monthly.html',
        monthly_reports=monthly_reports(only_month=now.month)
    )


@app.route('/monthly')
def monthly():
    return render_template(
        'monthly.html',
        monthly_reports=monthly_reports()
    )

@app.route('/insurance')
def insurance():
    return render_template(
        'insurance.html',
        insurance_claims=insurance_claims()
    )

@app.route('/tmp')
def tmp():
    with db_session() as session:
        # TODO: Generate numbers
        cash = 86124.17
        credit = 4895.157
        investments = 127445.59
        spent_in_last_10_days = 0
        monthly_income = 5266.00
        monthly_spent = 2527.26
        monthly_saved = 2527.26

        for category in {}:
            transactions = set()
            for term in category['search_terms']:
                transactions.update(transactions_for_term(term))
            category['transactions'] = list(transactions)[:5]

            total = 0
            for t in transactions:
                total += t.amount
            category['total'] = total * -1


    return render_template(
        'index.html',
        cash=cash,
        credit=credit,
        investments=investments,
        spent_in_last_10_days=spent_in_last_10_days,
        monthly_income=monthly_income,
        monthly_spent=monthly_spent,
        monthly_saved=monthly_saved,
        # categories=[category for category in CATEGORIES if len(category['transactions']) > 0],
    )

def transactions_for_term(term: str):
    with db_session() as session:
        return session.query(DbTransaction).filter(
            DbTransaction.description.ilike('%{}%'.format(term))
        )


@app.route('/banks')
def banks():
    banks = [
        {
            'name': 'Bank of America',
            'account': '1234',
            'routing': '1234',

        },
        {
            'name': 'Chase',
            'account': '5678',
            'routing': '5678',

        },
    ]
    return render_template(
        'banks.html',
        banks=banks
    )





@app.route('/transactions')
def transactions():
    with db_session() as session:
        transactions = session.query(DbTransaction).all()

    return render_template(
        'transactions.html',
        transactions=transactions
    )
