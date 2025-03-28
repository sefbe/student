"""Initial migration

Revision ID: 626cc26e490d
Revises: 
Create Date: 2025-01-01 19:22:16.913795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '626cc26e490d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payer_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    # ### end Alembic commands ###
