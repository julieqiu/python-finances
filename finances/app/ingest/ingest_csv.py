import argparse
import csv
import datetime
from os import listdir
from os.path import isfile, join

from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.app.ingest.constants import CSV_INGEST_INFO


def csv_to_transactions(filename: str,
                        db_model: str,
                        csv_col_to_db_col: dict,
                        skip_if_missing: set,
                        optional_cols: set):

    def create_transaction_values(csv_row: dict):
        transaction_values = dict()
        for csv_col, csv_val in csv_row.items():
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
                db_val = ' '.join([s for s in csv_val.split(' ') if s])
            transaction_values[db_col] = db_val
        return transaction_values


    def is_valid_transaction_values(transaction_values: dict,
                                    skip_if_missing: set,
                                    optional_cols: set) -> bool:
        for db_col, db_val in transaction_values.items():
            if db_col in skip_if_missing and db_val is None:
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
        return True

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for csv_row in reader:
            transaction_values = create_transaction_values(csv_row)

            if not is_valid_transaction_values(
                transaction_values,
                skip_if_missing,
                optional_cols):
                continue

            with db_session() as session:
                try:
                    session.execute(
                        insert(db_model).values(transaction_values)
                    )
                except Exception as err:
                    print(err)
                    print(transaction_values)
                    raise Exception



def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'csv_category',
        type=str,
        choices=[
            'EXPENSES',
            'INSURANCE_CLAIMS',
        ],
    )
    return parser


if __name__ == '__main__':
    parser = argument_parser()
    args = parser.parse_args()
    csv_ingest_info = CSV_INGEST_INFO[args.csv_category]

    mypath = csv_ingest_info['CSV_DIRECTORY']
    for f in listdir(mypath):
        if isfile(join(mypath, f)):
            print(
            """


            """
            )
            print(mypath + f)
            print(
            """


            """
            )
            csv_to_transactions(
                filename=(mypath + f),
                db_model=csv_ingest_info['DB_MODEL'],
                csv_col_to_db_col=csv_ingest_info['CSV_COL_TO_DB_COL'],
                skip_if_missing=csv_ingest_info['SKIP_IF_MISSING'],
                optional_cols=csv_ingest_info['OPTIONAL_COLS'],
            )
