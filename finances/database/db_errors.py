# pylint: disable=too-many-ancestors
"""Errors relating to database operations"""
from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError


class RestrictViolation(IntegrityError):
    """Violation of the RESTRICT constraint."""


class UniqueViolation(IntegrityError):
    """Violation of the UNIQUE constraint."""


class NotNullViolation(IntegrityError):
    """Violation of the NOT NULL constraint."""


class ForeignKeyViolation(IntegrityError):
    """Violation of the FOREIGN KEY constraint."""


class CheckViolation(IntegrityError):
    """Violation of the CHECK constraint."""


# Add error codes here as we find more errors we care about. (Keys must be str's.)
# https://www.postgresql.org/docs/9.2/static/errcodes-appendix.html
PG_ERROR_CODES = {
    '23001': RestrictViolation,
    '23502': NotNullViolation,
    '23503': ForeignKeyViolation,
    '23505': UniqueViolation,
    '23514': CheckViolation,
}


@contextmanager
def split_integrity_error():
    try:
        yield
    except IntegrityError as e:
        e.__class__ = PG_ERROR_CODES.get(e.orig.pgcode, e.__class__)
        raise e
