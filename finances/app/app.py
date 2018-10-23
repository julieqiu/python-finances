import datetime

from flask import Flask, render_template, request

from finances.app.controllers.monthly import monthly_reports
from finances.app.controllers.travel import travel_reports
from finances.app.controllers.transactions import (
    all_transactions,
    all_trip_transactions,
    transactions_for_term,
    transaction_classifications,
    trip_id_and_names,
    trip_transaction_category_names,
    update_table_values,
)
from finances.database import db_session

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

@app.route('/travel')
def travel():
    trs = []
    if 'funemployment2018' in request.query_string.decode():
        for trip_id in sorted([5, 6, 7, 8, 9, 10, 11], reverse=True):
            trs = trs + travel_reports(trip_id=trip_id)
    elif 'conferences2018' in request.query_string.decode():
        for trip_id in sorted([1, 2, 4], reverse=True):
            trs = trs + travel_reports(trip_id=trip_id)
    elif request.args.get('id'):
        trip_id = request.args.get('id')
        trs = travel_reports(trip_id=trip_id)
    else:
        trs = travel_reports()

    return render_template(
        'travel.html',
        travel_reports=trs
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


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method != 'GET':
        for key, value in request.form.items():
            if value:
                db_table = key.split('-')[0]
                db_col = key.split('-')[1]
                db_val = key.split('-')[2]
                if len(key.split('-')) == 4:
                    # for description_edited
                    db_col2 = key.split('-')[3]
                    db_val2 = value
                elif len(value.split('-')) == 2:
                    db_col2 = value.split('-')[0]
                    db_val2 = value.split('-')[1]

                import pdb; pdb.set_trace()
                update_table_values(
                    db_table,
                    update_values=(db_col2, db_val2),
                    where_values=(db_col, db_val),
                )

    if 'trips' in request.args.keys():
        trip_id = request.args.get('id')
        if trip_id and trip_id.isnumeric():
            trip_id = int(trip_id)

        category = request.args.get('category')
        transactions = all_trip_transactions(trip_id, category)

    elif 'term' in request.args.keys():
        term = request.args.get('term')
        transactions = transactions_for_term(term)

    else:
        l1 = request.args.get('l1')
        l2 = request.args.get('l2')
        l3 = request.args.get('l3')
        transactions = all_transactions(l1, l2, l3)

    return render_template(
        'transactions.html',
        url=request.url,
        transactions=transactions,
        trip_categories=trip_transaction_category_names(),
        trip_id_and_names=trip_id_and_names(),
        transaction_classifications=transaction_classifications(),
    )
