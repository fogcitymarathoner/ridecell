"""Create Reservation Table

Revision ID: f4cb01d78786
Revises: a630ea49557b
Create Date: 2017-04-21 17:19:12.271952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4cb01d78786'
down_revision = 'a630ea49557b'
branch_labels = ()
depends_on = None


def upgrade():
    op.create_table(
        'reservation',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.INTEGER, sa.ForeignKey('user.id')),
        sa.Column('parkspot_id', sa.INTEGER, sa.ForeignKey('parkspot.id')),
        sa.Column('starttime', sa.DateTime),
        sa.Column('endtime', sa.DateTime)
    )
    op.create_index(op.f('ix_time'), 'reservation', ['starttime', 'endtime'], unique=False)


def downgrade():
    op.drop_table('reservation')
    op.drop_index('ix_time')
