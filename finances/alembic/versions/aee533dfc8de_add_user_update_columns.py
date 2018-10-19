"""add user update columns

Revision ID: aee533dfc8de
Revises: 0b64a28128d5
Create Date: 2018-10-18 14:06:58.675625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aee533dfc8de'
down_revision = '0b64a28128d5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'transactions',
        sa.Column('description_edited', sa.String(), nullable=True)
    )


def downgrade():
    op.drop_column('transactions', 'description_edited')
