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


