from sqlalchemy.dialects.postgresql import insert

from finances.database import db_session
from finances.database.db_errors import UniqueViolation, split_integrity_error
from finances.database.models import DbTrip


TRAVEL_INFO = [
    ('05/08/2018', '05/14/2018', 'CLEVELAND', ),
    ('05/19/2018', '05/27/2018', 'GERMANY', ),
    ('06/22/2018', '06/24/2018', 'SIOUX FALLS', ),
    ('06/24/2018', '07/01/2018', 'LONDON', ),
    ('8/27/2018', '8/30/2018', 'DENVER' ),
    ('8/31/2018', '9/7/2018', 'AUSTIN + NEW ORLEANS' ),
    ('9/13/2018', '9/18/2018', 'ICELAND' ),
    ('9/18/2018', '9/20/2018', 'NORWAY' ),
    ('9/20/2018', '10/1/2018', 'IRELAND' ),
    ('10/1/2018', '10/10/2018', 'SPAIN' ),
]


for start_date, end_date, name in TRAVEL_INFO:
    try:
        with db_session() as session, split_integrity_error() as err:
            session.execute(
                insert(DbTrip).values({'name': name, 'start_date': start_date, 'end_date': end_date})
            )
    except UniqueViolation as err:
        print(err)
        continue
    except Exception as err:
        print(err)
        raise err
