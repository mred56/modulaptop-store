"""create laptops_components table

Revision ID: 06a5ce277e90
Revises: c0945a7be08a
Create Date: 2023-11-06 09:13:36.215035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06a5ce277e90'
down_revision = 'c0945a7be08a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('laptops_components',
    sa.Column('laptop_id', sa.UUID(), nullable=False),
    sa.Column('component_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['component_id'], ['components.component_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['laptop_id'], ['laptops.laptop_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('laptop_id', 'component_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('laptops_components')
    # ### end Alembic commands ###
