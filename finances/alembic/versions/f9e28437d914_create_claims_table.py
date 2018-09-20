"""create claims table

Revision ID: f9e28437d914
Revises: b8c2bd4f2ee5
Create Date: 2018-08-01 23:28:47.696235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9e28437d914'
down_revision = 'b8c2bd4f2ee5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'insurance_claims',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('service_date', sa.Date(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('claim_id', sa.String(), nullable=True),
        sa.Column('patient', sa.String(), nullable=True),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('billed', sa.Numeric(), nullable=True, default=0),
        sa.Column('allowed_amount', sa.Numeric(), nullable=True, default=0),
        sa.Column('paid', sa.Numeric(), nullable=True, default=0),
        sa.Column('deductible', sa.Numeric(), nullable=True, default=0),
        sa.Column('coinsurance', sa.Numeric(), nullable=True, default=0),
        sa.Column('not_covered', sa.Numeric(), nullable=True, default=0),
        sa.Column('personal_cost', sa.Numeric(), nullable=True, default=0),
        sa.Column('status', sa.Numeric(), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    )

def downgrade():
    op.drop_table('insurance_claims')
