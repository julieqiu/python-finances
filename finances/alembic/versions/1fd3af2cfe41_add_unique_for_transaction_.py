"""add unique for transaction classifications

Revision ID: 1fd3af2cfe41
Revises: aee533dfc8de
Create Date: 2018-10-23 17:17:05.763451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fd3af2cfe41'
down_revision = 'aee533dfc8de'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'transaction_classifications', ['l1', 'l2', 'l3'])


def downgrade():
    pass
