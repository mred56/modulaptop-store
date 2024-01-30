"""create orders table

Revision ID: 0e0aea7ffe40
Revises: 2c044db51519
Create Date: 2023-10-24 14:56:50.904894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e0aea7ffe40'
down_revision = '2c044db51519'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('order_date', sa.Date(), nullable=False),
    sa.Column('order_status', sa.String(length=20), nullable=False),
    sa.Column('customer_id', sa.UUID(), nullable=False),
    sa.Column('shipment_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['shipment_id'], ['shipments.shipment_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###
