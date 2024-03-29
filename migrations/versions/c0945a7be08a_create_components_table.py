"""create components table

Revision ID: c0945a7be08a
Revises: e4af226b6c85
Create Date: 2023-11-02 15:03:22.852789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0945a7be08a'
down_revision = 'e4af226b6c85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('components',
    sa.Column('component_id', sa.UUID(), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=True),
    sa.Column('make_year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('component_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('components')
    # ### end Alembic commands ###
