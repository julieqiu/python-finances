import datetime

from finances.database.models import DbTransaction
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction
from finances.domain.models import Report


INT_TO_MONTH = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}


def monthly_reports(year=2018, only_month=None):
    def report_for_month(month: int) -> Report:
        start_date = datetime.date(year, month, 1)
        if month != 12:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        else:
            end_date= datetime.date(year, month, 31)

        report = Report(
            start_date=start_date,
            end_date=end_date,
            transactions=transactions,
        )
        return report.to_dict()

    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        transactions = [
            db_transaction_to_domain_transaction(t)
            for t in db_transactions
        ]

    monthly_reports = {}
    if only_month:
        monthly_reports[INT_TO_MONTH[only_month]] = report_for_month(only_month)
    else:
        for month in range(1, 13):
            monthly_reports[INT_TO_MONTH[month]] = report_for_month(month)
    return monthly_reports
