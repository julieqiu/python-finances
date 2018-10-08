"""create transaction trips table

Revision ID: 9e95134e0ff1
Revises: f9e28437d914
Create Date: 2018-10-07 23:59:33.464484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e95134e0ff1'
down_revision = 'f9e28437d914'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'trip_transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('trip_id', sa.Integer(), nullable=False),
        sa.Column('transaction_id', sa.Integer(), nullable=False, unique=True),

        sa.ForeignKeyConstraint(['trip_id'], ['trips.id'], ),
        sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),

        sa.Column('category', sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table('trip_transactions')
