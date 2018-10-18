from os import listdir
from os.path import isfile, join

from finances.database import db_session
from finances.database.models import DbAccount


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
