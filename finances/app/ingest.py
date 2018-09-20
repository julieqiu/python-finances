import csv
from os import listdir
from os.path import isfile, join

from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.models import DbTransaction, DbAccount

CSV_TO_TRANSACTION_COL = {
    'amount': 'amount',
    'post date': 'date',
    'posting date': 'date',
    'date': 'date',
    'description': 'description',
    'type': 'type',
}

OPTIONAL = {'type'}


def csv_to_transactions(filename: str):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transaction_values = dict()
            for key, value in row.items():
                if not key:
                    continue
                col_name = CSV_TO_TRANSACTION_COL.get(key.lower())
                if not col_name:
                    continue

                transaction_values[col_name] = ' '.join([val for val in value.split(' ') if val])

            if not transaction_values.get('amount'):
                continue

            for _, col_name in CSV_TO_TRANSACTION_COL.items():
                try:
                    print(transaction_values[col_name])
                except KeyError:
                    if col_name in OPTIONAL:
                        continue
                    else:
                        raise Exception('Expected {}'.format(col_name))

            with db_session() as session:
                session.execute(
                    insert(DbTransaction).values(transaction_values)
                )


if __name__ == '__main__':
    mypath = '/Users/julie/Code/finances/finances/history/'
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
