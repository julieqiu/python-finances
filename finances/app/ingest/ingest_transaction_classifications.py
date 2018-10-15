import json

from sqlalchemy import Text
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import insert, array, ARRAY

from finances.app.classify.constants import CLASSIFICATION_TO_PHRASES
from finances.database import db_session
from finances.database.db_errors import UniqueViolation, split_integrity_error
from finances.database.models.db_transaction_classification import DbTransactionClassification


def write_to_db(tc: DbTransactionClassification):
    try:
        with db_session() as session, split_integrity_error() as err:
            session.add(tc)
            session.commit()
    except UniqueViolation as err:
        print(err)
    except Exception as err:
        print(err)
        import pdb; pdb.set_trace()
        raise err


def ingest_transaction_classifications():
    for l1, l1_dict in CLASSIFICATION_TO_PHRASES.items():
        for l2, l2_dict in l1_dict.items():
            for l3, phrases in l2_dict.items():
                write_to_db(
                    DbTransactionClassification(
                        l1=l1.upper(),
                        l2=l2.upper(),
                        l3=l3.upper(),
                        phrases=sorted(
                            list({p.lower() for p in phrases})
                        ),
                    )
                )


if __name__ == '__main__':
    ingest_transaction_classifications()
