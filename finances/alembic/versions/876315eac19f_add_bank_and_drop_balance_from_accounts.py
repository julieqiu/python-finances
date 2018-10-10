"""add bank and drop balance from accounts

Revision ID: 876315eac19f
Revises: ba190d9fe46c
Create Date: 2018-10-10 08:40:44.130706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '876315eac19f'
down_revision = 'ba190d9fe46c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('accounts', sa.Column('bank', sa.String(), nullable=False))
    op.add_column('accounts', sa.Column('number', sa.Integer()))
    op.add_column('accounts', sa.Column('routing', sa.Integer()))
    op.drop_column('accounts', 'balance')


def downgrade():
    op.drop_column('accounts', 'bank')
    op.drop_column('accounts', 'number')
    op.drop_column('accounts', 'routing')
    op.add_column('accounts', sa.Column('balance', sa.Numeric(), nullable=True))
