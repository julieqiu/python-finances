import argparse
from collections import deque
import csv
import datetime
from os import listdir
from os.path import isfile, join

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.models import DbTransaction, DbAccount
from finances.database.db_errors import UniqueViolation, split_integrity_error

from finances.app.ingest.constants import CSV_INGEST_INFO


def files_in_directory(csv_directory) -> list:
    return [
        (csv_directory + f)
        for f in listdir(csv_directory)
        if isfile(join(csv_directory, f)) and f != '.DS_Store'
    ]


def account_from_filename(filename, session) -> DbAccount:
    account_number = ''
    for bank in ['BankOfAmerica', 'Chase']:
        if bank not in filename:
            continue

        f = filename.split(bank)[1]
        while f[0].isnumeric():
            account_number += f[0]
            f = f[1:]
        account_number = int(account_number)
        break

    return session.query(DbAccount).filter_by(number=account_number).first()


def group_filenames_by_account(filenames) -> dict:
    account_to_filenames = {}
    with db_session() as session:
        for f in filenames:
            account = account_from_filename(f, session)
            if account_to_filenames.get(account.id):
                account_to_filenames[account.id].append(f)
            else:
                account_to_filenames[account.id] = [f]
    return account_to_filenames


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

def transaction_values_from_csv_row(csv_row: dict, csv_col_to_db_col: dict):
    transaction_values = dict()
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
            db_val = ' '.join([s for s in csv_val.split(' ') if s])
        transaction_values[db_col] = db_val

    return transaction_values


def is_valid_transaction_values(transaction_values: dict,
                                skip_if_missing: set,
                                optional_cols: set) -> bool:
    for db_col, db_val in transaction_values.items():
        if db_col in skip_if_missing and not db_val:
            return False
    return True


def csvfiles_to_transaction_values(filenames: list,
                                   last_transaction_date: datetime.date,
                                   csv_col_to_db_col: dict,
                                   skip_if_missing: set,
                                   optional_cols: set,
                                   account_id: int) -> list:
    if not filenames:
        return

    all_values = []
    seen = set()
    max_date = last_transaction_date

    count = 1
    # NOTE: Assuming this sorts files by date.
    for filename in sorted(filenames):
        values = transaction_values_for_file(
            filename,
            csv_col_to_db_col,
            skip_if_missing,
            optional_cols
        )

        for v in values:
            d = v.get('date')
            if not d:
                d = v.get('service_date')
                date_str = date_to_str(d)
            else:
                date_str = date_to_str(d)
            if d > max_date:
                if v.get('description'):
                    hash_key = v['description'] + date_str
                else:
                    hash_key = v['provider'] + date_str + v['status'] + v['billed']

                if hash_key in seen:
                    v['description'] = v['description'] + ' ' + str(count)
                    count += 1
                else:
                    seen.add(hash_key)

                v['account_id'] = account_id
                all_values.append(v)
            elif d == max_date:
                # TODO: Scan the end of all_values to see if we missed anything
                pass

        if not all_values:
            continue

        try:
            max_date = all_values[-1]['date']
        except Exception:
            max_date = all_values[-1]['service_date']

    return values


def transaction_values_for_file(filename: str,
                                csv_col_to_db_col: dict,
                                skip_if_missing: set,
                                optional_cols: set) -> list:

    values = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for csv_row in reader:
            transaction_values = transaction_values_from_csv_row(csv_row, csv_col_to_db_col)

            if not is_valid_transaction_values(
                transaction_values,
                skip_if_missing,
                optional_cols):
                continue

            values.append(transaction_values)

    return values


def write_transaction_values_to_db(transaction_values_list: list, db_model, filename):
    rows_to_write = []
    for transaction_values in transaction_values_list:
        try:
            # print(transaction_values['description'])
            with db_session() as session, split_integrity_error() as err:
                session.execute(
                    insert(db_model).values(transaction_values)
                )

        except UniqueViolation as err:
            print(err)
            print(transaction_values)
            rows_to_write.append(transaction_values)

    if not rows_to_write:
        return

    if type(filename) != str:
        import pdb; pdb.set_trace()

    tmp_file = 'tmp_{}'.format(filename.split('/')[-1])
    with open(tmp_file, 'w') as csv_writefile:
        writer = csv.DictWriter(csv_writefile, rows_to_write[0].keys())
        writer.writeheader()

        for tv in rows_to_write:
            writer.writerow(tv)
