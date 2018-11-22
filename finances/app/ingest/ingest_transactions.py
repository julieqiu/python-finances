import argparse
from collections import deque
import csv
import datetime
from os import listdir
from os.path import isfile, join

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.models import DbTransaction, DbAccount, DbTransactionClassification
from finances.database.db_errors import UniqueViolation, split_integrity_error

from finances.app.ingest.constants import CSV_INGEST_INFO
from finances.app.ingest.helpers.helper_filenames import (
    files_in_directory,
    group_filenames_by_account,
)
from finances.app.ingest.helpers.helper_expenses import (
    csvfiles_to_db_row_values,
    write_values_to_db,
)

TRANSACTIONS_CSV_INGEST_INFO = CSV_INGEST_INFO['TRANSACTIONS']


def classify_transaction(transaction_values: dict, transaction_classifications: list):
    if 'VENMO PAYMENT' in transaction_values['description'].upper() and transaction_values['amount'] >= 175:
        transaction_values['classification_id'] = tc.id

    for tc in transaction_classifications:
        for phrase in tc.phrases:
            if phrase.lower() in transaction_values['description'].lower():
                transaction_values['classification_id'] = tc.id
                return transaction_values
    return transaction_values


def ingest_transactions():
    # 1) Get all filepaths containing transactions
    filenames = files_in_directory(TRANSACTIONS_CSV_INGEST_INFO['CSV_DIRECTORY'])
    account_to_filenames = group_filenames_by_account(filenames)

    with db_session() as session:
        transaction_classifications = session.query(DbTransactionClassification).all()

    # 3) Process files
    for account_id, filenames in account_to_filenames.items():
        print(
        """

        """
        )
        print(filenames)
        print(
        """


        """
        )

        transaction_values = csvfiles_to_db_row_values(
            filenames=filenames,
            csv_col_to_db_col=TRANSACTIONS_CSV_INGEST_INFO['CSV_COL_TO_DB_COL'],
            skip_if_missing=TRANSACTIONS_CSV_INGEST_INFO['SKIP_IF_MISSING'],
            optional_cols=TRANSACTIONS_CSV_INGEST_INFO['OPTIONAL_COLS'],
            account_id=account_id,
        )

        for db_row_value in [
            classify_transaction(
                tv, transaction_classifications
            )
            for tv in transaction_values
        ]:
            write_values_to_db(
                db_row_value,
                db_model=TRANSACTIONS_CSV_INGEST_INFO['DB_MODEL'],
            )
            print(db_row_value['date'], db_row_value['description'])




if __name__ == '__main__':
    ingest_transactions()
