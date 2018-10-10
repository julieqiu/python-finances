"""drop trip_id column on transactions

Revision ID: ba190d9fe46c
Revises: 9e95134e0ff1
Create Date: 2018-10-09 17:50:17.707821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba190d9fe46c'
down_revision = '9e95134e0ff1'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('transactions', 'trip_id')


def downgrade():
    op.add_column('transactions', sa.Column('trip_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transactions', 'trips', ['trip_id'], ['id'])
