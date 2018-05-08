"""testing db

Revision ID: 94f38d2766ce
Revises: 
Create Date: 2018-05-04 00:46:27.367746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94f38d2766ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sample', 'box',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('sample', 'freezer',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('sample', 'origin_city',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('sample', 'origin_country',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('sample', 'origin_state',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('sample', 'shelf',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.drop_index('idx_sample_coordinates', table_name='sample')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_sample_coordinates', 'sample', ['coordinates'], unique=False)
    op.alter_column('sample', 'shelf',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('sample', 'origin_state',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('sample', 'origin_country',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('sample', 'origin_city',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.alter_column('sample', 'freezer',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('sample', 'box',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    # ### end Alembic commands ###