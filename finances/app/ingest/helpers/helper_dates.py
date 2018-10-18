import argparse
from collections import deque
import csv
import datetime
from os import listdir
from os.path import isfile, join

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.models import DbTransaction
from finances.database.db_errors import UniqueViolation, split_integrity_error

from finances.app.ingest.constants import CSV_INGEST_INFO


def str_to_date(s: str) -> datetime.date:
    current_date = None
    for date_format in ['%m/%d/%Y', '%m/%d/%y', '%b. %d, %Y']:
        try:
            current_date = datetime.datetime.strptime(s, date_format).date()
            break
        except ValueError:
            continue

    if not current_date:
        raise Exception('Could not convert {} to datetime'.format(s))

    return current_date


def date_to_str(d: datetime.date) -> str:
    return d.strftime('%m-%d-%Y')
