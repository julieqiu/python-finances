import datetime

from flask import Flask, render_template

from finances.database import db_session
from finances.models import Transaction
from finances.app.classify.constants import CATEGORY_TO_PHRASES

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
    with db_session() as session:
        # TODO: Generate numbers
        cash = 86124.17
        credit = 4895.157
        investments = 127445.59
        spent_in_last_10_days = 0
        monthly_income = 5266.00
        monthly_spent = 2527.26
        monthly_saved = 2527.26

        for category in CATEGORIES:
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



@app.route('/monthly')
def monthly():
    def contains_any(description, lst):
        for item in lst:
            if item.lower() in description.lower():
                return True
        return False

    def init_dict_for_month(month, monthly_info):
        month_start = datetime.date(2018, month, 1)
        month_end = datetime.date(2018, month + 1, 1) - datetime.timedelta(days=1)
        monthly_info[month_start.month] = {}

        monthly_info[month]['total'] = 0

        for keyword, _ in CATEGORY_TO_PHRASES.items():
            monthly_info[month][keyword] = {}
            monthly_info[month][keyword]['total'] = 0
            monthly_info[month][keyword]['expenses'] = []

        monthly_info[month]['other'] = {}
        monthly_info[month]['other']['total'] = 0
        monthly_info[month]['other']['expenses'] = []

        return monthly_info

    monthly_info = {}
    with db_session() as session:
        transactions = session.query(Transaction).all()

        for month in range(1, 12):
            monthly_info = init_dict_for_month(month, monthly_info)

            for t in transactions:
                if contains_any(t.description, CATEGORY_TO_PHRASES['skipped']):
                    continue

                if t.date.month == month and t.date.year == 2018:
                    found = False
                    for keyword, phrases in CATEGORY_TO_PHRASES.items():
                        if contains_any(t.description, phrases):
                            monthly_info[month][keyword]['total'] += t.amount
                            monthly_info[month][keyword]['expenses'].append((t.amount, t.description, t.date))
                            found = True
                            break

                    if not found:
                        monthly_info[month]['other']['total'] += t.amount
                        monthly_info[month]['other']['expenses'].append((t.amount, t.description, t.date))

                    monthly_info[month]['total'] += t.amount

    for month, monthly_dict in monthly_info.items():
        monthly_info[month]['categories'] = []
        for keyword, keyword_dict in monthly_dict.items():
            if keyword in ['categories', 'expenses', 'total']:
                continue
            if keyword_dict['total'] != 0:
                monthly_info[month]['categories'].append((keyword_dict['total'], keyword, keyword_dict['expenses']))

        monthly_info[month]['categories'].sort(reverse=True)


    return render_template(
        'monthly.html',
        monthly=monthly_info
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
def transactions_by_term(term: str):
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