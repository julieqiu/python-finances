import datetime

from finances.database.models import DbTransaction
from finances.database import db_session
from finances.domain.constructors import db_transaction_to_domain_transaction
from finances.domain.models import MonthlyReport


def monthly_reports(year=2018, only_month=None):
    def report_for_month(month: int) -> MonthlyReport:
        start_date = datetime.date(year, month, 1)
        if month != 12:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        else:
            end_date= datetime.date(year, month, 31)

        return MonthlyReport(
            start_date=start_date,
            end_date=end_date,
            transactions=transactions,
        )

    with db_session() as session:
        db_transactions = session.query(DbTransaction).all()
        transactions = [
            db_transaction_to_domain_transaction(t)
            for t in db_transactions
        ]

    if only_month:
        return [report_for_month(only_month)]

    monthly_reports = []
    for month in range(12, 0, -1):
        report = report_for_month(month)
        if report and report.transactions:
            monthly_reports.append(report_for_month(month))

    return sorted(monthly_reports, key=lambda r: r.month, reverse=True)
