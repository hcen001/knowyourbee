"""added comments column to sample model

Revision ID: 365b1f924cc0
Revises: 25caa2024d94
Create Date: 2018-03-29 16:49:40.519730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '365b1f924cc0'
down_revision = '25caa2024d94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sample', sa.Column('comments', sa.String(length=1024), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sample', 'comments')
    # ### end Alembic commands ###
