"""Person abstract class

Revision ID: 4d80b4b5ceab
Revises: 98020a6073ed
Create Date: 2018-03-14 17:42:26.593336

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4d80b4b5ceab'
down_revision = '98020a6073ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('partner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('fname', sa.String(length=128), server_default='First name', nullable=False),
    sa.Column('lname', sa.String(length=128), server_default='Last name', nullable=False),
    sa.Column('email', sa.String(length=128), server_default='someone@xample.org', nullable=False),
    sa.Column('phone', sa.String(length=128), server_default='N/A', nullable=False),
    sa.Column('institution', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('package',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('date_sent', sa.DateTime(), nullable=False),
    sa.Column('date_received', sa.DateTime(), nullable=False),
    sa.Column('process_location', sa.String(length=128), nullable=False),
    sa.Column('comments', sa.String(length=512), nullable=True),
    sa.Column('carrier', sa.String(length=64), nullable=True),
    sa.Column('partner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['partner_id'], ['partner.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('person')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('date_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('fname', sa.VARCHAR(length=128), server_default=sa.text("'First name'::character varying"), autoincrement=False, nullable=False),
    sa.Column('lname', sa.VARCHAR(length=128), server_default=sa.text("'Last name'::character varying"), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), server_default=sa.text("'someone@xample.org'::character varying"), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=128), server_default=sa.text("'N/A'::character varying"), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='person_pkey'),
    sa.UniqueConstraint('email', name='person_email_key')
    )
    op.drop_table('package')
    op.drop_table('partner')
    # ### end Alembic commands ###