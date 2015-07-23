"""'avatar'

Revision ID: 42f41406d280
Revises: 3ce3e13c0f2c
Create Date: 2015-07-21 16:46:43.066000

"""

# revision identifiers, used by Alembic.
revision = '42f41406d280'
down_revision = '3ce3e13c0f2c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    ### end Alembic commands ###
