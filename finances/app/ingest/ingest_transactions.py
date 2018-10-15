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
from finances.app.ingest.helper_ingest_expenses import (
    files_in_directory,
    group_filenames_by_account,
    last_transaction_date_for_account,
    csvfiles_to_transaction_values,
    write_transaction_values_to_db)

TRANSACTIONS_CSV_INGEST_INFO = CSV_INGEST_INFO['TRANSACTIONS']


def ingest_transactions():
    # 1) Get all filepaths containing transactions
    filenames = files_in_directory(TRANSACTIONS_CSV_INGEST_INFO['CSV_DIRECTORY'])
    account_to_filenames = group_filenames_by_account(filenames)

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

        with db_session() as session:
            last_transaction_date = last_transaction_date_for_account(
                account_id, session)

        transaction_values = csvfiles_to_transaction_values(
            filenames=filenames,
            last_transaction_date=last_transaction_date,
            csv_col_to_db_col=TRANSACTIONS_CSV_INGEST_INFO['CSV_COL_TO_DB_COL'],
            skip_if_missing=TRANSACTIONS_CSV_INGEST_INFO['SKIP_IF_MISSING'],
            optional_cols=TRANSACTIONS_CSV_INGEST_INFO['OPTIONAL_COLS'],
            account_id=account_id,
        )

        write_transaction_values_to_db(
            transaction_values,
            TRANSACTIONS_CSV_INGEST_INFO['DB_MODEL'],
            filenames[0])


if __name__ == '__main__':
    ingest_transactions()
