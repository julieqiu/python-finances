import argparse
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

COUNT = 1


def last_transaction_for_account(account, session) -> datetime.datetime:
    return session.query(
        DbTransaction.id
    ).filter_by(
        account_id=account.id
    ).order_by(
        DbTransaction.date.desc()
    )


def transaction_values_from_csv_row(csv_row: dict, csv_col_to_db_col: dict):
    transaction_values = dict()
    for csv_col, csv_val in csv_row.items():
        if csv_col:
            db_col = csv_col_to_db_col.get(csv_col.upper())

        if not db_col:
            continue

        # Removes unnescessary whitespace in db_val
        if db_col == 'service_date':
            db_val = datetime.datetime.strptime(csv_val, '%b. %d, %Y')
        elif csv_val and csv_val[0] == '$':
            db_val = csv_val[1:]
        elif csv_val == 'Does Not Apply':
            db_val = None
        else:
            try:
                db_val = ' '.join([s for s in csv_val.split(' ') if s])
            except Exception:
                import pdb; pdb.set_trace()
        transaction_values[db_col] = db_val

    return transaction_values


def is_valid_transaction_values(transaction_values: dict,
                                skip_if_missing: set,
                                optional_cols: set,
                                last_transaction: DbTransaction) -> bool:
    for db_col, db_val in transaction_values.items():
        if db_col in skip_if_missing and not db_val:
            return False

        try:
            print(transaction_values[db_col])
        except KeyError:
            if col_name in optional_cols:
                continue
            else:
                raise Exception(
                    'Expected {}: {}'.format(
                        col_name, csv_row
                    )
                )

    current_date = transaction_values['date']
    for date_format in ['%m/%d/%Y', '%m/%d/%y']:
        try:
            current_date = datetime.datetime.strptime(
                transaction_values['date'], date_format
            ).date()
        except ValueError:
            continue

    # Skipping any rows that occured before the last transaction in the db
    # TODO: Account fo transactions that occured on the same day
    # after the CSV was downloaded
    return current_date > last_transaction.date


def write_to_db(transaction_values: dict, db_model) -> None:
    with db_session() as session, split_integrity_error() as err:
        session.execute(
            insert(db_model).values(transaction_values)
        )


def csv_to_transactions(filename: str,
                        last_transaction: DbTransaction,
                        account_id: int,
                        db_model: str,
                        csv_col_to_db_col: dict,
                        skip_if_missing: set,
                        optional_cols: set) -> None:

    values = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for csv_row in reader:
            transaction_values = transaction_values_from_csv_row(csv_row, csv_col_to_db_col)
            if not is_valid_transaction_values(
                transaction_values,
                skip_if_missing,
                optional_cols,
                last_transaction):
                continue

            values.append(transaction_values)

    return values


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'csv_category',
        type=str,
        choices=[
            'TRANSACTIONS',
            'INSURANCE_CLAIMS',
        ],
    )
    return parser


def files_in_directory(csv_directory) -> list:
    return [
        (mypath + f)
        for f in listdir(mypath)
        if isfile(join(mypath, f)) and f != '.DS_Store'
    ]


def account_from_filename(filename, session) -> DbAccount:
    for bank in ['BankOfAmerica', 'Chase']:
        if bank in filename:
            f = filename.split(bank[1])
            account_number = ''
            while f[0].isnumeric():
                acount_number += f[0]
                f = f[1:]
        if account_number:
            account_number = int(account_number)
            return session.query(DbAccount).filter_by(number=account_number).first()
        return session.query(DbAccount).filter_by(
            number=account_number
        ).first()



def write_transaction_values_to_db(transaction_values_list: list, db_model):
    for transaction_values in transaction_values_list:
        try:
            write_to_db(transaction_values, db_model)

        except UniqueViolation as err:
            print(err)
            print(transaction_values)
            rows_to_write.append(csv_row)

        if not rows_to_write:
            return

        with open('tmp_{}'.format(filename.split('/')[-1]), 'w') as csv_writefile:
            writer = csv.DictWriter(csv_writefile, reader.fieldnames)
            writer.writeheader()

            for row in rows_to_write:
                try:
                    writer.writerow(csv_row)
                except Exception:
                    print(csv_row)
                    import pdb; pdb.set_trace()


def ingest_expenses(csv_category):
    csv_ingest_info = CSV_INGEST_INFO[csv_category]
    filenames = files_in_directory(csv_ingest_info['CSV_DIRECTORY'])

    for f in filenames:
        print(
        """


        """
        )
        print(f)
        print(
        """


        """
        )

        account = account_from_filename(f)
        last_transaction = last_transaction_for_account(account)
        transaction_values = csv_to_transactions(
            filename=f,
            last_transaction=last_transaction,
            account_id=account.id,
            db_model=csv_ingest_info['DB_MODEL'],
            csv_col_to_db_col=csv_ingest_info['CSV_COL_TO_DB_COL'],
            skip_if_missing=csv_ingest_info['SKIP_IF_MISSING'],
            optional_cols=csv_ingest_info['OPTIONAL_COLS'],
        )

        write_transaction_values_to_db(transaction_values, db_model)

if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()
    main(args.csv_category)
