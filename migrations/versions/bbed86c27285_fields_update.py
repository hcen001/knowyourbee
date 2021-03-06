"""fields update

Revision ID: bbed86c27285
Revises: 497519115b96
Create Date: 2018-06-18 19:04:57.425256

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bbed86c27285'
down_revision = '497519115b96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sample', 'lineage_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('sample', 'subspecies_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('specimen', 'date_collected',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('specimen', 'dna',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('specimen', 'measurement',
               existing_type=postgresql.ENUM('qubit', 'nanodrop', name='measurement_enum'),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('specimen', 'measurement',
               existing_type=postgresql.ENUM('qubit', 'nanodrop', name='measurement_enum'),
               nullable=False)
    op.alter_column('specimen', 'dna',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('specimen', 'date_collected',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('sample', 'subspecies_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('sample', 'lineage_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
