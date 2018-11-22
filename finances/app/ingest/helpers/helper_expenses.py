import argparse
from collections import deque
import decimal
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
from finances.app.ingest.helpers.helper_dates import str_to_date, date_to_str


def _hash_key_for_db_row(db_values: dict):
    d = db_values.get('date')
    if not d:
        d = db_values.get('service_date')

    date_str = date_to_str(d)

    if db_values.get('description'):
        try:
            x = db_values['amount']
            amount = str(float(decimal.Decimal(x)))
        except Exception:
            x = float(db_values['amount'].replace(',' , ''))
            amount = str(float(decimal.Decimal(x)))

        return db_values['description'] + date_str + amount

    return db_values['provider'] + date_str + db_values['status'] + db_values['billed']


def last_transaction_date_for_account(account_id, session) -> datetime.datetime:
    max_date = datetime.datetime.min.date()
    with db_session() as session:
        last_transaction = session.query(
            DbTransaction
        ).filter_by(
            account_id=account_id
        ).order_by(
            DbTransaction.date.desc()
        ).first()

    if last_transaction:
        max_date = last_transaction.date
    return max_date


def _db_row_values_from_csv_row(csv_row: dict, csv_col_to_db_col: dict):
    db_row_values = dict()
    for csv_col, csv_val in csv_row.items():
        if csv_col:
            db_col = csv_col_to_db_col.get(csv_col.upper())

        if not db_col:
            continue

        # Removes unnescessary whitespace in db_val
        if csv_val and csv_val[0] == '$':
            db_val = csv_val[1:]
        elif csv_val == 'Does Not Apply':
            db_val = None
        elif db_col == 'date' or db_col == 'service_date':
            db_val = str_to_date(csv_val)
        else:
            try:
                db_val = ' '.join([s for s in csv_val.split(' ') if s])
            except Exception:
                print(csv_row)
                import pdb; pdb.set_trace()
        db_row_values[db_col] = db_val

    return db_row_values


def is_valid_db_row_values(db_row_values: dict,
                                skip_if_missing: set,
                                optional_cols: set) -> bool:
    for db_col, db_val in db_row_values.items():
        if db_col in skip_if_missing and not db_val:
            return False
    return True


def edit_duplicates(db_row_values_list: list) -> list:
    seen = set()
    for rv in db_row_values_list:
        hash_key = _hash_key_for_db_row(rv)
        while hash_key in seen:
            if rv.get('description'):
                rv['description'] = rv['description'] + ' *'
            else:
                rv['status'] = rv['status'] + ' *'
            hash_key = _hash_key_for_db_row(rv)
        seen.add(hash_key)
    return db_row_values_list


def _db_row_values_for_file(filename: str,
                                csv_col_to_db_col: dict,
                                skip_if_missing: set,
                                optional_cols: set,
                                account_id: int) -> list:
    values = []
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for csv_row in reader:
            # if 'PayPal' in filename:
            #   import pdb; pdb.set_trace()

            db_row_values = _db_row_values_from_csv_row(csv_row, csv_col_to_db_col)

            if not is_valid_db_row_values(
                db_row_values,
                skip_if_missing,
                optional_cols):
                continue

            db_row_values['account_id'] = account_id
            if db_row_values.get('amount'):
                if ',' in db_row_values['amount']:
                    db_row_values['amount'] = float(db_row_values['amount'].replace(',' , ''))

            values.append(db_row_values)

    return values


def csvfiles_to_db_row_values(filenames: list,
                              csv_col_to_db_col: dict,
                              skip_if_missing: set,
                              optional_cols: set,
                              account_id: int) -> list:
    if not filenames:
        return

    # 1) Get all rows currently in DB and hash
    with db_session() as session:
        existing_transactions = {
            _hash_key_for_db_row(t.__dict__)
            for t in session.query(DbTransaction).all()
        }

    # 2) Hash all CSV rows + mark "duplicates" we want to keep; add to seen
    db_row_values_from_csvfiles = dict()

    for filename in sorted(filenames):  # NOTE: Assuming this sorts files by date.
        db_row_values = _db_row_values_for_file(
            filename,
            csv_col_to_db_col,
            skip_if_missing,
            optional_cols,
            account_id,
        )
        db_row_values = edit_duplicates(db_row_values)
        for rv in db_row_values:
            hash_key = _hash_key_for_db_row(rv)
            db_row_values_from_csvfiles[hash_key] = rv

    # 3) Write new CSV rows to DB
    values_to_write = []
    for hash_key, db_row_value in db_row_values_from_csvfiles.items():
        if hash_key not in existing_transactions:
            values_to_write.append(db_row_value)

    if not values_to_write:
        return values_to_write

    sort_key = 'date'
    if not values_to_write[0].get('date'):
        sort_key = 'service_date'

    return sorted(values_to_write, key=lambda v: v[sort_key])


def write_values_to_db(db_row_value: dict, db_model):
    with db_session() as session, split_integrity_error() as err:
        session.execute(
            insert(db_model).values(db_row_value)
        )
