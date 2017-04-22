"""Create ParkSpot Table

Revision ID: a630ea49557b
Revises: b01cbf477409
Create Date: 2017-04-21 17:15:31.756051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a630ea49557b'
down_revision = 'b01cbf477409'
branch_labels = ()
depends_on = None


def upgrade():
    op.create_table(
        'parkspot',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('lat', sa.Float),
        sa.Column('lng', sa.Float)
    )


def downgrade():
    op.drop_table('parkspot')
