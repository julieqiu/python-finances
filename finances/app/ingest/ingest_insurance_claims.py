import argparse
from collections import deque
import csv
import datetime
from os import listdir
from os.path import isfile, join

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from finances.database.db_errors import UniqueViolation, split_integrity_error

from finances.app.ingest.constants import CSV_INGEST_INFO
from finances.app.ingest.helpers.helper_filenames import (
    files_in_directory,
)
from finances.app.ingest.helpers.helper_expenses import (
    csvfiles_to_db_row_values,
    write_values_to_db,
)

INSURANCE_CLAIMS_CSV_INGEST_INFO = CSV_INGEST_INFO['INSURANCE_CLAIMS']


def ingest_insurance_claims():
    # 1) Get all filepaths containing transactions
    filenames = files_in_directory(INSURANCE_CLAIMS_CSV_INGEST_INFO['CSV_DIRECTORY'])
    print(
    """

    """
    )
    print(filenames)
    print(
    """


    """
    )

    claim_values = csvfiles_to_db_row_values(
        filenames=filenames,
        csv_col_to_db_col=INSURANCE_CLAIMS_CSV_INGEST_INFO['CSV_COL_TO_DB_COL'],
        skip_if_missing=INSURANCE_CLAIMS_CSV_INGEST_INFO['SKIP_IF_MISSING'],
        optional_cols=INSURANCE_CLAIMS_CSV_INGEST_INFO['OPTIONAL_COLS'],
        account_id=8,
    )

    for db_row_value in claim_values:
            write_values_to_db(
                db_row_value,
                db_model=INSURANCE_CLAIMS_CSV_INGEST_INFO['DB_MODEL'],
            )
            print(
                db_row_value['service_date'],
                db_row_value['billed'],
                db_row_value['provider'],
            )


if __name__ == '__main__':
    ingest_insurance_claims()
