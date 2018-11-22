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
    ('10/10/2018', '10/23/2018', 'ITALY + GREECE' ),
    ('11/16/2018', '11/18/2018', "HANNAH'S GRADUATION" ),
    ('12/23/2018', '01/06/2019', 'DUBLIN - CHRISTMAS + NYE 2018'),

    ('01/18/2019', '01/21/2019', 'LISBON'),
]


def ingest_trips():
    print('~~~ Adding TRIPS to DB ~~~')
    for start_date, end_date, name in TRAVEL_INFO:
        with db_session() as session:
            trips = set(t.name for t in session.query(DbTrip).all())
            if name not in trips:
                print(start_date, end_date, name)
                session.execute(
                    insert(DbTrip).values({'name': name, 'start_date': start_date, 'end_date': end_date})
                )


if __name__ == '__main__':
    ingest_trips()
