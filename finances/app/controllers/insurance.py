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


def insurance_claims(year=2018, only_month=None):
