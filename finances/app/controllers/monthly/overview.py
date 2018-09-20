from finances.app.classify.constants import CATEGORY_TO_PHRASES
from finances.database.models import DbTransaction
from finances.domain.models import Transaction, Report




def monthly_info():
    monthly_info = init_monthly_info_dict()

    with db_session() as session:
        transactions = session.query(Transaction).all()
        for t in transactions:
            for category, _ in CATEGORY_TO_PHRASES.items():
                if is_transaction_for_category(category, t):
                    monthly_info[t.date.month][category]

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


def is_transaction_for_category(category, transaction) -> bool:
    for category_to_phrases_dict in CATEGORY_TO_PHRASES[category]:
        for _, phrases in category_to_phrases_dict.items():
            for phrase in phrases:
                if phrase in t.description:
                    return True
    return False
