"""table account_request creation

Revision ID: d31013b0daf6
Revises: 88f55873e8bb
Create Date: 2018-03-13 11:21:52.652065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd31013b0daf6'
down_revision = '88f55873e8bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=192), nullable=False),
    sa.Column('fname', sa.String(length=50), nullable=False),
    sa.Column('lname', sa.String(length=50), nullable=False),
    sa.Column('granted', sa.Boolean(), server_default='f', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('account_request')
    # ### end Alembic commands ###
