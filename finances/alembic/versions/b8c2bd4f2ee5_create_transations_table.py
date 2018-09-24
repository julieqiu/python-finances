"""create transations table

Revision ID: b8c2bd4f2ee5
Revises:
Create Date: 2018-07-16 01:20:33.419868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8c2bd4f2ee5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('balance', sa.Numeric()),
    )

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    )

    op.create_unique_constraint(None, 'transactions', ['date', 'description', 'amount'])


def downgrade():
    op.drop_table('transactions')
    op.drop_table('accounts')
