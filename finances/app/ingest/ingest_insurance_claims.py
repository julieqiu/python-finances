import csv
from os import listdir
from os.path import isfile, join

from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.models import DbInsuranceClaim, DbAccount
from finances.ingest import constants


def csv_to_transactions(filename: str):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            claim_values = dict()
            for key, value in row.items():
                if not key:
                    continue

                col_name = constants.CSV_TO_CLAIM_COL.get(key.lower())
                if not col_name:
                    continue

                claim_values[col_name] = ' '.join([val for val in value.split(' ') if val])

            for _, col_name in constants.CSV_TO_CLAIM_COL.items():
                try:
                    print(claim_values[col_name])
                except KeyError:
                    raise Exception('Expected {}'.format(col_name))

            with db_session() as session:
                session.execute(
                    insert(DbInsuranceClaim).values(claim_values)
                )


if __name__ == '__main__':
    mypath = '/Users/julie/Code/finances/finances/history/insurance/'
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
            csv_to_transactions(mypath + f)
