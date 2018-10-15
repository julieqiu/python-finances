"""add transactions category_id

Revision ID: 0b64a28128d5
Revises: 479184a5edb0
Create Date: 2018-10-15 22:57:01.372736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b64a28128d5'
down_revision = '479184a5edb0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transactions', sa.Column('classification_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transactions', 'transaction_classifications', ['classification_id'], ['id'])


def downgrade():
    op.drop_column('transactions', 'classification_id')
