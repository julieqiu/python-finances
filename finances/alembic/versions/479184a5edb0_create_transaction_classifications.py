"""add transactions category

Revision ID: 479184a5edb0
Revises: 876315eac19f
Create Date: 2018-10-15 21:49:49.386814

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '479184a5edb0'
down_revision = '876315eac19f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transaction_classifications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('l1', sa.String(), nullable=False),
        sa.Column('l2', sa.String(), nullable=True),
        sa.Column('l3', sa.String(), nullable=True),
        sa.Column(
            'phrases',
            postgresql.ARRAY(sa.TEXT()),
            autoincrement=False,
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table('transaction_classifications')
