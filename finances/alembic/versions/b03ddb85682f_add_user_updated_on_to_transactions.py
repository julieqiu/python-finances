"""add user updated on to transactions

Revision ID: b03ddb85682f
Revises: 1fd3af2cfe41
Create Date: 2018-10-26 19:33:10.991742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b03ddb85682f'
down_revision = '1fd3af2cfe41'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transactions', sa.Column('user_updated_on', sa.DateTime()))


def downgrade():
    op.drop_column('transactions', 'user_updated_on')
