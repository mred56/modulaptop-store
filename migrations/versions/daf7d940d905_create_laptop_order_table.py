"""create laptop_order table

Revision ID: daf7d940d905
Revises: 06a5ce277e90
Create Date: 2023-11-07 09:22:20.302200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daf7d940d905'
down_revision = '06a5ce277e90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('laptop_order',
    sa.Column('laptop_order_id', sa.UUID(), nullable=False),
    sa.Column('order_id', sa.UUID(), nullable=False),
    sa.Column('laptop_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['laptop_id'], ['laptops.laptop_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('laptop_order_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('laptop_order')
    # ### end Alembic commands ###