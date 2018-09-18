from flask import Flask, render_template

from finances.database import db_session
from finances.models import Transaction

app = Flask(__name__)


CATEGORIES = [
    {
        'name': 'Lyft / Uber / Taxi / Via',
        'search_terms': ['lyft', 'uber', 'taxi'],
    },
    {
        'name': 'Paychecks',
        'search_terms': ['DIR DEP'],
    },
    {
        'name': 'Equinox',
        'search_terms': ['Equinox'],
    },
    {
        'name': 'Flights',
        'search_terms': ['JetBlue', 'Delta', 'United', 'Norwegian', 'Frontier'],
    },
]

def transactions_for_term(term: str):
    with db_session() as session:
        return session.query(Transaction).filter(
            Transaction.description.ilike('%{}%'.format(term))
        )


@app.route('/')
@app.route('/index')
def index():
    # with db_session() as session:
    #     for category in CATEGORIES:
    #         transactions = set()
    #         for term in category['search_terms']:
    #             transactions.update(transactions_for_term(term))
    #         category['transactions'] = list(transactions)[:5]

    #         total = 0
    #         for t in transactions:
    #             total += t.amount
    #         category['total'] = total * -1


    return render_template(
        'index.html',
        # categories=[category for category in CATEGORIES if len(category['transactions']) > 0],
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
        transactions = session.query(Transaction).all()

    return render_template(
        'transactions.html',
        transactions=transactions
    )


@app.route('/transactions/<string:term>')
def recipes_by_category(term: str):
    for category in CATEGORIES:
        if term != category['name']:
            continue

        transactions = set()
        for term in category['search_terms']:
            transactions.update(transactions_for_term(term))
            return render_template(
                'transactions.html',
                transactions=list(transactions),
            )

    transactions = transactions_for_term(term)
    return render_template(
        'transactions.html',
        transactions=list(transactions),
    )
