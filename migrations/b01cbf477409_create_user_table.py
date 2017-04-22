"""Create User Table

Revision ID: b01cbf477409
Revises: 
Create Date: 2017-04-21 17:12:54.649412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b01cbf477409'
down_revision = None
branch_labels = ('default',)
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(32))
    )


def downgrade():
    op.drop_table('user')
