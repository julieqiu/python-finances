import datetime

from flask import Flask, render_template, request

from finances.app.controllers.annual import annual_report
from finances.app.controllers.monthly import monthly_reports
from finances.app.controllers.travel import travel_reports
from finances.app.controllers.accounts import all_accounts
from finances.app.controllers.insurance import (
    insurance_report,
)

from finances.app.controllers.transactions import (
    transaction_classifications,
    trip_id_and_names,
    trip_transaction_category_names,
    transactions,
)
from finances.database import db_session

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        bank_to_accounts=all_accounts()
    )

@app.route('/accounts/<account_id>')
def accounts(account_id):
    return render_template(
        'index.html',
        bank_to_accounts=all_accounts(account_id)
    )

@app.route('/monthly')
def monthly():
    return render_template(
        'monthly.html',
        monthly_reports=monthly_reports()
    )

@app.route('/annual')
def annual():
    return render_template(
        'annual.html',
        annual_report=annual_report()
    )

@app.route('/travel')
def travel():
    return render_template(
        'travel.html',
        travel_reports=travel_reports(request)
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

@app.route('/insurance')
def insurance():
    if 'provider' in request.args.keys():
        provider = request.args.get('provider')
        report = insurance_report(provider=provider)
    else:
        report = insurance_report()

    return render_template(
        'insurance.html',
        insurance_report=report
    )


@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    return render_template(
        'transactions.html',
        url=request.url,
        transactions=transactions(request),
        trip_categories=trip_transaction_category_names(),
        trip_id_and_names=trip_id_and_names(),
        transaction_classifications=transaction_classifications(),
    )
