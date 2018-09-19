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

def monthly_info_dict():
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

    expenses = {}
    income = {}
    for month, monthly_dict in monthly_info.items():
        income[month] = {}
        expenses[month] = {}
        income[month]['categories'] = []
        expenses[month]['categories'] = []
        for keyword, keyword_dict in monthly_dict.items():
            if keyword in ['income', 'reimbursed']:
                income[month]['categories'].append((keyword_dict['total'], keyword, keyword_dict['expenses']))
            else:
                expenses[month]['categories'].append((keyword_dict['total'], keyword, keyword_dict['expenses']))



    return render_template(
        'monthly.html',
        monthly=monthly_info,
        income=income,
        expenses=expenses,
    )
